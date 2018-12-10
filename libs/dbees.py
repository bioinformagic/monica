from src.piper_pan import shell_runner
import requests
import pandas as pd
import ncbi_genome_download as ngd


# BASIC_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=%s&rettype=fasta'

def make_db(id_list):
    pass


def db_exist(id_list):
    """
    checks if a database already exists within the dblisting.csv (updated everytime a blastdb is downloaded and created)
    :param id_list list: list of IDs picked by the user
    :return: tuple (covered_ids, covered_dbs, non_covered)
    """
    with pd.read_csv("dblisting.csv", header=0) as dblisting:
        covered_ids = dblisting.ID.loc[dblisting.ID.isin(id_list)].tolist()
        covered_dbs = dblisting.database.loc[dblisting.ID.isin(covered_ids)].tolist()

    # list the difference between the user list and the ones found locally
    non_covered = list(set(id_list).difference(covered_ids))

    return covered_ids, covered_dbs, non_covered


def db_slice():
    """
    by using blastdb_aliastools makes a slice of another db based on the seqsID
    :return:
    """
    pass


def write_to_dblisting(id_list):
    """
    writes to dblistings new ids and their associated databases
    :param id_list:
    :return:
    """
    pass


def download_db(taxids, PATH, exp_name):
    """
    Downloads and create a BLAST database in the $BLASTDB path

    :param taxids: list of identifiers for your sequences (taxids)
    :param PATH: PATH to where your fasta file will be downloaded
    :param exp_name: name of the Experiment that will be used to name the database
    :return: None
    """
    # TODO exp_name may be changed to a uuid
    joint_gi = ','.join(taxids)
    #
    query = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={joint_gi}&rettype=fasta'
    fastas_requests = requests.get(query)

    # saving the output of requests into a file
    db_file = f"{PATH}/dbfile.fa"
    open(db_file, 'w').write(fastas_requests.text)

    # mounting the command for makeblastdb
    make_db_cmd = f'makeblastdb -in {db_file} -dbtype nucl -out $BLASTDB/{exp_name} -parse_seqids'

    shell_runner(make_db_cmd)
    # TODO add the dblisting writing after download

    return None


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