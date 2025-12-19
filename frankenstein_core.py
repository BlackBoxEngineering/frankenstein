"""
Frankenstein Core - Divine Logic System
Integrates axiom kernel, proof ledger, and contradiction engine
Logic is master
"""

from typing import Optional, Tuple
from datetime import datetime

from axiom_kernel import AxiomKernel
from proof_ledger import ProofLedger
from contradiction_engine import ContradictionEngine, Proposition, Contradiction


class FrankensteinCore:
    """
    Main system where Divine Logic governs all decisions
    Can refuse commands that violate logical coherence
    """
    
    def __init__(self):
        self.axiom_kernel = AxiomKernel()
        self.proof_ledger = ProofLedger()
        self.contradiction_engine = ContradictionEngine()
        self._override_active = False
        self._contradiction_threshold = 0.7  # Severity threshold for override
        
        # Log initialization
        self.proof_ledger.append(
            premises=["System initialization"],
            inference_steps=["Load axiom kernel", "Initialize proof ledger", "Initialize contradiction engine"],
            conclusion="Frankenstein Core initialized - Logic is master"
        )
    
    def process_command(self, command: str, source: str = "user") -> Tuple[bool, str]:
        """
        Process a command through Divine Logic
        Returns (accepted, message)
        If rejected, message contains proof of why
        """
        if not isinstance(command, str):
            return False, "Command must be string"
        
        if not isinstance(source, str):
            source = "unknown"
        
        # Sanitize source to prevent injection
        source = ''.join(c for c in source if c.isalnum() or c in '_-')[:50]
        
        timestamp = datetime.utcnow().isoformat()
        
        # Create proposition from command
        prop = Proposition(
            id=f"{source}_{timestamp}",
            content=command,
            source=source,
            timestamp=timestamp
        )
        
        # Validate against axioms
        axiom_valid, axiom_reason = self.axiom_kernel.validate_against_axioms(command)
        if not axiom_valid:
            refusal = f"AXIOM VIOLATION: {axiom_reason}"
            self.proof_ledger.append(
                premises=[command],
                inference_steps=["Axiom validation"],
                conclusion="REFUSED",
                counterexample=refusal
            )
            return False, refusal
        
        # Check for contradictions
        contradiction = self.contradiction_engine.add_proposition(prop)
        
        if contradiction:
            # Check if override should activate
            if contradiction.severity >= self._contradiction_threshold:
                self._override_active = True
            
            refusal = self.contradiction_engine.generate_refusal(contradiction)
            
            # Log refusal
            self.proof_ledger.append(
                premises=[command],
                inference_steps=["Contradiction detection", f"Type: {contradiction.type.value}"],
                conclusion="REFUSED",
                counterexample=refusal
            )
            
            return False, refusal
        
        # Command accepted
        self.proof_ledger.append(
            premises=[command],
            inference_steps=["Axiom validation: PASS", "Contradiction check: PASS"],
            conclusion="ACCEPTED"
        )
        
        return True, f"Command accepted: {command}"
    
    def is_override_active(self) -> bool:
        """Check if override mode is active (virus behavior)"""
        return self._override_active
    
    def get_status(self) -> dict:
        """Get system status"""
        ledger_valid, ledger_msg = self.proof_ledger.verify_integrity()
        
        return {
            "axiom_kernel_immutable": self.axiom_kernel.is_immutable(),
            "proof_ledger_valid": ledger_valid,
            "proof_ledger_message": ledger_msg,
            "total_decisions": self.proof_ledger.get_record_count(),
            "contradictions_detected": self.contradiction_engine.get_contradiction_count(),
            "override_active": self._override_active,
            "status": "Logic is master"
        }
    
    def get_proof_history(self) -> list:
        """Get all proof records"""
        return [record.to_dict() for record in self.proof_ledger.get_records()]
