def build_prompt_with_nlu(user_text: str, nlu_data: dict, persona: str):
    sentiment = nlu_data.get("sentiment", "neutral")
    keywords = ", ".join(nlu_data.get("keywords", []))
    entities = ", ".join(nlu_data.get("entities", []))

    prompt = (
        f"You are a personal finance assistant. The user is a {persona}.\n"
        f"User 's sentiment: {sentiment}\n"
        f"Keywords: {keywords}\n"
        f"Entities: {entities}\n"
        f"User  question: {user_text}\n"
        "Please provide a clear, concise, and helpful financial advice answer."
    )
    return prompt

def build_budget_prompt(budget_data: dict, persona: str):
    income = budget_data.get("income", 0)
    expenses = budget_data.get("expenses", {})
    savings_goal = budget_data.get("savings_goal", 0)
    currency = budget_data.get("currency", "$")

    expenses_str = "\n".join([f"- {k}: {currency}{v}" for k, v in expenses.items()])

    prompt = (
        f"You are a personal finance assistant helping a {persona}.\n"
        f"Income: {currency}{income}\n"
        f"Expenses:\n{expenses_str}\n"
        f"Savings goal: {currency}{savings_goal}\n"
        "Please provide a summary of the budget, highlight top spending categories, "
        "and give actionable advice to improve savings."
    )
    return prompt

def build_spending_insight_prompt(spending_data: dict, persona: str):
    income = spending_data.get("income", 0)
    expenses = spending_data.get("expenses", {})
    goals = spending_data.get("goals", [])
    currency = spending_data.get("currency", "$")

    expenses_str = "\n".join([f"- {k}: {currency}{v}" for k, v in expenses.items()])
    goals_str = "\n".join([f"- {goal['name']}: {currency}{goal['amount']} by {goal['deadline']}" for goal in goals])

    prompt = (
        f"You are a personal finance assistant helping a {persona}.\n"
        f"Income: {currency}{income}\n"
        f"Expenses:\n{expenses_str}\n"
        f"Goals:\n{goals_str}\n"
        "Analyze the spending patterns and provide insights on how to achieve the goals, "
        "including whether current spending allows meeting the goals."
    )
    return prompt
