import requests
import json
import logging
from typing import Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class APIClient:
    def __init__(self, base_url: str, timeout: int = 30, retry_count: int = 3):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Setup retry strategy
        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"GET request to: {url}")
        
        response = self.session.get(url, params=params, timeout=self.timeout)
        self.logger.info(f"Response status: {response.status_code}")
        return response
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"POST request to: {url}")
        
        response = self.session.post(url, data=data, json=json_data, timeout=self.timeout)
        self.logger.info(f"Response status: {response.status_code}")
        return response
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"PUT request to: {url}")
        
        response = self.session.put(url, data=data, json=json_data, timeout=self.timeout)
        self.logger.info(f"Response status: {response.status_code}")
        return response
    
    def delete(self, endpoint: str) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"DELETE request to: {url}")
        
        response = self.session.delete(url, timeout=self.timeout)
        self.logger.info(f"Response status: {response.status_code}")
        return response