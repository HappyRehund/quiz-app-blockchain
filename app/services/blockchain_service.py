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
            # Check if certificate already exists on blockchain
            try:
                cert_data = self.contract.functions.certificates(cert_id).call()
                if cert_data and len(cert_data) >= 4 and cert_data[3]:  # exists flag
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Certificate {cert_id} already exists on blockchain"
                    )
            except Exception as e:
                print(f"Error checking existing certificate: {e}")
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            tx = self.contract.functions.storeCertificate(
                cert_id, 
                cert_hash
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 300000,  # Increase gas limit
                'gasPrice': self.w3.eth.gas_price,
                'chainId': blockchain_config.chain_id
            })
            
            # Sign and send transaction
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            print(f"Transaction sent: {tx_hash.hex()}")
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            print(f"Transaction receipt: {receipt}")
            
            # Check if transaction was successful
            if receipt['status'] != 1:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Transaction failed on blockchain"
                )
            
            # Verify certificate was actually stored
            cert_data = self.contract.functions.certificates(cert_id).call()
            print(f"Certificate after storage: {cert_data}")
            
            if not cert_data or len(cert_data) < 4 or not cert_data[3]:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Certificate was not stored on blockchain properly"
                )
            
            return {
                "tx_hash": tx_hash.hex(),
                "block_number": receipt["blockNumber"],
                "status": receipt["status"]
            }
        
        except HTTPException:
            raise
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
    def get_certificate_hash(self, cert_id: str) -> Optional[str]:
        """Get certificate hash from blockchain"""
        if not self.w3.is_connected() or not self.contract:
            return None
        
        try:
            # Since 'certificates' mapping is public, Solidity creates a getter
            # certificates(string) returns (string certificateId, string certificateHash, uint256 timestamp, bool exists)
            cert_data = self.contract.functions.certificates(cert_id).call()
            print(f"Certificate data from blockchain: {cert_data}")
            
            # cert_data is a tuple: (certificateId, certificateHash, timestamp, exists)
            if cert_data and len(cert_data) >= 4 and cert_data[3]:  # Check exists flag
                return cert_data[1]  # Return certificateHash
            
            return None
        except Exception as e:
            print(f"Error getting certificate from blockchain: {e}")
            return None

blockchain_service = BlockchainService()