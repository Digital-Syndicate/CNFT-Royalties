#!/usr/bin/python3

#Version 1.0 by Huth S0lo - March 15, 2021

#Requires cardano-cli and a live node.  I havent added the code to use submit api.  Feel free to add it, and do a pull request.

import subprocess
import re
import shlex
import os
import json
import math
import os
import shlex
from datetime import datetime
from time import sleep
from collections import namedtuple
import random


print('This utility will mint a royalty token on a new policy.  The policy cannot have been used to mint anything previously, or it will not meet the guidelines of CIP-0027.  Please use a clean wallet, with no existing tokens.  You should send a fresh transaction to the payment wallet with ~3 ada.')
print("If you've found value in using this script, please consider delegating to BUDZ pool.")
sleep(5)

#################################variable initialization
json_loaded = None
ttl_buffer=1000000
json_data = []
wallet_balance = 0
burn_after_mint = False

#makeroyalty
#merkabacnft.policy

cli = 'cardano-cli'
network = '--mainnet' # Use '--tesnet-magic 1097911063' for testnet
node_home = '/opt/cardano/cnode/' #Replace with your node home folder
socket = '/opt/cardano/cnode/sockets/node0.socket' #replace with your socket location
project_folders = os.getenv('project_folders')
tx_file_folder = './' #Uses the local folder for tx files.  Change to another location if desired.
debug = False #Set to True for debug outputs

#################################Test Mode - Set to False to go live
wallet = input("What is the name of cli wallet to use to pay the transaction fees, without file extension.  i.e. for smallwallet.addr please type 'smallwallet'? ")
policy = input("What is the name of cli policy you want to create a royalty on, without file extension. i.e. for policy.policy.id please type 'policy.policy'? ")
percent = input("Please enter the percent royalty you would like used on this royalty token. i.e. for a 10% royalty, please type '10'? ")
output_loc = input("What wallet would you like your royalties sent to? ")
confirm_burn = input("Do you want to burn the token after minting? This is considered best practice ")
if confirm_burn == 'Yes' or confirm_burn == 'yes' or confirm_burn == 'y' or confirm_burn == 'y' or confirm_burn == 'YES':
    burn_after_mint = True



royalty_pct = round(float(percent)/100, 2)


with open(f'./{wallet}.addr') as f:
    payment_wallet = f.read().rstrip('\n')

with open(f'./{policy}.id') as f:
    policy_id = f.read().rstrip('\n')





def make_777_token():
    filename_begin = datetime.now().strftime("tx_%Y-%m-%d_%Hh%Mm%Ss") + str(random.randint(100000, 999999))
    if len(output_loc) > 64:
        token_json = '{"777":{"pct":"' + str(royalty_pct) + '","addr": ["' + output_loc[:64] +'","' + output_loc[64:] + '"]}}'
    else:
        token_json = '{"777":{"pct":"' + str(royalty_pct) + '","addr": ["' + output_loc + '"]}}'
    utxos = get_utxos(payment_wallet, filter='Both', min_amount=2000000)
    while True:
        if len(utxos) == 0:
            print('Not enough ada on this wallet.  Please send 3 ada to the wallet to continue')
            print('Press Ctrl-C to cancel. Otherwise this will continue to check the wallet once per minute')
            sleep(60)
        else:
            break
    tx_hash = utxos[0]['TxHash']
    tx_ix = utxos[0]['TxIx']
    tx_in = f'{tx_hash}#{tx_ix}'
    ll_amount = int(utxos[0]['Lovelace'])
    json_file = './' + filename_begin + 'royaltyjson.json'
    with open(json_file, 'w+') as file:
        file.write(token_json)
    tip = get_tip()
    ttl = tip + ttl_buffer
    min_fee = 0
    tx_draft = './' + filename_begin + '.draft'
    tx_raw = './' + filename_begin + '.raw'
    tx_signed = './' + filename_begin + '.signed'
    command = (f'{cli} transaction build-raw --fee {min_fee} --invalid-hereafter {ttl} --tx-in {tx_in} --tx-out {payment_wallet}+{ll_amount}+"1 {policy_id}" --mint "1 {policy_id}"  --metadata-json-file {json_file} --minting-script-file ./{policy}.script --out-file {tx_draft}')
    results = run_cli(command)
    print(command)
    min_fee = calc_min_fee(tx_draft, 1, witness_count=2, byron_witness_count=0)
    ll_amount = ll_amount = min_fee
    command = (f'{cli} transaction build-raw --fee {min_fee} --invalid-hereafter {ttl} --tx-in {tx_in} --tx-out {payment_wallet}+{ll_amount}+"1 {policy_id}" --mint "1 {policy_id}"  --metadata-json-file {json_file} --minting-script-file ./{policy}.script --out-file {tx_raw}')
    results = run_cli(command)
    print(command)
    command = (f"{cli} transaction sign --tx-body-file {tx_raw} --signing-key-file ./{wallet}.skey --signing-key-file {policy}.skey {network} --out-file {tx_signed}")
    results = run_cli(command)
    print(command)
    command = (f"{cli} transaction submit --tx-file {tx_signed} {network}")
    results = run_cli(command)
    print(command)
    spent_utxo = []
    spent_utxo.append(tx_in)
    if burn_after_mint == True:
        burn_token(spent_utxo)
    else:
        print('Royalty Token has been minted.  Good luck with the drop!')


def burn_token(spent_utxo):
    filename_begin = datetime.now().strftime("tx_%Y-%m-%d_%Hh%Mm%Ss") + str(random.randint(100000, 999999))
    while True:
        utxos = get_utxos(payment_wallet, filter=None, min_amount=1000000)
        tx_hash = utxos[0]['TxHash']
        tx_ix = utxos[0]['TxIx']
        tx_in = f'{tx_hash}#{tx_ix}'
        if tx_in in spent_utxo:
            print('Waiting for minting transaction to complete.  Sleeping for 60 seconds before retry.')
            sleep(60)
        else:
            break
    tx_hash = utxos[0]['TxHash']
    tx_ix = utxos[0]['TxIx']
    tx_in = f'{tx_hash}#{tx_ix}'
    ll_amount = int(utxos[0]['Lovelace'])
    tip = get_tip()
    ttl = tip + ttl_buffer
    min_fee = 0
    tx_draft = './' + filename_begin + '.draft'
    tx_raw = './' + filename_begin + '.raw'
    tx_signed = './' + filename_begin + '.signed'
    command = (
        f'{cli} transaction build-raw --fee {min_fee} --invalid-hereafter {ttl} --tx-in {tx_in} --tx-out {payment_wallet}+{ll_amount}+"1 {policy_id}" --mint "-1 {policy_id}"  --metadata-json-file {json_file} --minting-script-file ./{policy}.script --out-file {tx_draft}')
    results = run_cli(command)
    print(command)
    min_fee = calc_min_fee(tx_draft, 1, witness_count=2, byron_witness_count=0)
    ll_amount = ll_amount = min_fee
    command = (
        f'{cli} transaction build-raw --fee {min_fee} --invalid-hereafter {ttl} --tx-in {tx_in} --tx-out {payment_wallet}+{ll_amount}+"1 {policy_id}" --mint "-1 {policy_id}"  --metadata-json-file {json_file} --minting-script-file ./{policy}.script --out-file {tx_raw}')
    results = run_cli(command)
    print(command)
    command = (
        f"{cli} transaction sign --tx-body-file {tx_raw} --signing-key-file ./{wallet}.skey --signing-key-file {policy}.skey {network} --out-file {tx_signed}")
    results = run_cli(command)
    print(command)
    command = (f"{cli} transaction submit --tx-file {tx_signed} {network}")
    results = run_cli(command)
    print(command)
    print('Royalty Token has been minted and burned.  Good luck with the drop!')






def get_min_utxo() -> int:
    load_protocol_parameters()
    coin_Size = 2
    utxo_entry_size_without_val = 27
    ada_only_utxo_size = utxo_entry_size_without_val + coin_Size
    utxo_cost_word = protocol_parameters["utxoCostPerWord"]
    return ada_only_utxo_size*utxo_cost_word

def load_protocol_parameters():
    global protocol_parameters
    params_file = (f'{node_home}protocol.json')
    run_cli(
        f"{cli} query protocol-parameters {network} "
        f"--out-file {params_file}"
    )
    json_data = _load_text_file(params_file)
    protocol_parameters = json.loads(json_data)
    return params_file

def _load_text_file(fpath):
    text = open(fpath, "r").read()
    return text



def get_utxos(payment_wallet, filter=None, min_amount=1000000) -> list:
    result = run_cli(
    f"{cli} query utxo --address {payment_wallet} {network}"
    )
    raw_utxos = result.stdout.split("\n")[2:]
    # Parse the UTXOs into a list of dict objects
    utxos = []
    for utxo_line in raw_utxos:
        vals = utxo_line.split()
        utxo_dict = {
            "TxHash": vals[0],
            "TxIx": vals[1],
            "Lovelace": vals[2],
        }
        # Extra tokens will be separated by a "+" sign.
        extra = [i for i, j in enumerate(vals) if j == "+"]
        for i in extra:
            if 'TxOutDatum' in vals[i + 1]:
                continue
            asset = vals[i + 2]
            amt = vals[i + 1]
            if asset in utxo_dict:
                utxo_dict[asset] += amt
            else:
                utxo_dict[asset] = amt
        utxos.append(utxo_dict)
    # Filter utxos
    if filter == "Both":
        utxos = [
        utxo
        for utxo in utxos
        if len(utxo.keys()) == 3 and int(utxo['Lovelace']) > min_amount
    ]
    return utxos



def run_cli(cmd):
    os.environ["CARDANO_NODE_SOCKET_PATH"] = socket
    result = subprocess.run(shlex.split(cmd), capture_output=True)
    stdout = result.stdout.decode().strip()
    stderr = result.stderr.decode().strip()
    if debug:
        print(f'CMD: "{cmd}"')
        print(f'stdout: "{stdout}"')
        print(f'stderr: "{stderr}"')
    ResultType = namedtuple("Result", "stdout, stderr")
    return ResultType(stdout, stderr)


def get_tip() -> int:
    cmd = f"{cli} query tip {network}"
    result = run_cli(cmd)
    if "slot" not in result.stdout:
        raise ShelleyError(result.stderr)
    vals = json.loads(result.stdout)
    return vals["slot"]

def calc_min_fee(
    tx_draft,
    tx_out_count,
    witness_count,
    byron_witness_count=0,
) -> int:
    params_file = load_protocol_parameters()
    result = run_cli(
        f"{cli} transaction calculate-min-fee "
        f"--tx-body-file {tx_draft} "
        f"--tx-in-count 1 "
        f"--tx-out-count {tx_out_count} "
        f"--witness-count {witness_count} "
        f"--byron-witness-count {byron_witness_count} "
        f"{network} --protocol-params-file {params_file}"
    )
    min_fee = int(result.stdout.split()[0])
    return min_fee

make_777_token()