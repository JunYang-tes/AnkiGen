from Parser import *
from Formatter import HTML,RegHTML,RegStyle
import sys
import json
import io
import re
def parse(file):
    p=Parser(file)
    items=p.parse()
    ret=json.dumps(items,ensure_ascii=False,indent=4);
    f=io.open(file+".json",'w')
    f.write(ret)
    f.close()
    return items

def format(items,writer,formatter):
    for item in items:
        writer.write("\t".join(formatter.format(item["question"],item["answer"]))+"\n")


if __name__=='__main__':
    if len(sys.argv)==2:
        script,file=sys.argv
        input_file=io.open(file,encoding='utf-8')
        #parser = SeparatorParser(input_file,sp=['='])
        parser = MulLineTurn(input_file)
        #parser = Parser(io.open(file,encoding='utf-8'))
        parser = TurnParser(input_file)
        '''formatter = RegHTML(
            question_style=[
                RegStyle(re.compile('[a-zA-Z \-,]+'),'#2483E4')
            ],
            answer_style=[
            RegStyle(re.compile('^\s*[a-zA-Z\-]*\s[a-zA-Z]{1,4}\.'),'red'),
            RegStyle(re.compile('.*'),'#00FFC4')
        ])'''
        formatter = HTML('blue')
        #parser=TextRank(input_file)

        format(parser.parse(),io.open(file+".fmt.txt",'w',encoding='utf-8'),formatter)
    else:
        print 'Usage:%s filename'%(sys.argv[0])