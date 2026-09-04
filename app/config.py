from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  database_hostname: str
  database_port: str
  database_username: str
  database_name: str
  database_name_test: str
  database_password: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int
  
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8"
  )

settings = Settings() # type: ignore