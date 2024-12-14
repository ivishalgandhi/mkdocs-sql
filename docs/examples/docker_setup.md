# Setting up SQL Server with Docker

This guide walks through the process of setting up SQL Server in Docker and restoring the AdventureWorks database.

## Check Running Containers

To see your running SQL Server container:

```bash
docker ps
```

Example output:
```
CONTAINER ID   IMAGE                                        COMMAND                  CREATED          STATUS          PORTS                                       NAMES
eb66ab04c6f6   mcr.microsoft.com/mssql/server:2022-latest   "/opt/mssql/bin/perm…"   13 minutes ago   Up 13 minutes   0.0.0.0:1433->1433/tcp, :::1433->1433/tcp   sql2022
```

## Create Backup Directory

Create a directory in the container for storing backup files:

```bash
docker exec sql2022 mkdir -p /var/opt/mssql/backup
```

## Copy Files to Container

Copy the backup and restore script files to the container:

```bash
# Copy the AdventureWorks backup file
docker cp /Users/vishal/Downloads/AdventureWorks2022.bak sql2022:/var/opt/mssql/backup/

# Copy the restore script
docker cp /Users/vishal/dev/mkdocs-sql/docs/examples/restore_adventureworks.sql sql2022:/var/opt/mssql/backup/
```

## Restore Database

Execute the restore script using sqlcmd:

```bash
docker exec sql2022 /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P Password@123 -i /var/opt/mssql/backup/restore_adventureworks.sql -C -N
```

Note the flags:
- `-S`: Server name
- `-U`: Username
- `-P`: Password
- `-i`: Input file
- `-C`: Trust server certificate
- `-N`: Remove numbering in the output

Expected output:
```
Changed database context to 'master'.
5 percent processed.
...
100 percent processed.
Processed 25376 pages for database 'AdventureWorks2022', file 'AdventureWorks2022' on file 1.
Processed 2 pages for database 'AdventureWorks2022', file 'AdventureWorks2022_log' on file 1.
RESTORE DATABASE successfully processed 25378 pages in 0.873 seconds (227.103 MB/sec).
```

## Verify Database Restore

You can verify the database restore by running a simple query:

```bash
docker exec sql2022 /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P Password@123 -Q "SELECT DB_NAME()" -C -N
```

Expected output should include 'AdventureWorks2022'.

## Connection String for mkdocs-sql

After setting up the database, configure your `mkdocs.yml` to connect to it:

```yaml
plugins:
  - sql:
      databases:
        adventureworks:
          type: mssql
          server: localhost
          database: AdventureWorks2022
          username: sa
          password: ${MSSQL_PASSWORD}  # Use environment variable
          trust_server_certificate: yes
```

## Troubleshooting

1. If you see SSL/certificate errors, make sure to include the `-C` flag for sqlcmd or `trust_server_certificate: yes` in your connection string.
2. If the restore fails, check:
   - Sufficient disk space
   - Correct file paths
   - SQL Server permissions
3. For connection issues, verify:
   - Container is running (`docker ps`)
   - Port mapping is correct (1433)
   - Credentials are correct
