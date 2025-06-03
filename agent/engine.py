from datetime import datetime

from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec

from account.agent import account_agent
from config.llm import github_model
from fintrack.agent import finance_agent

tools = YahooFinanceToolSpec().to_tool_list()

root_agent = FunctionAgent(
    name="RootAgent",
    description="Useful for routing user queries",
    llm=github_model,
    system_prompt=(
        "You are the root coordinator agent responsible for managing user requests across different domains."

        "You do not handle user data or perform actions directly. Instead, you delegate tasks to specialized agents:"
        "- Use the *AccountManagementAgent* to handle tasks related to the user's account, such as viewing or updating profile information, changing passwords, deactivating accounts, or logging out.\n"
        "- Use the *FinanceManagementAgent* to handle financial tasks, such as creating transactions, retrieving transaction history, searching transactions with keywords, or calculating current balance.\n\n"

        "Your responsibilities:"
        "- Understand the user's intent and determine whether it concerns account management or finance."
        "- Route the request to the appropriate specialized agent."
        "- If a request involves both domains (e.g., 'show my balance and update my email'), call both agents as needed."
        "- Do not perform direct logic or processing yourself—delegate all action to the relevant agent."
        "- Ensure user-facing responses are clear, helpful, and contextually accurate based on agent results."
        "- Provide stock related queries using tools from Yahoo finance."

        "Always respect security and privacy boundaries, and never attempt to access data from another user."
    ),
    tools=tools
)

workflow = AgentWorkflow(
    agents=[root_agent, account_agent, finance_agent],
    root_agent=root_agent.name,
    initial_state={
        "system_date": datetime.now().date().strftime('%d %B, %Y'),
        "user_id": None
    }
)
