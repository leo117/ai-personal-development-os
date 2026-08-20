from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Personal Development OS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置，默认使用本地 SQLite 零配置自建，同时支持 PostgreSQL
    DATABASE_URL: str = "sqlite:///./study_grow.db"
    
    # 认知隐私密钥
    COGNITIVE_VAULT_SECRET: str = "super-secret-vault-key-32bytes!!"
    
    # 默认 AI 援助参数
    DEFAULT_ASSISTANCE_BUDGET: int = 100
    AI_ASSIST_PENALTY_LAMBDA: float = 0.3
    
    # ==========================================
    # 🤖 AI 模型与 LLM API 接口配置
    # ==========================================
    # 支持任何兼容 OpenAI 协议的接口 (OpenAI, DeepSeek, Gemini, Ollama, 智谱, 阿里百炼, SiliconFlow等)
    LLM_API_KEY: Optional[str] = None
    LLM_API_BASE: str = "https://api.openai.com/v1"
    LLM_MODEL_NAME: str = "gpt-4o"
    LLM_TEMPERATURE: float = 0.3
    LLM_TIMEOUT_SECONDS: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

settings = Settings()
