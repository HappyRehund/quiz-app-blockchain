from app.config.blockchain import blockchain_config
from fastapi import HTTPException, status
from typing import Dict, Optional
import time


class BlockchainService:
    def __init__(self):
        self.w3 = blockchain_config.w3
        self.account = blockchain_config.account
        self.contract = blockchain_config.get_contract()
    
    def store_certificate(self, cert_id: str, cert_hash: str) -> Dict:
        """Store certificate hash on blockchain"""
        if not self.w3.is_connected():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Blockchain network is not available"
            )
        
        if not self.contract:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Smart contract not initialized"
            )
        
        if not self.account:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Blockchain account not initialized"
            )
        
        try:
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            tx = self.contract.functions.storeCertificate(
                cert_id, 
                cert_hash
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 150000,
                'gasPrice': self.w3.eth.gas_price,
                'chainId': blockchain_config.chain_id
            })
            
            # Sign and send transaction
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            return {
                "tx_hash": tx_hash.hex(),
                "block_number": receipt["blockNumber"],
                "status": receipt["status"]
            }
        
        except Exception as e:
            print(f"Blockchain error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to store certificate on blockchain: {str(e)}"
            )
    
    def verify_certificate(self, cert_id: str, cert_hash: str) -> Dict:
        """Verify certificate on blockchain"""
        if not self.w3.is_connected():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Blockchain network is not available"
            )
        
        if not self.contract:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Smart contract not initialized"
            )
        
        try:
            # Verify hash
            is_valid = self.contract.functions.verifyHash(cert_id, cert_hash).call()
            
            # Get timestamp if valid
            timestamp = None
            if is_valid:
                timestamp = self.contract.functions.getTimestamp(cert_id).call()
            
            return {
                "is_valid": is_valid,
                "timestamp": timestamp
            }
        
        except Exception as e:
            print(f"Blockchain verification error: {e}")
            return {
                "is_valid": False,
                "timestamp": None
            }


blockchain_service = BlockchainService()