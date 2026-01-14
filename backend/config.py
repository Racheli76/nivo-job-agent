from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    mock_mode: bool = Field(True, validation_alias='MOCK_MODE')
    openai_api_key: str = Field('', validation_alias='OPENAI_API_KEY')
    openai_model: str = Field('gpt-4o-mini', validation_alias='OPENAI_MODEL')
    decide_threshold: int = Field(75, validation_alias='DECIDE_THRESHOLD')
    allowed_origins: List[str] = Field(
        ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
        validation_alias='ALLOWED_ORIGINS'
    )
    max_upload_size_bytes: int = Field(5 * 1024 * 1024, validation_alias='MAX_UPLOAD_SIZE_BYTES')
    redis_url: str = Field('', validation_alias='REDIS_URL')
    rate_limit_default: str = Field('60/minute', validation_alias='RATE_LIMIT_DEFAULT')

settings = Settings()
