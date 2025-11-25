from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Blockchain
    BLOCKCHAIN_RPC_URL: str
    BLOCKCHAIN_CHAIN_ID: int
    CONTRACT_ADDRESS: str = ""
    DEPLOYER_ADDRESS: str
    DEPLOYER_KEYSTORE_PATH: str
    DEPLOYER_PASSWORD: str
    
    # CORS
    CORS_ORIGINS: str = '["http://localhost:5173"]'
    
    # App
    APP_NAME: str = "Blockchain Bootcamp API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() # type: ignore