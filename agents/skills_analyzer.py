"""
Skills Analyzer Agent - ASI Alliance uAgent Implementation  
Analyzes and validates professional skills through AI processing
Registered on Agentverse as: skills-analyzer-w3rk.agent
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low

from ..models.agent_models import (
    SkillExtractionRequest, AgentMessage, AgentResponse
)
from ..models.professional_profile import Skill, SkillLevel, VerificationStatus
from ..services.metta_service import MeTTaService
from ..web3.smart_contracts import W3RKContractManager

# Agent Configuration
SKILLS_ANALYZER_SEED = "skills_analyzer_w3rk_hackathon_seed_2024"
SKILLS_ANALYZER_NAME = "skills-analyzer-w3rk"  
AGENTVERSE_MAILBOX = "skills-analyzer-w3rk@agentverse.ai"

class SkillsAnalyzerAgent:
    """
    Advanced Skills Analyzer Agent using ASI Alliance uAgents Framework
    
    Capabilities:
    - Natural language skill extraction from text and documents
    - Skill proficiency level assessment using MeTTa knowledge graphs
    - Real-time skill validation and evidence analysis
    - Industry-specific skill mapping and trends analysis  
    - Cross-platform skill verification coordination
    """
    
    def __init__(self):
        # Initialize uAgent with Agentverse integration
        self.agent = Agent(
            name=SKILLS_ANALYZER_NAME,
            seed=SKILLS_ANALYZER_SEED,
            mailbox=AGENTVERSE_MAILBOX,
            port=8002,
            endpoint=["http://localhost:8002/submit"]
        )
        
        # Initialize service dependencies
        self.metta_service = MeTTaService()
        self.contract_manager = W3RKContractManager()
        
        # Skills database and classification system
        self.skill_taxonomy: Dict[str, Dict[str, Any]] = {}
        self.industry_skills: Dict[str, List[str]] = {}
        self.skill_synonyms: Dict[str, List[str]] = {}
        self.verification_validators: Dict[str, List[str]] = {}
        
        # Processing state
        self.active_extractions: Dict[str, Dict[str, Any]] = {}
        self.validation_queue: List[Dict[str, Any]] = []
        
        # Setup agent protocols and load skill database
        self._setup_protocols()
        asyncio.create_task(self._initialize_skill_database())
        
        # Fund agent for mainnet deployment
        fund_agent_if_low(self.agent.wallet.address())
    
    def _setup_protocols(self):
        """Setup agent communication protocols"""
        
        # Skill Extraction Protocol
        extraction_protocol = Protocol("SkillExtraction")
        
        @extraction_protocol.on_message(model=SkillExtractionRequest)
        async def handle_skill_extraction(ctx: Context, sender: str, msg: SkillExtractionRequest):
            """Handle skill extraction from text content"""
            
            ctx.logger.info(f"🔍 Skill extraction request from {sender}")
            ctx.logger.info(f"📄 Document type: {msg.document_type}, Text length: {len(msg.text_content)}")
            
            try:
                # Perform comprehensive skill extraction
                extraction_result = await self._extract_skills_comprehensive(
                    text_content=msg.text_content,
                    document_type=msg.document_type,
                    existing_skills=msg.existing_skills,
                    industry_context=msg.industry_context
                )
                
                # Analyze skill proficiency levels
                proficiency_analysis = await self._analyze_skill_proficiency(
                    extracted_skills=extraction_result["skills"],
                    context=msg.text_content,
                    document_type=msg.document_type
                )
                
                # Generate skill recommendations
                recommendations = await self._generate_skill_recommendations(
                    extracted_skills=extraction_result["skills"],
                    existing_skills=msg.existing_skills,
                    industry_context=msg.industry_context
                )
                
                # Create structured response
                response = AgentResponse(
                    message_id=f"skill_extraction_{datetime.now().timestamp()}",
                    agent_type="skills_analyzer",
                    response_content=extraction_result["summary"],
                    analysis_results={
                        "extracted_skills": extraction_result["skills"],
                        "proficiency_analysis": proficiency_analysis,
                        "skill_categories": extraction_result["categories"],
                        "confidence_scores": extraction_result["confidence_scores"],
                        "recommendations": recommendations
                    },
                    action_items=recommendations["priority_actions"],
                    contract_updates=self._prepare_skill_contract_updates(extraction_result, sender),
                    confidence_score=extraction_result["overall_confidence"],
                    processing_time=extraction_result["processing_time"]
                )
                
                await ctx.send(sender, response)
                
                # Update blockchain if high confidence skills found
                if extraction_result["high_confidence_skills"]:
                    await self._update_blockchain_skills(
                        sender, extraction_result["high_confidence_skills"]
                    )
                
                ctx.logger.info(f"✅ Skill extraction completed for {sender}")
                
            except Exception as e:
                ctx.logger.error(f"❌ Skill extraction error: {str(e)}")
                error_response = AgentResponse(
                    message_id=f"error_{datetime.now().timestamp()}",
                    agent_type="skills_analyzer",
                    response_content=f"I encountered an error analyzing skills: {str(e)}",
                    analysis_results={"error": str(e)},
                    action_items=["Please try again with different text or contact support"],
                    confidence_score=0.0,
                    processing_time=0.0
                )
                await ctx.send(sender, error_response)
        
        # Conversational Skill Analysis Protocol for ASI:One
        chat_protocol = Protocol("ConversationalSkillAnalysis")
        
        @chat_protocol.on_message(model=AgentMessage)  
        async def handle_conversational_skill_input(ctx: Context, sender: str, msg: AgentMessage):
            """Handle natural language skill discussions for ASI:One integration"""
            
            ctx.logger.info(f"💬 Conversational skill analysis from {sender}")
            
            try:
                # Extract skills from natural conversation
                conversation_skills = await self._analyze_conversational_skills(
                    message_content=msg.content,
                    conversation_context=msg.metadata.get("conversation_context", {}),
                    user_profile=msg.metadata.get("user_profile", {})
                )
                
                # Provide skill-focused guidance and recommendations
                skill_guidance = await self._provide_skill_guidance(
                    message_content=msg.content,
                    identified_skills=conversation_skills["skills"],
                    user_background=msg.metadata.get("user_profile", {})
                )
                
                response = AgentResponse(
                    message_id=msg.id,
                    agent_type="skills_analyzer",
                    response_content=skill_guidance["response"],
                    analysis_results={
                        "conversation_skills": conversation_skills,
                        "skill_insights": skill_guidance["insights"],
                        "skill_gaps": skill_guidance["gaps"],
                        "learning_resources": skill_guidance["resources"]
                    },
                    action_items=skill_guidance["recommended_actions"],
                    contract_updates=skill_guidance.get("skill_updates", []),
                    confidence_score=skill_guidance["confidence"],
                    processing_time=skill_guidance["processing_time"]
                )
                
                await ctx.send(sender, response)
                ctx.logger.info(f"✅ Conversational skill analysis provided to {sender}")
                
            except Exception as e:
                ctx.logger.error(f"❌ Conversational skill analysis error: {str(e)}")
        
        # Skill Validation Protocol
        validation_protocol = Protocol("SkillValidation")
        
        @validation_protocol.on_message(model=dict)
        async def handle_skill_validation_request(ctx: Context, sender: str, msg: dict):
            """Handle skill validation requests from other agents or validators"""
            
            ctx.logger.info(f"🔐 Skill validation request from {sender}")
            
            try:
                validation_result = await self._validate_skill_evidence(
                    skill_name=msg["skill_name"],
                    evidence_data=msg["evidence_data"],
                    user_context=msg.get("user_context", {}),
                    validator_address=sender
                )
                
                response = {
                    "validation_id": msg.get("validation_id"),
                    "skill_name": msg["skill_name"],
                    "validation_result": validation_result,
                    "validator_agent": self.agent.address,
                    "timestamp": datetime.now().isoformat()
                }
                
                await ctx.send(sender, response)
                ctx.logger.info(f"✅ Skill validation completed for {sender}")
                
            except Exception as e:
                ctx.logger.error(f"❌ Skill validation error: {str(e)}")
        
        # Register protocols
        self.agent.include(extraction_protocol)
        self.agent.include(chat_protocol)
        self.agent.include(validation_protocol)
    
    async def _initialize_skill_database(self):
        """Initialize comprehensive skill database using MeTTa"""
        
        print("📚 Initializing Skills Database...")
        
        # Load skill taxonomy from MeTTa knowledge base
        self.skill_taxonomy = await self.metta_service.load_skill_taxonomy()
        
        # Load industry-specific skill mappings
        self.industry_skills = await self.metta_service.get_industry_skill_mappings()
        
        # Load skill synonyms and variations
        self.skill_synonyms = await self.metta_service.get_skill_synonyms()
        
        # Initialize validation network
        await self._setup_validation_network()
        
        print(f"✅ Skills Database initialized with {len(self.skill_taxonomy)} skills")
    
    async def _extract_skills_comprehensive(self, text_content: str, document_type: str,
                                         existing_skills: List[str], 
                                         industry_context: Optional[str]) -> Dict[str, Any]:
        """Comprehensive skill extraction using multiple techniques"""
        
        start_time = datetime.now()
        
        # Stage 1: Pattern-based extraction
        pattern_skills = self._extract_skills_by_patterns(text_content)
        
        # Stage 2: MeTTa knowledge graph matching
        metta_skills = await self.metta_service.extract_skills_with_reasoning(
            text=text_content,
            context=industry_context,
            document_type=document_type
        )
        
        # Stage 3: Contextual skill inference
        inferred_skills = await self._infer_skills_from_context(
            text_content, existing_skills, industry_context
        )
        
        # Stage 4: Combine and deduplicate
        all_skills = self._merge_and_deduplicate_skills(
            pattern_skills, metta_skills, inferred_skills
        )
        
        # Stage 5: Calculate confidence scores
        confidence_scores = await self._calculate_skill_confidence(
            skills=all_skills,
            text_content=text_content,
            document_type=document_type
        )
        
        # Stage 6: Categorize skills
        skill_categories = self._categorize_skills(all_skills)
        
        # Stage 7: Filter high confidence skills
        high_confidence_skills = [
            skill for skill, score in confidence_scores.items() 
            if score >= 0.7
        ]
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "skills": all_skills,
            "categories": skill_categories,
            "confidence_scores": confidence_scores,
            "high_confidence_skills": high_confidence_skills,
            "overall_confidence": sum(confidence_scores.values()) / len(confidence_scores) if confidence_scores else 0,
            "processing_time": processing_time,
            "summary": self._generate_extraction_summary(all_skills, skill_categories)
        }
    
    def _extract_skills_by_patterns(self, text: str) -> List[str]:
        """Extract skills using regex patterns and keyword matching"""
        
        skills = []
        text_lower = text.lower()
        
        # Programming languages
        programming_patterns = [
            r'\b(python|javascript|java|c\+\+|c#|php|ruby|go|rust|swift|kotlin)\b',
            r'\b(html|css|sql|r|matlab|scala)\b',
        ]
        
        # Frameworks and libraries
        framework_patterns = [
            r'\b(react|angular|vue|django|flask|spring|laravel|rails)\b',
            r'\b(tensorflow|pytorch|pandas|numpy|scikit-learn)\b',
        ]
        
        # Tools and technologies
        tool_patterns = [
            r'\b(git|docker|kubernetes|aws|azure|gcp|jenkins)\b',
            r'\b(photoshop|figma|sketch|illustrator|premiere)\b',
        ]
        
        all_patterns = programming_patterns + framework_patterns + tool_patterns
        
        for pattern in all_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            skills.extend([match.title() for match in matches])
        
        # Check against skill taxonomy
        for skill_name in self.skill_taxonomy.keys():
            if skill_name.lower() in text_lower:
                skills.append(skill_name)
        
        return list(set(skills))  # Remove duplicates
    
    async def _analyze_skill_proficiency(self, extracted_skills: List[str],
                                       context: str, document_type: str) -> Dict[str, Any]:
        """Analyze skill proficiency levels from context"""
        
        proficiency_analysis = {}
        
        for skill in extracted_skills:
            # Use MeTTa to analyze proficiency indicators
            proficiency_indicators = await self.metta_service.analyze_skill_proficiency(
                skill=skill,
                context=context,
                document_type=document_type
            )
            
            # Determine proficiency level
            level = self._determine_proficiency_level(skill, context, proficiency_indicators)
            
            proficiency_analysis[skill] = {
                "level": level,
                "indicators": proficiency_indicators,
                "confidence": proficiency_indicators.get("confidence", 0.5)
            }
        
        return proficiency_analysis
    
    def _determine_proficiency_level(self, skill: str, context: str, 
                                   indicators: Dict[str, Any]) -> SkillLevel:
        """Determine skill proficiency level based on context analysis"""
        
        context_lower = context.lower()
        skill_lower = skill.lower()
        
        # Advanced level indicators
        advanced_indicators = [
            f"expert in {skill_lower}", f"advanced {skill_lower}", f"senior {skill_lower}",
            f"lead {skill_lower}", f"architect", f"mastery", f"specialized in {skill_lower}"
        ]
        
        # Intermediate level indicators  
        intermediate_indicators = [
            f"experienced with {skill_lower}", f"proficient in {skill_lower}",
            f"working knowledge", f"familiar with {skill_lower}", f"2+ years"
        ]
        
        # Beginner level indicators
        beginner_indicators = [
            f"learning {skill_lower}", f"basic {skill_lower}", f"introduction to {skill_lower}",
            f"beginner", f"starting with {skill_lower}"
        ]
        
        if any(indicator in context_lower for indicator in advanced_indicators):
            return SkillLevel.ADVANCED
        elif any(indicator in context_lower for indicator in intermediate_indicators):
            return SkillLevel.INTERMEDIATE
        elif any(indicator in context_lower for indicator in beginner_indicators):
            return SkillLevel.BEGINNER
        else:
            # Use years of experience and context clues
            if "years" in context_lower and re.search(r'(\d+)\+?\s*years', context_lower):
                years_match = re.search(r'(\d+)\+?\s*years', context_lower)
                if years_match:
                    years = int(years_match.group(1))
                    if years >= 5:
                        return SkillLevel.ADVANCED
                    elif years >= 2:
                        return SkillLevel.INTERMEDIATE
            
            return SkillLevel.INTERMEDIATE  # Default assumption
    
    async def _generate_skill_recommendations(self, extracted_skills: List[str],
                                            existing_skills: List[str],
                                            industry_context: Optional[str]) -> Dict[str, Any]:
        """Generate skill recommendations based on analysis"""
        
        # Identify skill gaps using MeTTa knowledge graphs
        skill_gaps = await self.metta_service.identify_skill_gaps(
            current_skills=existing_skills + extracted_skills,
            industry=industry_context,
            target_roles=[]  # Could be enhanced with career goals
        )
        
        # Get trending skills in industry
        trending_skills = await self.metta_service.get_trending_skills(
            industry=industry_context,
            timeframe="2024"
        )
        
        # Generate learning path recommendations
        learning_paths = await self.metta_service.generate_learning_paths(
            current_skills=extracted_skills,
            target_skills=skill_gaps.get("high_priority", [])[:5]
        )
        
        priority_actions = []
        
        if skill_gaps.get("critical_gaps"):
            priority_actions.extend([
                f"Prioritize learning {skill}" for skill in skill_gaps["critical_gaps"][:2]
            ])
        
        if trending_skills:
            priority_actions.append(
                f"Consider learning trending skill: {trending_skills[0]}"
            )
        
        if extracted_skills:
            priority_actions.append(
                f"Get certification in {extracted_skills[0]} to validate your expertise"
            )
        
        return {
            "skill_gaps": skill_gaps,
            "trending_skills": trending_skills,
            "learning_paths": learning_paths,
            "priority_actions": priority_actions[:5],
            "complementary_skills": skill_gaps.get("complementary", [])[:3]
        }
    
    async def _analyze_conversational_skills(self, message_content: str,
                                          conversation_context: Dict[str, Any],
                                          user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skills mentioned in natural conversation"""
        
        start_time = datetime.now()
        
        # Extract skills from conversational text
        conversation_skills = await self.metta_service.extract_conversational_skills(
            message=message_content,
            context=conversation_context,
            user_background=user_profile
        )
        
        # Analyze skill mentions and context
        skill_context_analysis = {}
        for skill in conversation_skills:
            context_analysis = await self.metta_service.analyze_skill_context(
                skill=skill,
                message=message_content,
                conversation_history=conversation_context.get("history", [])
            )
            skill_context_analysis[skill] = context_analysis
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "skills": conversation_skills,
            "context_analysis": skill_context_analysis,
            "confidence": 0.8,  # Conversational extraction has moderate confidence
            "processing_time": processing_time
        }
    
    async def _provide_skill_guidance(self, message_content: str,
                                    identified_skills: List[str],
                                    user_background: Dict[str, Any]) -> Dict[str, Any]:
        """Provide personalized skill guidance based on conversation"""
        
        start_time = datetime.now()
        
        current_skills = user_background.get("skills", [])
        industry = user_background.get("industry", "")
        
        # Analyze skill relevance and provide guidance
        guidance_message = "I notice you mentioned some interesting skills! "
        
        if identified_skills:
            new_skills = [skill for skill in identified_skills if skill not in current_skills]
            if new_skills:
                guidance_message += f"The skills {', '.join(new_skills[:3])} would be great additions to your profile. "
        
        # Get skill market insights
        market_insights = await self.metta_service.get_skill_market_insights(
            skills=identified_skills,
            industry=industry
        )
        
        if market_insights.get("high_demand_skills"):
            guidance_message += f"Particularly, {market_insights['high_demand_skills'][0]} is in high demand right now. "
        
        # Generate learning recommendations
        learning_resources = await self.metta_service.get_learning_resources(
            skills=identified_skills[:3]
        )
        
        recommended_actions = []
        if new_skills:
            recommended_actions.extend([
                f"Add {skill} to your profile" for skill in new_skills[:2]
            ])
        
        if learning_resources:
            recommended_actions.append(
                f"Check out learning resources for {identified_skills[0] if identified_skills else 'your skills'}"
            )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "response": guidance_message,
            "insights": market_insights,
            "gaps": await self._identify_conversation_skill_gaps(identified_skills, user_background),
            "resources": learning_resources,
            "recommended_actions": recommended_actions,
            "confidence": 0.75,
            "processing_time": processing_time
        }
    
    def _merge_and_deduplicate_skills(self, *skill_lists) -> List[str]:
        """Merge multiple skill lists and remove duplicates"""
        
        all_skills = []
        for skill_list in skill_lists:
            all_skills.extend(skill_list)
        
        # Normalize and deduplicate
        normalized_skills = set()
        for skill in all_skills:
            # Handle synonyms and variations
            canonical_skill = self._get_canonical_skill_name(skill)
            normalized_skills.add(canonical_skill)
        
        return list(normalized_skills)
    
    def _get_canonical_skill_name(self, skill: str) -> str:
        """Get canonical name for skill (handle synonyms)"""
        
        skill_lower = skill.lower().strip()
        
        # Check if it's a known synonym
        for canonical, synonyms in self.skill_synonyms.items():
            if skill_lower in [s.lower() for s in synonyms]:
                return canonical
        
        return skill.title().strip()
    
    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into different types"""
        
        categories = {
            "Programming Languages": [],
            "Frameworks & Libraries": [],
            "Tools & Technologies": [],
            "Soft Skills": [],
            "Domain Expertise": [],
            "Other": []
        }
        
        for skill in skills:
            category = self._get_skill_category(skill)
            categories[category].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def _get_skill_category(self, skill: str) -> str:
        """Determine skill category"""
        
        skill_lower = skill.lower()
        
        # Programming languages
        if skill_lower in ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin']:
            return "Programming Languages"
        
        # Frameworks
        if skill_lower in ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'laravel', 'rails']:
            return "Frameworks & Libraries"
        
        # Tools
        if skill_lower in ['git', 'docker', 'kubernetes', 'aws', 'azure', 'jenkins']:
            return "Tools & Technologies"
        
        # Soft skills
        if skill_lower in ['leadership', 'communication', 'teamwork', 'problem solving', 'project management']:
            return "Soft Skills"
        
        # Check taxonomy if available
        if skill in self.skill_taxonomy:
            return self.skill_taxonomy[skill].get("category", "Other")
        
        return "Other"
    
    async def run(self):
        """Start the Skills Analyzer Agent"""
        print(f"🔍 Starting Skills Analyzer Agent...")
        print(f"📧 Agentverse Mailbox: {AGENTVERSE_MAILBOX}")
        print(f"🔗 Agent Address: {self.agent.address}")
        
        await self.agent.run()

# For direct execution and testing
if __name__ == "__main__":
    skills_analyzer = SkillsAnalyzerAgent()
    asyncio.run(skills_analyzer.run())