import applemusicpy
from applemusicpy.client import ResourceType

team_id = 'team_id'
key_id = 'key_id'
secret_file = 'AuthKey_' + key_id + '.p8'

with open(secret_file,'r') as f:
    secret_key = f.read()

auth = applemusicpy.Auth(secret_key=secret_key, key_id=key_id, team_id=team_id)
client = applemusicpy.Client(auth=auth)


# Library albums

params = {
    "ids": [1564530719,1568819304]
}

print(client.albums(storefront='en', params=params, type=ResourceType.CATALOG))

# Catalog albums