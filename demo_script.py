"""
Demo Script for W3RK Platform - ASI Alliance Hackathon
Demonstrates all key features and integrations
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any

class W3RKDemo:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.demo_user = {
            "wallet_address": "0x742d35Cc6635C0532925a3b8D0984C841e2489b0",
            "username": "demo_user",
            "display_name": "ASI Alliance Developer"
        }
    
    async def run_complete_demo(self):
        """Run complete platform demonstration"""
        print("🚀 W3RK Platform - ASI Alliance Hackathon Demo")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            # 1. System Health Check
            await self.demo_health_check(session)
            
            # 2. Profile Creation
            await self.demo_profile_creation(session)
            
            # 3. Agent Interactions
            await self.demo_agent_interactions(session)
            
            # 4. MeTTa Knowledge Graphs
            await self.demo_metta_reasoning(session)
            
            # 5. Blockchain Integration
            await self.demo_blockchain_features(session)
            
            # 6. Real-time Communication
            await self.demo_websocket_features(session)
            
        print("\n✅ Demo completed successfully!")
        print("🏆 W3RK Platform ready for ASI Alliance Hackathon evaluation")
    
    async def demo_health_check(self, session):
        """Demonstrate system health and status"""
        print("\n🔍 1. System Health Check")
        print("-" * 30)
        
        try:
            async with session.get(f"{self.base_url}/health") as resp:
                health_data = await resp.json()
                print(f"✅ System Status: {health_data.get('status', 'Unknown')}")
                print(f"📊 Uptime: {health_data.get('uptime', 'N/A')}")
                
            async with session.get(f"{self.base_url}/agents/status") as resp:
                agent_status = await resp.json()
                print(f"🤖 Active Agents: {len(agent_status.get('agents', []))}")
                
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    async def demo_profile_creation(self, session):
        """Demonstrate AI-powered profile creation"""
        print("\n👤 2. AI-Powered Profile Creation")
        print("-" * 35)
        
        profile_data = {
            **self.demo_user,
            "bio": "Passionate about ASI Alliance technology and decentralized AI systems",
            "title": "Senior AI Engineer",
            "industry": "Blockchain Technology"
        }
        
        try:
            async with session.post(
                f"{self.base_url}/profiles/", 
                json=profile_data
            ) as resp:
                if resp.status == 201:
                    profile = await resp.json()
                    print(f"✅ Profile created: {profile.get('username')}")
                    print(f"🆔 Profile ID: {profile.get('id')}")
                else:
                    print(f"ℹ️ Profile already exists or updated")
                    
        except Exception as e:
            print(f"❌ Profile creation failed: {e}")
    
    async def demo_agent_interactions(self, session):
        """Demonstrate multi-agent conversations"""
        print("\n🤖 3. Multi-Agent Professional Services")
        print("-" * 40)
        
        # Career Advisor Agent
        career_query = {
            "message": "I want to transition from web development to AI engineering. What skills should I focus on?",
            "agent_type": "career_advisor",
            "user_address": self.demo_user["wallet_address"]
        }
        
        try:
            async with session.post(
                f"{self.base_url}/chat/w3rk", 
                json=career_query
            ) as resp:
                response = await resp.json()
                print(f"💼 Career Advisor: {response.get('response', 'No response')[:100]}...")
                
        except Exception as e:
            print(f"❌ Career advisor interaction failed: {e}")
        
        # Skills Analyzer Agent
        skills_query = {
            "text": "Experienced Python developer with 5 years in machine learning, worked with TensorFlow, PyTorch, and deployed models on AWS",
            "user_address": self.demo_user["wallet_address"],
            "document_type": "resume"
        }
        
        try:
            async with session.post(
                f"{self.base_url}/chat/analyze-skills", 
                json=skills_query
            ) as resp:
                response = await resp.json()
                skills = response.get('extracted_skills', [])
                print(f"🧠 Skills Analyzer extracted {len(skills)} skills")
                if skills:
                    print(f"   Top skills: {', '.join(skills[:3])}")
                    
        except Exception as e:
            print(f"❌ Skills analysis failed: {e}")
    
    async def demo_metta_reasoning(self, session):
        """Demonstrate MeTTa knowledge graph reasoning"""
        print("\n🧠 4. MeTTa Knowledge Graph Reasoning")
        print("-" * 40)
        
        try:
            # Skill relationships
            async with session.get(f"{self.base_url}/metta/skill-relationships") as resp:
                relationships = await resp.json()
                print(f"🔗 Skill relationships in knowledge base: {len(relationships.get('relationships', []))}")
            
            # Career path analysis
            career_analysis = {
                "current_role": "Web Developer",
                "target_role": "AI Engineer",
                "user_address": self.demo_user["wallet_address"]
            }
            
            async with session.post(
                f"{self.base_url}/metta/career-paths", 
                json=career_analysis
            ) as resp:
                paths = await resp.json()
                print(f"🛤️ Career paths analyzed: {len(paths.get('paths', []))}")
                
        except Exception as e:
            print(f"❌ MeTTa reasoning failed: {e}")
    
    async def demo_blockchain_features(self, session):
        """Demonstrate blockchain integration"""
        print("\n⛓️ 5. Blockchain Professional Identity")
        print("-" * 38)
        
        try:
            # Profile verification
            verify_data = {
                "wallet_address": self.demo_user["wallet_address"],
                "profile_data": {
                    "skills": ["Python", "Machine Learning", "Blockchain"],
                    "experience_years": 5
                }
            }
            
            async with session.post(
                f"{self.base_url}/blockchain/verify-profile", 
                json=verify_data
            ) as resp:
                result = await resp.json()
                print(f"🔐 Profile verification: {result.get('status', 'Unknown')}")
                if result.get('transaction_hash'):
                    print(f"📝 Transaction: {result['transaction_hash'][:20]}...")
            
            # Achievement NFTs
            async with session.get(
                f"{self.base_url}/blockchain/achievements/{self.demo_user['wallet_address']}"
            ) as resp:
                achievements = await resp.json()
                print(f"🏆 Achievement NFTs: {len(achievements.get('achievements', []))}")
                
        except Exception as e:
            print(f"❌ Blockchain integration failed: {e}")
    
    async def demo_websocket_features(self, session):
        """Demonstrate real-time communication"""
        print("\n🔌 6. Real-time Agent Communication")
        print("-" * 37)
        
        try:
            # WebSocket status
            async with session.get(f"{self.base_url}/ws/stats") as resp:
                ws_stats = await resp.json()
                print(f"📡 Active WebSocket connections: {ws_stats.get('active_connections', 0)}")
                print(f"💬 Messages processed: {ws_stats.get('messages_processed', 0)}")
                
            print("✅ WebSocket system ready for real-time agent communication")
            
        except Exception as e:
            print(f"❌ WebSocket demo failed: {e}")

async def main():
    """Run the complete demo"""
    demo = W3RKDemo()
    await demo.run_complete_demo()

if __name__ == "__main__":
    print("Starting W3RK Platform Demo...")
    asyncio.run(main())