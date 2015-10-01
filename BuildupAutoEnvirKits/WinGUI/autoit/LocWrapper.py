# -*- coding: utf-8 -*-

import logging, sys

_logger = logging.getLogger(__name__)

from collections import namedtuple

WindowLocator = namedtuple('WindowLocator', 'title text')
WindowLocator.__new__.__defaults__ = ("", "")

ControlLocator = namedtuple('ControlLocator', 'id button clicks x y sel_str')
ControlLocator.__new__.__defaults__ = ("", "left", 1, None, None, "")


class AutoitLocator(object):
    
    def __init__(self):
        '''
        '''
        self.window = None  # assign a new WindowLocator()
        self.control = None  # assign a new ControlLocator()


if __name__ == '__main__':
    '''
    '''
    logging.basicConfig(
        format = '[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S',
    )
    
#     loc = WindowLocator("111", "222")
    loc = WindowLocator()
    loc.title = 'ttt'
    print loc.title, loc.text
    
#     loc = ControlLocator( WindowLocator("111", "222"), "&control")
#     print loc.win_info.title, loc.win_info.text, loc.id