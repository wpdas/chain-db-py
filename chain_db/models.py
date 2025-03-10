"""Model classes for the ChainDB Python client.

These classes provide base models that can be extended by users to get proper type hints.
"""

from typing import Dict, List, Any, Optional, TypeVar, Generic, Union, ForwardRef

# Type variable for generic models
T = TypeVar('T')

# Forward reference for TableDocModel
TableDocModelRef = ForwardRef('TableDocModel')

class TableModel:
    """
    Base model class for tables in ChainDB.
    
    Users can extend this class to create their own table models with proper type hints.
    The actual implementation of these methods is provided by the ChainDB library at runtime.
    """
    
    def __init__(self):
        """Initialize a table model."""
        self.current_doc: Dict[str, Any] = {}
        self.name: str = ""
    
    async def persist(self) -> Dict[str, Any]:
        """
        Persist the current document to the database.
        
        Returns:
            The persisted document with its doc_id.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    def get_current_doc_id(self) -> Optional[str]:
        """
        Get the ID of the current document.
        
        Returns:
            The document ID, or None if there is no current document.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    async def get_history(self, limit: int) -> List[Dict[str, Any]]:
        """
        Get the history of changes to the table.
        
        Args:
            limit: Maximum number of history entries to return.
            
        Returns:
            List of historical documents.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    async def refetch(self) -> None:
        """
        Refetch the table data from the database.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    def is_empty(self) -> bool:
        """
        Check if the table is empty.
        
        Returns:
            True if the table is empty, False otherwise.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    def get_name(self) -> str:
        """
        Get the name of the table.
        
        Returns:
            The table name.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    async def find_where(self, criteria: Dict[str, Any], limit: int = 1000, reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Find documents matching the given criteria.
        
        Args:
            criteria: Dictionary of field-value pairs to match.
            limit: Maximum number of documents to return.
            reverse: Whether to return documents in reverse order.
            
        Returns:
            List of matching documents.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    async def find_where_advanced(self, criteria: List[Any], limit: int = 1000, reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Find documents matching the given advanced criteria.
        
        Args:
            criteria: List of CriteriaAdvanced objects.
            limit: Maximum number of documents to return.
            reverse: Whether to return documents in reverse order.
            
        Returns:
            List of matching documents.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    async def get_doc(self, doc_id: str) -> TableDocModelRef:
        """
        Get a specific document by its ID.
        
        Args:
            doc_id: The document ID.
            
        Returns:
            TableDoc instance for the document.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")


class TableDocModel:
    """
    Base model class for table documents in ChainDB.
    
    Users can extend this class to create their own table document models with proper type hints.
    The actual implementation of these methods is provided by the ChainDB library at runtime.
    """
    
    def __init__(self):
        """Initialize a table document model."""
        self.doc: Dict[str, Any] = {}
        self.doc_id: str = ""
    
    async def update(self) -> Dict[str, Any]:
        """
        Update the document in the database.
        
        Returns:
            The updated document.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    async def refetch(self) -> None:
        """
        Refetch the document data from the database.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
    
    def get_table_name(self) -> str:
        """
        Get the name of the table this document belongs to.
        
        Returns:
            The table name.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")
        
    def is_empty(self) -> bool:
        """
        Check if the document is empty.
        
        Returns:
            True if the document is empty, False otherwise.
        """
        raise NotImplementedError("This method is implemented by ChainDB at runtime")

# Resolve forward reference
TableModel.__annotations__['get_doc'] = 'TableDocModel' 