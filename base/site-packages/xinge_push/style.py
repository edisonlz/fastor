#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ClickAction(object):
    TYPE_ACTIVITY = 1
    TYPE_URL = 2
    TYPE_INTENT = 3

    def __init__(self, actionType=1, url='', confirmOnUrl=0, activity='', intent=''):
        self.actionType = actionType
        self.url = url
        self.confirmOnUrl = confirmOnUrl
        self.activity = activity
        self.intent = intent
        self.intentFlag = 0
        self.pendingFlag = 0
        self.packageName = ""
        self.packageDownloadUrl = ""
        self.confirmOnPackage = 1

    def GetObject(self):
        ret = {}
        ret['action_type'] = self.actionType
        if self.TYPE_ACTIVITY == self.actionType:
            ret['activity'] = self.activity
            ret['aty_attr'] = {'if' :self.intentFlag, 'pf' :self.pendingFlag}
        elif self.TYPE_URL == self.actionType:
            ret['browser'] = {'url' :self.url, 'confirm' :self.confirmOnUrl}
        elif self.TYPE_INTENT == self.actionType:
            ret['intent'] = self.intent

        return ret

class Style(object):
    N_INDEPENDENT = 0
    N_THIS_ONLY = -1

    def __init__(self, builderId=0, ring=0, vibrate=0, clearable=1, nId=N_INDEPENDENT):
        self.builderId = builderId
        self.ring = ring
        self.vibrate = vibrate
        self.clearable = clearable
        self.nId = nId
        self.ringRaw = ""
        self.lights = 1
        self.iconType = 0
        self.iconRes = ""
        self.styleId = 1
        self.smallIcon = ""

