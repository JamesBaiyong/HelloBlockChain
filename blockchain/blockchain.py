# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @createTime: 2019-12-08 11:24
# @author: scdev030
import hashlib
import json
import time
from urllib.parse import urlparse

import requests

from blockchain.proof_of_work import ProofOfWork


class BlockChain(object):
    """
    区块链
    block and chain
    """
    def __init__(self):
        self.chain = []
        self.transactions = []
        # 生成祖先区块
        self.new_block(proof=1, previous_hash=1)
        self.nodes = set()
        self.proof_of_work = ProofOfWork()
        self.nodes.add(urlparse('http://127.0.0.1:7777').netloc)
        self.nodes.add(urlparse('http://127.0.0.1:7778').netloc)

    def new_block(self, proof, previous_hash=None):
        """
        创建一个区块,加入到链当中
        proof: proof of work
        previous_hash: 区块链hash
        返回: 区块
        """
        block = {
            'index': len(self.chain)+1,
            'transactions': self.transactions,
            'timestamp': time.time(),
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'proof': proof
        }
        self.chain.append(block)
        self.transactions = []
        return block

    def new_transaction(self, sender, recipient, details) -> int:
        """
        记录交易
        sender: 发起节点
        recipient: 接收节点
        amount: 总计数量
        返回: 区块的索引
        """
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'details': details
            })
        return self.last_block['index'] + 1

    def register_node(self, address):
        """
        注册新的节点
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        检查给定的链条是否合法
        """
        previous_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{previous_block}')
            print(f'{block}')
            print()
            print('#'*100)
            print()
            # 验证区块的hash
            if block['previous_hash'] != self.hash(previous_block):
                print('hash 验证失败')
                return False
            # 验证proof
            if not self.proof_of_work.guess_hash(previous_block['proof'], block['proof']):
                print('proof 验证失败')
                return False

            previous_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        """
        共识算法,通过用网络中最长的链作为事实链,解决冲突
        """
        neighbours = self.nodes
        print(neighbours)
        new_chain = None
        max_length = len(self.chain)

        # 获取网络中的所有节点的链,并验证
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                # 验证最长的事实链条
                if length > max_length:
                    if self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
                    else:
                        print('验证失败')
        # 验证通过后,更新事实链条
        if new_chain:
            self.chain = new_chain
            return True
        return False

    @staticmethod
    def hash(block):
        """
        生成hash
        """
        # 保证字典是有序的
        block_string = json.dumps(block, sort_keys=True, indent=4).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        返回最新到块
        """
        return self.chain[-1]
