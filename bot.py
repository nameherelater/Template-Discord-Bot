import os
import discord
import logging
from discord.ext import commands
import asyncio
import random
import time
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord')

token = os.environ.get("DISCORD_TOKEN")

commandPrefix = os.environ.get("COMMAND_PREFIX")
if not token:
    logger.error("Discord token not found! Set the DISCORD_TOKEN environment variable.")
    exit(1)

if not commandPrefix:
    logger.error("Discord commandPrefix not found! Set the COMMAND_PREFIX environment variable.")
    exit(1)


intents = discord.Intents.default()
intents.message_content = True  
intents.members = True

bot = commands.Bot(command_prefix=commandPrefix, intents=intents, help_command=None)

@bot.command(name="ping", help="Verifica o tempo de resposta do bot")
async def ping(ctx):
    # Ping Pong - Mede a latência do bot
    start_time = time.time()
    message = await ctx.send("Pinging...")
    end_time = time.time()

    api_latency = round(bot.latency * 1000)
    message_latency = round((end_time - start_time) * 1000)

    embed = discord.Embed(title="Pong!", color=discord.Color.green())
    embed.add_field(name="API Latency", value=f"{api_latency}ms", inline=True)
    embed.add_field(name="Message Latency", value=f"{message_latency}ms", inline=True)

    await message.edit(content=None, embed=embed)

@bot.command(name="help", help="Exibe a lista de comandos disponíveis")
async def help_command(ctx, command=None):
    # Mostrar comandos do bot e suas descrições
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blue())

    if command:
        cmd = bot.get_command(command)
        if cmd:
            embed.description = f"**{cmd.name}** - {cmd.help or 'No description available'}"
            embed.add_field(name="Usage", value=f"`!{cmd.name}`", inline=False)
        else:
            embed.description = f"Command `{command}` not found."
    else:
        embed.description = "Comandos disponíveis:"

        for cmd in bot.commands:
            if not cmd.hidden:
                embed.add_field(
                    name=f"{cmd.name}",
                    value=cmd.help or "No description available",
                    inline=False
                )

        embed.set_footer(text="Digite !help <command> para mais informações de cada comando")

    await ctx.send(embed=embed)

@bot.command(name="info", help="Exibe informações sobre o bot e seus criadores")
async def info(ctx):
    # Mostrar informações detalhadas do bot
    embed = discord.Embed(
        title="Como o bot foi feito",
        description="https://nameherelater.com/como-fazer-um-bot-no-discord/",
        color=discord.Color.blue()
    )

    embed.add_field(name="Nome do Bot", value=bot.user.name, inline=False)
    embed.add_field(name="Criado por", value="Desenvolvedores dedicados do NameHereLater", inline=False)
    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=False)
    embed.add_field(name="Comandos", value=str(len(bot.commands)), inline=False)
    embed.add_field(name="Prefixo", value="!", inline=False)

    await ctx.send(embed=embed)

@bot.command(name="greet", help="Cumprimenta um membro do servidor")
async def greet(ctx, *, member: discord.Member = None):
    # Saudar um membro do servidor com uma mensagem amigável
    member = member or ctx.author
    greeting = f"Olá {member.mention}! Espero que você tenha um ótimo dia!"

    embed = discord.Embed(
        title="Bom Dia!",
        description=greeting,
        color=discord.Color.gold()
    )

    await ctx.send(embed=embed)

@bot.command(name="joke", help="Conta uma piada aleatória para alegrar o chat")
async def joke(ctx): # Comando para contar piadas aleatórias
    jokes = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
    ]

    selected_joke = random.choice(jokes)

    embed = discord.Embed(
        title="Aqui está uma piada:",
        description=selected_joke,
        color=discord.Color.purple()
    )

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    # Lidar com erros

    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Comando não encontrado, tente `!help` para a lista de comandos")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Erro: {error.param.name}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para usar este comando")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"An error occurred: {error}")

# Inicialização do bot
@bot.event
async def on_ready():
    # Evento acionado quando o bot está conectado

    logger.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    logger.info(f'Connected to {len(bot.guilds)} guilds')

    # Definir status do bot no discord
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, 
        name="!help"
    ))

    logger.info('Bot is ready!')

# Importar keep_alive para executar um web Server
from keep_alive import keep_alive

# Executar bot
if __name__ == "__main__":
    logger.info("Starting Discord bot...")
    try:
        # Iniciar web server primeiro (importante para o Render)
        logger.info("Starting web server...")
        keep_alive()

        # Iniciar bot
        logger.info("Starting Discord bot...")
        bot.run(token)  # Use bot.run instead of asyncio.run para uma estabilidade melhor
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
