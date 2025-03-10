"""Constants for the ChainDB Python client."""

# Default API server
DEFAULT_API_SERVER = 'http://localhost:2818'

# API base path
API_BASE = '/api/v1'

# API endpoints
CONNECT = f"{API_BASE}/database/connect"
GET_TABLE = lambda table: f"{API_BASE}/table/{table}"
UPDATE_ITEM = lambda table: f"{API_BASE}/table/{table}/update"
PERSIST_NEW_DATA = lambda table: f"{API_BASE}/table/{table}/persist"
GET_HISTORY = lambda table, limit=25: f"{API_BASE}/table/{table}/history?limit={limit}"
FIND_WHERE_BASIC = lambda table: f"{API_BASE}/table/{table}/find"
FIND_WHERE_ADVANCED = lambda table: f"{API_BASE}/table/{table}/find-advanced"
GET_DOC = lambda table, doc_id: f"{API_BASE}/table/{table}/doc/{doc_id}"
WEB_SOCKET_EVENTS = f"{API_BASE}/events"

# Event types
class EventTypes:
    """Event types for WebSocket events."""
    TABLE_UPDATE = 'TableUpdate'
    TABLE_PERSIST = 'TablePersist'

# Operators for advanced queries
class Operators:
    """Operators for advanced queries."""
    EQUAL = 'Eq'
    NOT_EQUAL = 'Ne'
    GREATER_THAN = 'Gt'
    GREATER_THAN_OR_EQUAL = 'Ge'
    LESS_THAN = 'Lt'
    LESS_THAN_OR_EQUAL = 'Le'
    CONTAINS = 'Contains'
    STARTS_WITH = 'StartsWith'
    ENDS_WITH = 'EndsWith'
