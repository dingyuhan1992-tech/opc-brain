import json
from typing import Optional
from openai import OpenAI
from config import settings


class AIEngine:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = OpenAI(
                api_key=settings.LLM_API_KEY or "sk-placeholder",
                base_url=settings.LLM_BASE_URL,
            )
        return self._client

    def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"AI 调用失败: {str(e)}"

    def chat_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"{system_prompt}\n你必须以 JSON 格式输出。"},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=temperature,
            )
            text = resp.choices[0].message.content.strip()
            return json.loads(text)
        except Exception as e:
            return {"error": str(e)}


engine = AIEngine()
