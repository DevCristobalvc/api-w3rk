"""
uAgent Communication Models for W3RK Platform
Models for inter-agent communication and conversation management
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class AgentType(str, Enum):
    CAREER_ADVISOR = "career_advisor"
    SKILLS_ANALYZER = "skills_analyzer"
    NETWORK_CONNECTOR = "network_connector"
    OPPORTUNITY_MATCHER = "opportunity_matcher"
    PROFILE_ANALYZER = "profile_analyzer"

class MessageType(str, Enum):
    TEXT = "text"
    FILE_UPLOAD = "file_upload"
    SKILL_EXTRACTION = "skill_extraction"
    CAREER_ANALYSIS = "career_analysis"
    NETWORK_RECOMMENDATION = "network_recommendation"
    OPPORTUNITY_MATCH = "opportunity_match"
    PROFILE_UPDATE = "profile_update"
    SYSTEM = "system"

class ConversationStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"

class AgentMessage(BaseModel):
    """Message structure for agent communication"""
    id: str = Field(..., description="Unique message ID")
    conversation_id: str = Field(..., description="Conversation session ID")
    agent_type: AgentType = Field(..., description="Type of agent sending message")
    agent_address: str = Field(..., description="uAgent address")
    message_type: MessageType = Field(..., description="Type of message")
    content: str = Field(..., description="Message content")
    metadata: Dict[str, Any] = Field(default={}, description="Additional message metadata")
    attachments: List[str] = Field(default=[], description="File attachments (IPFS hashes)")
    timestamp: datetime = Field(default_factory=datetime.now)
    processed: bool = Field(default=False, description="Whether message has been processed")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AgentResponse(BaseModel):
    """Response from agent processing"""
    message_id: str = Field(..., description="Original message ID")
    agent_type: AgentType = Field(..., description="Responding agent type")
    response_content: str = Field(..., description="Agent's response content")
    analysis_results: Dict[str, Any] = Field(default={}, description="Structured analysis results")
    action_items: List[str] = Field(default=[], description="Recommended actions")
    contract_updates: List[Dict[str, Any]] = Field(default=[], description="Smart contract updates to perform")
    confidence_score: float = Field(default=0.0, ge=0, le=1, description="Confidence in analysis")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)

class ConversationSession(BaseModel):
    """Complete conversation session with multiple agents"""
    id: str = Field(..., description="Unique conversation ID")
    user_address: str = Field(..., description="User's wallet address")
    session_type: str = Field(..., description="Type of conversation session")
    status: ConversationStatus = Field(default=ConversationStatus.ACTIVE)
    active_agents: List[AgentType] = Field(default=[], description="Currently active agent types")
    messages: List[AgentMessage] = Field(default=[], description="All messages in conversation")
    responses: List[AgentResponse] = Field(default=[], description="All agent responses")
    context: Dict[str, Any] = Field(default={}, description="Conversation context and state")
    goals: List[str] = Field(default=[], description="Session objectives")
    achievements: List[str] = Field(default=[], description="Completed objectives")
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    duration_minutes: int = Field(default=0, description="Total session duration")
    
    def add_message(self, message: AgentMessage):
        """Add message to conversation"""
        self.messages.append(message)
        self.last_activity = datetime.now()
        
    def add_response(self, response: AgentResponse):
        """Add agent response to conversation"""
        self.responses.append(response)
        self.last_activity = datetime.now()
        
    def get_messages_by_agent(self, agent_type: AgentType) -> List[AgentMessage]:
        """Get all messages from specific agent"""
        return [msg for msg in self.messages if msg.agent_type == agent_type]
    
    def get_latest_message(self) -> Optional[AgentMessage]:
        """Get most recent message"""
        return self.messages[-1] if self.messages else None

# Agent-specific models
class CareerAnalysisRequest(BaseModel):
    """Request for career analysis from Career Advisor Agent"""
    user_profile: Dict[str, Any] = Field(..., description="User profile data")
    career_goals: List[str] = Field(default=[], description="Stated career goals")
    industry_preferences: List[str] = Field(default=[], description="Preferred industries")
    location_preferences: List[str] = Field(default=[], description="Location preferences")
    salary_expectations: Optional[Dict[str, float]] = Field(None, description="Salary range expectations")

class SkillExtractionRequest(BaseModel):
    """Request for skill extraction from Skills Analyzer Agent"""
    text_content: str = Field(..., description="Text to analyze for skills")
    document_type: str = Field(default="general", description="Type of document (resume, job_description, etc.)")
    existing_skills: List[str] = Field(default=[], description="Already identified skills")
    industry_context: Optional[str] = Field(None, description="Industry context for analysis")

class NetworkMatchRequest(BaseModel):
    """Request for network matching from Network Connector Agent"""
    user_profile: Dict[str, Any] = Field(..., description="User profile for matching")
    connection_criteria: Dict[str, Any] = Field(default={}, description="Matching criteria")
    max_recommendations: int = Field(default=10, ge=1, le=50, description="Maximum recommendations")
    exclude_addresses: List[str] = Field(default=[], description="Addresses to exclude")

class OpportunitySearchRequest(BaseModel):
    """Request for opportunity matching from Opportunity Matcher Agent"""
    user_skills: List[str] = Field(..., description="User's skills")
    experience_level: str = Field(..., description="Experience level")
    location_preferences: List[str] = Field(default=[], description="Preferred locations")
    job_types: List[str] = Field(default=[], description="Preferred job types")
    salary_range: Optional[Dict[str, float]] = Field(None, description="Salary expectations")

class ProfileUpdateInstruction(BaseModel):
    """Instruction for profile updates from Profile Analyzer Agent"""
    field_path: str = Field(..., description="Dot-notation path to field (e.g., 'skills.0.level')")
    new_value: Any = Field(..., description="New value for field")
    update_reason: str = Field(..., description="Reason for update")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in update")

# Agent Communication Protocol Models
class AgentHandshake(BaseModel):
    """Initial handshake between agents"""
    source_agent: str = Field(..., description="Source agent address")
    target_agent: str = Field(..., description="Target agent address")
    protocol_version: str = Field(default="1.0", description="Communication protocol version")
    capabilities: List[str] = Field(..., description="Agent capabilities")
    session_id: str = Field(..., description="Communication session ID")

class InterAgentMessage(BaseModel):
    """Message between agents in multi-agent workflows"""
    id: str = Field(..., description="Unique message ID")
    source_agent: AgentType = Field(..., description="Source agent")
    target_agents: List[AgentType] = Field(..., description="Target agents")
    message_type: str = Field(..., description="Inter-agent message type")
    payload: Dict[str, Any] = Field(..., description="Message payload")
    priority: int = Field(default=5, ge=1, le=10, description="Message priority")
    requires_response: bool = Field(default=False, description="Whether response is required")
    timeout_seconds: int = Field(default=30, description="Response timeout")
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentWorkflowState(BaseModel):
    """State management for multi-agent workflows"""
    workflow_id: str = Field(..., description="Unique workflow ID")
    user_address: str = Field(..., description="User initiating workflow")
    workflow_type: str = Field(..., description="Type of workflow")
    current_step: int = Field(default=0, description="Current workflow step")
    total_steps: int = Field(..., description="Total workflow steps")
    participating_agents: List[AgentType] = Field(..., description="Agents in workflow")
    agent_states: Dict[AgentType, str] = Field(default={}, description="Individual agent states")
    shared_context: Dict[str, Any] = Field(default={}, description="Shared workflow context")
    completed_tasks: List[str] = Field(default=[], description="Completed tasks")
    pending_tasks: List[str] = Field(default=[], description="Pending tasks")
    workflow_status: str = Field(default="active", description="Overall workflow status")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# Response Models
class AgentListResponse(BaseModel):
    """Response listing available agents"""
    agents: List[Dict[str, Any]] = Field(..., description="Available agents")
    total_agents: int = Field(..., description="Total number of agents")
    online_agents: int = Field(..., description="Currently online agents")

class ConversationHistoryResponse(BaseModel):
    """Response with conversation history"""
    conversation: ConversationSession = Field(..., description="Conversation session")
    message_count: int = Field(..., description="Total message count")
    agent_participation: Dict[AgentType, int] = Field(..., description="Messages per agent")

class AgentCapabilitiesResponse(BaseModel):
    """Response with agent capabilities"""
    agent_type: AgentType = Field(..., description="Agent type")
    capabilities: List[str] = Field(..., description="Agent capabilities")
    supported_inputs: List[str] = Field(..., description="Supported input types")
    response_formats: List[str] = Field(..., description="Response formats")
    average_response_time: float = Field(..., description="Average response time in seconds")