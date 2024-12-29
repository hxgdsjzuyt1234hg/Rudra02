from pyrogram import Client, filters
import asyncio

# Initialize the Pyrogram client with your configuration
app = Client("my_account")

@app.on_message(filters.command("usergroups", prefixes=["/", "@", "#"]))
async def user_groups(client, message):
    try:
        # Extract the user ID from the command
        user_id = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID.")
        return

    group_list = []

    # Iterate over all dialogs to find groups
    async for dialog in client.get_dialogs():
        if dialog.chat.type in ["group", "supergroup"]:
            # Iterate over members in the group to check if the user is a member
            async for member in client.get_chat_members(dialog.chat.id):
                if member.user.id == user_id:
                    group_list.append(dialog.chat.title)
                    break

    # Write the group names to a text file
    with open(f"user_{user_id}_groups.txt", "w") as file:
        for group in group_list:
            file.write(f"{group}\n")

    # Send the text file as a document
    await message.reply_document(f"user_{user_id}_groups.txt")

# Check if the event loop is already running
if not asyncio.get_event_loop().is_running():
    app.run()
else:
    asyncio.run(app.start())
