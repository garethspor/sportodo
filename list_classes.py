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
    INDEX_SEP = '.'

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

    @staticmethod
    def format_indices(indicies):
        if indicies is None:
            return ''
        return TodoListItem.INDEX_SEP.join([str(index) for index in indicies])

    def to_str(self, depth=0, indicies=None):
        indent = ' ' * depth
        check_box = '({})'.format('x' if self.done else ' ')
        prefix = TodoListItem.format_indices(indicies)
        out_str = '{}{} {} {}\n'.format(indent, check_box, prefix, self.text)
        return out_str

    def sub_items_to_str(self, depth=0, indicies=None):
        out_str = ''
        indicies = indicies if indicies else []
        for index, item in enumerate(self.sub_items):
            item_indicies = indicies + [index]
            out_str += item.to_str(depth=depth, indicies=item_indicies)
            out_str += item.sub_items_to_str(depth=depth+1, indicies=item_indicies)
        return out_str

    def __str__(self):
        return self.sub_items_to_str()

    def get_item_by_indecies(self, indicies):
        if isinstance(indicies, basestring):
            return self.get_item_by_indecies(TodoListItem.convert_string_to_indicies(indicies))
        if len(indicies) == 0:
            return self
        return self.sub_items[indicies[0]].get_item_by_indecies(indicies[1:])

    @staticmethod
    def convert_string_to_indicies(str):
        index_strings = str.split(TodoListItem.INDEX_SEP)
        return [int(index) for index in index_strings]

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
