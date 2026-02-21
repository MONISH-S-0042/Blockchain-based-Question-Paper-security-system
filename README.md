# Blockchain Secure Exam System

A proof-of-concept project that leverages **blockchain technology** to build a secure, transparent, and tamper-proof system for distributing sensitive examination papers.

This system replaces traditional trust-based workflows with a **decentralized, cryptographically secure process**, helping prevent:

- Examination paper leaks  
- Unauthorized access  
- Data tampering  
- Lack of auditability  

---

## 🚀 Features

- Secure storage using blockchain  
- Tamper-proof exam paper records  
- Decentralized verification  
- Transparent audit trail  
- Wallet-based authentication  

---

## 🛠 Tech Stack

- **Blockchain:** Ganache, Truffle  
- **Backend:** Python  
- **Frontend:** HTML / JavaScript  
- **Storage:** Pinata (IPFS)  
- **Wallet:** MetaMask  

---

## ✅ Prerequisites

Install the following before running the project:

- Ganache  
- Node.js & npm  
- MetaMask Browser Extension  
- Python  

---

## 🔗 Blockchain & Wallet Setup

### 1️⃣ Ganache Setup

1. Open **Ganache**
2. Create a **New Workspace**
3. Go to **Settings → Add Project**
4. Select the `truffle.config.js` file
5. Save & Restart Ganache

---

### 2️⃣ Import Account into MetaMask

1. In Ganache → Go to **Accounts**
2. Click the **key icon** to reveal the private key
3. Copy the private key

4. Open **MetaMask**
5. Click **Import Account**
6. Paste the private key

✔ Your balance should display **100 ETH**

---

### ⚠ If Balance is Not Visible

1. Go to **MetaMask → Networks → Add Custom Network**
2. Enter:

- **Network Name:** Ganache  
- **RPC URL:** (From Ganache)  
- **Chain ID:** (From Ganache)  
- **Currency Symbol:** ETH  

3. Save & Confirm

---

## 📦 Installation

Clone the repository and install dependencies:

npm install

## 🔐 Configuration
1️⃣ Pinata Setup
    Create a Pinata Cloud Account
    Generate an API Key
    Copy the JWT Token
    Paste it into:
    PINATA_JWT in app.py

2️⃣ Deploy Smart Contract
Run:
    truffle migrate --reset
Copy the deployed contract address and update:
CONTRACT_ADDRESS in app.py

**▶ Running the Application
Start Backend**
      cd backend
      python app.py
**Start Frontend**

Open a new terminal:

    cd frontend
    python -m http.server
    Open in Browser
    http://localhost:8000
