"""Basic example of using the ChainDB Python client."""

import asyncio
from chain_db import connect, Connection, EventTypes, TableModel
from typing import Dict, Any

# Define a class for your table structure by extending TableModel
class GreetingTable(TableModel):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self.greeting = "Hi"  # Add custom properties

async def main():
    # Connect to ChainDB
    connection = Connection(
        server="http://localhost:2818",
        database="test-db",
        user="root",
        password="1234"
    )
    db = await connect(connection)
    
    # Get a table with type casting using the model class
    greeting_table = await db.get_table("greeting", GreetingTable)
    print(f"Current document: {greeting_table.current_doc}")
    
    # Subscribe to table update events
    async def on_table_update(event_data):
        if event_data.table == "greeting":
            print(f"Greeting table updated: {event_data.data}")
    
    await db.events().subscribe(EventTypes.TABLE_UPDATE, on_table_update)
    
    # Modify and persist data
    greeting_table.current_doc["greeting"] = "Hello, ChainDB from Python!"
    result = await greeting_table.persist()
    
    # Get the doc_id of the newly created document
    print(f"New document ID: {result.get('doc_id')}")
    
    # You can also get the current document ID directly
    current_doc_id = greeting_table.get_current_doc_id()
    print(f"Current document ID: {current_doc_id}")
    
    # Get a specific document by its ID
    # We can use the ID we just got from the persist operation
    specific_doc = await greeting_table.get_doc(current_doc_id)
    
    # Access the document data and ID
    print(f"Specific document: {specific_doc.doc}")
    print(f"Specific document ID: {specific_doc.doc_id}")
    
    # Update a specific document
    specific_doc.doc["greeting"] = "Updated specific document"
    await specific_doc.update()
    
    # Get the last 10 changes
    history = await greeting_table.get_history(10)
    print(f"History: {history}")

if __name__ == "__main__":
    asyncio.run(main())
