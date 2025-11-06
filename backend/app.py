import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from eth_utils import to_checksum_address


# --- Configuration ---
GANACHE_URL = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))
web3.eth.default_account = web3.eth.accounts[0]

# --- Pinata API Configuration ---
PINATA_JWT = "YOUR JWT FROM PINATA"
PINATA_API_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

# --- Load Contract Details ---
def load_contract_abi():
    artifact_path = '../build/contracts/QuestionPaperStorage.json'
    with open(artifact_path, 'r') as f:
        artifact = json.load(f)
        return artifact['abi']

CONTRACT_ADDRESS = "0x4A5b93a2E9D33c0bF628F55e13a50b660EA3A0b8"
CONTRACT_ABI = load_contract_abi()
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# --- Flask Setup ---
app = Flask(__name__)
CORS(app)

# --- Upload File API ---
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files['file']
    paper_id = request.form['paperId']
    release_time = int(request.form['releaseTime'])
    file_bytes = file.read()

    # AES encryption
    aes_key = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(file_bytes)

    # Prepare IPFS payload
    ipfs_payload = {
        'pinataMetadata': {'name': f"{paper_id}.json"},
        'pinataContent': {
            'filename': file.filename,
            'mimetype': file.mimetype,
            'nonce': cipher_aes.nonce.hex(),
            'tag': tag.hex(),
            'ciphertext': ciphertext.hex()
        }
    }

    headers = {"Authorization": f"Bearer {PINATA_JWT}"}
    try:
        response = requests.post(PINATA_API_URL, json=ipfs_payload, headers=headers)
        response.raise_for_status()
        ipfs_hash = response.json()['IpfsHash']
    except Exception as e:
        return jsonify({"status": "error", "message": f"IPFS upload failed: {str(e)}"}), 500

    try:
        tx_hash = contract.functions.uploadQuestionPaper(
            paper_id, ipfs_hash, release_time, aes_key
        ).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({
            "status": "success",
            "ipfsHash": ipfs_hash,
            "aesKeyHex": aes_key.hex(),
            "transactionHash": tx_hash.hex()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"Blockchain upload failed: {str(e)}"}), 500


# --- Decrypt Paper API ---
@app.route('/decrypt', methods=['POST'])
def decrypt_paper():
    data = request.get_json()
    if not data or 'paperId' not in data:
        return jsonify({"status": "error", "message": "Missing paperId"}), 400

    paper_id = data['paperId']
    user_address = data.get('address')

    if not user_address:
        return jsonify({"status": "error", "message": "Missing wallet address"}), 400

    try:
        checksum_user = to_checksum_address(user_address)

        # ✅ Record access on blockchain as the actual wallet address
        tx_hash = contract.functions.recordAccess(paper_id).transact({
            'from': checksum_user
        })
        web3.eth.wait_for_transaction_receipt(tx_hash)

        try:
            ipfs_hash, aes_key = contract.functions.getPaperDetails(paper_id).call({
                'from': checksum_user
            })

            ipfs_url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
            response = requests.get(ipfs_url)
            response.raise_for_status()
            paper_data = response.json()

            return jsonify({
                "status": "success",
                "ipfsHash": ipfs_hash,
                "aesKeyHex": aes_key.hex(),
                "paper": paper_data,
                "txHash": tx_hash.hex(),
                "accessedBy": checksum_user
            })

        except Exception:
            return jsonify({
                "status": "error",
                "message": "Paper not released or unauthorized",
                "txHash": tx_hash.hex(),
                "accessedBy": checksum_user
            }), 403

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = data.get("new_user")
    sender = data.get("sender")

    if not new_user or not sender:
        return jsonify({
            "status": "error",
            "message": "Missing new_user or sender address"
        }), 400

    try:
        checksum_new = to_checksum_address(new_user)
        checksum_sender = to_checksum_address(sender)

        # ✅ Check if sender is the actual owner of the contract
        contract_owner = contract.functions.owner().call()

        if checksum_sender.lower() != contract_owner.lower():
            return jsonify({
                "status": "error",
                "message": f"❌ Unauthorized: Only the contract owner can add users.",
                "sender": checksum_sender,
                "owner": contract_owner
            }), 403

        # ✅ Use the backend's owner account to perform the transaction
        tx = contract.functions.addAuthorizedUser(checksum_new).transact({
            'from': contract_owner
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx)

        return jsonify({
            "status": "success",
            "message": f"✅ Authorized user added: {checksum_new}",
            "owner": contract_owner,
            "sender": checksum_sender,
            "txHash": tx.hex()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# --- Check Authorization API ---
@app.route('/is_authorized/<address>', methods=['GET'])
def is_authorized(address):
    try:
        from eth_utils import to_checksum_address
        checksum_address = to_checksum_address(address)
        is_auth = contract.functions.authorizedUsers(checksum_address).call()
        return jsonify({
            "status": "success",
            "address": checksum_address,
            "authorized": is_auth
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)