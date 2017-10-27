# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:59:47 2017

@author: Master
"""
from PyQt5 import QtCore

def open_event(settings):
    _finishcount = settings.value('finishcount', [], int)
    print('read settings: %s' % _finishcount)
    _finishcount.append(len(_finishcount))
    
def close_event(settings):
    _finishcount = settings.value('finishcount', [], int)
    settings.setValue('finishcount', _finishcount)
    print('save settings: %s' % _finishcount)