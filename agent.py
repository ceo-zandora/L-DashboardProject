import os
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
import requests

load_dotenv()

SITE_ID = os.environ.get("SITE_ID")
DASHBOARD_DB_ID = os.environ.get("DASHBOARD_DB_ID")
# Microsoft Graph API endpoint for SharePoint sites
graph_sharepoint_url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}"

def __generateToken():
    # Azure AD app registration settings
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRECT")
    tenant_id = os.environ.get("TENANT_ID")

    # Initialize Confidential Client Application
    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}"
    )

    # Acquire a token for Microsoft Graph API
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    # Return access token
    return result.get('access_token')

# Construct the URL for the SharePoint site
sharepoint_url = graph_sharepoint_url.format(SITE_ID)

access_token = __generateToken()

# Headers with access token
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

def getData():
    try:
        # Make a GET request to read all list items
        response = requests.get(f"{sharepoint_url}/lists/{DASHBOARD_DB_ID}/items?expand=fields", headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            items = response.json().get('value')
            dashboard_details = []
            for item in items:
                d_key = item.get('fields', {}).get('KEY', '')
                d_value = item.get('fields', {}).get('VALUE', '')
                dashboard_details.append({
                    'd_key': d_key,
                    'd_value': d_value
                })
            return dashboard_details
        else:
            return f"Error reading dashboard details: {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"