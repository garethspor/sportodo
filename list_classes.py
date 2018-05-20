""" todo list item classes
"""
from __future__ import print_function

import json

class TodoListItem(object):
    def __init__(self, text, done=False):
        self.text = text
        self.done = done
        self.sub_items = []

    def add_item(self, item):
        self.sub_items.append(item)

    TEXT_FIELD = 'text'
    DONE_FIELD = 'done'

    @staticmethod
    def construct_from_json(path):
        with open(path, 'r') as fileobj:
            data_list = json.load(fileobj)
        list = TodoListItem()
        for item_dict in data_list:
            list.add_item(constrct_item_from_dict(item_dict))
        return list

    @staticmethod
    def constrct_item_from_dict(item_dict):
        item = TodoListItem(item_dict.get(TodoListItem.TEXT_FIELD, ''),
                            done=item_dict.get(TodoListItem.DONE_FIELD, False))
        return item

