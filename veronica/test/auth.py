# Copyright 2021 Akretion (https://www.akretion.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import requests

url = "https://api-sbox.veronica.ec/api/v1.0/oauth/token?grant_type=password"

payload={'username': '1713310439001',
'password': '7fLy4Wm26z',
'client_id': '8fngv24vnndu9kst',
'client_secret': 'vnk2r7yf6rffaznj'}
files=[

]
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic OGZuZ3YyNHZubmR1OWtzdDp2bmsycjd5ZjZyZmZhem5q'
}

response = requests.post(url, headers=headers, data=payload, files=files)

print(response.text)

