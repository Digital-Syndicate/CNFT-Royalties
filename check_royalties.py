# Get Royalty Info v1.0
# By Huth S0lo / Digital Syndicate
# 4/20/2022

import requests
import json
from time import sleep
import pytz


api_network = 'api' #change to 'testnet' for testnet
base_url = f'https://{api_network}.koios.rest/api'
utc=pytz.UTC



def get_minting_hash(policy_id):
    sleep(.5)
    response = requests.get(f'{base_url}/v0/asset_info?_asset_policy={policy_id}&_asset_name=')
    if response.status_code == 200:
        noname_token = response.json()
        tx_hash = noname_token[0]['minting_tx_hash']
    else:
        tx_hash = None
    return tx_hash

def get_777_info(tx_hash):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json',}
    data = f'\u007b"_tx_hashes":["{tx_hash}"]\u007d'
    response = requests.post(f'{base_url}/v0/tx_info', headers=headers, data=data)
    royalty_info = {}
    if response.status_code == 200:
        response = response.json()
    if len(response) != 0:
        if 'metadata' in response[0]:
            i = 0
            while i < len(response[0]['metadata']):
                if response[0]['metadata'][i]['key'] == '777':
                    royalty_info = response[0]['metadata'][i]['json']
            i += 1
    return royalty_info



def run_royalty_check():
    policy_id = input('Please enter the policy id that you want to inquire about royalties: ')
    royalty_info = {}
    tx_hash = get_minting_hash(policy_id)
    if tx_hash != None:
        royalty_info = get_777_info(tx_hash)
    print(royalty_info)
    return royalty_info

run_royalty_check()
