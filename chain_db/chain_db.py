"""ChainDB class for the ChainDB Python client."""

from typing import Dict, Any, TypeVar, Generic, Optional, Callable
from .constants import DEFAULT_API_SERVER, CONNECT, WEB_SOCKET_EVENTS
from .utils import post
from .table import Table
from .events import Events
from .types import Connection, EventCallback

# Type variable for generic models
T = TypeVar('T')

class ChainDB:
    """
    Main class for interacting with ChainDB.
    """
    
    def __init__(self):
        """Initialize a ChainDB instance."""
        self.server = DEFAULT_API_SERVER
        self.database = ''
        self.auth = ''
        self._events = None
    
    async def connect(self, connection: Connection) -> None:
        """
        Connect to a ChainDB database.
        
        Args:
            connection: Connection information.
        
        Raises:
            Exception: If the connection fails.
        """
        self.server = connection.server or DEFAULT_API_SERVER
        self.database = connection.database
        
        try:
            response = post(f"{self.server}{CONNECT}", {
                "name": self.database,
                "user": connection.user,
                "password": connection.password
            })
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            self.auth = response.get('data', '')
        except Exception as e:
            raise Exception(f"Something went wrong with connect operation: {str(e)}")
    
    async def get_table(self, table_name: str) -> Table:
        """
        Initialize a table, fetching its more updated data.
        
        Args:
            table_name: Name of the table.
        
        Returns:
            Table instance.
        
        Raises:
            Exception: If the get_table fails.
        """
        table = Table(table_name, self)
        await table.refetch()
        return table
    
    def events(self):
        """
        Get the events handler.
        
        Returns:
            Object with methods to subscribe and unsubscribe from events.
        """
        return EventsHandler(self)

class EventsHandler:
    """
    Handles events for ChainDB.
    """
    
    def __init__(self, db: ChainDB):
        """
        Initialize an EventsHandler.
        
        Args:
            db: ChainDB instance.
        """
        self.db = db
        self._events = None
    
    async def _get_events(self) -> Events:
        """
        Get or create the Events instance.
        
        Returns:
            Events instance.
        """
        if not self._events:
            ws_url = self.db.server.replace('http', 'ws') + WEB_SOCKET_EVENTS
            self._events = Events(ws_url, self.db.auth)
            await self._events.connect()
        
        return self._events
    
    async def subscribe(self, event: str, callback: EventCallback) -> None:
        """
        Subscribe to an event.
        
        Args:
            event: Event name to subscribe to.
            callback: Function to call when the event is received.
        """
        events = await self._get_events()
        await events.subscribe(event, callback)
    
    async def unsubscribe(self, event: str, callback: Optional[EventCallback] = None) -> None:
        """
        Unsubscribe from an event.
        
        Args:
            event: Event name to unsubscribe from.
            callback: Optional callback to remove. If not provided, all callbacks for the event will be removed.
        """
        if not self._events or not self._events.is_connected():
            return
        
        await self._events.unsubscribe(event, callback)
    
    async def close_events(self) -> None:
        """
        Close the events transmission.
        """
        if self._events:
            await self._events.close()
            self._events = None

async def connect(connection: Connection) -> ChainDB:
    """
    Connect to a ChainDB database.
    
    Args:
        connection: Connection information.
    
    Returns:
        ChainDB instance.
    
    Raises:
        Exception: If the connection fails.
    """
    chain_db = ChainDB()
    await chain_db.connect(connection)
    return chain_db
