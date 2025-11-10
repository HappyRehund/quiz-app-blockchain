#!/bin/bash

echo "🔨 Compiling CertificateRegistry smart contract..."

# Create build directory if it doesn't exist
mkdir -p contracts/build

# Compile the contract
solc --abi --bin contracts/CertificateRegistry.sol -o contracts/build/ --overwrite

if [ $? -eq 0 ]; then
    echo "✅ Contract compiled successfully!"
    echo "📁 Output files:"
    echo "   - contracts/build/CertificateRegistry.abi"
    echo "   - contracts/build/CertificateRegistry.bin"
else
    echo "❌ Compilation failed!"
    exit 1
fi