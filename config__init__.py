"""
Configuration management for Project Corvus.
Centralizes all configuration with environment variable fallbacks.
"""
import os
from typing import Dict, Any
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()

class CorvusConfig(BaseSettings):
    """Main configuration class with validation."""
    
    # Firebase Configuration
    firebase_credentials_path: str = Field(
        default="config/firebase-credentials.json",
        env="FIREBASE_CREDENTIALS_PATH"
    )
    firestore_collection: str = Field(
        default="infrastructure_sovreignty",
        env="FIRESTORE_COLLECTION"
    )
    
    # Cloud Provider Configuration
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    gcp_project_id: str = Field(default=os.getenv("GCP_PROJECT_ID", ""))
    azure_subscription_id: str = Field(default=os.getenv("AZURE_SUBSCRIPTION_ID", ""))
    
    # Monitoring Configuration
    check_interval_seconds: int = Field(default=300, ge=60, le=3600)
    health_check_timeout: int = Field(default=30, ge=5, le=120)
    max_retry_attempts: int = Field(default=3, ge=1, le=5)
    
    # Alerting Configuration
    telegram_bot_token: str = Field(default="", env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str = Field(default="", env="TELEGRAM_CHAT_ID")
    alert_cooldown_minutes: int = Field(default=15, ge=1, le=1440)
    
    # Cost Optimization
    daily_cost_threshold_usd: float = Field(default=100.0, ge=0.0)
    optimize_underutilized_resources: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global configuration instance
config = CorvusConfig()