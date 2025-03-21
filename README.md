# Chain DB Python Client

A Python client for [Chain DB](https://github.com/wpdas/chain-db), a secure database system with built-in history tracking, offering AES-256-GCM encryption, atomic operations with rollback capability, and automatic backups.

## Installation

```bash
pip install chain-db
```

Or install from source:

```bash
git clone https://github.com/wpdas/chain-db-py.git
cd chain-db-py
pip install -e .
```

## Usage

### Connecting to Chain DB

```python
import asyncio
from chain_db import connect, Connection

async def main():
    # Connect to Chain DB
    connection = Connection(
        server="http://localhost:2818",  # If None, "http://localhost:2818" will be used as default
        database="my-database",
        user="root",
        password="1234"
    )
    db = await connect(connection)

asyncio.run(main())
```

### Working with Tables

```python
# Get a table instance
# If the table already exists in the chain, its data will be loaded
greeting_table = await db.get_table("greeting")

# Access the current document data (the last record stored in the table)
print(greeting_table.current_doc)  # e.g., {"greeting": "Hello"}
```

### Using Type Hints with Model Classes (as schemas)

You can define model classes (as schemas) to get better type hints and IDE support. Chain DB provides base model classes that you can extend:

```python
from chain_db import TableModel, connect, Connection

# Define a model class/schema by extending TableModel
class GreetingTable(TableModel):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self.greeting = "Hi"  # Add custom properties

# Connect to Chain DB
connection = Connection(
    server="http://localhost:2818",
    database="my-database",
    user="root",
    password="1234"
)
db = await connect(connection)

# Get a table with type casting using the model class (serves as a schema for the table also)
greeting_table = await db.get_table("greeting", GreetingTable)

# Now your IDE will provide autocompletion and type checking
print(greeting_table.current_doc)
greeting_table.current_doc["greeting"] = "Hello, Chain DB!"
result = await greeting_table.persist()
```

By extending `TableModel`, your class automatically inherits all the method signatures from the Chain DB library, providing proper type hints for all available methods.

### Modifying and Persisting Data

```python
# Modify the current document data
greeting_table.current_doc["greeting"] = "Hello, Chain DB!"

# Persist changes to database (creates a new record with a new doc_id)
result = await greeting_table.persist()

# The persist method returns the created document with its doc_id
print(result.get("doc_id"))  # e.g., "550e8400-e29b-41d4-a716-446655440000"

# You can also access the current document's ID directly
current_doc_id = greeting_table.get_current_doc_id()
print(current_doc_id)  # Same as result.get("doc_id")
```

### Getting a Specific Document

```python
# Get a specific document by its ID (assuming we know a document ID)
# The document ID is generated by ChainDB when data is persisted
doc_id = "550e8400-e29b-41d4-a716-446655440000"  # Example ID
specific_doc = await greeting_table.get_doc(doc_id)

# Access the document data
print(specific_doc.doc)  # e.g., {"greeting": "Hello from specific doc", "doc_id": "550e8400-e29b-41d4-a716-446655440000"}

# The doc_id is also available directly in the document object
print(specific_doc.doc.get("doc_id"))  # "550e8400-e29b-41d4-a716-446655440000"

# It's also available as a property of the TableDoc instance
print(specific_doc.doc_id)  # "550e8400-e29b-41d4-a716-446655440000"

# Update the specific document
specific_doc.doc["greeting"] = "Updated greeting for specific doc"
await specific_doc.update()  # Updates only this specific document

# Refetch the document data if it might have been updated elsewhere
await specific_doc.refetch()
print(specific_doc.doc)  # Updated data from the database

# Get the table name this document belongs to
table_name = specific_doc.get_table_name()  # "greeting"
```

Note: The `TableDoc` class is a simplified version of a table that only allows working with a specific document. When you call `get_doc()` on a table, it returns a `TableDoc` instance that contains the document data and methods to update or refetch that specific document. This prevents accidental creation of duplicate records and makes the API more intuitive.

### Getting Table History

```python
# Get the last 100 changes to the table
history = await greeting_table.get_history(100)
print(history)
# Example output:
# [
#   {"greeting": "Hello, Chain DB!"},
#   {"greeting": "Hello"},
#   {"greeting": "Hi there"},
#   ...
# ]
```

### Real-time Events with WebSockets

Chain DB supports real-time updates through WebSockets. You can subscribe to table events to get notified when data changes:

```python
from chain_db import EventTypes

# Subscribe to table update events
async def on_table_update(event_data):
    print(f"Table updated: {event_data.table}")
    print(f"New data: {event_data.data}")

await db.events().subscribe(EventTypes.TABLE_UPDATE, on_table_update)

# Subscribe to new data persistence events
async def on_table_persist(event_data):
    print(f"New data added to table: {event_data.table}")
    print(f"Data: {event_data.data}")

await db.events().subscribe(EventTypes.TABLE_PERSIST, on_table_persist)

# Unsubscribe from an event
await db.events().unsubscribe(EventTypes.TABLE_UPDATE, on_table_update)

# Close WebSocket connection when done
await db.events().close_events()
```

The `EventData` object contains:

- `event_type`: The type of event (TableUpdate, TablePersist)
- `database`: The database name
- `table`: The table name
- `data`: The data associated with the event
- `timestamp`: When the event occurred

### Querying Data

#### Basic Queries

```python
# Find items with exact matches
users = await user_table.find_where(
    {"active": True, "name": "John"},  # criteria
    10,  # limit (default: 1000)
    True  # reverse order (default: True)
)
```

You can also use model classes with queries for better type hints:

```python
from chain_db import TableModel

# Define a model class/schema for your user table by extending TableModel
class UserTable(TableModel):
    def __init__(self):
        super().__init__()
        # Add custom properties if needed
        self.user_count = 0

# Get a table with type casting
user_table = await db.get_table("users", UserTable)

# Now your IDE will provide autocompletion and type checking for all methods
users = await user_table.find_where(
    {"active": True, "name": "John"},
    10,
    True
)
```

#### Advanced Queries

```python
from chain_db import Operators, CriteriaAdvanced

# Find items with advanced criteria
criteria = [
    CriteriaAdvanced(
        field="name",
        operator=Operators.CONTAINS,
        value="John"
    ),
    CriteriaAdvanced(
        field="age",
        operator=Operators.GREATER_THAN,
        value=25
    )
]

users = await user_table.find_where_advanced(
    criteria,
    10,  # limit
    True  # reverse order
)
```

Available operators:

- `EQUAL` (==)
- `NOT_EQUAL` (!=)
- `GREATER_THAN` (>)
- `GREATER_THAN_OR_EQUAL` (>=)
- `LESS_THAN` (<)
- `LESS_THAN_OR_EQUAL` (<=)
- `CONTAINS` (for strings and arrays)
- `STARTS_WITH` (for strings)
- `ENDS_WITH` (for strings)

### Other Table Methods

```python
# Check if a table is empty
is_empty = greeting_table.is_empty()

# Get the table name
table_name = greeting_table.get_name()

# Refetch the table data from the database
await greeting_table.refetch()
```

## Complete Example

```python
import asyncio
from chain_db import connect, Connection, EventTypes, TableModel

# Define a model class/schema for your table by extending TableModel
class GreetingTable(TableModel):
    def __init__(self):
        super().__init__()  # Initialize the base class
        self.greeting = "Hi"  # Add custom properties

async def main():
    # Connect to Chain DB
    connection = Connection(
        server="http://localhost:2818",
        database="test-db",
        user="root",
        password="1234"
    )
    db = await connect(connection)

    # Get the "greeting" table with type casting
    greeting_table = await db.get_table("greeting", GreetingTable)
    print(f"Current document: {greeting_table.current_doc}")  # e.g., {"greeting": "Hi"}

    # Subscribe to table update events
    async def on_table_update(event_data):
        if event_data.table == "greeting":
            print(f"Greeting table updated: {event_data.data}")

    await db.events().subscribe(EventTypes.TABLE_UPDATE, on_table_update)

    # Modify and persist data
    greeting_table.current_doc["greeting"] = "Hello my dear!"
    result = await greeting_table.persist()  # Data is persisted on database

    # Get the doc_id of the newly created document
    print(f"New document ID: {result.get('doc_id')}")

    # You can also get the current document ID directly
    current_doc_id = greeting_table.get_current_doc_id()
    print(f"Current document ID: {current_doc_id}")

    # See the updated values
    print(f"Updated document: {greeting_table.current_doc}")  # {"greeting": "Hello my dear!", "doc_id": "..."}

    # Get a specific document by its ID
    # We can use the ID we just got from the persist operation
    specific_doc = await greeting_table.get_doc(current_doc_id)

    # Access the document data and ID
    print(f"Specific document: {specific_doc.doc}")  # {"greeting": "Hello my dear!", "doc_id": "..."}
    print(f"Specific document ID: {specific_doc.doc_id}")  # Same as current_doc_id

    # Update a specific document
    specific_doc.doc["greeting"] = "Updated specific document"
    await specific_doc.update()  # Updates only this specific document

    # Refetch the document to get the latest data
    await specific_doc.refetch()
    print(f"Updated document: {specific_doc.doc}")  # Latest data from the database

    # Get the last 100 changes
    history = await greeting_table.get_history(100)
    print(f"History: {history}")
    # [
    #   {"greeting": "Updated specific document"},
    #   {"greeting": "Hello my dear!"},
    #   {"greeting": "Hi"},
    #   ...
    # ]

    # Close WebSocket connection when done
    await db.events().close_events()

if __name__ == "__main__":
    asyncio.run(main())
```

## Development

### Type Hints in Python

Chain DB Python client supports type hints through Python's typing system. This provides several benefits:

1. **Better IDE Support**: Your IDE can provide autocompletion, method suggestions, and parameter hints.
2. **Static Type Checking**: Tools like mypy can catch type errors before runtime.
3. **Self-documenting Code**: Type hints make your code more readable and self-documenting.

To use type hints with Chain DB:

1. Extend the provided base model classes (classes here are like the table schema):

```python
from chain_db import TableModel, TableDocModel

# For tables (table schema)
class UserTable(TableModel):
    def __init__(self):
        super().__init__()
        # Add custom properties
        self.user_count = 0

# For table documents
class UserDoc(TableDocModel):
    def __init__(self):
        super().__init__()
        # Add custom properties
        self.last_accessed = None
```

2. Pass your model class as the second parameter to `get_table`:

```python
# Get a table with type casting
user_table = await db.get_table("users", UserTable)
```

3. Now you can use your table with full type support:

```python
# Your IDE will provide autocompletion and type checking for all methods
user_table.current_doc["name"] = "John"
user_id = user_table.get_current_doc_id()
users = await user_table.find_where({"active": True})
```

The base model classes (`TableModel` and `TableDocModel`) provide type hints for all the methods available in the Chain DB library. At runtime, the actual implementation of these methods is provided by the library.

### Setup Development Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/wpdas/chain-db-py.git
   cd chain-db-py
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Running Tests

```bash
pytest
```

### Running with ChainDB Server

1. Make sure you have ChainDB server running on port 2818.
2. Run the example:
   ```bash
   python examples/basic_example.py
   ```

## License

MIT
