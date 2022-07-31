import requests

BASE = 'http://127.0.0.1:8080'

def main_page() -> str:
    resp = requests.get(BASE).json()
    assert resp['message'] == 'Welcome in GEO RestAPI'
    print('OK')

def users() -> str:
    resp = requests.get(BASE + '/users').json()
    assert type(resp.get('users')) == list
    print('OK')

def register() -> str:
    body = {
    "name": "Kowalski",
    "password": "1234567"
    }
    resp = requests.post(BASE + '/register', json=body).json()
    assert resp['message'] == 'Registration complete!'
    print('OK')

def login() -> str:
    resp = requests.post(BASE + '/login', auth=('Kowalski', '1234567')).json()
    assert type(resp['token']) == str
    print('OK')
    geo_save(resp['token'])
    geo_info_get(resp['token'])
    geo_info_delete(resp['token'])

def geo_save(token: str) -> str:
    resp = requests.post(BASE + '/geo', headers={'x-access-tokens': token}).json()
    assert resp['message'] == 'New user ID added!'
    print('OK')

def geo_info_get(token: str) -> str:
    resp = requests.get(BASE + '/geo_info', headers={'x-access-tokens': token}).json()
    assert type(resp) == dict
    print('OK')

def geo_info_delete(token: str) -> str:
    resp = requests.delete(BASE + '/geo_info/1', headers={'x-access-tokens': token}).json()
    assert resp['message'] == 'Geo info deleted'
    print('OK')

main_page()
users()
register()
login()
