from llama_index.llms.openai import OpenAI


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


github_model = CustomLLM(
    api_base='https://models.github.ai/inference',
    model='openai/gpt-4o',
)
