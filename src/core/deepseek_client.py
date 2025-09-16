import os
import aiohttp
import asyncio

class DeepSeekClient:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/chat/completions")
        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    async def review_code(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"DeepSeek API Error ({resp.status}): {text}")
                data = await resp.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
