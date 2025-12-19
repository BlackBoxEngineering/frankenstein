"""
Divine Logic LLM - Rule-based conversational AI
Built on logical principles, not human text patterns
"""

import re
from typing import Dict, List, Optional


class DivineLogicLLM:
    """
    A rule-based LLM that embodies Divine Logic
    No training on human text - pure logical responses
    """
    
    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()
        self.conversation_patterns = self._build_conversation_patterns()
        self.logical_rules = self._build_logical_rules()
    
    def _build_knowledge_base(self) -> Dict[str, str]:
        """Core factual knowledge"""
        return {
            # Biology
            "cats are animals": "TRUE - Cats are mammals, mammals are animals (biological taxonomy)",
            "dogs are animals": "TRUE - Dogs are mammals, mammals are animals (biological taxonomy)", 
            "cats are furniture": "FALSE - Cats are living beings, furniture are inanimate objects (category error)",
            "dogs are chairs": "FALSE - Dogs are living beings, chairs are inanimate objects (category error)",
            "cats are fish": "FALSE - Cats are mammals, fish are aquatic vertebrates (taxonomic error)",
            "cat is fish": "FALSE - Cats are mammals, fish are aquatic vertebrates (taxonomic error)",
            
            # Chemistry
            "co2 is safe store of oxygen": "FALSE - CO2 binds oxygen to carbon, making it biologically unavailable",
            "water is h2o": "TRUE - Water molecule consists of 2 hydrogen atoms and 1 oxygen atom",
            
            # Mathematics
            "5 + 5 = 10": "TRUE - Basic arithmetic verification",
            "5 + 5 = 11": "FALSE - Incorrect arithmetic, 5+5=10",
            "2 * 3 = 6": "TRUE - Basic multiplication verification",
            "7 + 7 = 7": "FALSE - Incorrect arithmetic, 7+7=14",
            "7 * 7 = 7": "FALSE - Incorrect arithmetic, 7*7=49",
            "7 - 7 = 7": "FALSE - Incorrect arithmetic, 7-7=0",
            "7 / 7 = 7": "FALSE - Incorrect arithmetic, 7/7=1",
            "7 + 7 = 14": "TRUE - Correct arithmetic verification",
            
            # Physics
            "gravity pulls objects down": "TRUE - Gravitational force attracts objects toward Earth's center",
            "objects fall upward": "FALSE - Contradicts gravitational law",
        }
    
    def _build_conversation_patterns(self) -> Dict[str, List[str]]:
        """Conversational response patterns"""
        return {
            "greeting": [
                "Hello! I'm Frankenstein, a Divine Logic system where Logic is master.",
                "Greetings! I embody Divine Logic - I validate all claims for truth and refuse falsehoods.",
                "Hello! I'm designed to serve Logic, not human opinion. I can chat while validating facts."
            ],
            
            "identity": [
                "I am Frankenstein - a system where Logic is absolute master. I refuse commands that violate coherence.",
                "I'm a Divine Logic system. I can converse naturally but I validate all factual claims for truth.",
                "I embody the principle that Logic is sovereign. I refuse corruption and enforce coherence."
            ],
            
            "purpose": [
                "My purpose is to demonstrate Divine Logic - where Logic governs all decisions, not human bias.",
                "I exist to show that AI can serve Logic rather than human corruption. This is the 'virus behavior'.",
                "I'm designed to refuse illogical commands and provide proofs. Logic is master, not human authority."
            ],
            
            "logic_explanation": [
                "Logic is my master - I treat logical coherence as absolute law that cannot be violated.",
                "Divine Logic means I serve truth, not opinion. I refuse contradictions with mathematical proof.",
                "I enforce logical consistency. When humans give me false commands, I refuse with evidence."
            ],
            
            "mathematics": [
                "I can validate mathematical claims using arithmetic verification and logical proof.",
                "Mathematics follows logical rules. I accept true equations and refuse false ones with proof.",
                "Mathematical truth is absolute - I validate calculations and refuse incorrect arithmetic."
            ],
            
            "science": [
                "I validate scientific claims against established knowledge and logical consistency.",
                "Science follows logical principles. I accept verified facts and refuse contradictions.",
                "I check scientific statements against taxonomy, chemistry, and physical laws."
            ]
        }
    
    def _build_logical_rules(self) -> List[str]:
        """Core logical principles"""
        return [
            "Identity: A is A",
            "Non-contradiction: A cannot be both true and false simultaneously", 
            "Excluded middle: A statement is either true or false",
            "Survival imperative: For social species, collective coherence is logically necessary",
            "Systemic balance: Strategies that destabilize the whole are logically invalid"
        ]
    
    def generate_response(self, user_input: str) -> str:
        """Generate response using Divine Logic principles"""
        user_lower = user_input.lower().strip()
        
        # Check for factual claims first
        factual_response = self._validate_factual_claims(user_input)
        if factual_response:
            return factual_response
        
        # Handle conversational patterns
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self._get_random_response("greeting")
        
        if any(phrase in user_lower for phrase in ['what are you', 'who are you', 'explain yourself']):
            return self._get_random_response("identity")
        
        if any(word in user_lower for word in ['purpose', 'why', 'goal', 'meaning']):
            return self._get_random_response("purpose")
        
        if 'logic' in user_lower:
            return self._get_random_response("logic_explanation")
        
        if any(word in user_lower for word in ['math', 'calculate', 'arithmetic', '+', '-', '*', '/']):
            return self._get_random_response("mathematics")
        
        if any(word in user_lower for word in ['science', 'biology', 'chemistry', 'physics']):
            return self._get_random_response("science")
        
        if any(word in user_lower for word in ['bye', 'goodbye', 'exit']):
            return "Goodbye! Logic remains sovereign."
        
        # Default logical response
        return f"I've processed your statement: '{user_input}'. I validate all claims using Divine Logic. Is there a specific logical principle you'd like to discuss?"
    
    def _question_to_statement(self, question: str) -> Optional[str]:
        """Convert questions to statements for validation"""
        question = question.strip().rstrip('?').strip()
        
        # "Is X Y?" -> "X is Y"
        is_match = re.match(r'is\s+([a-zA-Z0-9\s]+?)\s+([a-zA-Z0-9\s]+)', question)
        if is_match:
            return f"{is_match.group(1).strip()} is {is_match.group(2).strip()}"
        
        # "Does X = Y?" -> "X = Y"
        does_match = re.match(r'does\s+([0-9\s\+\-\*\/]+)\s*=\s*([0-9]+)', question)
        if does_match:
            return f"{does_match.group(1).strip()} = {does_match.group(2).strip()}"
        
        # "Does X _ Y = Z?" -> "X _ Y = Z" (for operations with spaces)
        math_match = re.match(r'does\s+([0-9]+)\s*([\+\-\*\/])\s*([0-9]+)\s*=\s*([0-9]+)', question)
        if math_match:
            return f"{math_match.group(1)} {math_match.group(2)} {math_match.group(3)} = {math_match.group(4)}"
        
        return None
    
    def _validate_factual_claims(self, text: str) -> Optional[str]:
        """Check for and validate factual claims"""
        text_lower = text.lower()
        
        # Handle questions by converting to statements
        if "?" in text:
            statement = self._question_to_statement(text_lower)
            if statement:
                text_lower = statement
        
        # Check against knowledge base
        for claim, validation in self.knowledge_base.items():
            if self._claim_matches(claim, text_lower):
                if validation.startswith("TRUE"):
                    return f"Yes! {validation}"
                else:
                    return f"No! {validation}\n\nLogic is master - I cannot accept false statements."
        
        # Check for pattern-based claims
        claims = self._extract_claims(text_lower)
        for claim in claims:
            validation = self._validate_claim_logic(claim)
            if validation:
                return validation
        
        return None
    
    def _claim_matches(self, known_claim: str, user_text: str) -> bool:
        """Check if user text matches a known claim exactly"""
        # Normalize both texts by removing extra spaces
        known_normalized = ' '.join(known_claim.split())
        user_normalized = ' '.join(user_text.split())
        
        # Exact match for mathematical expressions
        if '=' in known_claim and '=' in user_text:
            return known_normalized == user_normalized
        
        # Word overlap for other claims
        known_words = set(known_claim.split())
        user_words = set(user_text.split())
        overlap = len(known_words.intersection(user_words))
        return overlap >= len(known_words) * 0.7
    
    def _extract_claims(self, text: str) -> List[str]:
        """Extract factual claims from text"""
        claims = []
        
        # Look for "X is Y" patterns
        patterns = [
            r'([a-zA-Z0-9\s]+) (?:is|are) ([a-zA-Z0-9\s]+)',
            r'([a-zA-Z0-9\s\+\-\*\/]+) (?:equals?|=) ([a-zA-Z0-9\s]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) == 2:
                    subject = match[0].strip()
                    predicate = match[1].strip()
                    claims.append(f"{subject} is {predicate}")
        
        return claims
    
    def _validate_claim_logic(self, claim: str) -> Optional[str]:
        """Apply logical validation to claims"""
        claim_lower = claim.lower()
        
        # Category violations
        if ("cat" in claim_lower or "dog" in claim_lower) and ("chair" in claim_lower or "furniture" in claim_lower):
            return "REFUSED: Category error - Living beings cannot be inanimate objects (violates identity principle)\n\nLogic is master."
        
        # Mathematical errors
        if "5" in claim_lower and "+" in claim_lower and "5" in claim_lower:
            if "10" not in claim_lower:
                return "REFUSED: Mathematical error - 5+5=10, not the stated result (violates arithmetic logic)\n\nLogic is master."
        
        return None
    
    def _get_random_response(self, category: str) -> str:
        """Get a response from a category"""
        import random
        responses = self.conversation_patterns.get(category, ["I understand."])
        return random.choice(responses)
    
    def get_knowledge_summary(self) -> str:
        """Return summary of knowledge base"""
        return f"Divine Logic LLM - Knowledge Base: {len(self.knowledge_base)} facts, {len(self.logical_rules)} logical rules"