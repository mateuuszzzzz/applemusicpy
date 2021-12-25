import applemusicpy
from applemusicpy.client import ResourceType

team_id = 'team_id'
key_id = 'key_id'
secret_file = 'AuthKey_' + key_id + '.p8'

with open(secret_file,'r') as f:
    secret_key = f.read()

auth = applemusicpy.Auth(secret_key=secret_key, key_id=key_id, team_id=team_id)
client = applemusicpy.Client(auth=auth)

params = {
    'limit': 3
}

print(client('GET', 'https://api.music.apple.com/v1/me/library/albums', params, ResourceType.LIBRARY))