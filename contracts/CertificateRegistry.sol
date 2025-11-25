// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateRegistry {
    struct Certificate {
        string certificateId;
        string certificateHash;
        uint256 timestamp;
        bool exists;
    }
    
    mapping(string => Certificate) public certificates;
    
    event CertificateStored(
        string indexed certificateId,
        string certificateHash,
        uint256 timestamp
    );
    
    function storeCertificate(
        string memory _certificateId,
        string memory _certificateHash
    ) public {
        require(!certificates[_certificateId].exists, "Certificate already exists");
        
        certificates[_certificateId] = Certificate({
            certificateId: _certificateId,
            certificateHash: _certificateHash,
            timestamp: block.timestamp,
            exists: true
        });
        
        emit CertificateStored(_certificateId, _certificateHash, block.timestamp);
    }
    
    function verifyHash(
        string memory _certificateId,
        string memory _certificateHash
    ) public view returns (bool) {
        if (!certificates[_certificateId].exists) {
            return false;
        }
        
        return keccak256(bytes(certificates[_certificateId].certificateHash)) == keccak256(bytes(_certificateHash));
    }
    
    function getTimestamp(string memory _certificateId) public view returns (uint256) {
        require(certificates[_certificateId].exists, "Certificate does not exist");
        return certificates[_certificateId].timestamp;
    }
    
    function getCertificate(string memory _certificateId) 
        public 
        view 
        returns (
            string memory certificateId,
            string memory certificateHash,
            uint256 timestamp
        ) 
    {
        require(certificates[_certificateId].exists, "Certificate does not exist");
        Certificate memory cert = certificates[_certificateId];
        return (cert.certificateId, cert.certificateHash, cert.timestamp);
    }

    function getCertificateHash(string memory _certificateId) public view returns (string memory) {
        require(certificates[_certificateId].exists, "Certificate does not exist");
        return certificates[_certificateId].certificateHash;
    }
}