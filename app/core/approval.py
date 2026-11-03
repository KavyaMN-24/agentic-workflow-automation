def request_approval(action_description: str) -> bool:
    print("\nHUMAN APPROVAL REQUIRED")
    print("=" * 40)
    print(f"Proposed action: {action_description}")

    response = input("Approve this action? (yes/no): ").strip().lower()

    if response == "yes":
        print("Action approved.")
        return True

    print("Action rejected.")
    return False