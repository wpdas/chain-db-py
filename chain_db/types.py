"""Type definitions for the ChainDB Python client."""

from typing import Dict, List, Any, Callable, Optional, TypeVar, Generic, Union

# Type variable for generic models
T = TypeVar('T')

class Connection:
    """Connection information for ChainDB."""
    
    def __init__(self, server: Optional[str], database: str, user: str, password: str):
        """
        Initialize a connection.
        
        Args:
            server: Server location. If None, "http://localhost:2818" will be used.
            database: Database name.
            user: User to access the database.
            password: Password to access the database.
        """
        self.server = server
        self.database = database
        self.user = user
        self.password = password

class BasicResponse:
    """Basic response from ChainDB API."""
    
    def __init__(self, success: bool, message: str, data: Any = None):
        """
        Initialize a basic response.
        
        Args:
            success: Whether the request was successful.
            message: Message from the server.
            data: Optional data from the server.
        """
        self.success = success
        self.message = message
        self.data = data

class EventData:
    """Event data from WebSocket events."""
    
    def __init__(self, event_type: str, database: str, table: str, data: Dict[str, Any], timestamp: int):
        """
        Initialize event data.
        
        Args:
            event_type: Type of event.
            database: Database name.
            table: Table name.
            data: Data associated with the event.
            timestamp: Timestamp of the event.
        """
        self.event_type = event_type
        self.database = database
        self.table = table
        self.data = data
        self.timestamp = timestamp

# Type for event callbacks
EventCallback = Callable[[EventData], None]

# Type for criteria in basic queries
Criteria = Dict[str, Union[str, int, bool]]

class CriteriaAdvanced:
    """Advanced criteria for queries."""
    
    def __init__(self, field: str, operator: str, value: Union[str, int, bool]):
        """
        Initialize advanced criteria.
        
        Args:
            field: Field name to filter.
            operator: Operator to use in comparison.
            value: Value to compare against.
        """
        self.field = field
        self.operator = operator
        self.value = value
