# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @createTime: 2019-12-08 12:37
from unittest import TestCase


# @author: scdev030
from blockchain.proof_of_work import ProofOfWork


class TestProofOfWork(TestCase):
    def test__proof(self):
        # --given
        proof = ProofOfWork()
        # --when
        new_proof = proof.proof(last_proof=0)
        # --then
        # 69732
        assert (new_proof == 69732)
