#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2018/1/2

from collections import  defaultdict
import json


def tree():
    return defaultdict(tree)


users = tree()
users['harold']['username'] = 'hrldcpr'
users['handler']['username'] = 'matthandlersux'

print(json.dumps(users))
