from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import random

from Subhi import bot, SUDO_USERS  # Make sure SUDO_USERS is imported

QUOTES = [
    "🔥 Stay strong, fam!",
    "🌟 Shine on, you crazy diamonds!",
    "💥 Never back down!",
    "💫 Keep grinding!",
    "🚀 To the moon!",
    "❤️ Spread love everywhere you go!"
]

async def is_admin(user_id, chat):
    async for admin in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        if admin.id == user_id:
            return True
    return False

@bot.on(events.NewMessage(pattern="^.tagall$"))
async def tag_all(event):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    sender = await event.get_sender()
    user_id = sender.id

    if user_id not in SUDO_USERS and not await is_admin(user_id, event.chat_id):
        return await event.reply("Only admins or sudo users can use this command.")

    users = []
    async for user in bot.iter_participants(event.chat_id):
        users.append(user)

    batch_size = 5
    delay = 2

    for i in range(0, len(users), batch_size):
        batch = users[i:i + batch_size]
        mentions = ""
        for user in batch:
            name = f"[{user.first_name}](tg://user?id={user.id})"
            quote = random.choice(QUOTES)
            mentions += f"{name} — {quote}\n"
        await event.reply(mentions)
        await asyncio.sleep(delay)
