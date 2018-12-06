import os
import glob

class dir_list:

    def __init__(self, patt= os.getcwd()): #store file names in CWD, if the user doen't provide a pattern
        self.repo= os.chdir(patt)
        self.cur= [] #current list
        self.con = dict()  # content of the files
        self.new= self.new_files() #new file



    def new_files(self): #update the list of file AND highlight which are the new files AND check the content
        new= glob.glob("*.txt")
        left=list(set(new) - set(self.cur))
        self.cur = new
        self.new=left
        self.con.update(self.content())
        return left

    def content(self): #read the content of the newly found files
        new_cont= dict()
        for i in self.new:
            with open(i, "r") as f:
                key=f.read()
            new_cont[i]=key
        return  new_cont





if __name__ == "__main__":
    m=dir_list()
    for i in range(1000000000):
        if len(m.new) != 0:
            print(m.cur, m.new, m.con)
        m.new_files()
