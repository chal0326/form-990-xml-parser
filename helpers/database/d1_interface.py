import json
import requests
import os
import sys
from settings.Settings import (
    cloudflare_account_id,
    cloudflare_api_token,
    cloudflare_d1_database_id
)
from helpers.loggingutil import Log_Details, log_error, log_progress

class D1Interface:
    _table_initialized = False

    def __init__(self):
        self.account_id = cloudflare_account_id
        self.database_id = cloudflare_d1_database_id
        self.api_token = cloudflare_api_token
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.database_id}/query"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

        # Verify connection/create table if needed
        if not D1Interface._table_initialized:
            self.initialize_table()
            D1Interface._table_initialized = True

    def query(self, sql, params=None):
        """Execute a SQL query against D1"""
        payload = {
            "sql": sql,
            "params": params or []
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log_error(e, f"D1 Query Failed: {sql}", Log_Details)
            return None

    def initialize_table(self):
        """Ensure the forms table exists"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS forms (
            ein TEXT,
            tax_year TEXT,
            form_type TEXT,
            data TEXT,
            PRIMARY KEY (ein, tax_year)
        );
        """
        self.query(create_table_sql)

    def form_exists(self, ein, tax_year):
        """Check if a form exists"""
        sql = "SELECT 1 FROM forms WHERE ein = ? AND tax_year = ?"
        result = self.query(sql, [ein, tax_year])

        if result and result.get('success') and result.get('result'):
             # Cloudflare D1 API response structure: { "success": true, "result": [ { "results": [ ... ] } ] }
             # We need to check if the query returned any rows
             rows = result['result'][0]['results']
             return len(rows) > 0
        return False

    def insert_form(self, all_data, schedules, form_type):
        """Insert form data into D1"""
        ein = all_data.get('FILEREIN')
        tax_year = all_data.get('TAXYEAR')

        # Embed schedules into all_data for storage as a single blob
        data_to_store = all_data.copy()
        data_to_store['schedules_data'] = schedules

        json_data = json.dumps(data_to_store)

        sql = "INSERT OR REPLACE INTO forms (ein, tax_year, form_type, data) VALUES (?, ?, ?, ?)"
        result = self.query(sql, [ein, tax_year, form_type, json_data])

        if result and result.get('success'):
            log_progress('', f"Successfully inserted/updated form for EIN: {ein} in D1", Log_Details)
            return True
        else:
            log_error(None, f"Failed to insert form for EIN: {ein} in D1", Log_Details)
            return False

    def delete_form(self, ein, tax_year):
         """Delete a form from D1"""
         sql = "DELETE FROM forms WHERE ein = ? AND tax_year = ?"
         self.query(sql, [ein, tax_year])
