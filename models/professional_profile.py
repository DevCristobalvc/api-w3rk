"""
Professional Profile Models for W3RK Platform
Comprehensive data structures for professional identity management
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    EXPERT = "expert"

class VerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class Skill(BaseModel):
    """Individual skill with verification and proficiency tracking"""
    name: str = Field(..., description="Skill name")
    level: SkillLevel = Field(..., description="Proficiency level")
    verification_status: VerificationStatus = Field(default=VerificationStatus.UNVERIFIED)
    endorsements: int = Field(default=0, description="Number of peer endorsements")
    evidence_ipfs_hash: Optional[str] = Field(None, description="IPFS hash of evidence")
    verified_by: List[str] = Field(default=[], description="List of verifier addresses")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator('name')
    def validate_skill_name(cls, v):
        if len(v) < 2 or len(v) > 50:
            raise ValueError('Skill name must be between 2-50 characters')
        return v.strip().title()

class Experience(BaseModel):
    """Professional experience entry with verification"""
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job position/title")
    description: str = Field(..., description="Job description")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date (None if current)")
    skills_used: List[str] = Field(default=[], description="Skills utilized in this role")
    achievements: List[str] = Field(default=[], description="Notable achievements")
    verification_status: VerificationStatus = Field(default=VerificationStatus.UNVERIFIED)
    evidence_ipfs_hash: Optional[str] = Field(None, description="IPFS hash of proof")
    
    @validator('description')
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError('Description must be at least 10 characters')
        return v

    @property
    def is_current(self) -> bool:
        return self.end_date is None

    @property
    def duration_months(self) -> int:
        end = self.end_date or datetime.now()
        return (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)

class Education(BaseModel):
    """Educational background with credentials"""
    institution: str = Field(..., description="Educational institution")
    degree: str = Field(..., description="Degree or certification name")
    field_of_study: str = Field(..., description="Major/specialization")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    gpa: Optional[float] = Field(None, ge=0, le=4, description="GPA (0-4 scale)")
    achievements: List[str] = Field(default=[], description="Academic achievements")
    verification_status: VerificationStatus = Field(default=VerificationStatus.UNVERIFIED)
    credential_ipfs_hash: Optional[str] = Field(None, description="IPFS hash of diploma/certificate")

class NetworkConnection(BaseModel):
    """Professional network connection"""
    user_address: str = Field(..., description="Connected user's wallet address")
    connection_type: str = Field(default="professional", description="Type of connection")
    endorsed_skills: List[str] = Field(default=[], description="Skills endorsed by this connection")
    mutual_connections: int = Field(default=0, description="Number of mutual connections")
    connection_strength: float = Field(default=1.0, ge=0, le=10, description="Connection strength score")
    connected_at: datetime = Field(default_factory=datetime.now)
    last_interaction: datetime = Field(default_factory=datetime.now)

class ReputationMetrics(BaseModel):
    """Comprehensive reputation scoring"""
    overall_score: float = Field(default=0.0, ge=0, le=100, description="Overall reputation score")
    skill_verification_score: float = Field(default=0.0, ge=0, le=100)
    network_quality_score: float = Field(default=0.0, ge=0, le=100)
    activity_score: float = Field(default=0.0, ge=0, le=100)
    peer_endorsement_score: float = Field(default=0.0, ge=0, le=100)
    total_endorsements: int = Field(default=0)
    verification_count: int = Field(default=0)
    last_updated: datetime = Field(default_factory=datetime.now)

class ProfessionalProfile(BaseModel):
    """Complete professional profile with AI-enhanced features"""
    # Core Identity
    wallet_address: str = Field(..., description="Unique Web3 wallet address")
    username: str = Field(..., description="Unique username")
    display_name: str = Field(..., description="Display name")
    bio: str = Field(default="", description="Professional biography")
    location: Optional[str] = Field(None, description="Location")
    
    # Professional Information
    title: str = Field(default="", description="Current professional title")
    industry: Optional[str] = Field(None, description="Industry sector")
    experience_years: int = Field(default=0, ge=0, description="Total years of experience")
    
    # Core Collections
    skills: List[Skill] = Field(default=[], description="Professional skills")
    experiences: List[Experience] = Field(default=[], description="Work experience")
    education: List[Education] = Field(default=[], description="Educational background")
    connections: List[NetworkConnection] = Field(default=[], description="Professional network")
    
    # Metrics & Verification
    reputation: ReputationMetrics = Field(default_factory=ReputationMetrics)
    profile_completion: float = Field(default=0.0, ge=0, le=100, description="Profile completion percentage")
    
    # Blockchain Integration
    profile_ipfs_hash: Optional[str] = Field(None, description="IPFS hash of complete profile")
    cv_ipfs_hash: Optional[str] = Field(None, description="IPFS hash of generated CV")
    nft_achievements: List[str] = Field(default=[], description="Achievement NFT token IDs")
    
    # AI Enhancement Data
    ai_generated_summary: Optional[str] = Field(None, description="AI-generated professional summary")
    career_recommendations: List[str] = Field(default=[], description="AI career suggestions")
    skill_gap_analysis: Dict[str, Any] = Field(default={}, description="AI skill gap analysis")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_ai_analysis: Optional[datetime] = Field(None, description="Last AI analysis timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @validator('wallet_address')
    def validate_wallet_address(cls, v):
        if not v.startswith('0x') or len(v) != 42:
            raise ValueError('Invalid Ethereum wallet address')
        return v.lower()
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be between 3-20 characters')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, hyphens and underscores')
        return v.lower()
    
    def calculate_profile_completion(self) -> float:
        """Calculate profile completion percentage based on filled fields"""
        total_fields = 0
        completed_fields = 0
        
        # Core fields (40% weight)
        core_fields = [self.display_name, self.bio, self.title, self.industry, self.location]
        total_fields += 5
        completed_fields += sum(1 for field in core_fields if field and field.strip())
        
        # Skills (25% weight)
        total_fields += 2
        if self.skills:
            completed_fields += 1
            if len(self.skills) >= 5:
                completed_fields += 1
        
        # Experience (20% weight)
        total_fields += 2
        if self.experiences:
            completed_fields += 1
            if len(self.experiences) >= 2:
                completed_fields += 1
        
        # Education (10% weight)
        total_fields += 1
        if self.education:
            completed_fields += 1
        
        # Network (5% weight)
        total_fields += 1
        if len(self.connections) >= 5:
            completed_fields += 1
        
        completion = (completed_fields / total_fields) * 100
        self.profile_completion = round(completion, 2)
        return self.profile_completion
    
    def get_verified_skills(self) -> List[Skill]:
        """Get only verified skills"""
        return [skill for skill in self.skills if skill.verification_status == VerificationStatus.VERIFIED]
    
    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        """Find skill by name"""
        for skill in self.skills:
            if skill.name.lower() == name.lower():
                return skill
        return None
    
    def add_skill_endorsement(self, skill_name: str, endorser_address: str) -> bool:
        """Add endorsement to a skill"""
        skill = self.get_skill_by_name(skill_name)
        if skill and endorser_address not in skill.verified_by:
            skill.endorsements += 1
            skill.verified_by.append(endorser_address)
            skill.updated_at = datetime.now()
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_current_experience(self) -> Optional[Experience]:
        """Get current job experience"""
        for exp in self.experiences:
            if exp.is_current:
                return exp
        return None
    
    def calculate_reputation_score(self) -> float:
        """Calculate overall reputation score using multiple metrics"""
        # Skill verification score (30%)
        verified_skills = len(self.get_verified_skills())
        skill_score = min(verified_skills * 10, 100)
        
        # Network quality score (25%)
        network_score = min(len(self.connections) * 2, 100)
        
        # Activity score (20%)
        activity_score = min(self.profile_completion, 100)
        
        # Endorsement score (25%)
        total_endorsements = sum(skill.endorsements for skill in self.skills)
        endorsement_score = min(total_endorsements * 5, 100)
        
        overall_score = (
            skill_score * 0.30 +
            network_score * 0.25 +
            activity_score * 0.20 +
            endorsement_score * 0.25
        )
        
        self.reputation.overall_score = round(overall_score, 2)
        self.reputation.skill_verification_score = skill_score
        self.reputation.network_quality_score = network_score
        self.reputation.activity_score = activity_score
        self.reputation.peer_endorsement_score = endorsement_score
        self.reputation.total_endorsements = total_endorsements
        self.reputation.verification_count = verified_skills
        self.reputation.last_updated = datetime.now()
        
        return self.reputation.overall_score

# Response Models for API
class ProfileResponse(BaseModel):
    """API response model for profile data"""
    profile: ProfessionalProfile
    ai_insights: Dict[str, Any] = Field(default={})
    recommendations: List[str] = Field(default=[])
    
class ProfileUpdateRequest(BaseModel):
    """Request model for profile updates"""
    field: str = Field(..., description="Field to update")
    value: Any = Field(..., description="New value")
    ai_enhanced: bool = Field(default=False, description="Request AI enhancement")

class SkillValidationRequest(BaseModel):
    """Request model for skill validation"""
    skill_name: str = Field(..., description="Skill to validate")
    evidence_description: str = Field(..., description="Evidence description")
    evidence_file: Optional[str] = Field(None, description="Base64 encoded evidence file")
    validator_addresses: List[str] = Field(default=[], description="Preferred validator addresses")