import subprocess
from telethon import events
from telethon.sync import TelegramClient
from telethon import Button
import asyncio

api_id = 18650979
api_hash = '80f326c75b6d4674b5078b2c875265df'
bot_token = '' # write me if you don't want use your own telegram api credentials

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
user = 'Example_name'
buttons_list = [[Button.inline('Send command to server', b'send')]]


@bot.on(events.NewMessage(pattern='/start', from_users=[user]))
async def start_handler(event):
    await bot.send_message(event.message.peer_id.user_id, 'Hello! Please, choose an operation:',
                           buttons=buttons_list)


@bot.on(events.CallbackQuery(data=b'send'))
async def send_command_handler(send_event):
    await send_event.answer()
    await bot.send_message(send_event.query.user_id, 'Enter command:')

    @bot.on(events.NewMessage(from_users=send_event.query.user_id))
    async def command_handler(new_command_event):
        args = f'{new_command_event.raw_text}'
        nmap_out = subprocess.run(args, shell=True, stdout=subprocess.PIPE)
        nmap_lines = nmap_out.stdout.splitlines()
        await bot.send_message(new_command_event.query.user_id, nmap_lines,
                           buttons=buttons_list)
        bot.remove_event_handler(command_handler)


bot.start(bot_token=bot_token)
loop = asyncio.get_event_loop()
loop.run_forever()
