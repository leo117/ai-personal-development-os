import httpx
from typing import Optional, List, Dict, Any
from app.core.config import settings

class LLMClient:
    """
    通用 LLM 调用客户端（兼容 OpenAI 协议接口，支持 DeepSeek / OpenAI / Ollama / 智谱 / 百炼等）
    """
    @classmethod
    def is_configured(cls) -> bool:
        return bool(settings.LLM_API_KEY and settings.LLM_API_KEY.strip())

    @classmethod
    def chat_completion(
        cls, 
        system_prompt: str, 
        user_prompt: str, 
        temperature: Optional[float] = None
    ) -> Optional[str]:
        """
        同步调用大模型聊天接口，若未配置或调用失败则返回 None
        """
        if not cls.is_configured():
            return None

        headers = {
            "Authorization": f"Bearer {settings.LLM_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": settings.LLM_MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature if temperature is not None else settings.LLM_TEMPERATURE
        }

        api_url = f"{settings.LLM_API_BASE.rstrip('/')}/chat/completions"

        try:
            with httpx.Client(timeout=settings.LLM_TIMEOUT_SECONDS) as client:
                response = client.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    print(f"[WARN] LLM API returned status {response.status_code}: {response.text}")
                    return None
        except Exception as e:
            print(f"[WARN] LLM API call failed: {e}")
            return None
