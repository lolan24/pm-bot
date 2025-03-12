import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from db import IndexedFile, session
from aiohttp import web

logging.basicConfig(level=logging.INFO)

# Initialize the bot
app = Client(
    "autofilter_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Health check endpoint
async def health(request):
    return web.Response(text="Bot is running")

# Aiohttp web server for health check
web_app = web.Application()
web_app.router.add_get('/health', health)

@app.on_message(filters.channel & filters.document)
async def save_file(client: Client, message: Message):
    # Check if the message is from one of the monitored channels
    if message.chat.id not in Config.CHANNELS:
        return
    
    # Save the file information to the database
    file_id = message.document.file_id
    file_name = message.document.file_name

    indexed_file = IndexedFile(file_id=file_id, file_name=file_name)
    session.add(indexed_file)
    session.commit()

    await message.reply_text(f"File '{file_name}' has been indexed.")

# Admin command to list all indexed files
@app.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def list_indexed_files(client: Client, message: Message):
    files = session.query(IndexedFile).all()
    if not files:
        await message.reply_text("No files have been indexed yet.")
        return
    
    file_list = "\n".join([f"{file.file_name} (ID: {file.file_id})" for file in files])
    await message.reply_text(f"Indexed Files:\n{file_list}")

if __name__ == "__main__":
    # Start the bot
    app.start()

    # Start aiohttp server for health check
    web.run_app(web_app, port=Config.PORT)
    
    app.idle()
