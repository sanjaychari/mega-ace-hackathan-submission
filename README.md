# mega-ace-hackathon-submission
Decentralized Cloud Governance via multisig accounts on the Algorand Blockchain

# Introduction
Effective Cloud Governance is a problem faced by many organizations. This solution is a prototype of using the power of multisig accounts on the Algorand Blockchain for decentralized, secure and convenient cloud governance.

# How it works
This is the workflow that would be followed in the finished product.
1. A user is linked to a standalone account on the Algorand Blockchain.
2. There is also a multisig account with all users within the organization and a customizable signature threshold number.
3. Whenever a user wants to boot an instance on a cloud platform(only GCP supported for now), other users will receive a notification to sign the transaction(not implemented yet, hardcoded for now). After the number of signatures matches the signature threshold value set in the multisig account, the transaction is approved and the instance is booted on GCP.

# Instructions
1. Set up LocalNet using Algokit on your local machine(https://developer.algorand.org/docs/get-started/algokit/). Choose playground while running algokit init.
2. Clone this repository
   $ git clone https://github.com/sanjaychari/mega-ace-hackathon-submission.git
3. Open the repository in VSCode. Modify gcp_service_account_key_path in demo.py according to your GCP account credentials.
4. Press F5 while demo.py is open in VSCode. The Dapp will run in the Beaker Sandbox.
