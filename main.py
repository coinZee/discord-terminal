import os
import discord
from dotenv import load_dotenv
import subprocess
from discord.ext import commands
import asyncio

load_dotenv()

########################
# Bot setup starts here
########################

BOT_KEY=os.getenv('BOT_KEY')
OWNER_ID=os.getenv('OWNER_ID')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "/", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="Your PC!!"))
    print('Logged in as {0.user}'.format(bot))

#######################
# Bot setup ends here
#######################

global process  # Declare process as a global variable
process = None  # Set process to None

# Main function to run the command
def run_command(command: str):
    global process  # Access the global process variable

    # Start the process with given command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    output, error = process.communicate() # Get the output and error of the process
    output = output.decode().strip() 
    if not output:
        output = "No output"
        process.kill() # Kills the process if there is no output
        return
    
    process.kill() # Kills the process after getting the output
    return output

# Command to kill process
@bot.hybrid_command()
@commands.is_owner()
async def ctrl_c(ctx):
    global process  # Access the global process variable
    # Checks if there any processes to kill
    if process == None:
        await ctx.send('No process to kill')
        return
    # If any process to kill, then kills it and send the 'process id' is killed
    process.kill()
    await ctx.send(f'``` {process.pid} killed ```')

@ctrl_c.error
async def ctrl_c_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You dont have access to do that <3", ephemeral=True)

# Function that happpens every time a message is sent
@bot.event
@commands.is_owner()
async def on_message(message):

    # Check if the message author is the bot itself
    if message.author == bot.user:
        return
    
    # Check if the message starts with the prefix
    if message.content.startswith("/"):
        await bot.process_commands(message)
        return
    
    # Check if the message author is the bot owner
    if str(message.author.id) != OWNER_ID:
        #await message.channel.send(message.author.id, ephemeral=True)
        #await message.channel.send(bot.owner_id, ephemeral=True)
        # Code for the none-bot owner
        await message.add_reaction('❌')
        #await message.channel.send("You cant use this bot", ephemeral=True) # Tells them they are not the owner u can uncommand this line if u want
        await asyncio.sleep(3)
        await message.remove_reaction('❌', bot.user)
        return

    else:
        # Code for owner 
        await message.add_reaction('✅')
        # Calls the function with what user gives as input
        response = run_command(str(message.content).lower().strip())
        if response == "" or None: # Checks if the response is None or ""
            response = "No output" # Then will reply with no output
        await message.channel.send(f"``` {response} ```")
        await message.remove_reaction('✅', bot.user)

# Command to check Your id to replace it the OWNER_ID in .env file
@bot.command()
@commands.is_owner()
async def show_id(ctx):
    await ctx.send(ctx.author.id, ephemeral=True)

# Run the bot
bot.run(BOT_KEY)
