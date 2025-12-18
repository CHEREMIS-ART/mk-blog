from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    RABBITMQ_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    APP_ENV: str = "local"

    COOKIE_NAME: str = "access_token"


settings = Settings()
