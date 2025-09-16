import os
import discord
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

REPO_CHANNELS = {
    "Boubker10/repo_test_codereviewer": 1417544173275578550,  
}

async def send_pr_review(repo_name: str, pr_number: int, review_message: str):
    channel_id = REPO_CHANNELS.get(repo_name)
    if not channel_id:
        print(f"⚠️ Aucun canal configuré pour {repo_name}")
        return

    await bot.wait_until_ready()

    try:
        channel = await bot.fetch_channel(channel_id)
        await channel.send(
            f"📢 Nouvelle review pour **{repo_name}** (PR #{pr_number}):\n\n{review_message}"
        )
        print(f"Message envoyé dans Discord pour PR #{pr_number}")
    except Exception as e:
        print(f"Impossible d'envoyer le message: {e}")

async def list_channels():
    """Affiche les canaux texte disponibles pour vérifier les IDs."""
    await bot.wait_until_ready()
    if not bot.guilds:
        print("Le bot n'est dans aucun serveur")
        return

    guild = bot.guilds[0]
    print(f"Serveur: {guild.name} (ID: {guild.id})\nCanaux texte disponibles :")
    for channel in guild.text_channels:
        print(f"- {channel.name} : {channel.id}")
