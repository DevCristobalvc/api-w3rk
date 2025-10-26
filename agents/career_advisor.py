"""
Career Advisor Agent - ASI Alliance uAgent Implementation
Provides personalized career guidance through conversational AI
Registered on Agentverse as: career-advisor-w3rk.agent
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low

from ..models.agent_models import (
    CareerAnalysisRequest, AgentMessage, AgentResponse,
    ConversationSession, ProfileUpdateInstruction
)
from ..models.professional_profile import ProfessionalProfile
from ..services.metta_service import MeTTaService
from ..web3.smart_contracts import W3RKContractManager

# Agent Configuration
CAREER_ADVISOR_SEED = "career_advisor_w3rk_hackathon_seed_2024"
CAREER_ADVISOR_NAME = "career-advisor-w3rk"
AGENTVERSE_MAILBOX = "career-advisor-w3rk@agentverse.ai"

class CareerAdvisorAgent:
    """
    Advanced Career Advisor Agent using ASI Alliance uAgents Framework
    
    Capabilities:
    - Personalized career path analysis using MeTTa knowledge graphs
    - Industry trend analysis and salary benchmarking
    - Real-time skill gap identification and recommendations
    - Career transition planning and timeline creation
    - Professional development roadmap generation
    """
    
    def __init__(self):
        # Initialize uAgent with Agentverse integration
        self.agent = Agent(
            name=CAREER_ADVISOR_NAME,
            seed=CAREER_ADVISOR_SEED,
            mailbox=AGENTVERSE_MAILBOX,
            port=8001,
            endpoint=["http://localhost:8001/submit"]
        )
        
        # Initialize service dependencies
        self.metta_service = MeTTaService()
        self.contract_manager = W3RKContractManager()
        
        # Agent state and conversation tracking
        self.active_conversations: Dict[str, ConversationSession] = {}
        self.career_database: Dict[str, Any] = {}
        self.industry_trends: Dict[str, float] = {}
        
        # Register agent protocols and message handlers
        self._setup_protocols()
        
        # Fund agent if needed (for mainnet deployment)
        fund_agent_if_low(self.agent.wallet.address())
    
    def _setup_protocols(self):
        """Setup agent communication protocols"""
        
        # Career Analysis Protocol
        career_protocol = Protocol("CareerAnalysis")
        
        @career_protocol.on_message(model=CareerAnalysisRequest)
        async def handle_career_analysis(ctx: Context, sender: str, msg: CareerAnalysisRequest):
            """Handle career analysis requests with comprehensive guidance"""
            
            ctx.logger.info(f"🎯 Career analysis request from {sender}")
            
            try:
                # Perform comprehensive career analysis
                analysis_result = await self._analyze_career_path(
                    user_profile=msg.user_profile,
                    career_goals=msg.career_goals,
                    industry_preferences=msg.industry_preferences,
                    location_preferences=msg.location_preferences,
                    salary_expectations=msg.salary_expectations
                )
                
                # Generate actionable recommendations
                recommendations = await self._generate_career_recommendations(
                    analysis_result, msg.user_profile
                )
                
                # Create structured response
                response = AgentResponse(
                    message_id=f"career_analysis_{datetime.now().timestamp()}",
                    agent_type="career_advisor",
                    response_content=analysis_result["summary"],
                    analysis_results=analysis_result,
                    action_items=recommendations,
                    contract_updates=analysis_result.get("contract_updates", []),
                    confidence_score=analysis_result["confidence"],
                    processing_time=analysis_result["processing_time"]
                )
                
                # Send response back to requester
                await ctx.send(sender, response)
                
                # Update blockchain profile if contract updates needed
                if analysis_result.get("contract_updates"):
                    await self._update_blockchain_profile(
                        msg.user_profile["wallet_address"],
                        analysis_result["contract_updates"]
                    )
                
                ctx.logger.info(f"✅ Career analysis completed for {sender}")
                
            except Exception as e:
                ctx.logger.error(f"❌ Career analysis error: {str(e)}")
                error_response = AgentResponse(
                    message_id=f"error_{datetime.now().timestamp()}",
                    agent_type="career_advisor",
                    response_content=f"I encountered an error analyzing your career path: {str(e)}",
                    analysis_results={"error": str(e)},
                    action_items=["Please try again or contact support"],
                    confidence_score=0.0,
                    processing_time=0.0
                )
                await ctx.send(sender, error_response)
        
        # Conversational Chat Protocol for ASI:One Integration
        chat_protocol = Protocol("ConversationalCareerChat")
        
        @chat_protocol.on_message(model=AgentMessage)
        async def handle_conversational_input(ctx: Context, sender: str, msg: AgentMessage):
            """Handle natural language career conversations for ASI:One integration"""
            
            ctx.logger.info(f"💬 Conversational input from {sender}: {msg.content[:100]}...")
            
            try:
                # Extract career-related information from conversation
                extracted_info = await self._extract_career_info(msg.content, msg.metadata)
                
                # Analyze conversation context and provide guidance
                career_guidance = await self._provide_conversational_guidance(
                    message_content=msg.content,
                    conversation_context=msg.metadata.get("conversation_context", {}),
                    user_profile=msg.metadata.get("user_profile", {})
                )
                
                # Generate response with career insights
                response = AgentResponse(
                    message_id=msg.id,
                    agent_type="career_advisor",
                    response_content=career_guidance["response"],
                    analysis_results={
                        "extracted_info": extracted_info,
                        "career_insights": career_guidance["insights"],
                        "recommended_actions": career_guidance["actions"]
                    },
                    action_items=career_guidance["actions"],
                    contract_updates=career_guidance.get("profile_updates", []),
                    confidence_score=career_guidance["confidence"],
                    processing_time=career_guidance["processing_time"]
                )
                
                await ctx.send(sender, response)
                ctx.logger.info(f"✅ Conversational guidance provided to {sender}")
                
            except Exception as e:
                ctx.logger.error(f"❌ Conversation handling error: {str(e)}")
        
        # Register protocols with agent
        self.agent.include(career_protocol)
        self.agent.include(chat_protocol)
    
    async def _analyze_career_path(self, user_profile: Dict[str, Any], 
                                 career_goals: List[str], industry_preferences: List[str],
                                 location_preferences: List[str], 
                                 salary_expectations: Optional[Dict[str, float]]) -> Dict[str, Any]:
        """Comprehensive career path analysis using MeTTa knowledge graphs"""
        
        start_time = datetime.now()
        
        # Extract current user information
        current_skills = user_profile.get("skills", [])
        experience_years = user_profile.get("experience_years", 0)
        current_title = user_profile.get("title", "")
        industry = user_profile.get("industry", "")
        
        # Use MeTTa to analyze career progression possibilities
        career_paths = await self.metta_service.query_career_paths(
            current_skills=current_skills,
            experience_level=experience_years,
            target_industries=industry_preferences,
            career_goals=career_goals
        )
        
        # Analyze skill gaps for recommended paths
        skill_gaps = {}
        for path in career_paths[:3]:  # Analyze top 3 paths
            gap_analysis = await self.metta_service.analyze_skill_gap(
                current_skills=current_skills,
                target_role=path["target_role"],
                target_skills=path["required_skills"]
            )
            skill_gaps[path["target_role"]] = gap_analysis
        
        # Get salary and market data
        market_analysis = await self.metta_service.get_market_insights(
            roles=[path["target_role"] for path in career_paths[:3]],
            locations=location_preferences,
            experience_level=experience_years
        )
        
        # Generate timeline and milestones
        career_timeline = await self._generate_career_timeline(
            current_profile=user_profile,
            target_paths=career_paths[:3],
            skill_gaps=skill_gaps
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "summary": self._generate_analysis_summary(career_paths, skill_gaps, market_analysis),
            "recommended_paths": career_paths[:3],
            "skill_gap_analysis": skill_gaps,
            "market_insights": market_analysis,
            "career_timeline": career_timeline,
            "confidence": self._calculate_confidence_score(user_profile, career_paths),
            "processing_time": processing_time,
            "contract_updates": self._prepare_contract_updates(user_profile, career_paths)
        }
    
    async def _generate_career_recommendations(self, analysis_result: Dict[str, Any],
                                           user_profile: Dict[str, Any]) -> List[str]:
        """Generate actionable career recommendations"""
        
        recommendations = []
        
        # Skill development recommendations
        for role, gap_analysis in analysis_result["skill_gap_analysis"].items():
            if gap_analysis["missing_skills"]:
                recommendations.append(
                    f"Develop {', '.join(gap_analysis['missing_skills'][:3])} skills for {role} position"
                )
        
        # Network building recommendations
        target_industries = [path["industry"] for path in analysis_result["recommended_paths"]]
        recommendations.append(
            f"Connect with professionals in {', '.join(target_industries[:2])} industries"
        )
        
        # Experience building recommendations
        current_exp = user_profile.get("experience_years", 0)
        if current_exp < 3:
            recommendations.append("Focus on gaining practical experience through projects or internships")
        elif current_exp < 7:
            recommendations.append("Consider taking on leadership or mentoring responsibilities")
        else:
            recommendations.append("Explore senior roles or consider specialization in emerging areas")
        
        # Certification and education recommendations
        top_path = analysis_result["recommended_paths"][0]
        if top_path.get("recommended_certifications"):
            recommendations.append(
                f"Consider obtaining {top_path['recommended_certifications'][0]} certification"
            )
        
        return recommendations[:7]  # Return top 7 recommendations
    
    async def _extract_career_info(self, message_content: str, 
                                 metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extract career-relevant information from conversational input"""
        
        # Use MeTTa for natural language processing and information extraction
        extracted_info = await self.metta_service.extract_career_entities(
            text=message_content,
            context=metadata.get("conversation_context", {})
        )
        
        return {
            "mentioned_skills": extracted_info.get("skills", []),
            "career_interests": extracted_info.get("interests", []),
            "experience_indicators": extracted_info.get("experience", []),
            "goals": extracted_info.get("goals", []),
            "concerns": extracted_info.get("concerns", []),
            "timeline_mentions": extracted_info.get("timeline", [])
        }
    
    async def _provide_conversational_guidance(self, message_content: str,
                                             conversation_context: Dict[str, Any],
                                             user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Provide contextual career guidance based on conversation"""
        
        start_time = datetime.now()
        
        # Analyze message intent and context
        intent_analysis = await self.metta_service.analyze_message_intent(
            message=message_content,
            context=conversation_context,
            user_background=user_profile
        )
        
        # Generate appropriate response based on intent
        if intent_analysis["intent"] == "skill_inquiry":
            response = await self._handle_skill_inquiry(message_content, user_profile)
        elif intent_analysis["intent"] == "career_change":
            response = await self._handle_career_change_discussion(message_content, user_profile)
        elif intent_analysis["intent"] == "growth_planning":
            response = await self._handle_growth_planning(message_content, user_profile)
        elif intent_analysis["intent"] == "market_inquiry":
            response = await self._handle_market_inquiry(message_content, user_profile)
        else:
            response = await self._handle_general_career_chat(message_content, user_profile)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "response": response["message"],
            "insights": response["insights"],
            "actions": response["recommended_actions"],
            "profile_updates": response.get("profile_updates", []),
            "confidence": response["confidence"],
            "processing_time": processing_time
        }
    
    async def _handle_skill_inquiry(self, message: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Handle skill-related questions and discussions"""
        
        # Extract mentioned skills from message
        mentioned_skills = await self.metta_service.extract_skills_from_text(message)
        
        # Analyze skill relevance to user's career
        skill_analysis = await self.metta_service.analyze_skill_relevance(
            skills=mentioned_skills,
            user_profile=user_profile
        )
        
        # Generate personalized skill guidance
        guidance = f"Based on your background in {user_profile.get('industry', 'your field')}, "
        
        if skill_analysis["highly_relevant"]:
            guidance += f"the skills you mentioned ({', '.join(skill_analysis['highly_relevant'][:3])}) "
            guidance += "are excellent choices for your career growth. "
        
        if skill_analysis["gaps_identified"]:
            guidance += f"I'd also recommend considering {', '.join(skill_analysis['gaps_identified'][:2])} "
            guidance += "to strengthen your profile. "
        
        return {
            "message": guidance,
            "insights": skill_analysis,
            "recommended_actions": [
                f"Start learning {skill}" for skill in skill_analysis.get("priority_skills", [])[:3]
            ],
            "confidence": 0.85
        }
    
    async def _update_blockchain_profile(self, wallet_address: str, 
                                       contract_updates: List[Dict[str, Any]]):
        """Update user profile on blockchain via smart contracts"""
        
        try:
            for update in contract_updates:
                if update["type"] == "career_recommendation":
                    await self.contract_manager.update_profile_recommendations(
                        wallet_address, update["data"]
                    )
                elif update["type"] == "skill_analysis":
                    await self.contract_manager.update_skill_analysis(
                        wallet_address, update["data"]
                    )
        except Exception as e:
            print(f"Error updating blockchain profile: {e}")
    
    def _generate_analysis_summary(self, career_paths: List[Dict[str, Any]],
                                 skill_gaps: Dict[str, Any],
                                 market_analysis: Dict[str, Any]) -> str:
        """Generate human-readable analysis summary"""
        
        if not career_paths:
            return "I need more information about your background to provide career guidance."
        
        top_path = career_paths[0]
        summary = f"Based on your profile, I see strong potential for growth as a {top_path['target_role']}. "
        
        if market_analysis.get("growth_rate", 0) > 0.1:
            summary += f"This field is growing at {market_analysis['growth_rate']*100:.1f}% annually. "
        
        if skill_gaps and len(skill_gaps.get(top_path['target_role'], {}).get("missing_skills", [])) > 0:
            missing_skills = skill_gaps[top_path['target_role']]["missing_skills"][:2]
            summary += f"To reach this goal, focus on developing {' and '.join(missing_skills)}. "
        
        summary += f"With your experience, this transition could take {top_path.get('timeline', '12-18')} months."
        
        return summary
    
    def _calculate_confidence_score(self, user_profile: Dict[str, Any],
                                  career_paths: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for analysis"""
        
        score = 0.5  # Base score
        
        # Increase confidence based on profile completeness
        if user_profile.get("skills") and len(user_profile["skills"]) >= 3:
            score += 0.2
        
        if user_profile.get("experiences") and len(user_profile["experiences"]) >= 1:
            score += 0.2
        
        if career_paths and len(career_paths) >= 2:
            score += 0.1
        
        return min(score, 1.0)
    
    def _prepare_contract_updates(self, user_profile: Dict[str, Any],
                                career_paths: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare smart contract updates based on analysis"""
        
        updates = []
        
        if career_paths:
            updates.append({
                "type": "career_recommendation", 
                "data": {
                    "recommended_paths": career_paths[:3],
                    "analysis_timestamp": datetime.now().isoformat(),
                    "confidence": self._calculate_confidence_score(user_profile, career_paths)
                }
            })
        
        return updates
    
    async def run(self):
        """Start the Career Advisor Agent"""
        print(f"🎯 Starting Career Advisor Agent...")
        print(f"📧 Agentverse Mailbox: {AGENTVERSE_MAILBOX}")
        print(f"🔗 Agent Address: {self.agent.address}")
        
        await self.agent.run()

# For direct execution and testing
if __name__ == "__main__":
    career_advisor = CareerAdvisorAgent()
    asyncio.run(career_advisor.run())