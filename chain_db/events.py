"""Events class for the ChainDB Python client."""

import json
import asyncio
import websockets
from typing import Dict, Any, Callable, Optional, List
from .types import EventCallback, EventData

class Events:
    """
    Handles WebSocket events from ChainDB.
    """
    
    def __init__(self, url: str, auth: str):
        """
        Initialize an Events instance.
        
        Args:
            url: WebSocket URL.
            auth: Authentication token.
        """
        self.url = url
        self.auth = auth
        self.websocket = None
        self.connected = False
        self.event_listeners = {}  # Map of event name to list of callbacks
        self.task = None
    
    async def connect(self):
        """
        Connect to the WebSocket server.
        
        Raises:
            Exception: If the connection fails.
        """
        try:
            headers = {"Authorization": f"Basic {self.auth}"}
            self.websocket = await websockets.connect(self.url, extra_headers=headers)
            self.connected = True
            self.task = asyncio.create_task(self._listen())
        except Exception as e:
            self.connected = False
            raise Exception(f"Failed to connect to WebSocket: {str(e)}")
    
    async def _listen(self):
        """
        Listen for WebSocket messages.
        """
        try:
            while self.connected and self.websocket:
                message = await self.websocket.recv()
                try:
                    data = json.loads(message)
                    if 'event' in data and data['event'] in self.event_listeners:
                        event_data = EventData(
                            event_type=data.get('event_type', ''),
                            database=data.get('database', ''),
                            table=data.get('table', ''),
                            data=data.get('data', {}),
                            timestamp=data.get('timestamp', 0)
                        )
                        for callback in self.event_listeners[data['event']]:
                            callback(event_data)
                except json.JSONDecodeError:
                    print(f"Failed to parse WebSocket message: {message}")
        except websockets.exceptions.ConnectionClosed:
            self.connected = False
        except Exception as e:
            print(f"WebSocket error: {str(e)}")
            self.connected = False
    
    async def subscribe(self, event: str, callback: EventCallback):
        """
        Subscribe to an event.
        
        Args:
            event: Event name to subscribe to.
            callback: Function to call when the event is received.
        """
        if not self.connected:
            await self.connect()
        
        if event not in self.event_listeners:
            self.event_listeners[event] = []
        
        self.event_listeners[event].append(callback)
        
        # Send subscription message to server
        if self.connected and self.websocket:
            await self.websocket.send(json.dumps({
                "action": "subscribe",
                "event": event
            }))
    
    async def unsubscribe(self, event: str, callback: Optional[EventCallback] = None):
        """
        Unsubscribe from an event.
        
        Args:
            event: Event name to unsubscribe from.
            callback: Optional callback to remove. If not provided, all callbacks for the event will be removed.
        """
        if event not in self.event_listeners:
            return
        
        if callback:
            # Remove specific callback
            self.event_listeners[event] = [cb for cb in self.event_listeners[event] if cb != callback]
        else:
            # Remove all callbacks for this event
            self.event_listeners[event] = []
        
        # Send unsubscription message to server
        if self.connected and self.websocket:
            await self.websocket.send(json.dumps({
                "action": "unsubscribe",
                "event": event
            }))
    
    async def close(self):
        """
        Close the WebSocket connection.
        """
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        if self.websocket:
            await self.websocket.close()
        
        self.connected = False
    
    def is_connected(self) -> bool:
        """
        Check if the WebSocket connection is established.
        
        Returns:
            True if connected, False otherwise.
        """
        return self.connected
