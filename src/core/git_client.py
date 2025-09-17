import os
import requests


class GitClient:
    def __init__(self, repo: str | None = None, token: str | None = None):
        if not repo:
            owner = os.getenv("GIT_USERNAME")
            name = os.getenv("GIT_repo")
            if not owner or not name:
                raise ValueError(
                    "GITHUB_REPO_OWNER ou GITHUB_REPO_NAME n'est pas défini dans les variables d'environnement."
                )
            repo = f"{owner}/{name}"

        self.repo = repo
        self.token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GIT_TOKEN")
        if not self.token:
            raise ValueError("Aucun token GitHub fourni. Définis GITHUB_TOKEN dans ton .env ou secrets.")

        self.base_url = f"https://api.github.com/repos/{repo}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_pull_request_files(self, pr_number: int):
        url = f"{self.base_url}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_pull_request_info(self, pr_number: int):
        url = f"{self.base_url}/pulls/{pr_number}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def comment_on_pr(self, pr_number: int, body: str):
        url = f"{self.base_url}/issues/{pr_number}/comments"
        data = {"body": body}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def list_open_pull_requests(self):
        url = f"{self.base_url}/pulls?state=open"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
