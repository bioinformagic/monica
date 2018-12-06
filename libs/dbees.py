from src.piper_pan import shell_runner
import requests
BASIC_URL='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=%s&rettype=fasta'

def make_db(gi_list):
    pass

def db_exist():
    pass

def db_slice():
    pass

def download_db(gi_list, PATH):
    query = BASIC_URL.format(','.join(gi_list))
    fastas_requests = requests.get(query)

    open(f"{PATH}dbfile.fa", 'w').write(fastas_requests.text)
