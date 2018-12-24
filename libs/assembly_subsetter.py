import subprocess as sbp
import os
from ete3 import NCBITaxa
import pandas as pd
import wget
import datetime as dt
import gzip
from Bio import  SeqIO as seq


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
        self.index='out.mmi'
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
            for x in self.ftps:
                if x[1].split('/')[-1] not in os.listdir():  #if the file is not present in the folder 
                    wget.download(x[1]) #download using ftp
                else:
                   pass
        os.chdir(self.home_path)

    def genomes_updated(self):
        if not os.listdir(self.genomes_path):
            return 0
        return 1
    # def genus_tag(self):
    #     path_to_fasta= 'db.fasta' #name of the file eventually created
    #     while len(os.listdir())!=1:
    #         with open(path_to_fasta, 'w+') as col:
    #             for x in self.ftps:
    #                 genus=x[0]
    #                 name=x[1].split('/')[-1] #name with extension
    #                 if name in os.listdir(os.getcwd()):
    #                     with gzip.open(name, 'rt') as handle:
    #                             f = seq.parse(handle, 'fasta')
    #                             for  index , value in enumerate(f):
    #                                     Value=[]
    #                                     value.id = genus+ '_'+ str(index)
    #                                     value.name = genus + '_'+ str(index)
    #                                     value.description = genus+ '_'+ str(index)
    #                                     Value.append(value)
    #                                     seq.write(Value, col, 'fasta')
    #                     os.remove(name)
    #                 else:
    #                      pass
    #     sbp.Popen('gzip ' + path_to_fasta, shell=True)

    def indexing(self):
        os.chdir(self.genomes_path)
        sbp.Popen(f'minimap2 -d {self.index} db.fasta.gz', shell=True)
        os.chdir(self.home_path)





if __name__ == '__main__':

    rs=AssemblySubsetter()
    rs.indexing()


