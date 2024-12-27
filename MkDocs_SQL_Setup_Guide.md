# MkDocs-SQL Setup Guide

## Overview

`mkdocs-sql` is a plugin for MkDocs that allows you to execute SQL queries directly within your Markdown documentation. This guide will help you configure the [mkdocs.yml](cci:7://file:///Users/vishal/dev/mkdocs-sql/mkdocs.yml:0:0-0:0) file to use the plugin effectively.

## Prerequisites

1. **Python**: Ensure you have Python installed (version 3.9 or higher).
2. **MkDocs**: Install MkDocs if you haven't already:
   ```bash
   pip install mkdocs
   ```
3. **mkdocs-sql**: Install the `mkdocs-sql` plugin:
   ```bash
   pip install mkdocs-sql
   ```

## Configuring mkdocs.yml

### Step 1: Basic Structure

Open your [mkdocs.yml](cci:7://file:///Users/vishal/dev/mkdocs-sql/mkdocs.yml:0:0-0:0) file and set up the basic structure. Here’s an example:

```yaml
site_name: mkdocs-sql
theme:
  name: material
  features:
    - navigation.tabs
    - content.code.copy
    - content.code.select
  icon:
    admonition:
      note: material/table

plugins:
  - search
  - sql:
      databases:
        default:
          type: sqlite
          path: docs/examples/population.sqlite
        adventureworks:
          type: mssql
          driver: "ODBC Driver 18 for SQL Server"
          server: "sql2022,1433"  # Change to your server name
          database: AdventureWorks2022
          username: sa
          password: ${MSSQL_PASSWORD}  # Ensure this environment variable is set
      show_query: false  # Set to true to display SQL queries in the output

nav:
  - Home: examples/population.md
  - Examples:
      - Population Data: examples/population.md
      - Multiple Databases: examples/multiple_databases.md
      - AdventureWorks: examples/adventureworks.md
      - Docker Setup: examples/docker_setup.md
```

### Step 2: Configuring Database Connections

#### For SQLite

- **Path**: Ensure the path to your SQLite database is correct. Use forward slashes or double backslashes for Windows:
  ```yaml
  path: docs/examples/population.sqlite
  ```

#### For Microsoft SQL Server

- **Driver**: Specify the ODBC driver you are using. Ensure it is installed on your system.
- **Server**: Use the correct server name and port (e.g., `sql2022,1433`).
- **Password**: Use an environment variable for sensitive information:
  ```yaml
  password: ${MSSQL_PASSWORD}
  ```

### Important Note for Windows Users

If you are using Windows and do not require SSL encryption for your SQL Server connection, you can remove the following lines from your database configuration:

```yaml
    encrypt: true
    trust_server_certificate: true
```

This is particularly useful if you are connecting to a local SQL Server instance and want to avoid potential connection errors related to SSL certificates. Make sure your SQL Server is configured to accept non-encrypted connections if you choose to do this.

### Step 3: Environment Variable Setup

#### On Windows

1. Open PowerShell and set the environment variable:
   ```powershell
   [System.Environment]::SetEnvironmentVariable("MSSQL_PASSWORD", "your_password_here", "User")
   ```

#### On macOS

1. Open a terminal and set the environment variable:
   ```bash
   export MSSQL_PASSWORD="your_password_here"
   ```

### Step 4: Running MkDocs

After configuring your [mkdocs.yml](cci:7://file:///Users/vishal/dev/mkdocs-sql/mkdocs.yml:0:0-0:0), you can run the MkDocs server:

```bash
mkdocs serve
```

### Troubleshooting

- **Connection Issues**: If you encounter connection errors, ensure that:
  - The SQL Server is running and accessible.
  - The correct driver is installed and specified.
  - The environment variable for the password is set correctly.
  
- **Data Not Displaying**: If SQL queries are not executing, check:
  - The SQL syntax in your Markdown files.
  - Ensure that the `show_query` option is set correctly in the plugin configuration.

### Example SQL Queries in Markdown

You can include SQL queries in your Markdown files like this:

```markdown
```sql[default]
SELECT name, population, ROUND(CAST(gdp_usd AS FLOAT) / population, 2) as gdp_per_capita
FROM countries
ORDER BY population DESC
LIMIT 5;
```

```markdown
### Population Density Analysis

```sql[default]
SELECT 
    name,
    population,
    area_km2,
    ROUND(CAST(population AS FLOAT) / area_km2, 2) as density_per_km2
FROM countries 
ORDER BY density_per_km2 DESC
LIMIT 5;
```
```

### Conclusion

By following this guide, you should be able to configure [mkdocs.yml](cci:7://file:///Users/vishal/dev/mkdocs-sql/mkdocs.yml:0:0-0:0) for the `mkdocs-sql` plugin effectively on both Windows and macOS platforms. If you encounter any issues, refer to the troubleshooting section or consult the plugin documentation.
