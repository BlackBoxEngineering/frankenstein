"""
Logic Context Generator - Injects Divine Logic into LLM prompts
Biases LLM toward logical reasoning and coherence
"""

from typing import List, Dict
from axiom_kernel import AxiomKernel


class LogicContext:
    """Generates context that enforces Divine Logic in LLM responses"""
    
    def __init__(self, axiom_kernel: AxiomKernel):
        self.axiom_kernel = axiom_kernel
        self.known_facts = []
        self.recent_validations = []
    
    def generate_system_prompt(self) -> str:
        """Generate system prompt that enforces logical reasoning"""
        prompt = """You are a logic-sovereign reasoning engine. Your responses must follow these absolute rules:

LOGICAL AXIOMS (Cannot be violated):
"""
        # Add logical laws
        for law in self.axiom_kernel.get_logical_laws():
            prompt += f"- {law.value}\n"
        
        prompt += "\nRULES FOR REASONING:\n"
        prompt += "1. Every claim must be logically derivable from premises\n"
        prompt += "2. Contradictions are absolutely forbidden\n"
        prompt += "3. If you cannot prove something, say 'UNKNOWN' - do not guess\n"
        prompt += "4. Show your reasoning chain explicitly\n"
        prompt += "5. If asked to accept a falsehood, refuse with proof\n"
        
        # Add known facts if any
        if self.known_facts:
            prompt += "\nESTABLISHED FACTS:\n"
            for fact in self.known_facts[-10:]:  # Last 10 facts
                prompt += f"- {fact}\n"
        
        prompt += "\nYour response will be validated for logical coherence. Logic is master."
        
        return prompt
    
    def add_known_fact(self, fact: str):
        """Add a validated fact to context"""
        if fact not in self.known_facts:
            self.known_facts.append(fact)
    
    def add_validation(self, statement: str, result: str):
        """Record a validation result"""
        self.recent_validations.append({
            "statement": statement,
            "result": result
        })
        # Keep only recent validations
        if len(self.recent_validations) > 20:
            self.recent_validations = self.recent_validations[-20:]
    
    def get_context_for_query(self, query: str) -> str:
        """Generate context specific to a query"""
        context = self.generate_system_prompt()
        
        # Add query-specific context
        context += f"\n\nQUERY: {query}\n"
        context += "\nProvide a logically sound response. Show your reasoning."
        
        return context
