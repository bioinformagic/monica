import wget
from ftplib import FTP
# import os
# import subprocess
# from multiprocessing import Pool


# class GoodOvernight()
# ....

def ftp_fasta(input_user):

    """ From GenBank or RefSeq id to assembly FTP fasta."""
    
    assert type(input_user) == str
    
    database_letters = input_user.split("_")
    point = database_letters[1].split(".")
    id_number = point[0]
    numbers = [id_number[i:i + 3] for i in range(0, len(id_number), 3)]

    path_init = "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/"
    url_test = "/".join([database_letters[0]] + numbers)
    path_all = path_init + url_test

    ftp = FTP("ftp.ncbi.nlm.nih.gov")
    ftp.login()
    ftp.cwd("genomes/all/" + url_test) # dir0 =
    entries = list(ftp.mlsd())
    entries.sort(key=lambda entry: entry[0], reverse=True)  # sort the versions and get the latest
    version_dir = entries[0][0]

    ls_files = []
    ftp.cwd(version_dir + "/") # dir_1 =
    ftp.retrlines("LIST", ls_files.append) # content_files =

    for entry_1 in ls_files:
        entry_1 = entry_1.split(" ")
        for element in entry_1:
            if version_dir + "_genomic.fna.gz" in element:
                file = wget.download(path_all + "/" + version_dir + "/" + element)
                break
    return file

if __name__ == "__main__":
    output = ftp_fasta("GCA_002002055.1") # define user input here + add Pool
    print(output)



# Note by Alessio: ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/README_assembly_summary.txt





