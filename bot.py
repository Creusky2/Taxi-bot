import discord
from discord import app_commands
from config import DISCORD_TOKEN
from commands import setup_commands

# Configuration des intents Discord
intents = discord.Intents.default()
intents.message_content = True  # Lire le contenu des messages
intents.guilds = True
intents.messages = True  # Lire les messages
intents.guild_messages = True  # Assure que les messages sont bien lus

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ {self.user} est connecté et prêt à recevoir des commandes !")
        await self.tree.sync()
        print("✅ Slash commands synchronisées avec Discord.")

# Instancier le bot
bot = MyBot()

# Ajouter les commandes
setup_commands(bot)

# Lancer le bot
bot.run(DISCORD_TOKEN)
