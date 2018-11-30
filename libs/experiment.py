import os
import glob
import subprocess as subp
# import dbees
# import bammer

class Experiment():
    """
    class that manages information about:

    - directory where files are stored
    - database to query against
    - number of threads to use
    - files organized per barcode
    - status of the experiment (ready | processing | finished)
    - bam files organization and final merging
    - streaming data to the web ui


    """

    def __init__(self,
                 dirname=os.getcwd(),
                 gi_list="",
                 threads=1,
                 num_barcodes=12):
        # TODO strip files from extensions
        self.dirname = dirname
        self.database = dbees.make_db(gi_list)
        self.threads = threads
        self.barcodes = dict()
        self.status = None
        for i in range(num_barcodes):
            barcode = 'BC' + str(i)
            barcode_glob = f"./{barcode}*"
            self.barcodes[barcode] = glob.glob(barcode_glob)

    def query(self):
        """
        function that:
        - prepares the magic-blast query
        - transform the sam output into bam
        - counts occurrences and calls self._stream to output everything
        - set the status to processing
        - reset the status to ready when finished
        """
        self.status = "processing"
        for barcode, filelist in self.barcodes.items():
            for filename in filelist:
                file_query = f'magicblast -query ./{filename} -db {self.database} -outfmt sam | ' \
                             f'samtools view -Sb - > {self.dirname}/bams/{filename}.bam'
                magicblastsam = subp.check_output(file_query, shell=True)

        self._stream()

        self.status = "ready"


    def _stream(self):
        pass