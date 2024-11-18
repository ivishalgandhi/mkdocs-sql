import sqlite3
import duckdb
import os
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
import re
import pandas as pd
from tabulate import tabulate
import yaml

class SQLPlugin(BasePlugin):
    config_scheme = (
        ('database', config_options.Type(dict, default={
            'type': 'sqlite',
            'path': None
        })),
        ('databasePath', config_options.Type(dict, default={
            'type': 'sqlite',
            'path': None
        })),
        ('show_query', config_options.Type(bool, default=True)),
        ('showQuery', config_options.Type(bool, default=True)),
    )

    def __init__(self):
        self.db_connection = None
        self.current_db_path = None

    def on_config(self, config):
        """Add SQL toggle assets to the config"""
        if 'extra_css' not in config:
            config['extra_css'] = []
        if 'extra_javascript' not in config:
            config['extra_javascript'] = []
        
        config['extra_css'].append('stylesheets/sql-toggle.css')
        config['extra_javascript'].append('javascripts/sql-toggle.js')
        return config

    def on_page_markdown(self, markdown, page, config, files):
        db_config = self.config.get('databasePath', self.config['database']).copy()
        show_query = self.config.get('showQuery', self.config['show_query'])  # default from config

        # Check for frontmatter
        if markdown.startswith('---'):
            try:
                # Find the end of frontmatter
                end_pos = markdown.find('---', 3)
                if end_pos != -1:
                    frontmatter = yaml.safe_load(markdown[3:end_pos])
                    # Override showQuery if specified in frontmatter
                    if 'showQuery' in frontmatter:
                        show_query = frontmatter['showQuery']
                    elif 'show_query' in frontmatter:  # backwards compatibility
                        show_query = frontmatter['show_query']
                    # Override database path if specified in frontmatter
                    if 'databasePath' in frontmatter:
                        db_path = frontmatter['databasePath']
                    elif 'database' in frontmatter:  # backwards compatibility
                        db_path = frontmatter['database']
                    # Handle ~ in path
                    if db_path.startswith('~'):
                        db_path = os.path.expanduser(db_path)
                    # Handle relative paths
                    if not os.path.isabs(db_path):
                        # Make path relative to the markdown file's directory
                        db_path = os.path.join(os.path.dirname(page.file.abs_src_path), db_path)
                    db_config['path'] = db_path
            except yaml.YAMLError:
                pass

        if not db_config.get('path'):
            return markdown

        def replace_sql_block(match):
            sql_query = match.group(1)
            try:
                # Check if we need to create a new connection
                db_path = db_config['path']
                if self.current_db_path != db_path:
                    if self.db_connection:
                        self.db_connection.close()
                    if db_config['type'] == 'duckdb':
                        self.db_connection = duckdb.connect(db_path)
                    else:
                        self.db_connection = sqlite3.connect(db_path)
                    self.current_db_path = db_path
                
                df = pd.read_sql_query(sql_query, self.db_connection)
                
                # Detect numeric columns including those with _population, _km2, _usd suffixes
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
                                # Format large numbers with commas
                                df[col] = df[col].apply(lambda x: '{:,.0f}'.format(x) if pd.notnull(x) else '')
                            else:
                                df[col] = df[col].round(2)

                # Generate HTML table with proper classes for alignment
                html_table = '<table>\n'
                
                # Headers
                html_table += '<thead>\n<tr>\n'
                for col in df.columns:
                    # Convert column names to title case and replace underscores
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
                        # Handle null values
                        if pd.isnull(val):
                            val = ''
                        html_table += f'<td class="{align_class}">{val}</td>\n'
                    html_table += '</tr>\n'
                html_table += '</tbody>\n</table>'

                # Generate raw markdown table for copy/paste
                raw_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=False)
                
                # Return the complete HTML structure
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
                error_msg = f"```\n{str(e)}\n```\n"
                return (
                    '<div class="sql-wrapper">\n'
                    '<div class="sql-controls">\n'
                    '<button class="sql-toggle" title="Toggle SQL Query"><span class="material-icons">code</span></button>\n'
                    '</div>\n'
                    f'<div class="sql-query" style="display: none;">\n'
                    f'```sql\n{sql_query}\n```\n'
                    '</div>\n'
                    f'**Error:** {error_msg}\n'
                    '</div>'
                )

        pattern = r"```sql\n(.*?)\n```"
        return re.sub(pattern, replace_sql_block, markdown, flags=re.DOTALL)

    def on_post_build(self, config):
        if self.db_connection:
            self.db_connection.close()
