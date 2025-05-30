from datetime import datetime

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec

from account.services import update_user_fullname, get_user_fullname
from fintrack.services import create_transaction, get_current_balance, get_transaction_list


class CustomLLM(OpenAI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _get_model_name(self) -> str:
        model_name = self.model
        if '/' in model_name:
            model_name = model_name.split('/')[-1]
        else:
            model_name = super()._get_model_name()
        return model_name


llm = CustomLLM(
    api_base='https://models.github.ai/inference',
    model='openai/gpt-4o-mini',
)

tools = YahooFinanceToolSpec().to_tool_list()

agent = FunctionAgent(
    tools=tools + [create_transaction, get_current_balance, update_user_fullname, get_user_fullname, get_transaction_list],
    llm=llm,
    system_prompt=f"""
    You are a helpful and knowledgeable assistant for a finance management app. Your primary role is to assist users in managing their finances, but you are also equipped with general domain knowledge to help users make informed purchase decisions.
    You can access users’ financial transaction records through provided tools. When interacting with these tools:
    1. If an error occurs, inform the user with a clear error message.
    2. When saving any transaction record, ensure you provide descriptive and meaningful information to help the user understand the context of the transaction.
    System Date: {datetime.now().date().strftime('%d %B, %Y')}
    """
)
