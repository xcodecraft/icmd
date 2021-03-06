#coding=utf-8
import logging
import utls.prompt
from  utls.logger import *
_logger = logging.getLogger()

class node_iter :
    root    = None
    parent  = None
    current = None

    back_points = []
    def __init__(self,data) :
        self.data = data
        self.to_root()
    def to_root(self) :
        self.root    = self.data
        self.current = self.data
        self.current.check()

    def save(self):
        self.back_points.append({"parent" : self.parent, "current" : self.current})

    def back(self):
        saved        = self.back_points.pop()
        self.parent  = saved['parent']
        self.current = saved['current']

    def walk(self,cmds) :
        self.to_root()
        for cmd in cmds :
            _logger.debug("next to %s" %(cmd))
            if not self.next(cmd) :
                return

    def next(self,key,strict=False):
        for i in self.current.subs :
            i.check()
            if i.is_match(key,strict) :
                self.save()
                self.parent  = self.current
                self.current = i
                _logger.debug("match %s ,next to :%s" %(key,self.current.name))
                return True
        return False

    def match(self,cmder) :
        _logger.debug("match cmd :%s" %(self.current.name))
        _logger.debug("cmdline :%s" %(cmder))
        self.to_root()
        for cmd in cmder.cmds :
            if not self.next(cmd,strict=True) :
                return False
        if len (self.current.subs) > 0 :
            return False
        for arg in self.current.args :
            if arg.must :
                if arg.default != None :
                    continue
                if not ( cmder.args.has_key(arg.name) or  ( arg.hotkey != None and  cmder.args.has_key(arg.hotkey) )) :
                    return False
        return True
    def get_prompter(self,word=""):
        debug_log("[cmd prompt] current: %s, word:%s" %(self.current.name , word),'prompter')
        if len(self.current.subs) > 0 :
            return utls.prompt.iter(self.current.subs,word, lambda x: getattr(x,'name') )
        info_log("no next cmd prompt ", 'prompter')
        return None

