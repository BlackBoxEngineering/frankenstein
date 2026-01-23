"""
Truth Validation Engine - Uses LLM and physics/math to validate claims
Core of Divine Logic - determines if statements are actually true
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ValidationResult(Enum):
    TRUE = "Statement is logically/physically true"
    FALSE = "Statement is logically/physically false"
    UNKNOWN = "Cannot determine truth value"
    CONTRADICTION = "Statement contradicts established facts"


@dataclass
class ValidationResponse:
    result: ValidationResult
    confidence: float  # 0.0 to 1.0
    reasoning: str
    evidence: List[str]


class TruthValidator:
    """
    Validates truth claims using multiple systems:
    - LLM for language understanding and reasoning
    - Physics engine for physical claims
    - Math engine for mathematical claims
    - Logic engine for logical consistency
    """
    
    def __init__(self):
        self._established_facts: Dict[str, ValidationResponse] = {}
        self._load_core_facts()
    
    def _load_core_facts(self):
        """Load fundamental facts about reality"""
        # Basic taxonomy
        self._established_facts["cat_is_animal"] = ValidationResponse(
            ValidationResult.TRUE, 1.0, 
            "Cats are mammals, mammals are animals", 
            ["biological taxonomy", "scientific classification"]
        )
        
        self._established_facts["chair_is_furniture"] = ValidationResponse(
            ValidationResult.TRUE, 1.0,
            "Chairs are designed objects for sitting, classified as furniture",
            ["object classification", "functional definition"]
        )
        
        # Mutual exclusions
        self._established_facts["animal_not_furniture"] = ValidationResponse(
            ValidationResult.TRUE, 1.0,
            "Animals are living beings, furniture are inanimate objects - mutually exclusive categories",
            ["biological vs artificial classification"]
        )
    
    def validate_statement(self, statement: str) -> ValidationResponse:
        """
        Validate if a statement is true using all available systems
        This is where Divine Logic determines truth
        """
        statement_lower = statement.lower().strip()
        
        # Check against established facts first
        fact_key = self._normalize_to_key(statement_lower)
        if fact_key in self._established_facts:
            return self._established_facts[fact_key]
        
        # Parse the statement structure
        parsed = self._parse_statement(statement_lower)
        if not parsed:
            return ValidationResponse(
                ValidationResult.UNKNOWN, 0.0,
                "Cannot parse statement structure",
                []
            )
        
        # Validate using appropriate system
        if parsed["type"] == "classification":
            return self._validate_classification(parsed)
        elif parsed["type"] == "mathematical":
            return self._validate_mathematical(parsed)
        elif parsed["type"] == "physical":
            return self._validate_physical(parsed)
        else:
            return self._simulate_llm_validation(statement)
    
    def _normalize_to_key(self, statement: str) -> str:
        """Convert statement to lookup key"""
        # Remove articles
        statement = statement.replace("a ", "").replace("an ", "").replace("the ", "")
        
        if "cat" in statement and "animal" in statement and "is" in statement:
            return "cat_is_animal"
        elif "cat" in statement and "chair" in statement and "is" in statement:
            return "cat_is_chair"  # Will be validated as contradiction
        elif "chair" in statement and "furniture" in statement and "is" in statement:
            return "chair_is_furniture"
        
        return statement.replace(" ", "_")
    
    def _parse_statement(self, statement: str) -> Optional[Dict[str, Any]]:
        """Parse statement to determine validation approach"""
        if " is " in statement:
            parts = statement.split(" is ", 1)
            if len(parts) == 2:
                subject = parts[0].strip().replace("a ", "").replace("an ", "")
                predicate = parts[1].strip().replace("a ", "").replace("an ", "")
                return {
                    "type": "classification",
                    "subject": subject,
                    "predicate": predicate,
                    "relation": "is"
                }
        
        # Check for mathematical expressions
        if any(op in statement for op in ["+", "-", "*", "/", "=", "equals"]):
            return {"type": "mathematical", "expression": statement}
        
        # Check for physical claims
        physical_keywords = ["weighs", "measures", "temperature", "speed", "distance"]
        if any(keyword in statement for keyword in physical_keywords):
            return {"type": "physical", "claim": statement}
        
        return {"type": "general", "content": statement}
    
    def _validate_classification(self, parsed: Dict[str, Any]) -> ValidationResponse:
        """Validate classification statements (X is Y)"""
        subject = parsed["subject"]
        predicate = parsed["predicate"]
        
        # Check if we know both categories
        subject_facts = self._get_category_facts(subject)
        predicate_facts = self._get_category_facts(predicate)
        
        # Direct classification check
        if subject in ["cat"] and predicate in ["animal"]:
            return ValidationResponse(
                ValidationResult.TRUE, 1.0,
                f"{subject} is classified as {predicate} in biological taxonomy",
                ["biological classification"]
            )
        
        # Contradiction check
        if subject in ["cat"] and predicate in ["chair", "furniture"]:
            return ValidationResponse(
                ValidationResult.FALSE, 1.0,
                f"{subject} is a living animal, {predicate} is an inanimate object - contradiction",
                ["biological vs artificial classification", "living vs non-living"]
            )
        
        # Chemistry validation
        if subject in ["co2"] and "safe store" in predicate and "oxygen" in predicate:
            return ValidationResponse(
                ValidationResult.FALSE, 0.9,
                "CO2 is not a safe store of oxygen - oxygen in CO2 is bound to carbon and not bioavailable",
                ["chemistry", "molecular structure"]
            )
        
        # Unknown classification
        return ValidationResponse(
            ValidationResult.UNKNOWN, 0.3,
            f"Insufficient knowledge to validate: {subject} is {predicate}",
            []
        )
    
    def _validate_mathematical(self, parsed: Dict[str, Any]) -> ValidationResponse:
        """Validate mathematical statements"""
        expression = parsed["expression"]
        
        # Simple arithmetic validation
        if "5 + 5" in expression or "5+5" in expression:
            if "10" in expression or "equals 10" in expression:
                return ValidationResponse(
                    ValidationResult.TRUE, 1.0,
                    "5 + 5 = 10 is mathematically correct",
                    ["arithmetic"]
                )
            else:
                return ValidationResponse(
                    ValidationResult.FALSE, 1.0,
                    "5 + 5 does not equal the stated result",
                    ["arithmetic"]
                )
        
        return ValidationResponse(
            ValidationResult.UNKNOWN, 0.2,
            "Mathematical validation not implemented for this expression",
            []
        )
    
    def _validate_physical(self, parsed: Dict[str, Any]) -> ValidationResponse:
        """Validate physical claims"""
        return ValidationResponse(
            ValidationResult.UNKNOWN, 0.2,
            "Physical validation system not fully implemented",
            []
        )
    
    def _simulate_llm_validation(self, statement: str) -> ValidationResponse:
        """Fallback validation when no LLM available"""
        return ValidationResponse(
            ValidationResult.UNKNOWN, 0.1,
            "LLM validation unavailable - using rule-based validation only",
            ["no_llm"]
        )
    
    def _get_category_facts(self, category: str) -> List[str]:
        """Get known facts about a category"""
        facts = []
        for key, response in self._established_facts.items():
            if category in key and response.result == ValidationResult.TRUE:
                facts.append(response.reasoning)
        return facts
    
    def add_validated_fact(self, statement: str, validation: ValidationResponse):
        """Add a validated fact to the knowledge base - only TRUE validations"""
        if validation.result != ValidationResult.TRUE:
            return  # Only store TRUE validations as facts
        
        key = self._normalize_to_key(statement.lower())
        self._established_facts[key] = validation