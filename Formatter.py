import types
import re
class Formatter:
    def __init__(self):
        pass
    def format(self,question,answers):
        pass
class HTML(Formatter):
    def __init__(self,color_question):
        self.color_question=color_question,
    def format(self,question,answers):
        ret=[]
        if isinstance(answers,(types.ListType)):
            for ans in answers:
                idx= ans.find(question)
                if idx!=-1:
                    ans=ans[:idx]+(u"<font color='%s'>" %(self.color_question))+ans[idx:idx+len(question)]+u"</font>"+ans[idx+len(question)]
                ret.append(ans)
        else:
            ret.append(answers)
        return (("<font color='%s'>"%(self.color_question))+question+u'</font>',u"<br/>".join(ret))
class RegStyle:
    def __init__(self,pattern,color):
        self.pattern=pattern
        self.color=color

class RegHTML(Formatter):
    def __init__(self,question_style=[RegStyle(re.compile('[a-zA-Z\-]+'),'red')],answer_style=[]):
        self.question_style=question_style
        self.answer_style = answer_style
    def format(self,question,answers):
        ret=[]
        question=self.line(self.question_style,question)
        if isinstance(answers,(types.ListType)):
            for ans in answers:
                ret.append(self.line(self.answer_style,ans))
        return (question,"<br/>".join(ret))
    def line(self,styles,line):
        ret=[]
        for style in styles:
            m= style.pattern.search(line)
            if m is not None:
                start=m.start()
                end=m.end()
                return line[:start]+("<font color='%s'>%s</font>"%(style.color,line[start:end]))+line[end:]
        return line