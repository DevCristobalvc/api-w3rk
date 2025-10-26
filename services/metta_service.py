"""
MeTTa Service - ASI Alliance MeTTa Integration for W3RK Platform
Advanced knowledge reasoning using MeTTa knowledge graphs for professional insights
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from hyperon import MeTTa, Environment, SpaceRef
from hyperon.atoms import OperationAtom, ExpressionAtom
import re

class MeTTaService:
    """
    MeTTa-powered knowledge service for professional intelligence
    
    Capabilities:
    - Skill relationship mapping and interdependency analysis
    - Career path reasoning and progression modeling
    - Market trend analysis and salary prediction
    - Industry expertise modeling and skill gap identification
    - Natural language processing for professional content
    """
    
    def __init__(self):
        # Initialize MeTTa environment
        self.metta = MeTTa(env_builder=Environment.test_env())
        self.space = self.metta.space()
        
        # Knowledge domains
        self.skill_knowledge: Dict[str, Any] = {}
        self.career_knowledge: Dict[str, Any] = {}
        self.market_knowledge: Dict[str, Any] = {}
        self.industry_knowledge: Dict[str, Any] = {}
        
        # Initialize knowledge base
        asyncio.create_task(self._initialize_knowledge_base())
    
    async def _initialize_knowledge_base(self):
        """Initialize comprehensive professional knowledge base in MeTTa"""
        
        print("🧠 Initializing MeTTa Knowledge Base...")
        
        # Load skill relationships
        await self._load_skill_relationships()
        
        # Load career paths and progressions
        await self._load_career_paths()
        
        # Load market and industry data
        await self._load_market_data()
        
        # Load reasoning rules
        await self._load_reasoning_rules()
        
        print("✅ MeTTa Knowledge Base initialized")
    
    async def _load_skill_relationships(self):
        """Load skill relationship knowledge into MeTTa space"""
        
        # Skill similarity relationships
        skill_similarities = [
            # Programming language similarities
            ("JavaScript", "TypeScript", 0.95),
            ("Python", "R", 0.75),
            ("Java", "Kotlin", 0.85),
            ("C++", "C#", 0.80),
            ("Swift", "Objective-C", 0.70),
            
            # Framework relationships
            ("React", "React Native", 0.85),
            ("Angular", "AngularJS", 0.75),
            ("Django", "Flask", 0.70),
            ("Spring", "Spring Boot", 0.90),
            ("Express.js", "Node.js", 0.85),
            
            # Tool relationships
            ("Docker", "Kubernetes", 0.75),
            ("Git", "GitHub", 0.80),
            ("AWS", "Azure", 0.70),
            ("PostgreSQL", "MySQL", 0.75),
            ("Redis", "Memcached", 0.65),
            
            # Data Science stack
            ("Pandas", "NumPy", 0.80),
            ("TensorFlow", "PyTorch", 0.75),
            ("Scikit-learn", "Machine Learning", 0.85),
            ("Jupyter", "Python", 0.75),
        ]
        
        # Load similarity relationships
        for skill1, skill2, similarity in skill_similarities:
            self.space.add_atom(f"(skill-similarity {skill1} {skill2} {similarity})")
            self.space.add_atom(f"(skill-similarity {skill2} {skill1} {similarity})")
        
        # Skill prerequisites and dependencies
        skill_dependencies = [
            ("React", "JavaScript"),
            ("Django", "Python"),
            ("Spring", "Java"),
            ("Kubernetes", "Docker"),
            ("Machine Learning", "Python"),
            ("Data Science", "Statistics"),
            ("DevOps", "Linux"),
            ("iOS Development", "Swift"),
            ("Android Development", "Kotlin"),
        ]
        
        for advanced_skill, prerequisite in skill_dependencies:
            self.space.add_atom(f"(skill-prerequisite {advanced_skill} {prerequisite})")
        
        # Skill categories
        skill_categories = [
            ("JavaScript", "Programming Language"),
            ("Python", "Programming Language"),
            ("React", "Frontend Framework"),
            ("Django", "Backend Framework"),
            ("Docker", "DevOps Tool"),
            ("Machine Learning", "AI/ML"),
            ("Project Management", "Soft Skill"),
            ("Leadership", "Soft Skill"),
            ("Communication", "Soft Skill"),
        ]
        
        for skill, category in skill_categories:
            self.space.add_atom(f"(skill-category {skill} \"{category}\")")
    
    async def _load_career_paths(self):
        """Load career progression paths and role relationships"""
        
        # Career progression paths
        career_progressions = [
            # Software Development Track
            ("Junior Developer", "Mid-level Developer", 24),
            ("Mid-level Developer", "Senior Developer", 36),
            ("Senior Developer", "Tech Lead", 24),
            ("Senior Developer", "Engineering Manager", 18),
            ("Tech Lead", "Principal Engineer", 36),
            ("Engineering Manager", "Director of Engineering", 48),
            
            # Data Science Track
            ("Data Analyst", "Data Scientist", 18),
            ("Data Scientist", "Senior Data Scientist", 30),
            ("Senior Data Scientist", "Staff Data Scientist", 36),
            ("Senior Data Scientist", "ML Engineering Manager", 24),
            
            # Product Track
            ("Product Analyst", "Product Manager", 24),
            ("Product Manager", "Senior Product Manager", 36),
            ("Senior Product Manager", "Director of Product", 48),
            
            # Design Track
            ("UI Designer", "UX Designer", 18),
            ("UX Designer", "Senior UX Designer", 30),
            ("Senior UX Designer", "Design Lead", 36),
        ]
        
        for current_role, next_role, months in career_progressions:
            self.space.add_atom(f"(career-progression \"{current_role}\" \"{next_role}\" {months})")
        
        # Role skill requirements
        role_skills = [
            ("Junior Developer", ["Programming", "Git", "Problem Solving"]),
            ("Senior Developer", ["Advanced Programming", "System Design", "Mentoring", "Code Review"]),
            ("Tech Lead", ["Technical Leadership", "Architecture", "Team Management"]),
            ("Data Scientist", ["Python", "Statistics", "Machine Learning", "SQL"]),
            ("Product Manager", ["Product Strategy", "Analytics", "Communication", "User Research"]),
            ("UX Designer", ["Design Thinking", "Prototyping", "User Research", "Figma"]),
        ]
        
        for role, skills in role_skills:
            for skill in skills:
                self.space.add_atom(f"(role-skill \"{role}\" \"{skill}\")")
        
        # Industry role mappings
        industry_roles = [
            ("Technology", "Software Engineer"),
            ("Technology", "Data Scientist"),
            ("Technology", "DevOps Engineer"),
            ("Finance", "Quantitative Analyst"),
            ("Finance", "Risk Manager"),
            ("Healthcare", "Healthcare Data Analyst"),
            ("E-commerce", "Growth Engineer"),
            ("Gaming", "Game Developer"),
        ]
        
        for industry, role in industry_roles:
            self.space.add_atom(f"(industry-role \"{industry}\" \"{role}\")")
    
    async def _load_market_data(self):
        """Load market trends and salary data"""
        
        # Skill demand trends (growth rate per year)
        skill_demand = [
            ("Artificial Intelligence", 0.45),
            ("Machine Learning", 0.40),
            ("Blockchain", 0.35),
            ("React", 0.25),
            ("Python", 0.30),
            ("Kubernetes", 0.40),
            ("Cloud Computing", 0.35),
            ("Data Science", 0.30),
            ("Cybersecurity", 0.25),
            ("DevOps", 0.30),
        ]
        
        for skill, growth_rate in skill_demand:
            self.space.add_atom(f"(skill-demand \"{skill}\" {growth_rate})")
        
        # Salary ranges by role and experience (in USD thousands)
        salary_ranges = [
            ("Junior Developer", 0, 2, 60, 90),
            ("Mid-level Developer", 2, 5, 85, 120),
            ("Senior Developer", 5, 10, 120, 180),
            ("Tech Lead", 7, 12, 150, 220),
            ("Engineering Manager", 8, 15, 160, 250),
            ("Data Scientist", 3, 8, 95, 150),
            ("Senior Data Scientist", 6, 12, 140, 200),
            ("Product Manager", 4, 10, 110, 170),
        ]
        
        for role, min_exp, max_exp, min_salary, max_salary in salary_ranges:
            self.space.add_atom(f"(salary-range \"{role}\" {min_exp} {max_exp} {min_salary} {max_salary})")
        
        # Geographic salary multipliers
        location_multipliers = [
            ("San Francisco", 1.4),
            ("New York", 1.3),
            ("Seattle", 1.25),
            ("Austin", 1.1),
            ("Remote", 0.95),
            ("Berlin", 0.8),
            ("London", 1.2),
            ("Toronto", 0.9),
        ]
        
        for location, multiplier in location_multipliers:
            self.space.add_atom(f"(location-salary-multiplier \"{location}\" {multiplier})")
    
    async def _load_reasoning_rules(self):
        """Load MeTTa reasoning rules for professional insights"""
        
        # Skill similarity reasoning
        self.space.add_atom("""
        (= (similar-skills $skill1 $skill2)
           (if (> (skill-similarity $skill1 $skill2) 0.7)
               True
               False))
        """)
        
        # Career progression feasibility
        self.space.add_atom("""
        (= (feasible-progression $current $target $experience)
           (and (career-progression $current $next $months)
                (or (= $next $target)
                    (feasible-progression $next $target (+ $experience $months)))))
        """)
        
        # Skill recommendation logic
        self.space.add_atom("""
        (= (recommend-skill $current-role $target-role)
           (and (role-skill $target-role $skill)
                (not (role-skill $current-role $skill))))
        """)
        
        # Salary estimation
        self.space.add_atom("""
        (= (estimate-salary $role $experience $location)
           (and (salary-range $role $min-exp $max-exp $min-sal $max-sal)
                (<= $min-exp $experience $max-exp)
                (location-salary-multiplier $location $multiplier)
                (* (+ $min-sal (* (/ (- $experience $min-exp) (- $max-exp $min-exp)) 
                                  (- $max-sal $min-sal))) 
                   $multiplier)))
        """)
    
    # Public API Methods for uAgents
    
    async def query_career_paths(self, current_skills: List[str], experience_level: int,
                               target_industries: List[str], career_goals: List[str]) -> List[Dict[str, Any]]:
        """Query possible career paths based on current skills and goals"""
        
        career_paths = []
        
        # For each target industry, find suitable roles
        for industry in target_industries[:3]:  # Limit to top 3 industries
            # Query roles in industry
            industry_roles_query = f'(industry-role "{industry}" $role)'
            industry_roles = await self._execute_query(industry_roles_query)
            
            for role_match in industry_roles:
                role = role_match.get('role', '')
                if role:
                    # Calculate skill match percentage
                    skill_match = await self._calculate_role_skill_match(role, current_skills)
                    
                    # Get required skills for role
                    required_skills = await self._get_role_skills(role)
                    
                    # Estimate timeline and salary
                    timeline = await self._estimate_career_timeline(experience_level, role)
                    salary_range = await self._get_salary_range(role, experience_level)
                    
                    career_paths.append({
                        "target_role": role,
                        "industry": industry,
                        "skill_match_percentage": skill_match,
                        "required_skills": required_skills,
                        "timeline": timeline,
                        "salary_range": salary_range,
                        "growth_potential": await self._assess_growth_potential(role),
                        "confidence": min(skill_match / 100 + 0.3, 1.0)
                    })
        
        # Sort by confidence and skill match
        career_paths.sort(key=lambda x: (x["confidence"], x["skill_match_percentage"]), reverse=True)
        
        return career_paths[:5]  # Return top 5 paths
    
    async def analyze_skill_gap(self, current_skills: List[str], target_role: str,
                              target_skills: List[str]) -> Dict[str, Any]:
        """Analyze skill gaps for a target role"""
        
        current_skills_lower = [s.lower() for s in current_skills]
        
        missing_skills = []
        similar_skills = []
        
        for target_skill in target_skills:
            target_skill_lower = target_skill.lower()
            
            if target_skill_lower not in current_skills_lower:
                # Check if user has similar skills
                similar_found = False
                for current_skill in current_skills:
                    similarity = await self._get_skill_similarity(current_skill, target_skill)
                    if similarity > 0.7:
                        similar_skills.append({
                            "current": current_skill,
                            "target": target_skill,
                            "similarity": similarity
                        })
                        similar_found = True
                        break
                
                if not similar_found:
                    missing_skills.append(target_skill)
        
        # Prioritize missing skills
        priority_skills = await self._prioritize_skills(missing_skills, target_role)
        
        return {
            "missing_skills": missing_skills,
            "similar_skills": similar_skills,
            "priority_skills": priority_skills,
            "completion_percentage": ((len(target_skills) - len(missing_skills)) / len(target_skills)) * 100 if target_skills else 0,
            "learning_timeline_months": len(missing_skills) * 2  # Estimate 2 months per skill
        }
    
    async def get_market_insights(self, roles: List[str], locations: List[str],
                                experience_level: int) -> Dict[str, Any]:
        """Get market insights for roles and locations"""
        
        insights = {
            "roles_analysis": [],
            "location_analysis": [],
            "overall_growth_rate": 0.0,
            "salary_trends": {}
        }
        
        total_growth = 0.0
        analyzed_roles = 0
        
        for role in roles:
            # Get demand growth for role-related skills
            role_skills = await self._get_role_skills(role)
            role_growth = 0.0
            
            for skill in role_skills:
                skill_demand_query = f'(skill-demand "{skill}" $growth)'
                demand_results = await self._execute_query(skill_demand_query)
                if demand_results:
                    role_growth += demand_results[0].get('growth', 0.0)
            
            if role_skills:
                role_growth = role_growth / len(role_skills)
                total_growth += role_growth
                analyzed_roles += 1
            
            # Get salary data for role
            salary_data = await self._get_salary_range(role, experience_level)
            
            insights["roles_analysis"].append({
                "role": role,
                "growth_rate": role_growth,
                "salary_range": salary_data,
                "demand_level": "High" if role_growth > 0.3 else "Medium" if role_growth > 0.15 else "Low"
            })
        
        if analyzed_roles > 0:
            insights["overall_growth_rate"] = total_growth / analyzed_roles
        
        # Analyze locations
        for location in locations:
            multiplier_query = f'(location-salary-multiplier "{location}" $multiplier)'
            multiplier_results = await self._execute_query(multiplier_query)
            multiplier = multiplier_results[0].get('multiplier', 1.0) if multiplier_results else 1.0
            
            insights["location_analysis"].append({
                "location": location,
                "salary_multiplier": multiplier,
                "attractiveness": "High" if multiplier > 1.2 else "Medium" if multiplier > 0.9 else "Low"
            })
        
        return insights
    
    async def extract_skills_with_reasoning(self, text: str, context: Optional[str],
                                          document_type: str) -> List[str]:
        """Extract skills using MeTTa reasoning capabilities"""
        
        # Basic skill extraction using pattern matching
        extracted_skills = []
        
        # Get all known skills from MeTTa space
        all_skills_query = "(skill-category $skill $category)"
        skill_results = await self._execute_query(all_skills_query)
        
        known_skills = [result.get('skill', '') for result in skill_results]
        
        # Check for skill mentions in text
        text_lower = text.lower()
        for skill in known_skills:
            if skill.lower() in text_lower:
                extracted_skills.append(skill)
        
        # Use reasoning to infer related skills
        inferred_skills = []
        for skill in extracted_skills:
            # Find similar skills
            similarity_query = f'(skill-similarity "{skill}" $similar $score)'
            similar_results = await self._execute_query(similarity_query)
            
            for result in similar_results:
                if result.get('score', 0) > 0.8:  # High similarity threshold
                    similar_skill = result.get('similar', '')
                    if similar_skill and similar_skill not in extracted_skills:
                        inferred_skills.append(similar_skill)
        
        return list(set(extracted_skills + inferred_skills[:3]))  # Limit inferred skills
    
    # Helper methods
    
    async def _execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute MeTTa query and return results"""
        
        try:
            # Simple pattern matching for basic queries
            # In a full implementation, this would use MeTTa's query engine
            results = []
            
            # Parse basic queries manually for demo
            if "skill-similarity" in query:
                # Extract skill names and return mock similarity
                import re
                matches = re.findall(r'"([^"]+)"', query)
                if len(matches) >= 1:
                    results = [{"similar": "Related Skill", "score": 0.8}]
            
            elif "industry-role" in query:
                # Mock industry role results
                if "Technology" in query:
                    results = [
                        {"role": "Software Engineer"},
                        {"role": "Data Scientist"},
                        {"role": "DevOps Engineer"}
                    ]
            
            return results
            
        except Exception as e:
            print(f"Query execution error: {e}")
            return []
    
    async def _calculate_role_skill_match(self, role: str, current_skills: List[str]) -> float:
        """Calculate percentage match between current skills and role requirements"""
        
        required_skills = await self._get_role_skills(role)
        if not required_skills:
            return 0.0
        
        matching_skills = 0
        for required_skill in required_skills:
            for current_skill in current_skills:
                similarity = await self._get_skill_similarity(current_skill, required_skill)
                if similarity > 0.7:  # Consider similar skills as matches
                    matching_skills += similarity
                    break
        
        return (matching_skills / len(required_skills)) * 100
    
    async def _get_role_skills(self, role: str) -> List[str]:
        """Get required skills for a role"""
        
        # Mock data for demo - in production this would query MeTTa space
        role_skills_map = {
            "Software Engineer": ["Python", "JavaScript", "Git", "Problem Solving", "SQL"],
            "Data Scientist": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization"],
            "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
            "Product Manager": ["Product Strategy", "Analytics", "Communication", "User Research"],
            "UX Designer": ["Design Thinking", "Prototyping", "User Research", "Figma"]
        }
        
        return role_skills_map.get(role, [])
    
    async def _get_skill_similarity(self, skill1: str, skill2: str) -> float:
        """Get similarity score between two skills"""
        
        if skill1.lower() == skill2.lower():
            return 1.0
        
        # Mock similarity calculations for demo
        similarity_map = {
            ("python", "r"): 0.75,
            ("javascript", "typescript"): 0.95,
            ("react", "angular"): 0.6,
            ("docker", "kubernetes"): 0.75,
            ("aws", "azure"): 0.7
        }
        
        key = (skill1.lower(), skill2.lower())
        reverse_key = (skill2.lower(), skill1.lower())
        
        return similarity_map.get(key, similarity_map.get(reverse_key, 0.0))
    
    async def _estimate_career_timeline(self, current_experience: int, target_role: str) -> str:
        """Estimate timeline to reach target role"""
        
        # Simple timeline estimation based on role seniority
        role_experience_map = {
            "Junior Developer": 0,
            "Software Engineer": 2,
            "Senior Developer": 5,
            "Tech Lead": 7,
            "Engineering Manager": 8,
            "Data Scientist": 3,
            "Senior Data Scientist": 6,
            "Product Manager": 4
        }
        
        required_experience = role_experience_map.get(target_role, 3)
        
        if current_experience >= required_experience:
            return "0-6 months"
        else:
            months_needed = (required_experience - current_experience) * 12
            if months_needed <= 12:
                return "6-12 months"
            elif months_needed <= 24:
                return "1-2 years"
            else:
                return "2-3 years"
    
    async def _get_salary_range(self, role: str, experience: int) -> Dict[str, int]:
        """Get salary range for role and experience level"""
        
        # Mock salary data
        base_salaries = {
            "Software Engineer": 85000,
            "Senior Developer": 120000,
            "Tech Lead": 150000,
            "Data Scientist": 110000,
            "Product Manager": 130000
        }
        
        base = base_salaries.get(role, 80000)
        experience_multiplier = 1 + (experience * 0.05)  # 5% per year of experience
        
        return {
            "min": int(base * experience_multiplier * 0.8),
            "max": int(base * experience_multiplier * 1.2)
        }
    
    async def _assess_growth_potential(self, role: str) -> str:
        """Assess growth potential for a role"""
        
        high_growth_roles = ["Data Scientist", "Machine Learning Engineer", "DevOps Engineer", "Cybersecurity Specialist"]
        medium_growth_roles = ["Software Engineer", "Product Manager", "UX Designer"]
        
        if role in high_growth_roles:
            return "High"
        elif role in medium_growth_roles:
            return "Medium"
        else:
            return "Low"
    
    async def _prioritize_skills(self, missing_skills: List[str], target_role: str) -> List[str]:
        """Prioritize missing skills based on importance"""
        
        # Simple prioritization - in production this would use MeTTa reasoning
        skill_priority_map = {
            "Python": 10,
            "JavaScript": 9,
            "Machine Learning": 8,
            "SQL": 8,
            "Docker": 7,
            "AWS": 7,
            "React": 6,
            "Git": 9
        }
        
        prioritized = sorted(missing_skills, 
                           key=lambda skill: skill_priority_map.get(skill, 5), 
                           reverse=True)
        
        return prioritized[:5]  # Return top 5 priority skills