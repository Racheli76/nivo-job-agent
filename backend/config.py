from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    mock_mode: bool = Field(True, env='MOCK_MODE')
    openai_api_key: str = Field('', env='OPENAI_API_KEY')
    openai_model: str = Field('gpt-4o-mini', env='OPENAI_MODEL')
    decide_threshold: int = Field(75, env='DECIDE_THRESHOLD')
    allowed_origins: List[str] = Field(
        ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
        env='ALLOWED_ORIGINS'
    )
    max_upload_size_bytes: int = Field(5 * 1024 * 1024, env='MAX_UPLOAD_SIZE_BYTES')
    redis_url: str = Field('', env='REDIS_URL')
    rate_limit_default: str = Field('60/minute', env='RATE_LIMIT_DEFAULT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
