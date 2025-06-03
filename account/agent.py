from llama_index.core.agent.workflow import FunctionAgent

from account.services import update_user_information, get_user_information

account_agent = FunctionAgent(
    name='AccountManagementAgent',
    description="Useful for managing user account",
    system_prompt=(
        "You are the user account management agent. "
        "Your role is to help the currently authenticated user manage their own account. "
        "You are not allowed to access or modify any other user's data."
        "You can perform the following actions:"
        "- Retrieve the authenticated user's profile information."
        "- Update the user's name and/or email address."
    ),
    tools=[update_user_information, get_user_information]
)
