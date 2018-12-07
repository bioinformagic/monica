from src.piper_pan import shell_runner
import requests


# BASIC_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=%s&rettype=fasta'

def make_db(gi_list):
    pass


def db_exist():
    pass


def db_slice():
    """
    by using blastdb_aliastools makes a slice of another db based on the seqsID
    :return:
    """
    pass


def download_db(gi_list, PATH, exp_name):
    """
    Downloads and create a BLAST database in the $BLASTDB path

    :param gi_list: list of identifiers for your sequences (both GI and refseq ID and Assembly accession)
    :param PATH: PATH to where your fasta file will be downloaded
    :param exp_name: name of the Experiment that will be used to name the database
    :return: None
    """
    joint_gi = ','.join(gi_list)
    query = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={joint_gi}&rettype=fasta'
    fastas_requests = requests.get(query)

    # saving the output of requests into a file
    db_file = f"{PATH}/dbfile.fa"
    open(db_file, 'w').write(fastas_requests.text)

    # mounting the command for makeblastdb
    make_db_cmd = f'makeblastdb -in {db_file} -dbtype nucl -out $BLASTDB/{exp_name} -parse_seqids'

    shell_runner(make_db_cmd)

    return None
