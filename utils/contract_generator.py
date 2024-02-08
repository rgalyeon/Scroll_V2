import aiohttp
import random
import re
import solcx


async def fetch_words(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            words = text.splitlines()
            return words


async def load_words_data():
    url_adj = "https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Adjectives-All.txt"
    url_nonce = "https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Nouns-All.txt"
    url_verb = "https://raw.githubusercontent.com/taikuukaits/SimpleWordlists/master/Wordlist-Verbs-All.txt"

    adjectives = await fetch_words(url_adj)
    nonce = await fetch_words(url_nonce)
    verbs = await fetch_words(url_verb)

    return adjectives, nonce, verbs


def generate_contract_name(adjectives, nonce):
    adj = random.choice(adjectives)
    adj = re.sub(r'[^a-zA-Z]', '', adj).capitalize()

    nonce = random.choice(nonce)
    nonce = re.sub(r'[^a-zA-Z]', '', nonce).capitalize()

    return f'{adj}{nonce}'


def generate_function_name(verbs, nonce):

    verb = random.choice(verbs)
    verb = re.sub(r'[^a-zA-Z]', '', verb).lower()

    nonce = random.choice(nonce)
    nonce = re.sub(r'[^a-zA-Z]', '', nonce).capitalize()

    return f'{verb}{nonce}'


def generate_sentence(nonce, verbs, adjs):
    marks = [';', '.', '!', '...', '!!', '']

    sent = (random.choice(adjs) + ' ' + random.choice(nonce) + ' ' + random.choice(verbs) + ' ' +
            random.choice(nonce) + random.choice(marks) + ' ')
    return sent


async def generate_solidity_contract():
    adjectives, nonce, verbs = await load_words_data()

    contract_name = generate_contract_name(adjectives, nonce)
    function_name = generate_function_name(verbs, nonce)
    sent = generate_sentence(nonce, verbs, adjectives)
    version = random.randint(0, 6)

    return f"""
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.{version};

contract {contract_name} {{
    function {function_name}() external pure returns (string memory) {{
        return "{sent}";
    }}
}}
""", contract_name


async def compile_contract():

    solidity_code, contract_name = await generate_solidity_contract()
    solcx.install_solc('0.8.20')

    compiled_sol = solcx.compile_standard({
        "language": "Solidity",
        "sources": {"contract.sol": {"content": solidity_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["metadata", "evm.bytecode", "evm.bytecode.sourceMap", "abi"]
                }
            }
        },
    }, solc_version='0.8.20')

    contract_interface = compiled_sol['contracts']['contract.sol'][contract_name]
    bytecode = contract_interface['evm']['bytecode']['object']
    abi = contract_interface['abi']

    return bytecode, abi
