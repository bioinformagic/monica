import os
from ete3 import NCBITaxa
import pandas as pd

ncbi=NCBITaxa()

PARENTS=['Fungi','Oomycota','Bacteria','Archaea','Viruses','Viroids','Nematodes','Rhizaria','Alveolata','Heterokonta']
PATHS=['refseq_path','magic_table_path']
assembly_refseq_table_ftp='ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt'
TABLE_HEADER_LINE=1


class RefseqSubsetter():
    def __init__(self,parents=PARENTS,refseq_path=PATHS[0],table_path=PATHS[1],header_line=TABLE_HEADER_LINE, refseq_summary_ftp=assembly_refseq_table_ftp):
        self.parents=parents
        self.descendants = [i for i in (ncbi.get_descendant_taxa(parents))]
        self.refseq_path=f'{os.getcwd()}/{refseq_path}'
        self.table_path=f'{os.getcwd()}/{table_path}'
        self.refseq_summary_ftp=refseq_summary_ftp
        self.header=''
        self.header_line=header_line
        self.table=None
        for path in PATHS:
            if not os.path.exists(path):
                os.mkdir(path)

    #def headerfinder(self):
    #    with open('assembly_summary_refseq.txt', 'r') as file:
    #        for i, line in enumerate(file):
    #            if i == self.header_line:
    #                 self.header= line.split(sep='\t')
    #            elif i > self.header_line:
    #                break

    def table_fetcher(self):
        pass

    def table_importer(self):
        #if not self.header:
        #    self.headerfinder()
        if not self.table:
            self.table_fetcher()
        else:
            self.table=pd.read_table(self.table_path, header=self.header_line, low_memory=False)

    def merger(self):
        if not self.table:
            pass
        else:
            taxids=pd.DataFrame.from_records(self.descendants, columns=['taxid'])
            self.table=self.table.merge(taxids, on='taxid')
            ftps=self.table['ftp_path']
        
     def ftp_downlaod(ftps):
        for ftp in ftps:
            wget.download(ftp)


if __name__ == '__main__':
   pass
