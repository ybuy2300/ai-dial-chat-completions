import asyncio

from task.clients.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    # 1.1. Create DialClient
    dial_client = DialClient(deployment_name='gpt-4o',)

    # 1.2. Create CustomDialClient
    dial_client_custom = DialClient(deployment_name='gpt-4o',)

    # 2. Create Conversation object
    conversation = Conversation()

    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    print("Provide System prompt or press 'enter' to continue.")
    prompt = input("> ").strip()

    if prompt:
        conversation.add_message(Message(Role.SYSTEM, prompt))
        print("System prompt successfully added to conversation.")
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(f"No System prompt provided. Will be used default System prompt: '{DEFAULT_SYSTEM_PROMPT}'")
    
    print()

    # 4. Use infinite cycle (while True) and get yser message from console
    print("Type your question or 'exit' to quit.")
    while(True):
        user_input = input("> ").strip()

    # 5. If user message is `exit` then stop the loop
        if(user_input == 'exit'):
            print("Existing ...")
            break

    # 6. Add user message to conversation history (role 'user')
        conversation.add_message(Message(Role.USER, user_input))

    # 7. If `stream` param is true -> call DialClient#stream_completion()
    #    else -> call DialClient#get_completion()
        if (stream):
            ai_response = await dial_client.stream_completion(conversation.get_messages)
        else:
            ai_response = dial_client.get_completion(conversation.get_messages())    

    # 8. Add generated message to history
        conversation.add_message(ai_response)



asyncio.run(
    start(False)
)
