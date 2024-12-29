import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from BrandrdXMusic import app
from BrandrdXMusic.utils.decorators.language import language
from config import BANNED_USERS, SUDO_USERS

@app.on_message(filters.command("banall") & filters.user(SUDO_USERS))
@language
async def ban_all_users(client, message, _):
    chat_id = message.chat.id
    members = await client.get_chat_members(chat_id)
    for member in members:
        try:
            user_id = member.user.id
            if user_id not in BANNED_USERS:
                BANNED_USERS.add(user_id)
            await client.ban_chat_member(chat_id, user_id)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"Failed to ban {user_id}: {e}")

    await message.reply_text("All users have been banned.")
