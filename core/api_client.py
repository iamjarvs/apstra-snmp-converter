"""
API client for Apstra AAA and tasks endpoints.
Handles authentication, polling, and token refresh.
"""
import requests
from typing import Dict, Any, Optional

class ApstraAPIClient:
    def __init__(self, host: str, username: str, password: str, timeout: int = 10):
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.token = None

    def login(self) -> bool:
        url = f"https://{self.host}/api/aaa/login"
        resp = requests.post(url, json={"username": self.username, "password": self.password}, timeout=self.timeout)
        if resp.status_code == 200 and 'token' in resp.json():
            self.token = resp.json()['token']
            return True
        return False

    def get_tasks(self, blueprint_id: str) -> Optional[Dict[str, Any]]:
        if not self.token:
            if not self.login():
                return None
        url = f"https://{self.host}/api/blueprints/{blueprint_id}/tasks"
        headers = {"AUTHTOKEN": self.token}
        resp = requests.get(url, headers=headers, timeout=self.timeout)
        if resp.status_code == 200:
            return resp.json()
        return None
