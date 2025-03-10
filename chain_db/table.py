"""Table class for the ChainDB Python client."""

from typing import Dict, List, Any, TypeVar, Generic, Optional, Union, Callable, Type, cast
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
    
    Type Parameters:
        T: Optional model class to cast the table to.
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
        self.current_doc = {}  # Current document data, renamed from currentDoc to follow Python conventions
    
    async def persist(self) -> Dict[str, Any]:
        """
        Persist the current document to the database.
        This will create a new document with a new doc_id.
        
        Returns:
            The persisted document with its doc_id.
        
        Raises:
            Exception: If the persist fails.
        """
        url = f"{self.db.server}{PERSIST_NEW_DATA(self.name)}"
        
        try:
            response = post(url, self.current_doc, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            # Update the current document with the persisted data
            self.current_doc = response.get('data', {})
            
            return self.current_doc
        except Exception as e:
            raise Exception(f"Something went wrong with persist operation: {str(e)}")
    
    async def get_history(self, limit: int) -> List[Dict[str, Any]]:
        """
        Get the history of changes to the table.
        
        Args:
            limit: Maximum number of history entries to return.
        
        Returns:
            List of historical documents.
        
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
        Refetch the table data from the database.
        
        Raises:
            Exception: If the refetch fails.
        """
        url = f"{self.db.server}{GET_TABLE(self.name)}"
        
        try:
            response = get(url, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            # Update the current document with the latest data from the database
            self.current_doc = response.get('data', {})
        except Exception as e:
            raise Exception(f"Something went wrong with refetch operation: {str(e)}")
    
    def is_empty(self) -> bool:
        """
        Check if the table is empty.
        
        Returns:
            True if the table is empty, False otherwise.
        """
        return not bool(self.current_doc)
    
    def get_name(self) -> str:
        """
        Get the name of the table.
        
        Returns:
            Table name.
        """
        return self.name
    
    def get_current_doc_id(self) -> Optional[str]:
        """
        Get the ID of the current document.
        
        Returns:
            The document ID, or None if there is no current document.
        """
        return self.current_doc.get('doc_id')
    
    async def find_where(self, criteria: Criteria, limit: int = 1000, reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Find documents matching the given criteria.
        
        Args:
            criteria: Dictionary of field-value pairs to match.
            limit: Maximum number of documents to return.
            reverse: Whether to return documents in reverse order.
        
        Returns:
            List of matching documents.
        
        Raises:
            Exception: If the find_where fails.
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
        Find documents matching the given advanced criteria.
        
        Args:
            criteria: List of CriteriaAdvanced objects.
            limit: Maximum number of documents to return.
            reverse: Whether to return documents in reverse order.
        
        Returns:
            List of matching documents.
        
        Raises:
            Exception: If the find_where_advanced fails.
        """
        url = f"{self.db.server}{FIND_WHERE_ADVANCED(self.name)}"
        
        # Convert CriteriaAdvanced objects to dictionaries
        criteria_dicts = []
        for c in criteria:
            criteria_dicts.append({
                "field": c.field,
                "operator": c.operator,
                "value": c.value
            })
        
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
            
            data = response.get('data', {})
            return TableDoc(self.name, doc_id, data, self.db)
        except Exception as e:
            raise Exception(f"Something went wrong with get_doc operation: {str(e)}")
