import applemusicpy
from applemusicpy.client import ResourceType

team_id = 'team_id'
key_id = 'key_id'
secret_file = 'AuthKey_' + key_id + '.p8'

with open(secret_file,'r') as f:
    secret_key = f.read()

auth = applemusicpy.Auth(secret_key=secret_key, key_id=key_id, team_id=team_id)
client = applemusicpy.Client(auth=auth)

# Catalog albums
ids = [1564530719, 1568819304]
ids = [str(id) for id in ids]

params = {
    "ids": ','.join(ids)
}

response = client.albums(storefront='us', params=params, type=ResourceType.CATALOG)
print(response)

# Library albums
response = client.albums(type=ResourceType.LIBRARY)
print(response)