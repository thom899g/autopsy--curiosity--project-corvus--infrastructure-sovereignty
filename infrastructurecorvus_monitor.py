"""
Core monitoring engine for Project Corvus.
Implements multi-cloud infrastructure sovereignty monitoring with automated remediation.
"""
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass
import asyncio

import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from config import config
from .firebase_client import FirebaseClient
from .cloud_providers import CloudProviderFactory

logger = structlog.get_logger()

class HealthStatus(Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class ResourceType(Enum):
    """Cloud resource types."""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    SECURITY = "security"

@dataclass
class ResourceMetric:
    """Resource metric data class."""
    resource_id: str
    resource_type: ResourceType
    provider: str
    region: str
    status: HealthStatus
    metrics: Dict[str,