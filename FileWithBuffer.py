class File:
    def __init__(self,readable):
        self.readable=readable
        self.buf=[]
    def unread(self,line):
        self.buf.append(line)
    def readline(self):
        if len(self.buf)>0:
            return self.buf.pop()
        return self.readable.readline()
    def __iter__(self):
        return It(self);
class It:
    def __init__(self,file):
        self.file=file
    def next(self):
        ret=self.file.readline()
        if  len(ret)==0:
            raise StopIteration
        return ret
    def __iter__(self):
        return self;