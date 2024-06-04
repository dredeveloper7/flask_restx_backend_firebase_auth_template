import os 
from dotenv import load_dotenv

load_dotenv()


# The original information for this config is found from firebase 
# Each app you create in firebase has a config json
# We placed the Key:Value pairs of the original json in .env file
# If using this as template - make sure .env is in /app folder

config = {
    "type": os.environ["type"],
    "project_id": os.environ["project_id"],
    "private_key_id": os.environ["private_key_id"],
    "private_key": os.environ["private_key"],
    "client_email": os.environ["client_email"],
    "client_id": os.environ["client_id"],
    "auth_uri":  os.environ["auth_uri"],
    "token_uri":  os.environ["token_uri"],
    "auth_provider_x509_cert_url": os.environ["auth_provider_x509_cert_url"],
    "client_x509_cert_url":  os.environ["client_x509_cert_url"],
    "universe_domain": os.environ["universe_domain"]
}