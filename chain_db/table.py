"""Table class for the ChainDB Python client."""

from typing import Dict, List, Any, TypeVar, Generic, Optional, Union, Callable
from .constants import GET_TABLE, PERSIST_NEW_DATA, GET_HISTORY, FIND_WHERE_BASIC, FIND_WHERE_ADVANCED, GET_DOC
from .utils import post, get
from .table_doc import TableDoc
from .types import Criteria, CriteriaAdvanced

# Forward reference for ChainDB
ChainDB = TypeVar('ChainDB')

# Type variable for generic models
T = TypeVar('T')

class Table(Generic[T]):
    """
    Represents a table in ChainDB.
    """
    
    def __init__(self, name: str, db: ChainDB):
        """
        Initialize a Table.
        
        Args:
            name: Name of the table.
            db: ChainDB instance.
        """
        self.name = name
        self.db = db
        self.currentDoc = {}  # Current document data
    
    async def persist(self) -> Dict[str, Any]:
        """
        Persist table data changes.
        Creates a new record with the current document data.
        
        Returns:
            The created document with its doc_id.
        
        Raises:
            Exception: If the persist fails.
        """
        url = f"{self.db.server}{PERSIST_NEW_DATA(self.name)}"
        
        body = {
            "data": self.currentDoc
        }
        
        try:
            response = post(url, body, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            return response.get('data', {})
        except Exception as e:
            raise Exception(f"Something went wrong with persist operation: {str(e)}")
    
    async def get_history(self, limit: int) -> List[Dict[str, Any]]:
        """
        Get the history of changes.
        A list of transactions from the most recent to the most old in a range of depth.
        
        Args:
            limit: Maximum number of records to return.
        
        Returns:
            List of historical records.
        
        Raises:
            Exception: If the get_history fails.
        """
        url = f"{self.db.server}{GET_HISTORY(self.name, limit)}"
        
        try:
            response = get(url, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            return response.get('data', [])
        except Exception as e:
            raise Exception(f"Something went wrong with get_history operation: {str(e)}")
    
    async def refetch(self) -> None:
        """
        Refetch the table data.
        
        Raises:
            Exception: If the refetch fails.
        """
        url = f"{self.db.server}{GET_TABLE(self.name)}"
        
        try:
            response = get(url, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            self.currentDoc = response.get('data', {})
        except Exception as e:
            raise Exception(f"Something went wrong with refetch operation: {str(e)}")
    
    def is_empty(self) -> bool:
        """
        Check if the table is empty.
        
        Returns:
            True if the table is empty, False otherwise.
        """
        return not bool(self.currentDoc)
    
    def get_name(self) -> str:
        """
        Get the table's name.
        
        Returns:
            Table name.
        """
        return self.name
    
    def get_current_doc_id(self) -> Optional[str]:
        """
        Get the current document ID.
        
        Returns:
            Current document ID, or None if there is no current document.
        """
        return self.currentDoc.get('doc_id')
    
    async def find_where(self, criteria: Criteria, limit: int = 1000, reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Find items in the table using basic criteria with exact matches.
        
        Args:
            criteria: Object with fields and values to match exactly.
            limit: Maximum number of items to return.
            reverse: If True, returns items in reverse order.
        
        Returns:
            Array of found items matching the criteria.
        
        Raises:
            Exception: If the find_where fails.
        
        Example:
            # Find items where age is 44
            table.find_where({"age": 44})
            
            # Find items with multiple criteria
            table.find_where({
                "age": 44,
                "name": "john",
                "active": True,
                "score": 100
            })
        """
        url = f"{self.db.server}{FIND_WHERE_BASIC(self.name)}"
        
        body = {
            "criteria": criteria,
            "limit": limit,
            "reverse": reverse
        }
        
        try:
            response = post(url, body, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            return response.get('data', [])
        except Exception as e:
            raise Exception(f"Something went wrong with find_where operation: {str(e)}")
    
    async def find_where_advanced(self, criteria: List[CriteriaAdvanced], limit: int = 1000, reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Find items in the table using advanced criteria with operators.
        
        Args:
            criteria: Array of criteria to filter items.
            limit: Maximum number of items to return.
            reverse: If True, returns items in reverse order.
        
        Returns:
            Array of found items matching the criteria.
        
        Raises:
            Exception: If the find_where_advanced fails.
        
        Example:
            # Find items where greeting contains "hello"
            from chain_db_py.constants import Operators
            
            table.find_where_advanced([
                {
                    "field": "greeting",
                    "operator": Operators.CONTAINS,
                    "value": "hello"
                }
            ])
        """
        url = f"{self.db.server}{FIND_WHERE_ADVANCED(self.name)}"
        
        # Convert CriteriaAdvanced objects to dictionaries
        criteria_dicts = [
            {
                "field": c.field,
                "operator": c.operator,
                "value": c.value
            } for c in criteria
        ]
        
        body = {
            "criteria": criteria_dicts,
            "limit": limit,
            "reverse": reverse
        }
        
        try:
            response = post(url, body, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            return response.get('data', [])
        except Exception as e:
            raise Exception(f"Something went wrong with find_where_advanced operation: {str(e)}")
    
    async def get_doc(self, doc_id: str) -> TableDoc:
        """
        Get a specific document by its ID.
        
        Args:
            doc_id: The document ID to retrieve.
        
        Returns:
            A TableDoc instance with the specific document data.
        
        Raises:
            Exception: If the get_doc fails.
        """
        url = f"{self.db.server}{GET_DOC(self.name, doc_id)}"
        
        try:
            response = get(url, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            # Create a TableDoc instance with the document data
            return TableDoc(self.name, doc_id, response.get('data', {}), self.db)
        except Exception as e:
            raise Exception(f"Something went wrong with get_doc operation: {str(e)}")
