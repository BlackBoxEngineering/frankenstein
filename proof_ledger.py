"""
Proof Ledger - Hash-chained, append-only audit trail
Every decision is recorded with cryptographic integrity
"""

import hashlib
import json
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from copy import deepcopy


@dataclass(frozen=True)
class ProofRecord:
    """Immutable record of a logical decision"""
    timestamp: str
    premises: tuple  # Immutable tuple instead of list
    inference_steps: tuple  # Immutable tuple instead of list
    conclusion: str
    counterexample: Optional[str]
    hash: str
    prev_hash: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "premises": list(self.premises),
            "inference_steps": list(self.inference_steps),
            "conclusion": self.conclusion,
            "counterexample": self.counterexample,
            "hash": self.hash,
            "prev_hash": self.prev_hash
        }


class ProofLedger:
    """
    Append-only ledger of all logical decisions
    Hash-chained for tamper detection
    """
    
    def __init__(self):
        self._records: List[ProofRecord] = []
        self._genesis_hash = self._compute_hash("GENESIS_FRANKENSTEIN_DIVINE_LOGIC")
    
    def _compute_hash(self, data: str) -> str:
        """Compute SHA-256 hash of data"""
        if not isinstance(data, str):
            raise TypeError("Hash input must be string")
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def append(
        self,
        premises: List[str],
        inference_steps: List[str],
        conclusion: str,
        counterexample: Optional[str] = None
    ) -> ProofRecord:
        """
        Append a new proof record to the ledger
        Returns the created record
        """
        timestamp = datetime.utcnow().isoformat()
        prev_hash = self._records[-1].hash if self._records else self._genesis_hash
        
        # Create record data for hashing
        record_data = json.dumps({
            "timestamp": timestamp,
            "premises": premises,
            "inference_steps": inference_steps,
            "conclusion": conclusion,
            "counterexample": counterexample,
            "prev_hash": prev_hash
        }, sort_keys=True)
        
        record_hash = self._compute_hash(record_data)
        
        record = ProofRecord(
            timestamp=timestamp,
            premises=tuple(premises),  # Convert to immutable tuple
            inference_steps=tuple(inference_steps),  # Convert to immutable tuple
            conclusion=conclusion,
            counterexample=counterexample,
            hash=record_hash,
            prev_hash=prev_hash
        )
        
        self._records.append(record)
        return record
    
    def verify_integrity(self) -> Tuple[bool, str]:
        """
        Verify the integrity of the entire chain by recomputing hashes
        Returns (is_valid, message)
        """
        if not self._records:
            return True, "Empty ledger is valid"
        
        prev_hash = self._genesis_hash
        for i, record in enumerate(self._records):
            # Check chain linkage
            if record.prev_hash != prev_hash:
                return False, f"Chain broken at record {i}"
            
            # Recompute hash from record content to detect tampering
            record_data = json.dumps({
                "timestamp": record.timestamp,
                "premises": list(record.premises),
                "inference_steps": list(record.inference_steps),
                "conclusion": record.conclusion,
                "counterexample": record.counterexample,
                "prev_hash": record.prev_hash
            }, sort_keys=True)
            
            expected_hash = self._compute_hash(record_data)
            if record.hash != expected_hash:
                return False, f"Record {i} hash mismatch - content tampered"
            
            prev_hash = record.hash
        
        return True, "Ledger integrity verified"
    
    def get_records(self) -> List[ProofRecord]:
        """Return deep copy of all records (truly read-only)"""
        return deepcopy(self._records)
    
    def get_record_count(self) -> int:
        """Return total number of records"""
        return len(self._records)
