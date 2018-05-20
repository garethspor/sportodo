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
    SUB_ITEMS_FIELD = 'sub_items'

    def to_serializable(self):
        item_list = []
        for item in self.sub_items:
            if item.sub_items:
                sub_items = [sub_item.to_serializable() for sub_item in item.sub_items]
            item_dict = {TodoListItem.TEXT_FIELD: item.text,
                         TodoListItem.DONE_FIELD: item.done}
            item_list.append(item_dict)
        return item_list

    def to_json_file(self, path):
        with open(path, 'w') as fileobj:
            json.dump(self.to_serializable(), fileobj, indent=2)

    def __str__(self):
        out_str = ''
        for item in self.sub_items:
            out_str += '{}\n'.format(item.text)
        return out_str

    @staticmethod
    def construct_from_json(path):
        with open(path, 'r') as fileobj:
            data_list = json.load(fileobj)
        list = TodoListItem('main')
        for item_dict in data_list:
            list.add_item(TodoListItem.constrct_item_from_dict(item_dict))
        return list

    @staticmethod
    def constrct_item_from_dict(item_dict):
        item = TodoListItem(item_dict.get(TodoListItem.TEXT_FIELD, ''),
                            done=item_dict.get(TodoListItem.DONE_FIELD, False))
        return item

