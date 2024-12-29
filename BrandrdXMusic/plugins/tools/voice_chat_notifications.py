from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("my_bot")

@app.on_message(filters.command("start_bot") & filters.user(OWNER_ID))
async def start_bot(client: Client, message: Message):
    await message.reply("Bot is now running!")

@app.on_message(filters.command("stop_bot") & filters.user(OWNER_ID))
async def stop_bot(client: Client, message: Message):
    await message.reply("Bot is stopping...")
    await app.stop()

@app.on_message(filters.video_chat_started)
async def vc_started(client: Client, message: Message):
    chat_members = await app.get_chat_members(message.chat.id)
    members_info = []
    for member in chat_members:
        user = member.user
        members_info.append(f"{user.first_name} (@{user.username}) [ID: {user.id}]")
    members_text = "\n".join(members_info)
    await message.reply(f"The following members have joined the voice chat:\n{members_text}")

@app.on_message(filters.video_chat_ended)
async def vc_ended(client: Client, message: Message):
    chat_members = await app.get_chat_members(message.chat.id)
    members_info = []
    for member in chat_members:
        user = member.user
        members_info.append(f"{user.first_name} (@{user.username}) [ID: {user.id}]")
    members_text = "\n".join(members_info)
    await message.reply(f"The following members have left the voice chat:\n{members_text}")

app.run()
