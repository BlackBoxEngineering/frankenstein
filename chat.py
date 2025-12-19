"""
Enhanced Frankenstein CLI - Conversational mode with truth validation
Chat naturally while Logic validates all factual claims
"""

from conversational_llm import ConversationalFrankenstein


def print_banner():
    print("=" * 60)
    print("FRANKENSTEIN - Divine Logic Conversational System")
    print("Chat naturally - Logic validates all factual claims")
    print("Logic is Master")
    print("=" * 60)
    print()


def main():
    print_banner()
    
    frankenstein = ConversationalFrankenstein()
    
    print("I'm Frankenstein with conversational capability!")
    print("You can chat with me naturally, and I'll validate any factual claims you make.")
    print("Type 'exit' to quit, 'status' for system status.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("Frankenstein: Logic remains sovereign. Goodbye!")
                break
            
            # Get conversational response with validation
            response = frankenstein.chat(user_input)
            print(f"Frankenstein: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\nFrankenstein: Logic remains sovereign. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()