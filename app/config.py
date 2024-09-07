from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    super_admin_email: str
    super_admin_password: str
    super_admin_name: str

    class Config:
        env_file = ".env"

settings = Settings()
