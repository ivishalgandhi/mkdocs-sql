# mkdocs-sql

A MkDocs plugin for executing and displaying SQL queries in your documentation.

## Features

- Embed output SQL queries in your markdown files
- Support for SQLite databases
- Display results as formatted tables
- Error handling and display
- Database configuration via mkdocs.yml

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

## Configuration

| Option | Description | Default |
|--------|-------------|---------|
| databasePath.type | Database type (currently only sqlite) | sqlite |
| databasePath.path | Path to database file | None |
| showQuery | Show SQL queries by default | true |

## License

MIT
