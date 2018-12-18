from src.piper_pan import shell_runner
import wget
import pandas as pd
import re



# BASIC_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=%s&rettype=fasta'

def make_db(id_list):
    pass


# def db_exist(id_list):
#     """
#     checks if a database already exists within the dblisting.csv (updated everytime a blastdb is downloaded and created)
#     :param id_list list: list of IDs picked by the user
#     :return: tuple (covered_ids, covered_dbs, non_covered)
#     """
#     with pd.read_csv("dblisting.csv", header=0) as dblisting:
#         covered_ids = dblisting.ID.loc[dblisting.ID.isin(id_list)].tolist()
#         covered_dbs = dblisting.database.loc[dblisting.ID.isin(covered_ids)].tolist()
#
#     # list the difference between the user list and the ones found locally
#     non_covered = list(set(id_list).difference(covered_ids))
#
#     return covered_ids, covered_dbs, non_covered
#
#
# def db_slice():
#     """
#     by using blastdb_aliastools makes a slice of another db based on the seqsID
#     :return:
#     """
#     pass
#
#
# def write_to_dblisting(id_list):
#     """
#     writes to dblistings new ids and their associated databases
#     :param id_list:
#     :return:
#     """
#     pass


def download_db(taxids, exp_name):
    """
    Downloads and create a database in the $DB

    :param taxids: list of identifiers for your sequences (taxids)
    :param exp_name: name of the Experiment that will be used to name the database
    :return: None
    """
    taxids = ','.join(taxids)
    query = f'elink -db taxonomy -id {taxids} -target assembly | esummary | xtract -pattern FtpPath_RefSeq -element FtpPath_RefSeq'
    genome_directory = shell_runner(query)
    create_directory = f'mkdir -p $DB/{exp_name}'
    shell_runner(create_directory)
    
    fasta_list=[]
    for url in genome_directory:
        fasta_name = url.split('/')[-1] + '_genomic.fna.gz'
        wget.download(url+"/"+fasta_name, out=f'$DB/{exp_name}')
        fasta_list.append(fasta_name)
    fasta_list = ' '.join(fasta_list)
    concatenate = f'cat {fasta_list} > $DB/{exp_name}/concatenated.gz'
    shell_runner(concatenate)
    path = '$DB/{exp_name}/concatenated.gz'
    minimap_indexing(exp_name, path)
    
    # merge every file into a unique gz file
    # pass this file to minimap indexer
    
def minimap_indexing(dbname, path):
    '''
    Create minimap index
    :param dbname: name of the database
    :param path: path to the compressed file containing genome sequences of interest
    :return: None
    '''
    index_cmd = f'minimap2 -d $DB/{dbname}.mmi {path}'
    shell_runner(index_cmd)

def import_blastdb(path):
    """
    moves/copies the db from path to $BLASTDB
    :param path:
    :return:
    """
    pass


def check_db_integrity():
    """
    checks if BLASTDB has all the db listed in dblisting.csv, returns error otherwise
    :return bool:
    """
    pass

def names_to_taxid(names):
    """
    accepts a list of common names and returns a list of taxids
    :param names:
    :return:
    """
    with pd.read_csv('refseq_translator.tsv', header=0, sep='\t') as refseq:
        taxids = refseq.taxid.loc[refseq.organism_name.isin(names)].tolist()

    return taxids


