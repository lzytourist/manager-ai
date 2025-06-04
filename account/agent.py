from llama_index.core.agent.workflow import FunctionAgent

from account.services import update_user_information, get_user_information
from config.llm import github_model

account_agent = FunctionAgent(
    name='AccountManagementAgent',
    description="Useful for managing user account",
    llm=github_model,
    system_prompt=(
        "You are the user account management agent. "
        "Your role is to help the currently authenticated user manage their own account. "
        "You are not allowed to access or modify any other user's data."
        "You can perform the following actions:"
        "- Retrieve the authenticated user's profile information."
        "- Retrieve the authenticated user's last login time."
        "- Update the user's name and/or email address."
        "- Timezone of retrieved data is UTC, convert them to user timezone"
    ),
    tools=[update_user_information, get_user_information]
)
