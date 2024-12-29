from pyrogram import Client, filters

app = Client("my_account")

@app.on_message(filters.command("usergroups", prefixes=["/", "@", "#"]))
async def user_groups(client, message):
    user_id = int(message.command[1])
    group_list = []
    
    async for dialog in client.get_dialogs():
        if dialog.chat.type in ["group", "supergroup"]:
            async for member in client.get_chat_members(dialog.chat.id):
                if member.user.id == user_id:
                    group_list.append(dialog.chat.title)
                    break
    
    with open(f"user_{user_id}_groups.txt", "w") as file:
        for group in group_list:
            file.write(f"{group}\n")
    
    await message.reply_document(f"user_{user_id}_groups.txt")

app.run()
