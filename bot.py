import os
import discord
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')

async def send_message(message: str, user_message: str, is_priv: bool):
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
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
    # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # If the user message contains a '?' in front of the text, it becomes a private message
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, True)
        else:
            await send_message(message, user_message, False)

def handle_response(message:str) -> str:
    p_message = message.lower()

    if p_message == "!help":
        return "`This is a help message that you can modify`"
