import os
import sys
import json
import time
import argparse
from typing import Dict, Optional
from web3 import Web3
from eth_utils import keccak

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def fetch_storage_root(w3: Web3, address: str, block: str) -> Optional[str]:
    """
    Fetches and returns the storage root hash of an account.
    This gives a soundness snapshot of the contract's storage state.
    """
    try:
        address = Web3.to_checksum_address(address)
        proof = w3.eth.get_proof(address, [], block_identifier=block)
        return proof.storageHash
    except Exception as e:
        print(f"❌ Failed to fetch storage root for {address}: {e}")
        return None
        
    storage_root = fetch_storage_root(w3, args.address, args.block)
    if not storage_root:
        print("❌ Could not retrieve storage root.")
        sys.exit(2)
    
    if storage_root == "0x" or len(storage_root) < 4:
        print("⚠️ Warning: Storage root appears empty or invalid. Check RPC or block number.")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-state-soundness — compute the storage root hash of a contract to check state soundness (useful for Aztec/Zama and general Web3 state audits)."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--address", required=True, help="Contract address to verify")
    p.add_argument("--block", default="finalized", help="Block number or tag (default: finalized)")
    p.add_argument("--expected", help="Optional expected storage root hash to compare against")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout in seconds (default: 30)")
    p.add_argument("--json", action="store_true", help="Output results as JSON")
    return p.parse_args()

def main() -> None:
    start_time = time.time()
    args = parse_args()
    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check RPC_URL or --rpc.")
        sys.exit(1)

    print("🔧 zk-state-soundness")
    print(f"🔗 RPC: {args.rpc}")
    try:
        print(f"🧭 Chain ID: {w3.eth.chain_id}")
    except Exception:
        pass
    print(f"🏷️ Contract: {args.address}")
    print(f"🧱 Block: {args.block}")

    storage_root = fetch_storage_root(w3, args.address, args.block)
    if not storage_root:
        print("❌ Could not retrieve storage root.")
        sys.exit(2)

    print(f"📦 Storage root hash: {storage_root}")
    match = None
    if args.expected:
        match = storage_root.lower() == args.expected.lower()
        status = "✅ MATCH" if match else "❌ MISMATCH"
        print(f"Expected: {args.expected}\nStatus: {status}")

    elapsed = time.time() - start_time
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        result = {
            "rpc": args.rpc,
            "chain_id": None,
            "address": Web3.to_checksum_address(args.address),
            "block": args.block,
            "storage_root": storage_root,
            "expected": args.expected,
            "match": match,
            "elapsed_seconds": round(elapsed, 2)
        }
        try:
            result["chain_id"] = w3.eth.chain_id
        except Exception:
            pass
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if (match is None or match) else 2)

if __name__ == "__main__":
    main()
