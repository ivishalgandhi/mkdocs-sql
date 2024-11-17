import sqlite3
import duckdb
import os
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import re
import pandas as pd
from tabulate import tabulate

class SQLPlugin(BasePlugin):
    config_scheme = (
        ('database', config_options.Type(dict, default={
            'type': 'sqlite',
            'path': None
        })),
    )

    def __init__(self):
        self.db_connection = None

    def on_page_markdown(self, markdown, page, config, files):
        db_config = self.config['database']
        if not db_config.get('path'):
            return markdown

        def replace_sql_block(match):
            sql_query = match.group(1)
            try:
                if not self.db_connection:
                    if db_config['type'] == 'duckdb':
                        self.db_connection = duckdb.connect(db_config['path'])
                    else:
                        self.db_connection = sqlite3.connect(db_config['path'])
                
                df = pd.read_sql_query(sql_query, self.db_connection)
                result_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=False)
                
                return f"```sql\n{sql_query}\n```\n\n**Results:**\n\n{result_table}\n"
            except Exception as e:
                return f"```sql\n{sql_query}\n```\n\n**Error:**\n\n```\n{str(e)}\n```\n"

        pattern = r"```sql\n(.*?)\n```"
        return re.sub(pattern, replace_sql_block, markdown, flags=re.DOTALL)

    def on_post_build(self, config):
        if self.db_connection:
            self.db_connection.close()
