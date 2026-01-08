# backend/realtime/websocket_server.py - WebSocket Server for Real-Time Updates
"""
Real-time WebSocket server for live dashboard updates.
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict):
        """Broadcast message to all connected clients"""
        message_json = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


# Global connection manager
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint handler"""
    await manager.connect(websocket)
    
    try:
        # Send welcome message
        await manager.send_personal_message(
            json.dumps({
                "type": "connection",
                "status": "connected",
                "timestamp": datetime.utcnow().isoformat()
            }),
            websocket
        )
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "ping":
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "pong",
                            "timestamp": datetime.utcnow().isoformat()
                        }),
                        websocket
                    )
                elif message_type == "subscribe":
                    # Handle subscription to specific events
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "subscribed",
                            "events": message.get("events", [])
                        }),
                        websocket
                    )
                    
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "message": "Invalid JSON"
                    }),
                    websocket
                )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


async def broadcast_update(update_type: str, data: Dict):
    """Broadcast update to all connected clients"""
    message = {
        "type": update_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.broadcast(message)


async def broadcast_alert(alert_data: Dict):
    """Broadcast alert to all clients"""
    await broadcast_update("alert", alert_data)


async def broadcast_statistics(stats: Dict):
    """Broadcast statistics update"""
    await broadcast_update("statistics", stats)


async def broadcast_new_analysis(analysis_data: Dict):
    """Broadcast new analysis result"""
    await broadcast_update("analysis", analysis_data)
