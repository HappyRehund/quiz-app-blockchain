from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
HTTP_PROVIDER = os.getenv("BLOCKCHAIN_RPC_URL", "http://localhost:8545") or "http://localhost:8545"
DEPLOYER_ADDRESS = os.getenv("DEPLOYER_ADDRESS") or ""
KEYSTORE_PATH = os.getenv("DEPLOYER_KEYSTORE_PATH") or ""
PASSWORD = os.getenv("DEPLOYER_PASSWORD") or ""
CHAIN_ID = int(os.getenv("BLOCKCHAIN_CHAIN_ID", "110261"))

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER))
assert w3.is_connected(), "❌ Web3 connection failed"
print("✅ Connected to blockchain")

# Load private key from keystore
with open(KEYSTORE_PATH, 'r') as keyfile:
    key_data = keyfile.read()
    private_key = w3.eth.account.decrypt(key_data, PASSWORD)

print(f"📝 Deployer address: {DEPLOYER_ADDRESS}")

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

# Prepare contract deployment
CertificateRegistry = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Get nonce
nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(DEPLOYER_ADDRESS))

# Build transaction
print("🔨 Building deployment transaction...")
transaction = CertificateRegistry.constructor().build_transaction({
    "chainId": CHAIN_ID,
    "from": Web3.to_checksum_address(DEPLOYER_ADDRESS),
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.eth.gas_price
})

# Sign transaction
print("✍️  Signing transaction...")
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send transaction
print("📤 Sending deployment transaction...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
print(f"📋 Transaction hash: {tx_hash.hex()}")

# Wait for receipt
print("⏳ Waiting for transaction confirmation...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

if tx_receipt["status"] == 1:
    print(f"✅ Contract deployed successfully!")
    print(f"📍 Contract address: {tx_receipt['contractAddress']}")
    print(f"🔢 Block number: {tx_receipt['blockNumber']}")
    print(f"\n⚠️  IMPORTANT: Copy this contract address to your .env file:")
    print(f"CONTRACT_ADDRESS={tx_receipt['contractAddress']}")
else:
    print("❌ Contract deployment failed!")