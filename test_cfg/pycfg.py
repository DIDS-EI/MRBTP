
# config.py

from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 3306

@dataclass
class AppConfig:
    db: DatabaseConfig = DatabaseConfig()
    debug: bool = False
