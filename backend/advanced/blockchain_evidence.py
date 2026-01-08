# backend/advanced/blockchain_evidence.py - Blockchain Evidence Storage
"""
Blockchain-based evidence storage for immutable audit trail.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional
import os


class BlockchainEvidence:
    """Blockchain-style evidence storage with hash chaining"""
    
    def __init__(self, chain_file: str = "data/blockchain_evidence.json"):
        self.chain_file = chain_file
        self.chain = []
        self.load_chain()
    
    def load_chain(self):
        """Load existing blockchain from file"""
        if os.path.exists(self.chain_file):
            try:
                with open(self.chain_file, 'r') as f:
                    self.chain = json.load(f)
            except:
                self.chain = []
                self._create_genesis_block()
        else:
            self.chain = []
            self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the first block in the chain"""
        genesis = {
            'index': 0,
            'timestamp': datetime.utcnow().isoformat(),
            'data': {'type': 'genesis', 'message': 'Veritas Finance Evidence Chain'},
            'previous_hash': '0',
            'hash': self._calculate_hash(0, datetime.utcnow().isoformat(), {'type': 'genesis'}, '0')
        }
        self.chain.append(genesis)
        self._save_chain()
    
    def _calculate_hash(self, index: int, timestamp: str, data: Dict, previous_hash: str) -> str:
        """Calculate SHA-256 hash for a block"""
        block_string = f"{index}{timestamp}{json.dumps(data, sort_keys=True)}{previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def _get_latest_block(self) -> Dict:
        """Get the latest block in the chain"""
        return self.chain[-1] if self.chain else None
    
    def _save_chain(self):
        """Save blockchain to file"""
        os.makedirs(os.path.dirname(self.chain_file), exist_ok=True)
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def add_evidence(self, evidence_type: str, evidence_data: Dict, product_id: int, 
                    analysis_id: Optional[int] = None) -> Dict:
        """Add evidence to blockchain"""
        latest_block = self._get_latest_block()
        previous_hash = latest_block['hash'] if latest_block else '0'
        
        block_data = {
            'type': evidence_type,
            'product_id': product_id,
            'analysis_id': analysis_id,
            'evidence': evidence_data,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        new_block = {
            'index': len(self.chain),
            'timestamp': datetime.utcnow().isoformat(),
            'data': block_data,
            'previous_hash': previous_hash,
            'hash': self._calculate_hash(
                len(self.chain),
                datetime.utcnow().isoformat(),
                block_data,
                previous_hash
            )
        }
        
        self.chain.append(new_block)
        self._save_chain()
        
        return {
            'block_index': new_block['index'],
            'block_hash': new_block['hash'],
            'timestamp': new_block['timestamp'],
            'verified': self._verify_block(new_block)
        }
    
    def _verify_block(self, block: Dict) -> bool:
        """Verify a block's integrity"""
        expected_hash = self._calculate_hash(
            block['index'],
            block['timestamp'],
            block['data'],
            block['previous_hash']
        )
        return expected_hash == block['hash']
    
    def verify_chain(self) -> Dict:
        """Verify entire blockchain integrity"""
        if len(self.chain) <= 1:
            return {'valid': True, 'corrupted_blocks': []}
        
        corrupted = []
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            prev_block = self.chain[i - 1]
            
            # Verify hash
            if not self._verify_block(block):
                corrupted.append(i)
            
            # Verify previous hash link
            if block['previous_hash'] != prev_block['hash']:
                corrupted.append(i)
        
        return {
            'valid': len(corrupted) == 0,
            'corrupted_blocks': corrupted,
            'total_blocks': len(self.chain),
            'valid_blocks': len(self.chain) - len(corrupted)
        }
    
    def get_evidence_for_product(self, product_id: int) -> List[Dict]:
        """Get all evidence blocks for a product"""
        evidence = []
        for block in self.chain:
            if block['data'].get('product_id') == product_id:
                evidence.append({
                    'block_index': block['index'],
                    'hash': block['hash'],
                    'type': block['data'].get('type'),
                    'timestamp': block['timestamp'],
                    'evidence': block['data'].get('evidence')
                })
        return evidence
    
    def get_chain_summary(self) -> Dict:
        """Get blockchain summary statistics"""
        return {
            'total_blocks': len(self.chain),
            'genesis_timestamp': self.chain[0]['timestamp'] if self.chain else None,
            'latest_timestamp': self.chain[-1]['timestamp'] if self.chain else None,
            'verification': self.verify_chain()
        }
