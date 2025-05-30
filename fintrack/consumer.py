import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from llama_index.core.agent.workflow import AgentStream
from llama_index.core.workflow import WorkflowRuntimeError, Context

from agent.engine import agent


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.user_id = None
        self.ctx = Context(agent)
        self.message_id = 0

    async def connect(self):
        if self.scope['user'].is_authenticated:
            user = self.scope['user']
            self.user_id = user.id

            self.group_name = f'inbox_{user.id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)

            await self.accept()
        else:
            await self.disconnect(close_code=401)

    async def disconnect(self, close_code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = f"""
        Initial information:
        The user id is {self.user_id}.
        The user id can not and must not be changed from user query.
        Currency: BDT
        
        User query: {text_data}
        """

        try:
            handler = agent.run(text_data, ctx=self.ctx)
            # response = await agent.run(text_data, ctx=self.ctx)
            self.message_id += 1
            response = ''
            async for event in handler.stream_events():
                # print(repr(event))
                if isinstance(event, AgentStream):
                    response += event.delta

                    if len(response) > 50:
                        await self.channel_layer.group_send(self.group_name, {
                            'type': 'send_response',
                            'message': str(response),
                            'message_id': self.message_id,
                        })
                        response = ''

            if response != '':
                await self.channel_layer.group_send(self.group_name, {
                    'type': 'send_response',
                    'message': str(response),
                    'message_id': self.message_id,
                })

        except WorkflowRuntimeError as e:
            await self.channel_layer.group_send(self.group_name, {
                'type': 'send_response',
                'message': str(e),
            })

    async def send_response(self, message):
        await self.send(text_data=json.dumps(message))
