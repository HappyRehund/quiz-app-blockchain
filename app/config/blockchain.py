from web3 import Web3
from app.config.settings import settings
import json


class BlockchainConfig:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
        self.chain_id = settings.BLOCKCHAIN_CHAIN_ID
        self.contract_address = settings.CONTRACT_ADDRESS
        self.deployer_address = settings.DEPLOYER_ADDRESS
        
        # Load private key from keystore
        try:
            with open(settings.DEPLOYER_KEYSTORE_PATH, 'r') as keyfile:
                encrypted_key = keyfile.read()
                self.private_key = self.w3.eth.account.decrypt(
                    encrypted_key, 
                    settings.DEPLOYER_PASSWORD
                )
                self.account = self.w3.eth.account.from_key(self.private_key)
        except Exception as e:
            print(f"Error loading keystore: {e}")
            self.private_key = None
            self.account = None
    
    def is_connected(self) -> bool:
        return self.w3.is_connected()
    
    def get_contract(self, abi_path: str = "contracts/build/CertificateRegistry.abi"):
        try:
            with open(abi_path, 'r') as f:
                abi = json.load(f)
            
            return self.w3.eth.contract(
                address=self.contract_address,
                abi=abi
            )
        except Exception as e:
            print(f"Error loading contract: {e}")
            return None


blockchain_config = BlockchainConfig()