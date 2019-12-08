# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @createTime: 2019-12-08 12:22
# @author: scdev030
import hashlib


class ProofOfWork(object):
    """
    工作证明算法
    """
    def proof(self, last_proof) -> int:
        """
        找出一个数,和当前的proof生成hash,hash最后四位为0
        """
        proof = 0
        while self.guess_hash(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def guess_hash(last_proof, proof) -> bool:
        """
        验证proof
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # print(f'now: hash is {guess_hash}')
        return guess_hash[:4] == "0000"
