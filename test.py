from google.cloud import secretmanager

# Initialize the Secret Manager client
client = secretmanager.SecretManagerServiceClient()

# Access the secret
secret_name = "GCP_SA_KEY" 
project_id = "plantcare-443106"  
secret_version = "latest"

# Build the resource name of the secret
name = f"projects/{project_id}/secrets/{secret_name}/versions/{secret_version}"

# Access the secret version
response = client.access_secret_version(name=name)

# Get the secret payload
service_account_info = response.payload.data.decode('UTF-8')

print(service_account_info)