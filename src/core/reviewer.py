import os
import asyncio
from dotenv import load_dotenv

from .git_client import GitClient
from .linter import Linter
from .deepseek_client import DeepSeekClient
from .discord_bot import send_pr_review

load_dotenv()

class Reviewer:
    def __init__(self, repo: str, token: str = None):
        self.repo = repo
        self.client = GitClient(repo, token)
        self.linter = Linter()
        self.deepseek = DeepSeekClient(api_key=os.getenv("DEEPSEEK_API_KEY"))

    async def analyze_pr(self, pr_number: int, post_to_github: bool = True, post_to_discord: bool = True):
        pr_url = f"https://github.com/{self.repo}/pull/{pr_number}"
        if self.client.has_already_reviewed(pr_number):
            print(f"⏩ PR #{pr_number} déjà traitée, on ignore.")

            if post_to_discord:
                await send_pr_review(
                    self.repo,
                    pr_number,
                    f"⚠️ PR #{pr_number} a déjà été reviewée par CodeReviewerIA.\n👉 Consultez la review ici : {pr_url}"
                )
            return None
        files = self.client.get_pull_request_files(pr_number)

        diffs = []
        for f in files:
            filename = f["filename"]
            patch = f.get("patch", "")
            diffs.append(f"### File: {filename}\n{patch}")

        full_diff = "\n\n".join(diffs)

        prompt = f"""
        You are a senior software engineer reviewing a pull request.
        Analyze the following diff and provide:

        You are an expert Python developer and code reviewer.
        Please review the following pull request diff carefully and provide:

        - ✅ Strengths
        - ⚠️ Issues
        - 💡 Suggestions ( always give a code suggestions)

        Respond **in Markdown format**, **concise**, **under 1500 characters**, so it can be posted directly on Discord.



        --- PULL REQUEST DIFF ---
        {full_diff}
        """

        ai_feedback = await self.deepseek.review_code(prompt)

        lint_feedback = []
        for f in files:
            filename = f["filename"]
            lint_result = self.linter.check_file(filename)
            if lint_result:
                lint_feedback.append(f"📝 Formatage requis dans `{filename}`:\n{lint_result}")

        message = "## 🤖 Code Review by CodeReviewerIA\n\n" + ai_feedback
        if lint_feedback:
            message += "\n\n---\n\n" + "\n".join(lint_feedback)
        
        message_with_signature = message + "\n\n<!-- reviewed-by-codereviewer-ia -->"

        if post_to_github:
            self.client.comment_on_pr(pr_number, message_with_signature)

        if post_to_discord:
            await send_pr_review(self.repo, pr_number, message_with_signature)

        return message_with_signature

    async def analyze_all_open_prs(self, post_to_github: bool = True, post_to_discord: bool = True):
        prs = self.client.list_open_pull_requests()
        for pr in prs:
            pr_number = pr["number"]
            print(f"Analyse PR #{pr_number}")
            await self.analyze_pr(pr_number, post_to_github, post_to_discord)
