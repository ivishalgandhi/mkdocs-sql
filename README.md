# mkdocs-sql

A MkDocs plugin for executing and embedding output of SQL queries in your documentation.

## Features

- Embed output of SQL queries in your markdown files
- Support for SQLite databases
- Display results as formatted tables
- Error handling and display
- Database configuration via mkdocs.yml
- Live updates - changes to database reflect immediately in documentation
- Toggle SQL queries on/off
- Toggle between formatted and raw markdown views

## Installation

```bash
pip install mkdocs-sql
```

## Usage

1. Add to mkdocs.yml:
```yaml
plugins:
  - sql:
      databasePath:
        type: sqlite
        path: ./path/to/database.file
```

2. In your markdown files:
```markdown
---
databasePath: ./relative/path/to/database.file
showQuery: true  # optional, defaults to true
---

```sql
SELECT * FROM users LIMIT 5;
```
```

## Example Database Management

The plugin comes with a sample population database and management script. You can use it to test live updates:

```bash
# Reset database to initial state
python docs/examples/create_sample_db.py --reset

# Update a city's population (±10% random change)
python docs/examples/create_sample_db.py --update-city "New York"

# Update a country's population (±5% random change)
python docs/examples/create_sample_db.py --update-country "United States"
```

Changes to the database are reflected immediately in the documentation - just refresh the page!

## Configuration

| Option | Description | Default |
|--------|-------------|---------|
| databasePath.type | Database type (currently only sqlite) | sqlite |
| databasePath.path | Path to database file | None |
| showQuery | Show SQL queries by default | true |

## License

MIT
