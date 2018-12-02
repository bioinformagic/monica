import wget
from ftplib import FTP
import os
import subprocess
from multiprocessing import Pool


# class GoodOvernight()
# ....

def ftp_fasta(input_user):

    """ From genseq or refseq id to assembly FTP fasta."""

    assert type(input_user) == str

    letter = input_user.split("_")
    point = letter[1].split(".")
    point_0 = point[0]
    number = [point_0[i:i + 3] for i in range(0, len(point_0), 3)]

    path_init = "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/"
    url_test = letter[0] + "/" + number[0] + "/" + number[1] + "/" + number[2]
    path_all = path_init + url_test

    ftp = FTP("ftp.ncbi.nlm.nih.gov")
    ftp.login()
    ftp.cwd("genomes/all/" + url_test) # dir0 =
    entries = list(ftp.mlsd())
    entries.sort(key=lambda entry: entry[0], reverse=True)
    version_dir = entries[0][0]

    ls_1 = []
    ftp.cwd(version_dir + "/") # dir_1 =
    ftp.retrlines("LIST", ls_1.append) # content_files =

    for entry_1 in ls_1:
        entry_1 = entry_1.split(" ")
        for element in entry_1:
            if version_dir + "_genomic.fna.gz" in element:
                file = wget.download(path_all + "/" + version_dir + "/" + element)
                # assert os.path.exists("./file")
                return file


if __name__ == "__main__":
    output = ftp_fasta("GCA_002002055.1") # define user input here + add Pool
    print(output)



# Note by Alessio: ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/README_assembly_summary.txt


