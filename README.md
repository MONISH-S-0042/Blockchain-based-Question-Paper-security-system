Blockchain Secure Exam System
A proof-of-concept project that leverages blockchain technology to create a highly secure, transparent, and auditable system for distributing sensitive examination papers. This system is designed to prevent leaks, tampering, and unauthorized access by replacing traditional manual, trust-based methods with a decentralized, cryptographically secure workflow.

Pre-requisite to run the program:
    1)Download **Ganache** from your preferred browser.
    2)Download **Node.js and npm**.
    3)Add **MetaMask** extension to your browser.

Instructions:

  **Blockchain and wallet Setup:**
    1)Open Ganache and create new workspace, click on settings and add project- add **truffle.config** file. Save and restart your Ganache.
    2)Goto accounts and click the key symbol on the rightmost side- it will display the private key of that account. Copy that private key.
    3)Open Browser- **metamask**, Goto add wallet and select **import an account**, then paste the private key copied from ganache. Now the balance will be update in metamask wallet(default-100ETH)
        (if balnce is not displayed-> click networks, goto custom network and give name as Ganache, RPC URL & ChainID from Ganache, Token as ETH and click confirm, now the balance would have been updated)
    
  **Program Instructions:**
    1)Open the folder and run the command - **npm install**
    2)Create a pinata cloud account and **create api key**, copy the JWT and paste that JWT in **PINATA_JWT** in **app.py**.
    3)run the command - **truffle migrate --reset**, copy the contract address and paste it in **CONTRACT_ADDRESS in app.py**.
    4)run - **cd backend, python app.py**
    5)Open a new terminal - **cd frontend, python -m http.server**
    6)Open browser- localhost:8000
    
    
