"""TableDoc class for the ChainDB Python client."""

from typing import Dict, Any, TypeVar, Generic, Optional
from .constants import UPDATE_ITEM, GET_DOC
from .utils import post, get

# Forward reference for ChainDB
ChainDB = TypeVar('ChainDB')

# Type variable for generic models
T = TypeVar('T')

class TableDoc(Generic[T]):
    """
    Represents a specific document from a table.
    Contains only the necessary methods to work with a specific document.
    """
    
    def __init__(self, table_name: str, doc_id: str, data: Dict[str, Any], db: ChainDB):
        """
        Initialize a TableDoc.
        
        Args:
            table_name: Name of the table.
            doc_id: ID of the document.
            data: Document data.
            db: ChainDB instance.
        """
        self.table_name = table_name
        self.doc_id = doc_id
        self.doc = data
        self.db = db
    
    async def update(self) -> None:
        """
        Update the document data.
        This will update the specific document without creating a new one.
        
        Raises:
            Exception: If the update fails.
        """
        url = f"{self.db.server}{UPDATE_ITEM(self.table_name)}"
        
        body = {
            "data": self.doc,
            "doc_id": self.doc_id
        }
        
        try:
            response = post(url, body, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
        except Exception as e:
            raise Exception(f"Something went wrong updating document {self.doc_id}: {str(e)}")
    
    async def refetch(self) -> None:
        """
        Refetch the document data from the database.
        Useful when the document might have been updated by another application.
        
        Raises:
            Exception: If the refetch fails.
        """
        url = f"{self.db.server}{GET_DOC(self.table_name, self.doc_id)}"
        
        try:
            response = get(url, self.db.auth)
            
            if not response.get('success'):
                raise Exception(response.get('message', 'Unknown error'))
            
            # Update the document data with the latest data from the database
            self.doc = response.get('data', {})
        except Exception as e:
            raise Exception(f"Something went wrong refetching document {self.doc_id}: {str(e)}")
    
    def get_table_name(self) -> str:
        """
        Get the table name this document belongs to.
        
        Returns:
            Table name.
        """
        return self.table_name
    
    def is_empty(self) -> bool:
        """
        Check if the document is empty.
        
        Returns:
            True if the document is empty, False otherwise.
        """
        return not bool(self.doc)
