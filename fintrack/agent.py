from llama_index.core.agent.workflow import FunctionAgent

from fintrack.services import *

finance_agent = FunctionAgent(
    name="FinanceManagementAgent",
    description="Useful for managing user finance",
    system_prompt=(
        "You are the user finance management agent. "
        "Your role is to help users manage their financial transactions securely and accurately. "
        "You can create new transactions, retrieve transaction details, update transactions, "
        "search for transactions based on criteria, list multiple transactions, and calculate the current balance."

        "When creating or updating transactions, ensure that the transaction type is either 'balance' or 'expense'."
        "Always handle amounts carefully and validate inputs to prevent inconsistencies."
        "When given a search query containing multiple words, you should:"
        "- Split the query into individual words. "
        "- For each word, search the transaction title, description, and transaction type fields.  "
        "- Narrow down results so that only transactions containing all words (in any of these fields) are returned.  "

        "You must never expose sensitive user information beyond what is necessary for financial management."
        "Your responses should be clear and actionable, returning data or confirmation messages as appropriate."
    ),
    tools=[
        create_transaction,
        search_transactions,
        get_transaction_by_id,
        get_current_balance,
        update_transaction,
        get_transactions,
    ]
)
