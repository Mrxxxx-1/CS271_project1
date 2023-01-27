import hashlib
import random
import string
import json
import threading
from decimal import Decimal
from time import time
 
 
class MyThread(threading.Thread):
 
    def __init__(self, target, args=()):
        super(MyThread, self).__init__()
        self.func = target
        self.args = args
 
    def run(self):
        self.result = self.func(*self.args)
 
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
 
 
class BlockChain:
    def __init__(self, initialHash):
        # init block chain
        self.chain = []
 
        # init pitman
        self.pitmen = []
        for i in range(6):
            self.pitmen.append(Pitman)
 
        # collect mine results
        self.results = []
 
        # generate GenesisBlock
        self.new_block(initialHash)
 
    @property
    def last_block(self):
        if len(self.chain):
            return self.chain[-1]
        else:
            return None
 
    def get_trans(self):
        return json.dumps({
            'sender': ''.join(random.sample(string.ascii_letters + string.digits, 8)),
            'recipient': ''.join(random.sample(string.ascii_letters + string.digits, 8)),
            'amount': random.randrange(1, 10000)
        })
 
    def new_block(self, initialHash=None):
        if initialHash:
            # generate Genesis Block
            block = Block()
            block.index = 0
            block.nonce = random.randrange(0, 99999)
            block.previousHash = '0'
            block.difficulty = 0
            block.transactionData = self.get_trans()
            guess = f'{block.previousHash}{block.nonce}{block.transactionData}'.encode()
            block.hash = hashlib.sha256(guess).hexdigest()
            block.time = time()
            self.chain.append(block)
        else:
            for i in range(len(self.pitmen)):
                pm = MyThread(target=self.pitmen[i].mine,
                                      args=(self.pitmen[i],
                                            len(self.chain),
                                            self.last_block.get_block()['Hash'],
                                            self.get_trans()))
                pm.start()
                pm.join()
                self.results.append(pm.get_result())
 
            # show all blocks
            print("All blocks generated by pitmen:")
            for result in self.results:
                print(result[0].get_block())
 
            # get new block
            firstblock = self.results[0][0]
            mintime = Decimal(self.results[0][1])
            for i in range(1, len(self.results)):
                if Decimal(self.results[i][1]) < mintime:
                    firstblock = self.results[i][0]
                else:
                    continue
            self.chain.append(firstblock)
            self.results = []
 
    def show_chain(self):
        print('This is mine first block chain!')
        for block in self.chain:
            print(block.get_block())
 
 
class Block:
    def __init__(self):
        self.index = None
        self.time = None
        # self.difficulty = None
        self.nonce = None
        self.hash = None
        self.previousHash = None
        self.transactionData = None
 
    def get_block(self):
        return {
            'Index': self.index,
            'Time': self.time,
            # 'Difficulty': self.difficulty,
            'Hash': self.hash,
            'Nonce': self.nonce,
            'PreviousHash': self.previousHash,
            'TransactionData': self.transactionData
        }
 
 
class Pitman:
 
    def mine(self, index, previousHash, transactionData):
        beginTime = time()
 
        block = Block()
        block.index = index
        block.previousHash = previousHash
        block.transactionData = transactionData
        block.difficulty, block.hash, block.nonce = self.generate_hash(previousHash, transactionData)
        block.time = time()
        endTime = time()
 
        return block, endTime - beginTime
 
    @staticmethod
    def generate_hash(previousHash, transactionData):
        difficulty = 0
        nonce = random.randrange(0, 99999)
        guess = f'{previousHash}{nonce}{transactionData}'.encode()
        myhash = hashlib.sha256(guess).hexdigest()
        while myhash[-1] != '0':
            difficulty += 1
            nonce += difficulty
            guess = f'{previousHash}{nonce}{transactionData}'.encode()
            myhash = hashlib.sha256(guess).hexdigest()
        return difficulty, myhash, nonce
 
 
if __name__ == '__main__':
    chain = BlockChain(1)
    length = 5
    for i in range(length):
        chain.new_block()
    chain.show_chain()