from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Alpogo Notifier"

    model_config = SettingsConfigDict(env_file=".env.development")