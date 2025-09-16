import subprocess

class Linter:
    def check_file(self, filepath: str) -> str | None:
        try:
            result = subprocess.run(
                ["black", "--check", filepath],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                return result.stdout + result.stderr
            return None
        except Exception as e:
            return f"Erreur lors du linting: {e}"
