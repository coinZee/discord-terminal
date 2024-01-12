import os
import discord
from dotenv import load_dotenv
import subprocess
from discord.ext import commands

load_dotenv()

BOT_KEY=os.getenv('BOT_KEY')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Your PC!!"))
    print('Logged in as {0.user}'.format(bot))

global process  # Declare process as a global variable
process = None  # Set process to None

def run_command(command: str):
    global process  # Access the global process variable
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode().strip()
    if not output:
        output = "No output"
        process.kill()
        return

    process.kill()
    return output

@bot.hybrid_command()
async def ctrl_c(ctx):
    global process  # Access the global process variable
    if process == None:
        await ctx.send('No process to kill')
        return
    process.kill()
    await ctx.send(f'{process.pid} killed')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("/"):
        await bot.process_commands(message)
        return
    await message.add_reaction('✅')
    response = run_command(str(message.content).lower().strip())
    if response == "":
        response = "No output"
    await message.channel.send(f"``` {response} ```")
    await message.remove_reaction('✅', bot.user)
        
bot.run(BOT_KEY)
