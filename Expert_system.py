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
            if all(backward_chaining(cond, facts) for cond in rule["if"]):
                return True
    return False              

def expert_system():
    user_facts = input("Please enter the facts(comma separated) ").split(',')
    user_facts = [fact.strip() for fact in user_facts]
    
    results = forward_chaining(user_facts)
    deseases = results - set(user_facts)
    
    if deseases:
        print("You may have ",",".join(deseases))
    else:
        print("No deseases could be inferred from the given symptoms")
    
    query = input("Want to check by disease?(yes/no)")
    if query.lower() == "yes":
        goal = input("goal:").strip()
        if backward_chaining(goal, set(user_facts)):
            print("matched")
        else:
            print("NOt matched")        
expert_system()