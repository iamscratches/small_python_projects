# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 00:56:37 2021

@author: subhankar
"""

from hashlib import sha256
import time

# print(len(sha256("ABC".encode("ascii")).hexdigest()))
MAX_NONCE = 10000000000000000
def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def mine(block_number, transactions, previous_hash, prefix_zeros):
    prefix_str = '0' * prefix_zeros
    start = time.time()
    for nonce in range(100000000,MAX_NONCE):        
        text = str(block_number) + transactions + previous_hash + str(nonce)
        new_hash = SHA256(text)
        if(new_hash.startswith(prefix_str)):
            print(f"\nYAY! Successfully mined bitcoins with nonce value: {nonce}")            
            return new_hash
        if(time.time() - start) > 5 :
            start = time.time()
            print(".",end=(" "))
    raise BaseException((f"Couldn't find correct after trying {MAX_NONCE} times"))

if __name__ == '__main__':
    transactions ='''
    Dhaval->Bhavin->20,
    Mando->Cara->45
    '''
    difficulty = 8
    start = time.time()
    print("start mining",end=(' '))
    new_hash = mine(5, transactions, 'b5d4045c3f466fa91fe2cc6abe79232a1a57cdf104f7a26e716e0a1e2789df78', difficulty)
    print(new_hash)
    total_time = str(time.time() - start)
    print(f'end mining.\n Mining took: {total_time} seconds')