# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @createTime: 2019-12-08 12:53
# @author: scdev030

from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain.blockchain import BlockChain
from blockchain.proof_of_work import ProofOfWork

app = Flask(__name__)

node_id = str(uuid4())
block_chain = BlockChain()
proof_of_work = ProofOfWork()


@app.route('/mine', methods=['GET'])
def mine():
    """
    创建新的区块,并添加到原本区块中
    """
    # 生成下一个proof
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = proof_of_work.proof(last_proof)
    # sender为0表示此节点开采了新硬币
    block_chain.new_transaction(sender="0", recipient=node_id, details='生成一个币')
    # 添加新块
    previous_hash = block_chain.hash(last_block)
    block = block_chain.new_block(proof, previous_hash)
    response = {
        'message': "挖出了新币",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    创建新的交易记录
    """
    values = request.get_json()
    required = ['sender', 'recipient', 'details']
    if not all(k in values for k in required):
        return '参数缺失', 400
    index = block_chain.new_transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        details=values['details'])
    response = {'message': f'交易会添加到新的区块{index}中'}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "节点错误", 400
    for node in nodes:
        block_chain.register_node(node)
    response = {
        'message': '新节点添加完成',
        'total_nodes': list(block_chain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = block_chain.resolve_conflicts()
    if replaced:
        response = {
            'message': '区块链已更新',
            'new_chain': block_chain.chain
        }
    else:
        response = {
            'message': '已有的区块链合法',
            'chain': block_chain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
