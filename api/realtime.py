# api/realtime.py - Real-Time API Endpoints
"""
Real-time endpoints for WebSocket and live updates.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.realtime.websocket_server import manager, websocket_endpoint
from backend.realtime.scheduler import scheduler, initialize_scheduler
import json

router = APIRouter()


@router.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_endpoint(websocket)


@router.post("/api/v1/realtime/start")
async def start_realtime():
    """Start real-time monitoring and scheduled jobs"""
    try:
        initialize_scheduler()
        return {
            "status": "started",
            "message": "Real-time monitoring and scheduled jobs started"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/api/v1/realtime/stop")
async def stop_realtime():
    """Stop real-time monitoring"""
    try:
        scheduler.stop()
        return {
            "status": "stopped",
            "message": "Real-time monitoring stopped"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
