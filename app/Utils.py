import os
import json

def read_vaultfile():
    with open(os.path.join('.', 'vault', 'test.json'), 'r') as file:
        data = json.load(file)
        print(data)
        return data