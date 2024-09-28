import json
import os
import sys
sys.path.extend(['.', '..'])
from mijiaAPI import mijiaLogin

username = os.getenv('XIAOMI_USERNAME')
password = os.getenv('XIAOMI_PASSWORD')
print(f'username: {username}, password: {password[:3]}***')
api = mijiaLogin()
auth = api.login(username, password)
with open('jsons/auth.json', 'w') as f:
    json.dump(auth, f, indent=2)
