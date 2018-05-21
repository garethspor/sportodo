""" todo list item classes
"""
from __future__ import print_function

import argparse
import json

TEXT_FIELD = 'text'
DONE_FIELD = 'done'
SUB_ITEMS_FIELD = 'sub_items'

class TodoListItem(object):
    def __init__(self, text, done=False):
        self.text = text
        self.done = done
        self.sub_items = []

    def add_sub_item(self, item):
        self.sub_items.append(item)


    def to_serializable(self):
        item_list = []
        for item in self.sub_items:
            item_dict = {TEXT_FIELD: item.text}
            if item.done:
                item_dict[DONE_FIELD] = True
            if item.sub_items:
                item_dict[SUB_ITEMS_FIELD] = item.to_serializable()
            item_list.append(item_dict)
        return item_list

    def to_json_file(self, path):
        with open(path, 'w') as fileobj:
            json.dump(self.to_serializable(), fileobj, indent=2)

    def to_str(self, depth=0, index=None):
        indent = ' ' * depth
        check_box = '({})'.format('x' if self.done else ' ')
        out_str = '{}{} {} - {}'.format(indent, check_box, index, self.text)
        if self.sub_items:
            sub_item_str = self.sub_items_to_str(depth=depth + 1, index=index)
            out_str = '\n'.join([out_str, sub_item_str])
        return out_str

    def sub_items_to_str(self, depth=0, index=None):
        out_strs = []
        if index is None:
            index = TodoListIndex()
        for sub_index, item in enumerate(self.sub_items):
            item_index = index.make_sub_index(sub_index)
            out_strs.append(item.to_str(depth=depth, index=item_index))
        return '\n'.join(out_strs)

    def __str__(self):
        return self.sub_items_to_str()

    def get_item_by_indecies(self, index):
        next_index = index.pop()
        if next_index is None:
            return self
        return self.sub_items[next_index].get_item_by_indecies(index)

    @staticmethod
    def construct_from_json(path):
        with open(path, 'r') as fileobj:
            data_list = json.load(fileobj)
        list = TodoListItem('main')
        for item_dict in data_list:
            list.add_sub_item(TodoListItem.constrct_item_from_dict(item_dict))
        return list

    @staticmethod
    def constrct_item_from_dict(item_dict):
        item = TodoListItem(item_dict.get(TEXT_FIELD, ''),
                            done=item_dict.get(DONE_FIELD, False))
        sub_items = item_dict.get(SUB_ITEMS_FIELD, None)
        if sub_items:
            for sub_item in sub_items:
                item.add_sub_item(TodoListItem.constrct_item_from_dict(sub_item))
        return item


INDEX_SEP = '.'

class TodoListIndex():
    def __init__(self, init_index=None):
        if init_index is None:
            self.index_list = []
        elif isinstance(init_index, basestring):
            index_strs = init_index.split(INDEX_SEP)
            self.index_list = [int(index) for index in index_strs]
        else:
            self.index_list = list(init_index)

    def __str__(self):
        return INDEX_SEP.join([str(index) for index in self.index_list])

    def pop(self):
        if self.index_list:
            popped = self.index_list[0]
            self.index_list = self.index_list[1:]
            return popped
        return None

    def make_sub_index(self, sub_index):
        ret = TodoListIndex(self.index_list)
        ret.index_list.append(sub_index)
        return ret
