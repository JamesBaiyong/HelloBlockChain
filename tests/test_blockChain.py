# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @createTime: 2019-12-08 12:00

from unittest import TestCase


# @author: scdev030
from blockchain.blockchain import BlockChain


class TestBlockChain(TestCase):
    def test__block_genesis_block(self):
        # given
        bc = BlockChain()
        # when
        genesis_block = bc.last_block
        # then
        assert (genesis_block['previous_hash'] == 1)
        assert (genesis_block['proof'] == 1)
        assert (genesis_block['index'] == 1)
