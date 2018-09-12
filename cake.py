import discord, traceback, config
from discord.ext import commands
from os import listdir
from os.path import isfile, join

def get_prefix(bot, message):
    prefixes = ['!']

    #Allow only ! in PM
    if not message.guild:
        return '!'

    #Allow multiple prefixes while not in a PM
    return commands.when_mentioned_or(*prefixes)(bot, message)


#Modules directory
mods_dir = "slices"

bot = commands.Bot(command_prefix=get_prefix, description='A Modular Cakebot!')

#Load modules (slices)
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(mods_dir) if isfile(join(mods_dir, f))]:
        try:
            bot.load_extension(mods_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()


@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    #List Servers
    print("Servers connected to:")
    for guild in bot.guilds:
        print(guild.name)

    print("\nSuccessfully logged in!")
    print("-------------------")

bot.run(config.bot_token, bot=True, reconnect=True)