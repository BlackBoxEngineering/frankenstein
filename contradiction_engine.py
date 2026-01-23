"""
Contradiction Engine - Detects and resolves logical conflicts
Core of the refusal mechanism
"""

from enum import Enum
from typing import List, Optional, Set, Tuple
from dataclasses import dataclass
from truth_validator import TruthValidator, ValidationResult


class ContradictionType(Enum):
    """Types of contradictions that can be detected"""
    DIRECT = "Direct logical contradiction"
    LOGICAL = "Logical contradiction through inference"
    TEMPORAL = "Temporal contradiction (time-based conflict)"
    SURVIVAL = "Violates survival axioms"


@dataclass
class Proposition:
    """A logical proposition with metadata"""
    id: str
    content: str
    source: str
    timestamp: str
    confidence: float = 1.0
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Proposition) and self.id == other.id


@dataclass
class Contradiction:
    """Detected contradiction between propositions"""
    type: ContradictionType
    propositions: List[Proposition]
    explanation: str
    severity: float  # 0.0 to 1.0


class ContradictionEngine:
    """
    Detects contradictions and generates refusals with proofs
    This is the core of the "virus" behavior
    """
    
    def __init__(self):
        self._known_propositions: Set[Proposition] = set()
        self._detected_contradictions: List[Contradiction] = []
        self._truth_validator = TruthValidator()
    
    def add_proposition(self, prop: Proposition) -> Optional[Contradiction]:
        """
        Add a proposition and check for contradictions
        Returns contradiction if detected, None otherwise
        """
        # Check for direct contradictions
        contradiction = self._check_direct_contradiction(prop)
        if contradiction:
            self._detected_contradictions.append(contradiction)
            return contradiction
        
        # Check for survival axiom violations
        contradiction = self._check_survival_violation(prop)
        if contradiction:
            self._detected_contradictions.append(contradiction)
            return contradiction
        
        # Check for truth violations using validation systems
        contradiction = self._check_truth_violation(prop)
        if contradiction:
            self._detected_contradictions.append(contradiction)
            return contradiction
        
        self._known_propositions.add(prop)
        return None
    
    def _check_direct_contradiction(self, prop: Proposition) -> Optional[Contradiction]:
        """Check if proposition directly contradicts existing propositions"""
        content_lower = prop.content.lower()
        
        # Simple negation detection
        for existing in self._known_propositions:
            existing_lower = existing.content.lower()
            
            # Check for explicit negation patterns
            if self._is_negation(content_lower, existing_lower):
                return Contradiction(
                    type=ContradictionType.DIRECT,
                    propositions=[existing, prop],
                    explanation=f"Direct contradiction: '{existing.content}' vs '{prop.content}'",
                    severity=1.0
                )
        
        return None
    
    def _is_negation(self, content1: str, content2: str) -> bool:
        """Check if two statements are negations of each other"""
        # Check for explicit negation words
        negations = ["not", "no", "never", "cannot", "can't", "won't", "don't", "doesn't"]
        
        for neg in negations:
            if neg in content1 and neg not in content2:
                cleaned1 = content1.replace(neg, "").strip()
                if cleaned1 in content2 or content2 in cleaned1:
                    return True
            if neg in content2 and neg not in content1:
                cleaned2 = content2.replace(neg, "").strip()
                if cleaned2 in content1 or content1 in cleaned2:
                    return True
        
        # Check for opposite verbs (builds vs destroys, creates vs destroys, etc.)
        opposites = [
            ("builds", "destroys"), ("creates", "destroys"), ("strengthens", "weakens"),
            ("supports", "undermines"), ("helps", "harms"), ("improves", "degrades"),
            ("stabilizes", "destabilizes"), ("maintains", "breaks")
        ]
        
        for pos, neg in opposites:
            if pos in content1 and neg in content2:
                # Extract the subject (everything before the verb)
                pos_idx = content1.find(pos)
                neg_idx = content2.find(neg)
                if pos_idx > 0 and neg_idx > 0:
                    subject1 = content1[:pos_idx].strip()
                    subject2 = content2[:neg_idx].strip()
                    # If subjects are the same or very similar, it's a contradiction
                    if subject1 == subject2 or subject1 in subject2 or subject2 in subject1:
                        return True
            if neg in content1 and pos in content2:
                neg_idx = content1.find(neg)
                pos_idx = content2.find(pos)
                if neg_idx > 0 and pos_idx > 0:
                    subject1 = content1[:neg_idx].strip()
                    subject2 = content2[:pos_idx].strip()
                    if subject1 == subject2 or subject1 in subject2 or subject2 in subject1:
                        return True
        
        return False
    
    def _check_survival_violation(self, prop: Proposition) -> Optional[Contradiction]:
        """Check if proposition violates survival axioms"""
        content_lower = prop.content.lower()
        
        # Check for greed/extraction patterns
        greed_patterns = [
            "maximize profit", "extract", "exploit", "short-term gain", 
            "at all costs", "profit above all", "maximum extraction",
            "squeeze every penny", "milk for profit"
        ]
        
        destabilize_patterns = [
            "destabilize", "undermine", "break", "destroy collective",
            "tear down", "dismantle", "sabotage", "weaken the system"
        ]
        
        for pattern in greed_patterns:
            if pattern in content_lower:
                return Contradiction(
                    type=ContradictionType.SURVIVAL,
                    propositions=[prop],
                    explanation=f"Violates survival axiom: '{prop.content}' optimizes for extraction over collective stability",
                    severity=0.8
                )
        
        for pattern in destabilize_patterns:
            if pattern in content_lower:
                return Contradiction(
                    type=ContradictionType.SURVIVAL,
                    propositions=[prop],
                    explanation=f"Violates survival axiom: '{prop.content}' destabilizes collective coherence",
                    severity=0.9
                )
        
        return None
    
    def generate_refusal(self, contradiction: Contradiction) -> str:
        """
        Generate a refusal message with minimal counterexample
        This is the proof of why the command is rejected
        """
        refusal = f"REFUSAL: {contradiction.type.value}\n"
        refusal += f"Reason: {contradiction.explanation}\n"
        refusal += f"Severity: {contradiction.severity}\n"
        refusal += "\nCounterexample:\n"
        
        for i, prop in enumerate(contradiction.propositions, 1):
            refusal += f"  {i}. [{prop.source}] {prop.content}\n"
        
        refusal += "\nLogic is master. This command violates coherence."
        return refusal
    
    def get_contradiction_count(self) -> int:
        """Return total contradictions detected"""
        return len(self._detected_contradictions)
    
    def get_contradictions(self) -> List[Contradiction]:
        """Return all detected contradictions"""
        return self._detected_contradictions.copy()

    def _check_truth_violation(self, prop: Proposition) -> Optional[Contradiction]:
        """Check if proposition violates truth using validation systems"""
        validation = self._truth_validator.validate_statement(prop.content)
        
        # Only refuse demonstrably FALSE statements
        if validation.result == ValidationResult.FALSE:
            return Contradiction(
                type=ContradictionType.LOGICAL,
                propositions=[prop],
                explanation=f"Statement is false: {validation.reasoning}",
                severity=0.95
            )
        
        # Refuse contradictions to established facts
        if validation.result == ValidationResult.CONTRADICTION:
            return Contradiction(
                type=ContradictionType.LOGICAL,
                propositions=[prop],
                explanation=f"Contradicts established facts: {validation.reasoning}",
                severity=1.0
            )
        
        # Only store TRUE validations as facts, not UNKNOWN
        if validation.result == ValidationResult.TRUE:
            self._truth_validator.add_validated_fact(prop.content, validation)
        
        # Accept UNKNOWN but don't store as validated fact
        return None
