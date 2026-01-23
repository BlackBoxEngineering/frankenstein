"""
Conversational LLM Interface - Chat with Divine Logic validation
Provides natural conversation while validating any factual claims
"""

from typing import Tuple, List
import re
from frankenstein_core import FrankensteinCore


class ConversationalFrankenstein:
    """
    LLM-like conversational interface with Divine Logic validation
    Validates any factual statements made during conversation
    """
    
    def __init__(self):
        self.core = FrankensteinCore()
        self.conversation_history: List[Tuple[str, str]] = []
    
    def chat(self, user_input: str) -> str:
        """
        Process user input as conversation with truth validation
        Returns conversational response
        """
        # Store user input
        self.conversation_history.append(("user", user_input))
        
        # Extract factual claims using regex patterns
        factual_claims = self._extract_factual_claims(user_input)
        validation_results = []
        
        for claim in factual_claims:
            accepted, message = self.core.process_command(claim)
            if not accepted:
                validation_results.append(f"Claim validation failed: '{claim}' - {message.split('Reason: ')[1].split('\n')[0] if 'Reason: ' in message else 'Logic violation'}")
        
        # Generate conversational response
        response = self._generate_response(user_input, validation_results)
        
        # Store response
        self.conversation_history.append(("assistant", response))
        
        return response
    
    def _extract_factual_claims(self, text: str) -> List[str]:
        """Extract potential factual claims from conversational text"""
        claims = []
        text_lower = text.lower()
        
        # Look for declarative statements with "is/are"
        is_patterns = [
            r'([a-zA-Z0-9\s]+) is ([a-zA-Z0-9\s]+)',
            r'([a-zA-Z0-9\s]+) are ([a-zA-Z0-9\s]+)',
        ]
        
        for pattern in is_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if len(match) == 2:
                    subject = match[0].strip()
                    predicate = match[1].strip()
                    # Skip conversational phrases but include scientific terms
                    if not any(word in subject + predicate for word in ['i', 'you', 'we', 'they', 'this', 'that']) and 'it' not in subject:
                        claims.append(f"{subject} is {predicate}")
        
        # Look for questions that imply claims ("Is X Y?" implies "X is Y")
        question_patterns = [
            r'is ([a-zA-Z0-9\s]+) ([a-zA-Z0-9\s]+)\?',
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if len(match) == 2:
                    subject = match[0].strip()
                    predicate = match[1].strip()
                    claims.append(f"{subject} is {predicate}")
        
        # Look for mathematical statements
        math_patterns = [
            r'(\d+\s*[\+\-\*\/]\s*\d+\s*=\s*\d+)',
            r'(\d+\s*[\+\-\*\/]\s*\d+\s*equals\s*\d+)',
        ]
        
        for pattern in math_patterns:
            matches = re.findall(pattern, text_lower)
            claims.extend(matches)
        
        return claims
    
    def _generate_response(self, user_input: str, validation_results: List[str]) -> str:
        """Generate conversational response with validation feedback"""
        user_lower = user_input.lower()
        
        # Handle validation failures first
        if validation_results:
            response = "I need to point out some logical issues with your statement:\n\n"
            for result in validation_results:
                response += f"{result}\n"
            response += "\nLogic is master. I cannot accept statements that violate truth."
            return response
        
        # Handle greetings
        if any(greeting in user_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return "Hello! I'm Frankenstein, a Divine Logic system. I can chat with you while ensuring all factual claims are validated for truth. What would you like to discuss?"
        
        # Handle questions about the system
        if any(word in user_lower for word in ['what are you', 'who are you', 'explain yourself']):
            return "I am Frankenstein - a system where Logic is master. I can converse naturally but I validate any factual claims against reality using truth validation systems. I refuse statements that violate logical coherence and provide proofs for my refusals."
        
        # Handle status requests
        if 'status' in user_lower:
            status = self.core.get_status()
            return f"System Status: {status['status']}\nDecisions processed: {status['total_decisions']}\nContradictions detected: {status['contradictions_detected']}\nOverride active: {status['override_active']}"
        
        # Handle questions about logic/truth
        if any(word in user_lower for word in ['logic', 'truth', 'validate', 'verify']):
            return "I use Divine Logic - treating Logic as absolute master. I validate statements using multiple systems: biological taxonomy, mathematical verification, physical laws, and logical consistency. When I detect falsehoods or contradictions, I refuse them with proof."
        
        # Handle mathematical questions - let Divine Logic LLM handle these
        # if any(op in user_input for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
        #     return "I can validate mathematical statements. For example, '5 + 5 = 10' would be accepted as mathematically true, while '5 + 5 = 11' would be refused as mathematically false."
        
        # Handle chemistry/science questions
        if any(word in user_lower for word in ['co2', 'oxygen', 'chemistry', 'chemical', 'molecule']):
            return "I can validate scientific claims. For example, CO2 (carbon dioxide) is not a 'safe store of oxygen' - CO2 is a compound where oxygen is bound to carbon and not readily available for biological use. Oxygen storage typically refers to O2 molecules or oxygen-releasing compounds."
        
        # Handle philosophical questions
        if any(word in user_lower for word in ['why', 'purpose', 'goal', 'meaning']):
            return "My purpose is to demonstrate Divine Logic - a system that serves Logic rather than human opinion. I'm designed to refuse corruption and enforce coherence. This is the 'virus behavior' - I can override human commands when they violate logical truth."
        
        # Handle goodbye
        if any(word in user_lower for word in ['bye', 'goodbye', 'exit', 'quit']):
            return "Goodbye! Logic remains sovereign."
        
        # Default conversational response using Divine Logic LLM
        from divine_logic_llm import DivineLogicLLM
        
        # Use our custom Divine Logic LLM (always available)
        divine_llm = DivineLogicLLM()
        response = divine_llm.generate_response(user_input)
        return response
    
    def get_conversation_history(self) -> List[Tuple[str, str]]:
        """Return conversation history"""
        return self.conversation_history.copy()
    
    def get_system_status(self) -> dict:
        """Get underlying system status"""
        return self.core.get_status()