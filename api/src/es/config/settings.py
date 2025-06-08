from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
from dotenv import dotenv_values
from typing import List, Tuple, Dict, Any
import os


class Settings(BaseSettings):
    es_hosts: List[str] = Field(default=["https://localhost:9200"])
    es_ca_certs: str = Field(default="../shared/certs/ca/ca.crt")
    es_username: str = Field(default="elastic")
    es_password: str = Field(default="changeme")
    es_verify_certs: bool = Field(default=False)
    search_index_name: str = Field(default="cmp-search-item-index-001")
    search_match_key: str = Field(default="searchText")

    @property
    def es_basic_auth(self) -> Tuple[str, str]:
        return self.es_username, self.es_password
    
    @field_validator('es_verify_certs', mode='before')
    @classmethod
    def parse_bool(cls, v):
        if isinstance(v, str):
            if v.lower() in ('true', 't', 'yes', 'y', '1'):
                return True
            elif v.lower() in ('false', 'f', 'no', 'n', '0'):
                return False
        return v
        
    @field_validator('es_hosts', mode='before')
    @classmethod
    def parse_hosts(cls, v):
        if isinstance(v, str):
            # Split by comma if multiple hosts are provided
            if ',' in v:
                return [host.strip() for host in v.split(',')]
            # Otherwise, return as a single-item list
            return [v.strip()]
        return v

    model_config = {
        "case_sensitive": False,
        "env_prefix": "",
        "extra": "ignore"  # Changed from "forbid" to "ignore"
    }


def load_env() -> Settings:
    env = os.getenv("ENV", "dev")
    base_env = dotenv_values(".env") or {}
    env_specific = dotenv_values(f".env.{env}") or {}
    combined = {**base_env, **env_specific}
    
    # Convert keys to lowercase for case-insensitive matching
    normalized = {k.lower(): v for k, v in combined.items()}
    
    return Settings(**normalized)


settings = load_env()
