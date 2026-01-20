from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    from_email: str = "test@local.dev"
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_PASSWORD: str = ""
    AMQP_URL: str = 'amqp://guest:guest@localhost:5672/'