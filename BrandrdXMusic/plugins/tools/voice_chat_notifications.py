from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("my_bot")

async def is_admin(client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "creator")

@app.on_message(filters.command("start_bot"))
async def start_bot(client: Client, message: Message):
    if await is_admin(client, message):
        await message.reply("Bot is now running!")
    else:
        await message.reply("You are not authorized to use this command.")

@app.on_message(filters.command("stop_bot"))
async def stop_bot(client: Client, message: Message):
    if await is_admin(client, message):
        await message.reply("Bot is stopping...")
        await app.stop()
    else:
        await message.reply("You are not authorized to use this command.")

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

if __name__ == "__main__":
    app.start()
    app.idle()
