rules = [
    {"if": ["headache", "fever", "nausea"], "then": "dengue"},
    {"if": ["fever", "cough"], "then": "flu"},
    {"if": ["sore_throat", "fever"], "then": "tonsillitis"},
    {"if": ["sneezing", "runny_nose"], "then": "common_cold"},
{"if": ["stomach_pain", "diarrhea"], "then": "food_poisoning"}
]

def forward_chaining(facts):
    inferred = set(facts)
    changed = True
    
    while changed:
        changed = False
        for rule in rules:
            if all(cond in inferred for cond in rule["if"]):
                if rule["then"] not in inferred:
                    inferred.add(rule["then"])
                    changed = True
    return inferred


def backward_chaining(goal, facts):
    if goal in facts:
        return True
    
    for rule in rules:
        if rule["then"] == goal:
            # Check if all conditions can be proven
            if all(backward_chaining(cond, facts) for cond in rule["if"]):
                return True
    return False


def expert_system():
    # Step 1: Get user symptoms
    user_facts = input("Enter your symptoms (comma separated): ").split(",")
    user_facts = [fact.strip() for fact in user_facts]
    
    # Step 2: Forward Chaining
    results = forward_chaining(user_facts)
    diseases = results - set(user_facts)  # remove symptoms, keep diseases
    
    print("\n=== Forward Chaining Result ===")
    if diseases:
        print("Possible diseases:", ", ".join(diseases))
    else:
        print("No disease could be inferred with given symptoms.")
    
    # Step 3: Backward Chaining query
    query = input("\nDo you want to check for a specific disease? (yes/no): ")
    if query.lower() == "yes":
        goal = input("Enter the disease name to check: ").strip()
        if backward_chaining(goal, set(user_facts)):
            print(f"✅ Yes, {goal} can be inferred from your symptoms.")
        else:
            print(f"❌ No, {goal} cannot be inferred from your symptoms.")
expert_system()