from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
HTTP_PROVIDER = os.getenv("BLOCKCHAIN_RPC_URL", "http://localhost:8545") or "http://localhost:8545"
DEPLOYER_ADDRESS = os.getenv("DEPLOYER_ADDRESS") or ""
PASSWORD = os.getenv("DEPLOYER_PASSWORD") or ""
CHAIN_ID = int(os.getenv("BLOCKCHAIN_CHAIN_ID", "110261"))

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER))

# IMPORTANT: Inject PoA middleware for Clique consensus
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

assert w3.is_connected(), "❌ Web3 connection failed"
print("✅ Connected to blockchain")
print(f"🌐 Network ID: {w3.net.version}")

# Load ABI and bytecode
abi_path = "contracts/build/CertificateRegistry.abi"
bin_path = "contracts/build/CertificateRegistry.bin"

# Check if build files exist
if not os.path.exists(abi_path) or not os.path.exists(bin_path):
    print("❌ Contract build files not found!")
    print("Please compile the contract first:")
    print("  solc --abi --bin contracts/CertificateRegistry.sol -o contracts/build/")
    exit(1)

with open(abi_path, "r") as f:
    contract_abi = json.load(f)

with open(bin_path, "r") as f:
    contract_bytecode = f.read().strip()

print("✅ Contract ABI and bytecode loaded")

# Check balance
balance = w3.eth.get_balance(Web3.to_checksum_address(DEPLOYER_ADDRESS))
print(f"💰 Account balance: {w3.from_wei(balance, 'ether')} ETH")

# Unlock account
print("🔓 Unlocking account...")
try:
    w3.geth.personal.unlock_account(Web3.to_checksum_address(DEPLOYER_ADDRESS), PASSWORD, 0)
    print("✅ Account unlocked")
except Exception as e:
    print(f"⚠️  Warning: Could not unlock account: {e}")
    print("Continuing with signed transaction method...")

# Prepare contract deployment
CertificateRegistry = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Deploy using transact (simpler method)
print("🔨 Deploying contract...")
try:
    tx_hash = CertificateRegistry.constructor().transact({
        'from': Web3.to_checksum_address(DEPLOYER_ADDRESS),
        'gas': 5000000
    })
    
    print(f"📋 Transaction hash: {tx_hash.hex()}")
    print("⏳ Waiting for transaction confirmation...")
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if tx_receipt["status"] == 1:
        print(f"✅ Contract deployed successfully!")
        print(f"📍 Contract address: {tx_receipt['contractAddress']}")
        print(f"🔢 Block number: {tx_receipt['blockNumber']}")
        print(f"⛽ Gas used: {tx_receipt['gasUsed']:,}")
        print(f"\n⚠️  IMPORTANT: Copy this contract address to your .env file:")
        print(f"CONTRACT_ADDRESS={tx_receipt['contractAddress']}")
    else:
        print("❌ Contract deployment failed!")
        print(f"⛽ Gas used: {tx_receipt['gasUsed']:,} / 5,000,000")
        
except Exception as e:
    print(f"❌ Deployment error: {e}")