#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TimeInterval(object):
    STR_START = 'start'
    STR_END = 'end'
    STR_HOUR = 'hour'
    STR_MIN = 'min'

    def __init__(self, startHour=0, startMin=0, endHour=0, endMin=0):
        self.startHour = startHour
        self.startMin = startMin
        self.endHour = endHour
        self.endMin = endMin

    def _isValidTime(self, hour, minute):
        return isinstance(hour, int) and isinstance(minute, int) and hour >= 0 and hour <=23 and minute >=0 and minute <= 59

    def _isValidInterval(self):
        return self.endHour * 60 + self.endMin >= self.startHour * 60 + self.startMin

    def GetObject(self):
        if not (self._isValidTime(self.startHour, self.startMin) and self._isValidTime(self.endHour, self.endMin)):
            return None
        if not self._isValidInterval():
            return None
        return {
                self.STR_START:{self.STR_HOUR:str(self.startHour), self.STR_MIN:str(self.startMin)},
                self.STR_END:{self.STR_HOUR:str(self.endHour), self.STR_MIN:str(self.endMin)}
            }
