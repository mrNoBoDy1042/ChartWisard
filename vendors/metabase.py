import requests
import base64
import json

from db import schemas


class MetabaseAPI:    
    def __init__(self, user: schemas.User = None):
        self.access_token = user.access_token
        self.refresh_token = user.refresh_token
        self.url = user.metabase_url
        return super().__init__()

    def build_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-Metabase-Session': self.access_token
        }
    
    @staticmethod
    def authorize(email: str, password: str, url: str) -> str:
        resp = requests.post(
            f'{url}/api/session',
            json={
                "username": email,
                "password": password,
            }
        )
        return resp.json()['id']

    def get_databases(self):
        resp = requests.get(
            f'{self.metabase_url}/api/database/',
            headers=self.build_headers()
        )
        return [
            {'id': item['id'], 'name': item['name']}
            for item in resp.json()['data']
        ]

    def get_database_schema(self, database_id: int):
        resp = requests.get(
            f'{self.metabase_url}/api/database/schema{database_id}?include=tables.fields',
            headers=self.build_headers()
        )
        
        tables_info = resp.json()['tables']
        parsed_schema = {
            table['name']: [
                field['name']
                for field in table['fields']
            ]
            for table in tables_info
        }
        return parsed_schema
    
    def get_query_url(self, database_id: int, sql_query: str):
        metabase_query = {
            'dataset_query':{
                'database': database_id,
                'native':
                    {
                        'query': sql_query,
                        'template-tags': {}
                    },
                'type':'native'
            },
            'display':'table',
            'visualization_settings':{}
        }
        encoded_query = base64.b64encode(json.dumps(metabase_query).encode()).decode()
        return f'{self.metabase_url}/question#{encoded_query}'

    def run_query(self, database_id: int, sql_query: str):
        metabase_query = {
            'database': database_id,
            'native': {
                    'query': sql_query.replace('\n', ' '),
                    'template-tags': {}
            },
            'type': 'native',
            'middleware': {
                'js-int-to-string?': True,
                'add-default-userland-constraints?': True
            }
        }

        response = requests.post(
            'https://metabase.amazinghiring.com/api/dataset/',
            headers=self.build_headers(),
            json=metabase_query,
        )
        return response.json()