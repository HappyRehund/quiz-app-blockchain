import json
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware
from solcx import compile_source, install_solc, set_solc_version
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Install and set Solidity version (MATCH THE WORKING VERSION)
print("📦 Installing Solidity compiler...")
install_solc('0.8.0')
set_solc_version('0.8.0')

def compile_contract(contract_file):
    """Compile the Solidity contract"""
    print("🔨 Compiling contract...")
    
    with open(contract_file, 'r') as f:
        contract_source = f.read()
    
    compiled_sol = compile_source(
        contract_source,
        output_values=['abi', 'bin'],
        solc_version='0.8.0'  # USE 0.8.0
    )
    
    contract_id, contract_interface = compiled_sol.popitem()
    print(f"✅ Contract compiled: {contract_id}")
    return contract_interface

def deploy_contract(w3, contract_interface, deployer_address, password):
    """Deploy the contract to the blockchain"""
    print("🚀 Deploying contract...")
    
    # Unlock account
    w3.geth.personal.unlock_account(deployer_address, password, 0)
    print("✅ Account unlocked")
    
    # Create contract instance
    Contract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    
    # Build transaction
    tx_hash = Contract.constructor().transact({
        'from': deployer_address,
        'gas': 3000000
    })
    
    print(f"📋 Transaction hash: {tx_hash.hex()}")
    print("⏳ Waiting for transaction receipt...")
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if tx_receipt['status'] == 1:
        contract_address = tx_receipt.contractAddress
        print(f"✅ Contract deployed at: {contract_address}")
        print(f"⛽ Gas used: {tx_receipt['gasUsed']:,}")
        return contract_address, contract_interface['abi']
    else:
        print(f"❌ Deployment failed!")
        print(f"⛽ Gas used: {tx_receipt['gasUsed']:,}")
        return None, None

def main():
    # Configuration
    HTTP_PROVIDER = os.getenv("BLOCKCHAIN_RPC_URL", "http://localhost:8545")
    DEPLOYER_ADDRESS = os.getenv("DEPLOYER_ADDRESS")
    PASSWORD = os.getenv("DEPLOYER_PASSWORD")
    
    # Validate required environment variables
    if not DEPLOYER_ADDRESS:
        print("❌ DEPLOYER_ADDRESS not set in .env file!")
        return
    
    if not PASSWORD:
        print("❌ DEPLOYER_PASSWORD not set in .env file!")
        return
    
    # Connect to blockchain
    w3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    if not w3.is_connected():
        print("❌ Failed to connect to blockchain!")
        return
    
    print(f"✅ Connected to blockchain. Network ID: {w3.net.version}")
    
    # Check balance
    balance = w3.eth.get_balance(Web3.to_checksum_address(DEPLOYER_ADDRESS))
    print(f"💰 Account balance: {w3.from_wei(balance, 'ether')} ETH")
    
    # Compile contract
    contract_interface = compile_contract('contracts/CertificateRegistry.sol')
    
    # Deploy contract
    contract_address, abi = deploy_contract(
        w3, 
        contract_interface, 
        DEPLOYER_ADDRESS, 
        PASSWORD
    )
    
    if contract_address:
        print(f"\n🎉 === Deployment Complete ===")
        print(f"📍 Contract Address: {contract_address}")
        print(f"\n⚠️  IMPORTANT: Add this to your .env file:")
        print(f"CONTRACT_ADDRESS={contract_address}")
        
        # Save ABI for future use
        os.makedirs('contracts/build', exist_ok=True)
        with open('contracts/build/CertificateRegistry.abi', 'w') as f:
            json.dump(abi, f, indent=2)
        print("✅ ABI saved to contracts/build/CertificateRegistry.abi")

if __name__ == '__main__':
    main()