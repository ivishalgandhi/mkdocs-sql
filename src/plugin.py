import sqlite3
import duckdb
import os
import pyodbc
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import re
import pandas as pd
from tabulate import tabulate
import yaml
from typing import Dict, Any, Optional

class DatabaseConnection:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self.type = config.get('type', 'sqlite')
        
    def connect(self) -> None:
        """Establish database connection based on configuration."""
        if self.connection:
            return

        if self.type == 'mssql':
            self.connection = self._connect_mssql()
        elif self.type == 'duckdb':
            self.connection = duckdb.connect(self.config['path'])
        else:  # sqlite
            self.connection = sqlite3.connect(self.config['path'])

    def _connect_mssql(self):
        """Create a connection to SQL Server."""
        params = {
            'Driver': self.config.get('driver', 'ODBC Driver 18 for SQL Server'),
            'Server': self.config['server'],
            'Database': self.config['database'],
        }
        
        if 'trusted_connection' in self.config:
            params['Trusted_Connection'] = 'yes'
        else:
            params['Uid'] = self.config.get('username')
            # Get password from environment variable if it starts with ${
            pwd = self.config.get('password', '')
            if isinstance(pwd, str) and pwd.startswith('${') and pwd.endswith('}'):
                env_var = pwd[2:-1]  # Remove ${ and }
                pwd = os.environ.get(env_var, '')
            params['Pwd'] = pwd
        
        # Handle boolean parameters that need to be 'yes' or 'no'
        param_mapping = {
            'encrypt': 'Encrypt',
            'trust_server_certificate': 'TrustServerCertificate'
        }
        
        for config_key, param_key in param_mapping.items():
            if config_key in self.config:
                params[param_key] = 'yes' if self.config[config_key] else 'no'
        
        # Handle other parameters
        if 'port' in self.config:
            params['Port'] = self.config['port']
        
        conn_str = ';'.join(f"{k}={v}" for k, v in params.items() if v is not None)
        print(f"Connection string (with password masked): {conn_str.replace(params.get('Pwd', ''), '***')}")
        return pyodbc.connect(conn_str)

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame."""
        self.connect()
        return pd.read_sql_query(query, self.connection)

    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

class SQLPlugin(BasePlugin):
    config_scheme = (
        ('databases', config_options.Type(dict, default={})),
        ('show_query', config_options.Type(bool, default=True)),
    )

    def __init__(self):
        self.connections: Dict[str, DatabaseConnection] = {}

    def on_config(self, config):
        """Initialize database configurations."""
        if 'extra_css' not in config:
            config['extra_css'] = []
        if 'extra_javascript' not in config:
            config['extra_javascript'] = []
        
        config['extra_css'].append('stylesheets/sql-toggle.css')
        config['extra_javascript'].append('javascripts/sql-toggle.js')
        return config

    def on_page_markdown(self, markdown, page, config, files):
        """Process SQL blocks in markdown."""
        show_query = self.config.get('show_query', True)
        db_configs = self.config.get('databases', {}).copy()

        # Parse frontmatter for database configs and show_query setting
        if markdown.startswith('---'):
            try:
                end_pos = markdown.find('---', 3)
                if end_pos != -1:
                    frontmatter = yaml.safe_load(markdown[3:end_pos])
                    if 'show_query' in frontmatter:
                        show_query = frontmatter['show_query']
                    if 'databases' in frontmatter:
                        db_configs.update(frontmatter['databases'])
            except yaml.YAMLError:
                pass

        def replace_sql_block(match):
            sql_query = match.group(2)  # SQL query is now in group 2
            db_name = match.group(1) if match.group(1) else 'default'
            
            try:
                if db_name not in db_configs:
                    raise ValueError(f"Database configuration '{db_name}' not found")

                if db_name not in self.connections:
                    self.connections[db_name] = DatabaseConnection(db_configs[db_name])
                
                df = self.connections[db_name].execute_query(sql_query)
                
                # Format numeric columns
                numeric_patterns = ['_population$', '_km2$', '_usd$', 'percentage$', 'density', 'gdp', 'area']
                numeric_cols = set()
                
                # Add columns that match numeric patterns
                for col in df.columns:
                    if any(col.lower().endswith(pattern) or pattern in col.lower() for pattern in numeric_patterns):
                        numeric_cols.add(col)
                
                # Add columns that are actually numeric
                numeric_cols.update(df.select_dtypes(include=['float64', 'int64']).columns)
                
                # Format numeric values
                for col in numeric_cols:
                    if col in df.columns:
                        if df[col].dtype in ['float64', 'int64']:
                            if any(pattern in col.lower() for pattern in ['percentage', 'density']):
                                df[col] = df[col].round(2)
                            elif any(pattern in col.lower() for pattern in ['population', 'gdp', 'area']):
                                df[col] = df[col].apply(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else '')
                            else:
                                df[col] = df[col].round(2)

                # Generate HTML table
                html_table = '<table>\n'
                
                # Headers
                html_table += '<thead>\n<tr>\n'
                for col in df.columns:
                    header = col.replace('_', ' ').title()
                    align_class = 'align-right' if col in numeric_cols else 'align-left'
                    html_table += f'<th class="{align_class}">{header}</th>\n'
                html_table += '</tr>\n</thead>\n'
                
                # Body
                html_table += '<tbody>\n'
                for _, row in df.iterrows():
                    html_table += '<tr>\n'
                    for col, val in row.items():
                        align_class = 'align-right' if col in numeric_cols else 'align-left'
                        val = '' if pd.isnull(val) else val
                        html_table += f'<td class="{align_class}">{val}</td>\n'
                    html_table += '</tr>\n'
                html_table += '</tbody>\n</table>'

                # Generate raw markdown table
                raw_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=False)
                
                return (
                    '<div class="sql-wrapper">\n'
                    '<div class="sql-controls">\n'
                    '<button class="sql-toggle" title="Toggle SQL Query"><span class="material-icons">code</span></button>\n'
                    '<button class="table-toggle" title="Toggle Table View"><span class="material-icons">grid_on</span></button>\n'
                    '</div>\n'
                    f'<div class="sql-query" style="display: none;">\n'
                    f'```sql\n{sql_query}\n```\n'
                    '</div>\n'
                    f'<div class="table-wrapper">\n'
                    f'<div class="formatted-table">{html_table}</div>\n'
                    f'<div class="raw-table" style="display: none;">\n'
                    f'```\n{raw_table}\n```\n'
                    '</div>\n'
                    '</div>\n'
                    '</div>'
                )
            except Exception as e:
                return (
                    '<div class="sql-wrapper">\n'
                    '<div class="sql-controls">\n'
                    '<button class="sql-toggle" title="Toggle SQL Query"><span class="material-icons">code</span></button>\n'
                    '</div>\n'
                    f'<div class="sql-query" style="display: none;">\n'
                    f'```sql\n{sql_query}\n```\n'
                    '</div>\n'
                    f'**Error:** ```\n{str(e)}\n```\n'
                    '</div>'
                )

        # Updated regex pattern to capture optional database name
        pattern = r'```sql(?:\[(.*?)\])?\n(.*?)\n```'
        return re.sub(pattern, replace_sql_block, markdown, flags=re.DOTALL)

    def on_post_build(self, config):
        """Clean up database connections."""
        for connection in self.connections.values():
            connection.close()
