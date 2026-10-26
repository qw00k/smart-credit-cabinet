from pydantic_settings import BaseSettings

class Nastroiki(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:admin@db:5432/credit_db"
    SECRET_KEY: str = "supersecretkey"
    OLLAMA_URL: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "qwen2.5:1.5b"

    class Config:
        env_file = ".env"

nastroiki = Nastroiki()
