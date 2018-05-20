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
            item_dict = {TodoListItem.TEXT_FIELD: item.text,
                         TodoListItem.DONE_FIELD: item.done}
            if item.sub_items:
                item_dict[TodoListItem.SUB_ITEMS_FIELD] = item.to_serializable()
            item_list.append(item_dict)
        return item_list

    def to_json_file(self, path):
        with open(path, 'w') as fileobj:
            json.dump(self.to_serializable(), fileobj, indent=2)

    def __str__(self, depth=0, prefix=''):
        out_str = ''
        for index, item in enumerate(self.sub_items):
            indent = ' ' * depth
            check_box = '({})'.format('x' if item.done else ' ')
            item_prefix = '{}{}.'.format(prefix, index)
            out_str += '{}{} {} {}\n'.format(indent, check_box, item_prefix, item.text)
            if item.sub_items:
                out_str += item.__str__(depth=depth+1, prefix=item_prefix)
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
        sub_items = item_dict.get(TodoListItem.SUB_ITEMS_FIELD, None)
        if sub_items:
            for sub_item in sub_items:
                item.add_item(TodoListItem.constrct_item_from_dict(sub_item))
        return item
