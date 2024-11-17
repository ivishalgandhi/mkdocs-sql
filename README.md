# mkdocs-sql

A MkDocs plugin for executing and displaying SQL queries in your documentation.

## Features

- Execute SQL queries directly in your markdown files
- Support for SQLite and DuckDB
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
      database:
        type: sqlite  # or duckdb
        path: ./path/to/database.file
```

2. In your markdown files:
```markdown
```sql
SELECT * FROM users LIMIT 5;
```
```

## Configuration

| Option | Description | Default |
|--------|-------------|---------|
| database.type | Database type (sqlite/duckdb) | sqlite |
| database.path | Path to database file | None |

## License

MIT
