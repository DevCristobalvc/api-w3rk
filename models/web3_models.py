"""
Web3 Models for W3RK Platform
Blockchain integration data models
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class BlockchainProfile(BaseModel):
    """Blockchain-stored professional profile"""
    wallet_address: str = Field(..., description="User's wallet address")
    profile_hash: str = Field(..., description="IPFS hash of profile data")
    verification_status: str = Field(default="pending", description="Verification status")
    last_updated: datetime = Field(default_factory=datetime.now)
    reputation_score: float = Field(default=0.0, ge=0, le=100)

class Achievement(BaseModel):
    """Professional achievement NFT model"""
    token_id: int = Field(..., description="NFT token ID")
    achievement_type: str = Field(..., description="Type of achievement")
    title: str = Field(..., description="Achievement title")
    description: str = Field(..., description="Achievement description")
    metadata_uri: str = Field(..., description="IPFS metadata URI")
    earned_date: datetime = Field(default_factory=datetime.now)

class SkillVerification(BaseModel):
    """Blockchain skill verification"""
    skill_name: str = Field(..., description="Name of the skill")
    proficiency_level: str = Field(..., description="Skill proficiency level")
    verifier_address: str = Field(..., description="Address of verifier")
    verification_date: datetime = Field(default_factory=datetime.now)
    evidence_hash: str = Field(..., description="IPFS hash of evidence")

class SmartContractTransaction(BaseModel):
    """Smart contract transaction record"""
    transaction_hash: str = Field(..., description="Blockchain transaction hash")
    contract_address: str = Field(..., description="Smart contract address")
    function_name: str = Field(..., description="Contract function called")
    gas_used: int = Field(..., description="Gas used for transaction")
    transaction_cost: float = Field(..., description="Transaction cost in ETH")