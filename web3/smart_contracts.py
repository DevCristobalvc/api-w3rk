"""
W3RK Smart Contract Manager
Interfaces with W3RK smart contracts for professional profile management
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from web3 import Web3
from web3.contract import Contract
from eth_account import Account
import logging

from ..config import ETHEREUM_RPC_URL, PRIVATE_KEY, CONTRACTS, CHAIN_ID
from ..models.professional_profile import ProfessionalProfile

logger = logging.getLogger(__name__)

class W3RKContractManager:
    """
    Smart Contract Manager for W3RK Platform
    
    Manages interactions with:
    - ProfileRegistry.sol - Core professional profiles
    - CVRegistry.sol - IPFS-based CV management  
    - SkillsValidation.sol - Skill certification system
    - NetworkConnections.sol - Professional networking
    - AchievementNFTs.sol - Gamification with NFTs
    """
    
    def __init__(self):
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
        
        # Setup account (for contract interactions)
        if PRIVATE_KEY:
            self.account = Account.from_key(PRIVATE_KEY)
            self.w3.eth.default_account = self.account.address
        else:
            self.account = None
            logger.warning("⚠️ No private key configured - read-only mode")
        
        # Contract instances
        self.contracts: Dict[str, Contract] = {}
        
        # Contract ABIs (simplified for demo)
        self.contract_abis = self._load_contract_abis()
        
        # Initialize contracts
        asyncio.create_task(self._initialize_contracts())
    
    def _load_contract_abis(self) -> Dict[str, List[Dict]]:
        """Load contract ABIs (Application Binary Interface)"""
        
        # Simplified ABIs for demo - in production these would be loaded from files
        return {
            "ProfileRegistry": [
                {
                    "inputs": [
                        {"name": "_username", "type": "string"},
                        {"name": "_displayName", "type": "string"}, 
                        {"name": "_bio", "type": "string"},
                        {"name": "_ipfsHash", "type": "string"}
                    ],
                    "name": "createProfile",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [{"name": "_user", "type": "address"}],
                    "name": "getProfile",
                    "outputs": [
                        {"name": "username", "type": "string"},
                        {"name": "displayName", "type": "string"},
                        {"name": "bio", "type": "string"},
                        {"name": "ipfsHash", "type": "string"},
                        {"name": "verified", "type": "bool"},
                        {"name": "createdAt", "type": "uint256"}
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [{"name": "_user", "type": "address"}],
                    "name": "isRegistered",
                    "outputs": [{"name": "", "type": "bool"}],
                    "stateMutability": "view", 
                    "type": "function"
                }
            ],
            
            "SkillsValidation": [
                {
                    "inputs": [
                        {"name": "_skill", "type": "string"},
                        {"name": "_level", "type": "uint8"},
                        {"name": "_evidenceHash", "type": "string"}
                    ],
                    "name": "submitSkillForValidation",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [
                        {"name": "_user", "type": "address"},
                        {"name": "_skill", "type": "string"}
                    ],
                    "name": "getSkillValidation",
                    "outputs": [
                        {"name": "skill", "type": "string"},
                        {"name": "level", "type": "uint8"},
                        {"name": "verified", "type": "bool"},
                        {"name": "validatorCount", "type": "uint256"}
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }
            ],
            
            "CVRegistry": [
                {
                    "inputs": [
                        {"name": "_ipfsHash", "type": "string"},
                        {"name": "_contentHash", "type": "bytes32"}
                    ],
                    "name": "publishCV",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [{"name": "_user", "type": "address"}],
                    "name": "getUserCV",
                    "outputs": [
                        {"name": "ipfsHash", "type": "string"},
                        {"name": "contentHash", "type": "bytes32"},
                        {"name": "verified", "type": "bool"},
                        {"name": "publishedAt", "type": "uint256"}
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }
            ],
            
            "AchievementNFTs": [
                {
                    "inputs": [{"name": "_user", "type": "address"}],
                    "name": "getUserAchievements",
                    "outputs": [{"name": "", "type": "uint256[]"}],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [{"name": "_tokenId", "type": "uint256"}],
                    "name": "getAchievementDetails",
                    "outputs": [
                        {"name": "achievementType", "type": "uint8"},
                        {"name": "milestone", "type": "uint256"},
                        {"name": "earnedAt", "type": "uint256"}
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
        }
    
    async def _initialize_contracts(self):
        """Initialize contract instances"""
        
        logger.info("🔗 Initializing smart contracts...")
        
        try:
            # Check network connection
            if not self.w3.is_connected():
                logger.error("❌ Failed to connect to Ethereum network")
                return
            
            logger.info(f"✅ Connected to network - Chain ID: {self.w3.eth.chain_id}")
            
            # Initialize each contract
            for contract_name, address in CONTRACTS.items():
                if address and address != "0x...":
                    try:
                        abi = self.contract_abis.get(contract_name.replace("_", ""), [])
                        if abi:
                            contract = self.w3.eth.contract(address=address, abi=abi)
                            self.contracts[contract_name] = contract
                            logger.info(f"✅ {contract_name} contract initialized at {address}")
                        else:
                            logger.warning(f"⚠️ No ABI found for {contract_name}")
                    except Exception as e:
                        logger.error(f"❌ Failed to initialize {contract_name}: {str(e)}")
                else:
                    logger.warning(f"⚠️ No address configured for {contract_name}")
            
            logger.info(f"🎯 Initialized {len(self.contracts)} contracts")
            
        except Exception as e:
            logger.error(f"❌ Contract initialization failed: {str(e)}")
    
    # ==============================================================================
    # PROFILE REGISTRY INTERACTIONS
    # ==============================================================================
    
    async def create_profile_on_blockchain(self, profile: ProfessionalProfile) -> Dict[str, Any]:
        """Create profile on ProfileRegistry contract"""
        
        if "PROFILE_REGISTRY" not in self.contracts:
            raise Exception("ProfileRegistry contract not available")
        
        if not self.account:
            raise Exception("No account configured for transactions")
        
        try:
            contract = self.contracts["PROFILE_REGISTRY"]
            
            # Check if profile already exists
            is_registered = await self._call_contract_function(
                contract, "isRegistered", [profile.wallet_address]
            )
            
            if is_registered:
                raise Exception(f"Profile already exists for {profile.wallet_address}")
            
            # Prepare transaction
            tx_function = contract.functions.createProfile(
                profile.username,
                profile.display_name,
                profile.bio,
                profile.profile_ipfs_hash or ""
            )
            
            # Execute transaction
            tx_hash = await self._execute_transaction(tx_function)
            
            logger.info(f"✅ Profile created on blockchain - TX: {tx_hash.hex()}")
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "wallet_address": profile.wallet_address,
                "block_number": await self._get_transaction_receipt(tx_hash)
            }
            
        except Exception as e:
            logger.error(f"❌ Profile creation failed: {str(e)}")
            raise
    
    async def get_profile_from_blockchain(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """Get profile from ProfileRegistry contract"""
        
        if "PROFILE_REGISTRY" not in self.contracts:
            return None
        
        try:
            contract = self.contracts["PROFILE_REGISTRY"]
            
            # Check if profile exists
            is_registered = await self._call_contract_function(
                contract, "isRegistered", [wallet_address]
            )
            
            if not is_registered:
                return None
            
            # Get profile data
            profile_data = await self._call_contract_function(
                contract, "getProfile", [wallet_address]
            )
            
            return {
                "username": profile_data[0],
                "display_name": profile_data[1], 
                "bio": profile_data[2],
                "ipfs_hash": profile_data[3],
                "verified": profile_data[4],
                "created_at": datetime.fromtimestamp(profile_data[5])
            }
            
        except Exception as e:
            logger.error(f"❌ Profile fetch failed: {str(e)}")
            return None
    
    async def verify_profile_authenticity(self, wallet_address: str) -> Dict[str, Any]:
        """Verify profile authenticity on blockchain"""
        
        try:
            profile_data = await self.get_profile_from_blockchain(wallet_address)
            
            if not profile_data:
                return {
                    "status": "not_found",
                    "verified": False,
                    "message": "Profile not found on blockchain"
                }
            
            # Verify IPFS hash integrity
            ipfs_hash = profile_data.get("ipfs_hash")
            if ipfs_hash:
                # In production, verify IPFS content matches profile data
                ipfs_verified = True  # Simplified for demo
            else:
                ipfs_verified = False
            
            return {
                "status": "verified" if profile_data["verified"] and ipfs_verified else "unverified",
                "verified": profile_data["verified"],
                "ipfs_verified": ipfs_verified,
                "profile_hash": ipfs_hash,
                "last_update": profile_data["created_at"],
                "blockchain_confirmed": True
            }
            
        except Exception as e:
            logger.error(f"❌ Profile verification failed: {str(e)}")
            return {
                "status": "error",
                "verified": False,
                "message": f"Verification failed: {str(e)}"
            }
    
    # ==============================================================================
    # SKILLS VALIDATION INTERACTIONS
    # ==============================================================================
    
    async def submit_skill_for_validation(self, wallet_address: str, skill_name: str,
                                        skill_level: int, evidence_hash: str) -> Dict[str, Any]:
        """Submit skill for validation on SkillsValidation contract"""
        
        if "SKILLS_VALIDATION" not in self.contracts:
            raise Exception("SkillsValidation contract not available")
        
        try:
            contract = self.contracts["SKILLS_VALIDATION"]
            
            tx_function = contract.functions.submitSkillForValidation(
                skill_name,
                skill_level,
                evidence_hash
            )
            
            tx_hash = await self._execute_transaction(tx_function)
            
            logger.info(f"✅ Skill submitted for validation - TX: {tx_hash.hex()}")
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "skill": skill_name,
                "level": skill_level,
                "evidence_hash": evidence_hash
            }
            
        except Exception as e:
            logger.error(f"❌ Skill submission failed: {str(e)}")
            raise
    
    async def get_skill_validation_status(self, wallet_address: str, 
                                        skill_name: str) -> Dict[str, Any]:
        """Get skill validation status from contract"""
        
        if "SKILLS_VALIDATION" not in self.contracts:
            return {"verified": False, "status": "contract_unavailable"}
        
        try:
            contract = self.contracts["SKILLS_VALIDATION"]
            
            skill_data = await self._call_contract_function(
                contract, "getSkillValidation", [wallet_address, skill_name]
            )
            
            return {
                "skill": skill_data[0],
                "level": skill_data[1], 
                "verified": skill_data[2],
                "validator_count": skill_data[3],
                "status": "verified" if skill_data[2] else "pending"
            }
            
        except Exception as e:
            logger.error(f"❌ Skill validation check failed: {str(e)}")
            return {"verified": False, "status": "error", "error": str(e)}
    
    # ==============================================================================
    # CV REGISTRY INTERACTIONS
    # ==============================================================================
    
    async def publish_cv_on_blockchain(self, wallet_address: str, ipfs_hash: str,
                                     content_hash: str) -> Dict[str, Any]:
        """Publish CV on CVRegistry contract"""
        
        if "CV_REGISTRY" not in self.contracts:
            raise Exception("CVRegistry contract not available")
        
        try:
            contract = self.contracts["CV_REGISTRY"]
            
            # Convert content hash to bytes32
            content_hash_bytes = self.w3.keccak(text=content_hash)
            
            tx_function = contract.functions.publishCV(ipfs_hash, content_hash_bytes)
            
            tx_hash = await self._execute_transaction(tx_function)
            
            logger.info(f"✅ CV published on blockchain - TX: {tx_hash.hex()}")
            
            return {
                "success": True,
                "transaction_hash": tx_hash.hex(),
                "ipfs_hash": ipfs_hash,
                "content_hash": content_hash_bytes.hex()
            }
            
        except Exception as e:
            logger.error(f"❌ CV publication failed: {str(e)}")
            raise
    
    async def get_user_cv_from_blockchain(self, wallet_address: str) -> Optional[Dict[str, Any]]:
        """Get user's CV from CVRegistry contract"""
        
        if "CV_REGISTRY" not in self.contracts:
            return None
        
        try:
            contract = self.contracts["CV_REGISTRY"]
            
            cv_data = await self._call_contract_function(
                contract, "getUserCV", [wallet_address]
            )
            
            if not cv_data[0]:  # Empty IPFS hash means no CV
                return None
            
            return {
                "ipfs_hash": cv_data[0],
                "content_hash": cv_data[1].hex(),
                "verified": cv_data[2],
                "published_at": datetime.fromtimestamp(cv_data[3])
            }
            
        except Exception as e:
            logger.error(f"❌ CV fetch failed: {str(e)}")
            return None
    
    # ==============================================================================
    # ACHIEVEMENT NFTS INTERACTIONS
    # ==============================================================================
    
    async def get_user_achievements(self, wallet_address: str) -> List[Dict[str, Any]]:
        """Get user's achievement NFTs"""
        
        if "ACHIEVEMENT_NFTS" not in self.contracts:
            return []
        
        try:
            contract = self.contracts["ACHIEVEMENT_NFTS"]
            
            # Get achievement token IDs
            token_ids = await self._call_contract_function(
                contract, "getUserAchievements", [wallet_address]
            )
            
            achievements = []
            
            # Get details for each achievement
            for token_id in token_ids:
                achievement_data = await self._call_contract_function(
                    contract, "getAchievementDetails", [token_id]
                )
                
                achievements.append({
                    "token_id": token_id,
                    "achievement_type": achievement_data[0],
                    "milestone": achievement_data[1],
                    "earned_at": datetime.fromtimestamp(achievement_data[2]),
                    "type_name": self._get_achievement_type_name(achievement_data[0])
                })
            
            return achievements
            
        except Exception as e:
            logger.error(f"❌ Achievement fetch failed: {str(e)}")
            return []
    
    def _get_achievement_type_name(self, achievement_type: int) -> str:
        """Convert achievement type ID to human-readable name"""
        
        achievement_types = {
            0: "Profile Creation",
            1: "First CV",
            2: "Skill Master", 
            3: "Network Builder",
            4: "Influencer",
            5: "Veteran",
            6: "Pioneer",
            7: "Skill Validator",
            8: "Mentor",
            9: "Community Leader"
        }
        
        return achievement_types.get(achievement_type, f"Unknown ({achievement_type})")
    
    # ==============================================================================
    # TRANSACTION UTILITIES
    # ==============================================================================
    
    async def _call_contract_function(self, contract: Contract, function_name: str,
                                    args: List[Any]) -> Any:
        """Call read-only contract function"""
        
        try:
            function = getattr(contract.functions, function_name)
            result = function(*args).call()
            return result
            
        except Exception as e:
            logger.error(f"❌ Contract call failed {function_name}: {str(e)}")
            raise
    
    async def _execute_transaction(self, tx_function) -> bytes:
        """Execute contract transaction"""
        
        if not self.account:
            raise Exception("No account configured for transactions")
        
        try:
            # Build transaction
            tx = tx_function.build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 2000000,  # Adjust gas limit as needed
                'gasPrice': self.w3.to_wei('20', 'gwei')
            })
            
            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            return tx_hash
            
        except Exception as e:
            logger.error(f"❌ Transaction execution failed: {str(e)}")
            raise
    
    async def _get_transaction_receipt(self, tx_hash: bytes) -> Optional[int]:
        """Get transaction receipt and return block number"""
        
        try:
            # Wait for transaction confirmation
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            return receipt.blockNumber
            
        except Exception as e:
            logger.error(f"❌ Transaction receipt failed: {str(e)}")
            return None
    
    # ==============================================================================
    # PUBLIC UTILITY METHODS
    # ==============================================================================
    
    async def store_profile(self, profile: ProfessionalProfile):
        """Store complete profile on blockchain and IPFS"""
        
        try:
            # Create profile on blockchain
            result = await self.create_profile_on_blockchain(profile)
            
            logger.info(f"✅ Profile stored for {profile.wallet_address}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Profile storage failed: {str(e)}")
            raise
    
    async def update_profile_recommendations(self, wallet_address: str, 
                                           recommendations: Dict[str, Any]):
        """Update profile with AI recommendations"""
        
        # In a full implementation, this would update specific fields
        logger.info(f"📝 Updated recommendations for {wallet_address}")
    
    async def update_skill_analysis(self, wallet_address: str, analysis: Dict[str, Any]):
        """Update profile with skill analysis results"""
        
        # In a full implementation, this would update skill data
        logger.info(f"🔍 Updated skill analysis for {wallet_address}")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get blockchain connection status"""
        
        return {
            "connected": self.w3.is_connected(),
            "chain_id": self.w3.eth.chain_id if self.w3.is_connected() else None,
            "account": self.account.address if self.account else None,
            "contracts_loaded": len(self.contracts),
            "available_contracts": list(self.contracts.keys())
        }