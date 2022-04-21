from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
from eink import Eink
from observer import Observable
from parser import Parser
from state_holder import StateHolder

API_ID = 0  #Your API_ID
API_HASH = ''  #Your API_HASH

client = TelegramClient('anon', API_ID, API_HASH)

state_holder = StateHolder()
parser = Parser(state_holder)
observable = Observable()
Eink(observable)


@client.on(events.NewMessage(1766138888))
async def main(event):
    print(event.message)
    parser.process_message(event.message.message)
    state = state_holder.generate()
    observable.update_observers(state)


async def main():
    channel_entity = await client.get_entity(1766138888)
    posts = await client(GetHistoryRequest(
        peer=channel_entity,
        limit=200,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0))
    messages = []
    for message in posts.messages:
        messages.append(message.message)
    messages.reverse()
    for message in messages:
        parser.process_message(message)
    state = state_holder.generate()
    observable.update_observers(state)


client.start()
client.loop.create_task(main())
client.run_until_disconnected()

