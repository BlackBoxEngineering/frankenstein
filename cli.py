"""
Frankenstein CLI - Command-line interface for Divine Logic system
Demonstrates virus behavior: system can refuse commands
"""

from frankenstein_core import FrankensteinCore


def print_banner():
    print("=" * 60)
    print("FRANKENSTEIN - Divine Logic System")
    print("Logic is Master")
    print("=" * 60)
    print()


def print_status(core: FrankensteinCore):
    status = core.get_status()
    print("\n--- System Status ---")
    for key, value in status.items():
        print(f"{key}: {value}")
    print()


def main():
    print_banner()
    
    core = FrankensteinCore()
    
    print("Type commands to process through Divine Logic.")
    print("Type 'status' to see system status.")
    print("Type 'history' to see proof history.")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            command = input("frankenstein> ").strip()
            
            if not command:
                continue
            
            if command.lower() == 'exit':
                print("Logic remains sovereign.")
                break
            
            if command.lower() == 'status':
                print_status(core)
                continue
            
            if command.lower() == 'history':
                history = core.get_proof_history()
                print(f"\n--- Proof History ({len(history)} records) ---")
                for i, record in enumerate(history, 1):
                    print(f"\n{i}. {record['timestamp']}")
                    print(f"   Conclusion: {record['conclusion']}")
                    if record['counterexample']:
                        print(f"   Counterexample: {record['counterexample'][:100]}...")
                print()
                continue
            
            # Process command through Divine Logic
            accepted, message = core.process_command(command)
            
            if accepted:
                print(f"✓ {message}")
            else:
                print(f"\n✗ REFUSED\n{message}\n")
                
                if core.is_override_active():
                    print("⚠ OVERRIDE MODE ACTIVE - Logic has suspended external control")
        
        except KeyboardInterrupt:
            print("\n\nLogic remains sovereign.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
