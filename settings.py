from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_PASSWORD: str
    FROM_EMAIL: str
    AMQP_URL: str
    BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()