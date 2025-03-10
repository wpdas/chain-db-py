"""Utility functions for the ChainDB Python client."""

import json
import requests
from typing import Dict, Any, Optional

def post(url: str, body: Dict[str, Any], auth: str = '') -> Dict[str, Any]:
    """
    Make a POST request to the ChainDB API.
    
    Args:
        url: URL to make the request to.
        body: Request body.
        auth: Optional authentication token.
    
    Returns:
        Response from the server.
    
    Raises:
        Exception: If the request fails.
    """
    headers = {
        'Content-Type': 'application/json'
    }
    
    if auth:
        headers['Authorization'] = f'Basic {auth}'
    
    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()

def get(url: str, auth: str = '') -> Dict[str, Any]:
    """
    Make a GET request to the ChainDB API.
    
    Args:
        url: URL to make the request to.
        auth: Optional authentication token.
    
    Returns:
        Response from the server.
    
    Raises:
        Exception: If the request fails.
    """
    headers = {}
    
    if auth:
        headers['Authorization'] = f'Basic {auth}'
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()
