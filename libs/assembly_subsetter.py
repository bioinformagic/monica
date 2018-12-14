import subprocess as sbp
import os
from ete3 import NCBITaxa
import pandas as pd
import wget
import datetime as dt

ncbi=NCBITaxa()

PARENTS=['Fungi','Oomycota','Bacteria','Archaea','Viruses','Viroids','Nematodes','Rhizaria','Alveolata','Heterokonta']
PATHS=['genomes','magic_tables']
assembly_refseq_table_ftp='ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt'
assembly_genbank_table_ftp='ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/assembly_summary_genbank.txt'
TABLE_HEADER_LINE=1
HOME=os.getcwd()

class AssemblySubsetter():
    ''' Gonna write the documentation, I swear it'''
    def __init__(self, parents=PARENTS, genomes=PATHS[0], tables=PATHS[1], header_line=TABLE_HEADER_LINE, refseq_summary_ftp=assembly_refseq_table_ftp, genbank_summary_ftp=assembly_genbank_table_ftp, home_path=HOME):
        self.parents=parents
        self.descendants = []
        self.home_path=home_path
        self.genomes_path= f'{self.home_path}/{genomes}'
        self.tables_path= f'{self.home_path}/{tables}'
        self.refseq_summary_ftp=refseq_summary_ftp
        self.genbank_summary_ftp=genbank_summary_ftp
        self.header_line=header_line
        self.ftps=[]
        self.refseq_table=None
        self.genbank_table=None
        self.genera=[]
        for path in [self.genomes_path, self.tables_path]:
            if not os.path.exists(path):
                os.mkdir(path)

    def descendants_finder(self):
        for parent in self.parents:
            for i in ncbi.get_descendant_taxa(parent):
                self.descendants.append(i)

    def tables_fetcher(self):
        os.chdir(self.tables_path)
        if not self.tables_updated():
            wget.download(self.refseq_summary_ftp)
            wget.download(self.genbank_summary_ftp)
            with open ('log', 'w+') as log:
                log.write(str(dt.date.today()))
        os.chdir(self.home_path)

    def tables_updated(self):
        if not os.listdir(self.tables_path):
            return 0
        with open('log', 'r') as log:
            date=log.read()
        date=dt.datetime.strptime(date,'%Y-%m-%d')
        delta=dt.datetime.now()-date
        if delta.days>7:
            return 0
        return 1

    def tables_importer(self):
        if not (self.refseq_table or self.genbank_table):
            self.tables_fetcher()
        self.refseq_table=pd.read_table(f'{self.tables_path}/{self.refseq_summary_ftp.split(sep="/")[-1]}', header=self.header_line, low_memory=False)
        self.genbank_table=pd.read_table(f'{self.tables_path}/{self.genbank_summary_ftp.split(sep="/")[-1]}', header=self.header_line, low_memory=False)

    def merger(self):
        if not self.refseq_table:
            self.tables_importer()
        if not self.descendants:
            self.descendants_finder()

        taxids=pd.DataFrame(self.descendants, columns=['taxid'])
        self.refseq_table = self.refseq_table.merge(taxids, on='taxid')

        for name in self.refseq_table['organism_name']:
            self.genera.append(name.split(sep=' ')[0])
        self.refseq_table['genera']=self.genera

        self.refseq_table=self.refseq_table.drop_duplicates(subset=['genera'], keep='last')

        for genus, ftp in zip(self.refseq_table.iloc[:,-1], self.refseq_table.iloc[:,-2]):
            self.ftps.append((genus, ftp))

    def genomes_fetcher(self):
        os.chdir(self.genomes_path)
        if not self.genomes_updated():
            #enters here when genomes path is empty or to be updated
            pass
        os.chdir(self.home_path)

    def genomes_updated(self):
        if not os.listdir(self.genomes_path):
            return 0
        return 1
    def genus_tag(self.ftps):
        for x in self.ftps:
            genus=x[0]
            name=x[1].split('/')[-1] #name with extension
            name_ext=('.').join(name.split('.')[:-1]) #namewithoutextension
            f_name= name_ext[:-4]+'_'+genus+'.fna' #finalnamewithgenus
            if name in os.listdir(os.getcwd()):
                with gzip.open(name, 'rt') as handle: #poen the zip file
                    with open(f_name, 'w') as file:
                        f = seq.parse(handle, 'fasta')
                        Value = []
                        for  index , value in enumerate(f):
                                value.id = genus+ '_'+ str(index) #index modification
                                value.name = genus + '_'+ str(index)
                                value.description = genus+ '_'+ str(index)
                                Value.append(value)
                                seq.write(Value[-1], file, 'fasta') #re-add sequences to a newfile with updated name 
                sbp.Popen('gzip ' + f_name, shell=True) #zip new file
                os.remove(name)#remove old file
            else:
                pass



if __name__ == '__main__':

    rs=AssemblySubsetter()
    rs.merger()

