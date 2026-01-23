"""
Inference Engine - Basic logical inference and deduction
Implements modus ponens, modus tollens, and simple rules
"""

from typing import List, Optional, Tuple, Set
from dataclasses import dataclass


@dataclass
class Fact:
    """A known fact"""
    statement: str
    confidence: float = 1.0


@dataclass
class Rule:
    """An if-then rule"""
    premise: str  # If this
    conclusion: str  # Then this
    confidence: float = 1.0


@dataclass
class Inference:
    """Result of logical inference"""
    conclusion: str
    premises: List[str]
    rule_applied: str
    confidence: float


class InferenceEngine:
    """Basic logical inference engine"""
    
    def __init__(self):
        self.facts: Set[str] = set()
        self.rules: List[Rule] = []
        self._load_basic_rules()
    
    def _load_basic_rules(self):
        """Load basic logical rules"""
        # Taxonomy rules
        self.add_rule("X is mammal", "X is animal")
        self.add_rule("X is cat", "X is mammal")
        self.add_rule("X is dog", "X is mammal")
        self.add_rule("X is human", "X is mortal")
        
        # Property inheritance
        self.add_rule("X is animal", "X is living")
        self.add_rule("X is living", "X requires energy")
    
    def add_fact(self, fact: str):
        """Add a known fact"""
        self.facts.add(fact.lower().strip())
    
    def add_rule(self, premise: str, conclusion: str, confidence: float = 1.0):
        """Add an inference rule"""
        self.rules.append(Rule(
            premise=premise.lower().strip(),
            conclusion=conclusion.lower().strip(),
            confidence=confidence
        ))
    
    def can_infer(self, statement: str) -> Optional[Inference]:
        """Check if statement can be inferred from known facts"""
        statement = statement.lower().strip()
        
        # Direct fact check
        if statement in self.facts:
            return Inference(
                conclusion=statement,
                premises=[statement],
                rule_applied="Direct fact",
                confidence=1.0
            )
        
        # Try modus ponens: If we have "A" and rule "A → B", infer "B"
        for rule in self.rules:
            # Check if we can apply this rule
            inference = self._try_apply_rule(rule, statement)
            if inference:
                return inference
        
        # Try chained inference (2 steps)
        for rule1 in self.rules:
            for rule2 in self.rules:
                inference = self._try_chain_rules(rule1, rule2, statement)
                if inference:
                    return inference
        
        return None
    
    def _try_apply_rule(self, rule: Rule, target: str) -> Optional[Inference]:
        """Try to apply a rule to reach target conclusion"""
        # Check if rule conclusion matches target
        if not self._matches_pattern(rule.conclusion, target):
            return None
        
        # Extract variable binding
        binding = self._extract_binding(rule.conclusion, target)
        if not binding:
            return None
        
        # Check if premise is satisfied
        premise_instance = self._apply_binding(rule.premise, binding)
        if premise_instance in self.facts:
            return Inference(
                conclusion=target,
                premises=[premise_instance],
                rule_applied=f"Modus ponens: {rule.premise} -> {rule.conclusion}",
                confidence=rule.confidence
            )
        
        return None
    
    def _try_chain_rules(self, rule1: Rule, rule2: Rule, target: str) -> Optional[Inference]:
        """Try to chain two rules: A → B, B → C"""
        # Check if rule2 conclusion matches target
        if not self._matches_pattern(rule2.conclusion, target):
            return None
        
        # Check if rule1 conclusion matches rule2 premise
        if not self._matches_pattern(rule1.conclusion, rule2.premise):
            return None
        
        # Extract binding from target
        binding = self._extract_binding(rule2.conclusion, target)
        if not binding:
            return None
        
        # Check if initial premise is satisfied
        premise_instance = self._apply_binding(rule1.premise, binding)
        if premise_instance in self.facts:
            intermediate = self._apply_binding(rule1.conclusion, binding)
            return Inference(
                conclusion=target,
                premises=[premise_instance, intermediate],
                rule_applied=f"Chain: {rule1.premise} -> {rule1.conclusion} -> {rule2.conclusion}",
                confidence=rule1.confidence * rule2.confidence
            )
        
        return None
    
    def _matches_pattern(self, pattern: str, statement: str) -> bool:
        """Check if statement matches pattern (with variable X)"""
        if 'x' not in pattern:
            return pattern == statement
        
        # Simple pattern matching
        pattern_parts = pattern.split('x')
        if len(pattern_parts) != 2:
            return False
        
        prefix, suffix = pattern_parts
        return statement.startswith(prefix) and statement.endswith(suffix)
    
    def _extract_binding(self, pattern: str, statement: str) -> Optional[str]:
        """Extract variable binding from pattern match"""
        if 'x' not in pattern:
            return None if pattern != statement else ""
        
        pattern_parts = pattern.split('x')
        if len(pattern_parts) != 2:
            return None
        
        prefix, suffix = pattern_parts
        if not (statement.startswith(prefix) and statement.endswith(suffix)):
            return None
        
        # Extract the variable value
        start = len(prefix)
        end = len(statement) - len(suffix) if suffix else len(statement)
        return statement[start:end].strip()
    
    def _apply_binding(self, pattern: str, binding: str) -> str:
        """Apply variable binding to pattern"""
        return pattern.replace('x', binding)
    
    def explain_inference(self, statement: str) -> str:
        """Explain how a statement can be inferred"""
        inference = self.can_infer(statement)
        if not inference:
            return f"Cannot infer '{statement}' from known facts"
        
        explanation = f"Conclusion: {inference.conclusion}\n"
        explanation += f"Premises: {', '.join(inference.premises)}\n"
        explanation += f"Rule: {inference.rule_applied}\n"
        explanation += f"Confidence: {inference.confidence:.2f}"
        
        return explanation
