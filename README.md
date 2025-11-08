# zk-state-soundness

# Overview
This repository provides a simple Python CLI tool to verify the **state soundness** of smart contracts.  
It retrieves the **storage root hash** of a contract from the blockchain, which represents the Merkle root of all storage slots.  
This is useful for verifying that the contract's state has not been tampered with, especially for systems integrating privacy or FHE frameworks like **Aztec** or **Zama**.

# Features
- Retrieve on-chain storage root hash for any address  
- Compare against an expected hash  
- Works across Ethereum, L2s, and private devnets  
- Supports finalized and custom block tags  
- Optional JSON output for CI pipelines  
- Execution time display for benchmarking  

# Installation
1. Install Python 3.9+  
2. Install dependencies:
   pip install web3 eth-utils
3. Export your RPC endpoint or pass it directly:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

# Usage
Check a contract’s current storage root:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa

Compare against an expected root hash:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa --expected 0xabc123...

Select a specific block:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa --block 21000000

Output results in JSON:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa --json

# Environment variable usage
To avoid passing `--rpc` every time, you can set an environment variable once:
On Linux/macOS:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

On Windows PowerShell:
   setx RPC_URL "https://mainnet.infura.io/v3/YOUR_KEY"

After that, you can simply run:
   python app.py --address 0xYourContract

# Expected Output
Example:
🔧 zk-state-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🧭 Chain ID: 1  
🏷️ Contract: 0x00000000219ab540356cBB839Cbe05303d7705Fa  
🧱 Block: finalized  
📦 Storage root hash: 0x4d0e2df5b2...  
✅ MATCH  
⏱️ Completed in 0.48s

If the hashes differ:
❌ MISMATCH  
Exit code: 2

## Notes
- Works for both smart contracts and EOAs (though EOAs have no storage root).  
- The storage root reflects the state at the specified block — ideal for reproducibility.  
- For Aztec/Zama-integrated systems, this hash can be used in zero-knowledge proofs to confirm state integrity.  
- For CI/CD monitoring, the tool can be automated to detect unauthorized state changes between deployments.
