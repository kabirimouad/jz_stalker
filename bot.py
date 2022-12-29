import os
import discord
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')

async def send_message(message, user_message, is_priv):
    try:
        response = handle_response(user_message)
        await message.author.send(response) if is_priv else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    client = discord.Client(intents=discord.Intents.default())
    @client.event
    async def on_ready():
        print(f'{client.user} is running!')
    client.run(token)

def handle_response(message:str) -> str:
    p_message = message.lower()

    if p_message == "!help":
        return "`This is a help message that you can modify`"