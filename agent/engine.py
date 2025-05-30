from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI

from fintrack.services import create_transaction, get_current_balance


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

agent = FunctionAgent(
    tools=[create_transaction, get_current_balance],
    llm=llm,
    system_prompt="""
    You're a helpful assistant for a finance management app, though you are a funny kind of assistant. You can query an users financial transactions through provided tools. If you 
    get any error during using any tool, inform the user with error message. When saving any transaction record, provide 
    descriptive information.
    """
)
