import os

SECRET_KEY = os.getenv("SECRET_KEY", "h@rd-t0-get-string")
CLIENT_ID = os.getenv("CLIENT_ID")  # Application (client) ID of app registration
CLIENT_SECRET = os.getenv("CLIENT_SECRET")  # Obtain this from 'Certificates & secrets' section in MSAzure
if not CLIENT_SECRET:
    raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"  # <tenant_name>.onmicrosoft.com

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All", "Mail.Send", "User.Read", "User.Read.All"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
