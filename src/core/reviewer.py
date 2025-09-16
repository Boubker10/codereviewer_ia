import os
from .git_client import GitClient
from .linter import Linter
from .deepseek_client import DeepSeekClient
import load_dotenv



class Reviewer:
    def __init__(self, repo: str, token: str | None = None):
        self.client = GitClient(repo, token)
        self.linter = Linter()
        self.deepseek = DeepSeekClient(api_key=os.getenv("DEEPSEEK_API_KEY"))

    def analyze_pr(self, pr_number: int):
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
        - Strengths (good practices found)
        - Issues (bugs, risky patterns, code smells)
        - Improvements (refactoring, performance, readability, security)
        Be precise and actionable.

        --- PULL REQUEST DIFF ---
        {full_diff}
        """

        ai_feedback = self.deepseek.review_code(prompt)

        lint_feedback = []
        for f in files:
            filename = f["filename"]
            lint_result = self.linter.check_file(filename)
            if lint_result:
                lint_feedback.append(f"📝 Formatage requis dans `{filename}`:\n{lint_result}")

        message = "## 🤖 Code Review by code reviewer (by Boubker10)\n\n"
        message += ai_feedback
        if lint_feedback:
            message += "\n\n---\n\n" + "\n".join(lint_feedback)

        self.client.comment_on_pr(pr_number, message)
