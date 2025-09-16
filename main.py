import os
from dotenv import load_dotenv
from src.core.reviewer import Reviewer
from src.core.discord_bot import bot

load_dotenv()

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

    repo_name = f"{os.getenv('GITHUB_USERNAME')}/repo_test_codereviewer"
    github_token = os.getenv("GITHUB_TOKEN")
    reviewer = Reviewer(repo_name, github_token)

    print("🔍 Analyse de toutes les PR ouvertes...")
    await reviewer.analyze_all_open_prs(post_to_github=True, post_to_discord=True)
    # await reviewer.analyze_pr(pr_number=3, post_to_github=True, post_to_discord=True)
    print("💡 Reviews postées. Le bot reste actif pour les prochaines PR.")

bot.run(os.getenv("DISCORD_TOKEN"))
