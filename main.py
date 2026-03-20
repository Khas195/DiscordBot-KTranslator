import discord
from discord.ext import commands
import logging
import textwrap
from dotenv import load_dotenv
import os
import webserver
from deep_translator import GoogleTranslator

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()

## If you want to use message content or member information, you need to enable the corresponding intents. Make sure to also enable these intents in the Discord Developer Portal for your bot.
## Intents documentation: https://discordpy.readthedocs.io/en/stable/intents.html
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!k', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!khelp'):
        helpMessage = f'''
        Here is how to use the bot, {message.author.mention}!
        Tag a message with the flag of the language you want to translate to!
        For example, if you want to translate a message to Vietnamese, you can tag it with the :flag_vn: emoji.
        You can also use the command !khelp to get this message again!'''

        ## f strings are a convenient way to format strings in Python. They allow you to embed expressions inside string literals, using curly braces {}. In this case, {message.author.mention} will be replaced with the mention of the user who sent the message, making the response more personalized.
        ## multiline string example: https://www.programiz.com/python-programming/multiline-string
        await message.reply(textwrap.dedent(helpMessage).strip())

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    # Check if the reaction is a flag emoji
    if reaction.emoji in ['🇻🇳', '🇺🇸', '🇯🇵', '🇰🇷', '🇨🇳']:
        # Get the message that was reacted to
        message = reaction.message

        # Translate the message content based on the emoji
        if reaction.emoji == '🇻🇳':
            translated = GoogleTranslator(source='auto', target='vi').translate(text=message.content)
            translated_text = f'Translated to Vietnamese: {translated}'
        elif reaction.emoji == '🇺🇸':
            translated = GoogleTranslator(source='auto', target='en').translate(text=message.content)
            translated_text = f'Translated to English: {translated}'
        elif reaction.emoji == '🇯🇵':
            translated = GoogleTranslator(source='auto', target='ja').translate(text=message.content)
            translated_text = f'Translated to Japanese: {translated}'
        elif reaction.emoji == '🇰🇷':
            translated = GoogleTranslator(source='auto', target='ko').translate(text=message.content)
            translated_text = f'Translated to Korean: {translated}'
        elif reaction.emoji == '🇨🇳':
            translated = GoogleTranslator(source='auto', target='zh').translate(text=message.content)
            translated_text = f'Translated to Chinese: {translated}'

        await message.reply(translated_text)

webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.INFO)