#-*- coding:UTF-8 -*-
import re
#import snailseg
from FileWithBuffer import File
import types
class Parser:
    def __init__(self,readable):
        self.file=File(readable)
        self.question_pattern=[re.compile(u'“([^”]*)”'),
                               re.compile('"([^"]*)"'),
                               re.compile('“([^“]*)“')]

        self.current_question=""
        self.current_question_words=[]
        self.xuci=[]
        self.question=0
        self.answer=1
        self.answer_end1=2
        self.answer_end2=3

    def parse(self):
        items=[]
        question=0
        answer=1
        stat=0
        maybe_anwsers=[]
        for line in self.file:
            try:
                line=unicode(line.strip(),'utf-8')
            except TypeError:
                pass
            if(len(line)==0 or line.isdigit() or line.isdecimal()):
                continue
            if line.startswith(u'【'):
                continue
            if stat == question:
                item=dict()
                item["answer"]=[]
                self.current_question=item["question"]=self.get_question(line)
                #分词，并大致过滤一下虚词
                #self.current_question_words=[x for x in snailseg.cut(self.current_question) if len(x)>=2]
                stat=answer
                items.append(item)
            else:
                stat,ans=self.get_answer(line)
                item["answer"].append(ans)


        return items
    def get_question(self,line):
        for pattern in self.question_pattern:
            m=pattern.search(line)
            if not m is None:
                return m.groups()[0]
        return line
    def amost_en(self,line):
        en=0
        not_en=0
        for x in line:
            ch=ord(x)
            if ch==32:
                en+=1
            elif ch>255:
                not_en+=1
        return en>not_en

    def get_answer(self,line):
        idx=line.find(':--end--:')
        if idx!=-1:
            return (self.question,line[:idx])
        else:
            return (self.answer,line)

class LineBasedParser:
    def __init__(self,readable):
        self.file=File(readable)
    def parse(self):
        items=[]
        for line in self.file:
            line=line.strip()
            try:
                line=unicode(line,'utf-8')
            except TypeError:
                pass
            used,item=self.parse_(line)
            if used is False:
                self.file.unread(line)
            if item is None:
                continue
            if isinstance(item,types.ListType):
                for it in item:
                    items.append(it)
            else:
                items.append(item)
        return items
    def parse_(self,line):
        raise NotImplementedError()
class SeparatorParser(LineBasedParser):
    def __init__(self,readable,sp=[':',u'：']):
        LineBasedParser.__init__(self,readable)
        self.sp=sp;
    def parse_(self,line):
        idx=-1
        for ch in self.sp:
            idx=line.find(ch)
            if(idx!=-1):
                break
        if idx==-1:
            return (True,None)
        return (True,{
            "answer":line[idx+1:],
            "question":line[:idx]
        })
class TurnParser(LineBasedParser):
    ANSWER=1,
    QUESTION=2,
    def __init__(self,readable):
        LineBasedParser.__init__(self,readable)
        self.state=TurnParser.QUESTION
        self.item=None
    def parse_(self,line):
        if len(line)==0:
            return (True,None)
        if self.state==TurnParser.QUESTION:
            self.item=dict()
            self.item["question"]=line
            self.state=TurnParser.ANSWER
            return (True,None)
        else:
            self.item["answer"]=line
            self.state=TurnParser.QUESTION
            return (True,self.item)


class MulLineTurn(LineBasedParser):

    def __init__(self,readable,question=re.compile('^\s*\d')):
        LineBasedParser.__init__(self,readable)
        self.item=None
        self.question_pattern=question

    def parse_(self,line):
        if len(line)==0:
            return (True,None)
        if self.question_pattern.match(line):
            item=self.item;
            self.item=dict()
            self.item["question"]=line
            self.item["answer"]=[]
            return (True,item)
        else:
            if self.item is not None:
                self.item["answer"].append(line)
            return (True,None)
