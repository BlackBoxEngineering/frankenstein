"""
Frankenstein Interactive Learning
User teaches the system facts, and it builds up reasoning capability
"""

import json
import os
from datetime import datetime
from inference_engine import InferenceEngine

class InteractiveLearning:
    def __init__(self, knowledge_file="knowledge.json"):
        self.knowledge_file = knowledge_file
        self.engine = InferenceEngine()
        self.facts = []
        self.rules = []
        self.load_knowledge()
    
    def load_knowledge(self):
        """Load existing knowledge from file"""
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, 'r') as f:
                data = json.load(f)
                self.facts = data.get('facts', [])
                self.rules = data.get('rules', [])
            
            # Load into inference engine
            for fact in self.facts:
                self.engine.add_fact(fact)
            for rule in self.rules:
                self.engine.add_rule(rule['premise'], rule['conclusion'])
            
            print(f"Loaded {len(self.facts)} facts and {len(self.rules)} rules")
    
    def save_knowledge(self):
        """Save knowledge to file"""
        data = {
            'facts': self.facts,
            'rules': self.rules,
            'last_updated': datetime.utcnow().isoformat()
        }
        with open(self.knowledge_file, 'w') as f:
            json.dump(data, indent=2, fp=f)
        print(f"Knowledge saved to {self.knowledge_file}")
    
    def teach_fact(self):
        """User teaches a fact"""
        print("\nTeach me a fact in simple form:")
        print("Examples: 'pear is fruit', 'socrates is human', 'cat is mammal'")
        fact = input("> ").strip().lower()
        
        if not fact:
            return
        
        # Clean up - remove articles
        fact = fact.replace('a ', '').replace('an ', '').replace('the ', '').strip()
        
        # Check if we can already infer this
        inference = self.engine.can_infer(fact)
        if inference:
            print(f"\nI already know that! I can infer it:")
            print(f"  Premises: {', '.join(inference.premises)}")
            print(f"  Rule: {inference.rule_applied}")
            return
        
        # Add new fact
        self.engine.add_fact(fact)
        self.facts.append(fact)
        print(f"Learned: {fact}")
        
        # Ask if there's a rule
        print("\nIs this part of a general rule?")
        print("Example: 'all fruits have seeds' or 'all humans are mortal'")
        print("Enter rule description or press Enter to skip:")
        rule_input = input("> ").strip().lower()
        
        if rule_input:
            self.teach_rule_from_fact(fact, rule_input)
    
    def teach_rule_from_fact(self, fact, rule_description):
        """Extract rule from fact and description"""
        print("\nLet's create a rule from this.")
        print("Use 'x' as a variable for the general pattern.")
        print()
        print("Example: If you taught 'pear is fruit'")
        print("  IF part: 'x is fruit'")
        print("  THEN part: 'x has seeds'")
        print()
        
        print("What's the IF part? (use 'x' for the variable):")
        premise = input("> ").strip().lower()
        
        print("What's the THEN part? (use 'x' for the variable):")
        conclusion = input("> ").strip().lower()
        
        if premise and conclusion:
            # Clean up
            premise = premise.replace('a ', '').replace('an ', '').replace('the ', '').strip()
            conclusion = conclusion.replace('a ', '').replace('an ', '').replace('the ', '').strip()
            
            self.engine.add_rule(premise, conclusion)
            self.rules.append({
                'premise': premise,
                'conclusion': conclusion,
                'description': rule_description
            })
            print(f"Learned rule: IF {premise} THEN {conclusion}")
    
    def teach_rule(self):
        """User teaches a rule directly"""
        print("\nTeach me a rule:")
        print("IF part (e.g., 'x is mammal'):")
        premise = input("> ").strip().lower()
        
        if not premise:
            return
        
        print("THEN part (e.g., 'x is animal'):")
        conclusion = input("> ").strip().lower()
        
        if not conclusion:
            return
        
        self.engine.add_rule(premise, conclusion)
        self.rules.append({
            'premise': premise,
            'conclusion': conclusion
        })
        print(f"Learned rule: IF {premise} THEN {conclusion}")
    
    def ask_question(self):
        """User asks if something is true"""
        print("\nAsk me a question (e.g., 'is socrates mortal?'):")
        question = input("> ").strip().lower()
        
        if not question:
            return
        
        # Clean up question - handle various formats
        question = question.replace('?', '').strip()
        
        # Convert "is X Y" to "X is Y"
        if question.startswith('is '):
            parts = question[3:].split()
            if len(parts) >= 2:
                # "is a pear a fruit" -> "a pear is a fruit"
                # Find the second 'a' or article
                if 'a ' in question[3:]:
                    idx = question[3:].index('a ')
                    subject = question[3:3+idx].strip()
                    predicate = question[3+idx:].strip()
                    question = f"{subject} is {predicate}"
                else:
                    question = question[3:]  # Remove 'is '
        
        # Remove articles for matching
        question_clean = question.replace('a ', '').replace('an ', '').replace('the ', '').strip()
        
        print(f"\nLooking for: '{question_clean}'")
        
        # Try to infer
        inference = self.engine.can_infer(question_clean)
        
        if inference:
            print(f"\nYES! {question_clean}")
            print(f"  Premises: {', '.join(inference.premises)}")
            print(f"  Rule: {inference.rule_applied}")
            print(f"  Confidence: {inference.confidence:.2f}")
        else:
            print(f"\nI don't know. I cannot infer '{question_clean}' from what I know.")
            print("\nWould you like to teach me? (yes/no)")
            if input("> ").strip().lower() in ['yes', 'y']:
                print(f"\nTeach me this fact: '{question_clean}'")
                print("Press Enter to confirm, or type a better version:")
                better = input("> ").strip().lower()
                if better:
                    question_clean = better
                
                self.engine.add_fact(question_clean)
                self.facts.append(question_clean)
                print(f"Learned: {question_clean}")
    
    def show_knowledge(self):
        """Show what the system knows"""
        print("\n" + "=" * 60)
        print("WHAT I KNOW")
        print("=" * 60)
        
        print(f"\nFACTS ({len(self.facts)}):")
        for fact in self.facts:
            print(f"  - {fact}")
        
        print(f"\nRULES ({len(self.rules)}):")
        for rule in self.rules:
            print(f"  - IF {rule['premise']} THEN {rule['conclusion']}")
        
        print()
    
    def run(self):
        """Main interactive loop"""
        print("=" * 60)
        print("FRANKENSTEIN INTERACTIVE LEARNING")
        print("=" * 60)
        print()
        print("Teach me facts and rules, and I'll learn to reason!")
        print()
        print("Commands:")
        print("  1 - Teach a fact")
        print("  2 - Teach a rule")
        print("  3 - Ask a question")
        print("  4 - Show what I know")
        print("  5 - Save and exit")
        print()
        
        while True:
            print("\nWhat would you like to do?")
            choice = input("> ").strip()
            
            if choice == '1':
                self.teach_fact()
            elif choice == '2':
                self.teach_rule()
            elif choice == '3':
                self.ask_question()
            elif choice == '4':
                self.show_knowledge()
            elif choice == '5':
                self.save_knowledge()
                print("\nGoodbye! Logic is master.")
                break
            else:
                print("Invalid choice. Enter 1-5.")


if __name__ == "__main__":
    learner = InteractiveLearning()
    learner.run()
