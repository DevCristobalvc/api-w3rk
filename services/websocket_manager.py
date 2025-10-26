"""
WebSocket Manager for Real-time Communication
Manages WebSocket connections for live agent interactions
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    """
    Manages WebSocket connections for real-time agent communication
    
    Features:
    - User-specific connection management
    - Broadcast messaging to specific users or groups
    - Connection state tracking and cleanup
    - Message queuing for offline users
    - Real-time agent response delivery
    """
    
    def __init__(self):
        # Active WebSocket connections by user address
        self.connections: Dict[str, WebSocket] = {}
        
        # Connection metadata
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
        
        # Message queues for offline users
        self.message_queues: Dict[str, List[Dict[str, Any]]] = {}
        
        # Active conversations by user
        self.conversations: Dict[str, List[str]] = {}
        
        # Connection statistics
        self.stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_sent": 0,
            "messages_received": 0
        }
    
    async def connect(self, websocket: WebSocket, user_address: str):
        """Accept new WebSocket connection"""
        try:
            await websocket.accept()
            
            # Store connection
            self.connections[user_address] = websocket
            
            # Initialize metadata
            self.connection_metadata[user_address] = {
                "connected_at": datetime.now(),
                "last_activity": datetime.now(),
                "messages_sent": 0,
                "messages_received": 0,
                "agent_sessions": []
            }
            
            # Initialize conversation tracking
            if user_address not in self.conversations:
                self.conversations[user_address] = []
            
            # Update statistics
            self.stats["total_connections"] += 1
            self.stats["active_connections"] += 1
            
            logger.info(f"✅ WebSocket connected for user {user_address}")
            
            # Send welcome message
            await self._send_welcome_message(websocket, user_address)
            
            # Deliver queued messages if any
            await self._deliver_queued_messages(user_address)
            
        except Exception as e:
            logger.error(f"❌ WebSocket connection error for {user_address}: {str(e)}")
            raise
    
    def disconnect(self, user_address: str):
        """Handle WebSocket disconnection"""
        try:
            if user_address in self.connections:
                # Remove connection
                del self.connections[user_address]
                
                # Update statistics
                self.stats["active_connections"] -= 1
                
                # Keep metadata for reconnection
                if user_address in self.connection_metadata:
                    self.connection_metadata[user_address]["disconnected_at"] = datetime.now()
                
                logger.info(f"🔌 WebSocket disconnected for user {user_address}")
                
        except Exception as e:
            logger.error(f"❌ WebSocket disconnection error for {user_address}: {str(e)}")
    
    async def send_message_to_user(self, user_address: str, message: Dict[str, Any]) -> bool:
        """Send message to specific user"""
        try:
            # Check if user is connected
            if user_address in self.connections:
                websocket = self.connections[user_address]
                
                # Add timestamp
                message["timestamp"] = datetime.now().isoformat()
                
                # Send message
                await websocket.send_text(json.dumps(message))
                
                # Update statistics
                self.stats["messages_sent"] += 1
                if user_address in self.connection_metadata:
                    self.connection_metadata[user_address]["messages_sent"] += 1
                    self.connection_metadata[user_address]["last_activity"] = datetime.now()
                
                logger.debug(f"📤 Message sent to {user_address}: {message.get('type', 'unknown')}")
                return True
                
            else:
                # Queue message for offline user
                await self._queue_message_for_user(user_address, message)
                logger.debug(f"📥 Message queued for offline user {user_address}")
                return False
                
        except WebSocketDisconnect:
            # Handle connection loss
            self.disconnect(user_address)
            await self._queue_message_for_user(user_address, message)
            return False
            
        except Exception as e:
            logger.error(f"❌ Error sending message to {user_address}: {str(e)}")
            return False
    
    async def broadcast_to_all(self, message: Dict[str, Any], exclude_users: List[str] = None):
        """Broadcast message to all connected users"""
        exclude_users = exclude_users or []
        
        message["timestamp"] = datetime.now().isoformat()
        message["broadcast"] = True
        
        sent_count = 0
        failed_users = []
        
        for user_address, websocket in list(self.connections.items()):
            if user_address not in exclude_users:
                try:
                    await websocket.send_text(json.dumps(message))
                    sent_count += 1
                    
                except (WebSocketDisconnect, Exception) as e:
                    logger.error(f"❌ Broadcast failed for {user_address}: {str(e)}")
                    failed_users.append(user_address)
        
        # Clean up failed connections
        for user_address in failed_users:
            self.disconnect(user_address)
        
        logger.info(f"📡 Broadcast sent to {sent_count} users, {len(failed_users)} failed")
        return sent_count
    
    async def send_agent_response(self, user_address: str, agent_type: str, 
                                response: Dict[str, Any]):
        """Send agent response to user"""
        message = {
            "type": "agent_response",
            "agent": agent_type,
            "response": response,
            "user_address": user_address
        }
        
        return await self.send_message_to_user(user_address, message)
    
    async def send_typing_indicator(self, user_address: str, agent_type: str, 
                                  is_typing: bool = True):
        """Send typing indicator for agent"""
        message = {
            "type": "typing_indicator",
            "agent": agent_type,
            "is_typing": is_typing
        }
        
        return await self.send_message_to_user(user_address, message)
    
    async def send_system_notification(self, user_address: str, notification: Dict[str, Any]):
        """Send system notification to user"""
        message = {
            "type": "system_notification",
            "notification": notification
        }
        
        return await self.send_message_to_user(user_address, message)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            **self.stats,
            "connected_users": len(self.connections),
            "queued_messages": sum(len(queue) for queue in self.message_queues.values()),
            "active_conversations": len(self.conversations)
        }
    
    def get_user_connection_info(self, user_address: str) -> Dict[str, Any]:
        """Get connection information for specific user"""
        if user_address not in self.connection_metadata:
            return {"connected": False}
        
        metadata = self.connection_metadata[user_address]
        is_connected = user_address in self.connections
        
        return {
            "connected": is_connected,
            "metadata": metadata,
            "queued_messages": len(self.message_queues.get(user_address, [])),
            "active_conversations": self.conversations.get(user_address, [])
        }
    
    async def _send_welcome_message(self, websocket: WebSocket, user_address: str):
        """Send welcome message to newly connected user"""
        welcome_message = {
            "type": "connection_established",
            "message": "Welcome to W3RK Platform! 🚀",
            "features": {
                "real_time_chat": True,
                "agent_communication": True,
                "live_updates": True
            },
            "available_agents": [
                "career_advisor",
                "skills_analyzer", 
                "network_connector",
                "opportunity_matcher",
                "profile_analyzer"
            ],
            "user_address": user_address,
            "timestamp": datetime.now().isoformat()
        }
        
        await websocket.send_text(json.dumps(welcome_message))
    
    async def _queue_message_for_user(self, user_address: str, message: Dict[str, Any]):
        """Queue message for offline user"""
        if user_address not in self.message_queues:
            self.message_queues[user_address] = []
        
        # Add to queue with timestamp
        queued_message = {
            **message,
            "queued_at": datetime.now().isoformat()
        }
        
        self.message_queues[user_address].append(queued_message)
        
        # Limit queue size to prevent memory issues
        max_queue_size = 100
        if len(self.message_queues[user_address]) > max_queue_size:
            # Remove oldest messages
            self.message_queues[user_address] = self.message_queues[user_address][-max_queue_size:]
    
    async def _deliver_queued_messages(self, user_address: str):
        """Deliver queued messages to reconnected user"""
        if user_address not in self.message_queues:
            return
        
        queued_messages = self.message_queues[user_address]
        if not queued_messages:
            return
        
        # Send notification about queued messages
        await self.send_system_notification(user_address, {
            "type": "queued_messages",
            "count": len(queued_messages),
            "message": f"You have {len(queued_messages)} unread messages"
        })
        
        # Deliver messages one by one
        for message in queued_messages:
            message["delivered_from_queue"] = True
            await self.send_message_to_user(user_address, message)
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)
        
        # Clear queue after delivery
        self.message_queues[user_address] = []
        
        logger.info(f"📬 Delivered {len(queued_messages)} queued messages to {user_address}")
    
    def add_conversation(self, user_address: str, conversation_id: str):
        """Add conversation to user's active conversations"""
        if user_address not in self.conversations:
            self.conversations[user_address] = []
        
        if conversation_id not in self.conversations[user_address]:
            self.conversations[user_address].append(conversation_id)
    
    def remove_conversation(self, user_address: str, conversation_id: str):
        """Remove conversation from user's active conversations"""
        if user_address in self.conversations:
            if conversation_id in self.conversations[user_address]:
                self.conversations[user_address].remove(conversation_id)
    
    async def cleanup_inactive_connections(self, max_idle_minutes: int = 30):
        """Clean up inactive connections"""
        current_time = datetime.now()
        inactive_users = []
        
        for user_address, metadata in self.connection_metadata.items():
            last_activity = metadata.get("last_activity")
            if last_activity:
                idle_minutes = (current_time - last_activity).total_seconds() / 60
                if idle_minutes > max_idle_minutes:
                    inactive_users.append(user_address)
        
        for user_address in inactive_users:
            if user_address in self.connections:
                try:
                    websocket = self.connections[user_address]
                    await websocket.close()
                except:
                    pass
                finally:
                    self.disconnect(user_address)
        
        if inactive_users:
            logger.info(f"🧹 Cleaned up {len(inactive_users)} inactive connections")