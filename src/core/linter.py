import subprocess
import os


class Linter:
    def __init__(self, base_path="."):
        self.base_path = base_path

    def check_file(self, filename: str) -> str | None:
        file_path = os.path.join(self.base_path, filename)

        if not os.path.exists(file_path):
            return f"Fichier introuvable: {file_path}"
        try:

            result = subprocess.run(
                ["black", "--check", "--diff", file_path],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return result.stdout 
            return None
        except Exception as e:
            return f"Erreur lors du lint: {e}"
