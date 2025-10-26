"""
MeTTa Models for W3RK Platform
Data models for MeTTa knowledge graph integration
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class SkillRelation(BaseModel):
    """Skill relationship model for MeTTa knowledge graphs"""
    source_skill: str = Field(..., description="Source skill name")
    target_skill: str = Field(..., description="Target skill name")
    relationship_type: str = Field(..., description="Type of relationship (similarity, prerequisite, etc.)")
    strength: float = Field(..., ge=0, le=1, description="Relationship strength")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in relationship")

class CareerPath(BaseModel):
    """Career progression path model"""
    source_role: str = Field(..., description="Starting role")
    target_role: str = Field(..., description="Target role")
    timeline_months: int = Field(..., description="Expected timeline in months")
    required_skills: List[str] = Field(default=[], description="Skills needed for transition")
    difficulty_score: float = Field(..., ge=0, le=10, description="Difficulty score")

class MarketInsight(BaseModel):
    """Market analysis and insights"""
    skill_name: str = Field(..., description="Skill or role name")
    demand_growth: float = Field(..., description="Annual demand growth rate")
    salary_trend: str = Field(..., description="Salary trend direction")
    market_saturation: float = Field(..., ge=0, le=1, description="Market saturation level")
    geographic_distribution: Dict[str, float] = Field(default={}, description="Geographic demand distribution")