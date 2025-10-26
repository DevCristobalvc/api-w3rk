"""
W3RK Platform Configuration
Enhanced configuration for ASI Alliance Hackathon submission
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==============================================================================
# ASI ALLIANCE INTEGRATION SETTINGS
# ==============================================================================

# ASI1.AI API Configuration
ASI_API_KEY = os.getenv("ASI_API_KEY", "sk_ed969150aed64671904ea6b3e50ee791ff54ef8a8cdd4c8980a32766ba3efc21")
ASI_API_URL = os.getenv("ASI_API_URL", "https://api.asi1.ai/v1/chat/completions")

# uAgents Framework Configuration
UAGENTS_ENVIRONMENT = os.getenv("UAGENTS_ENVIRONMENT", "testnet")
AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY", "")
AGENTVERSE_BASE_URL = "https://agentverse.ai/api/v1/"

# MeTTa Configuration
METTA_ENVIRONMENT = os.getenv("METTA_ENVIRONMENT", "development")
METTA_KNOWLEDGE_PATH = "./metta/knowledge_base/"

# ==============================================================================
# BLOCKCHAIN & WEB3 SETTINGS
# ==============================================================================

# Ethereum/Blockchain Configuration
ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL", "https://sepolia.infura.io/v3/YOUR_PROJECT_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")  # For contract interactions
CHAIN_ID = int(os.getenv("CHAIN_ID", "11155111"))  # Sepolia testnet

# Smart Contract Addresses (updated after deployment)
CONTRACTS = {
    "PROFILE_REGISTRY": os.getenv("PROFILE_REGISTRY_ADDRESS", "0x..."),
    "CV_REGISTRY": os.getenv("CV_REGISTRY_ADDRESS", "0x..."),
    "SKILLS_VALIDATION": os.getenv("SKILLS_VALIDATION_ADDRESS", "0x..."),
    "NETWORK_CONNECTIONS": os.getenv("NETWORK_CONNECTIONS_ADDRESS", "0x..."),
    "ACHIEVEMENT_NFTS": os.getenv("ACHIEVEMENT_NFTS_ADDRESS", "0x...")
}

# IPFS Configuration
IPFS_API_URL = os.getenv("IPFS_API_URL", "http://localhost:5001")
IPFS_GATEWAY_URL = os.getenv("IPFS_GATEWAY_URL", "https://ipfs.io/ipfs/")
PINATA_API_KEY = os.getenv("PINATA_API_KEY", "")
PINATA_SECRET_KEY = os.getenv("PINATA_SECRET_KEY", "")

# ==============================================================================
# SERVER & APPLICATION SETTINGS  
# ==============================================================================

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
RELOAD = os.getenv("RELOAD", "True").lower() == "true"

# Application Settings
APP_NAME = "W3RK Platform"
APP_VERSION = "1.0.0 - ASI Alliance"
APP_DESCRIPTION = "Decentralized Professional Network with ASI Alliance Integration"

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:3000",  # React development
    "http://localhost:3001", 
    "https://w3rk-demo.vercel.app",  # Production frontend
    "*"  # Allow all for hackathon demo
]

# ==============================================================================
# DATABASE & STORAGE SETTINGS
# ==============================================================================

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./w3rk_platform.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Session and Security
SECRET_KEY = os.getenv("SECRET_KEY", "w3rk_hackathon_secret_key_2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ==============================================================================
# AI & PROCESSING SETTINGS
# ==============================================================================

# AI Processing Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MAX_PROCESSING_TIME = int(os.getenv("MAX_PROCESSING_TIME", "30"))  # seconds
MAX_CONCURRENT_AGENTS = int(os.getenv("MAX_CONCURRENT_AGENTS", "10"))

# Agent Configuration
AGENT_PORTS = {
    "career_advisor": 8001,
    "skills_analyzer": 8002, 
    "network_connector": 8003,
    "opportunity_matcher": 8004,
    "profile_analyzer": 8005
}

AGENT_SEEDS = {
    "career_advisor": "career_advisor_w3rk_hackathon_seed_2024",
    "skills_analyzer": "skills_analyzer_w3rk_hackathon_seed_2024",
    "network_connector": "network_connector_w3rk_hackathon_seed_2024", 
    "opportunity_matcher": "opportunity_matcher_w3rk_hackathon_seed_2024",
    "profile_analyzer": "profile_analyzer_w3rk_hackathon_seed_2024"
}

# ==============================================================================
# HACKATHON DEMO SETTINGS
# ==============================================================================

# Demo Configuration
DEMO_MODE = os.getenv("DEMO_MODE", "True").lower() == "true"
DEMO_USER_ADDRESS = "0x742d35Cc6635C0532925a3b8D0984C841e2489b0"
DEMO_PROFILES_COUNT = 100
DEMO_CONVERSATIONS_COUNT = 50

# Performance Monitoring
ENABLE_METRICS = True
METRICS_COLLECTION_INTERVAL = 60  # seconds

# Logging Configuration  
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==============================================================================
# FEATURE FLAGS
# ==============================================================================

# Feature Toggles for Hackathon Demo
FEATURES = {
    "ASI_ALLIANCE_INTEGRATION": True,
    "UAGENTS_FRAMEWORK": True,
    "METTA_KNOWLEDGE_GRAPHS": True,
    "BLOCKCHAIN_INTEGRATION": True,
    "IPFS_STORAGE": True,
    "REAL_TIME_CHAT": True,
    "WEBSOCKET_SUPPORT": True,
    "ACHIEVEMENT_NFTS": True,
    "SKILL_VALIDATION": True,
    "CAREER_ANALYSIS": True,
    "DEMO_MODE": DEMO_MODE
}

# API Rate Limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # seconds