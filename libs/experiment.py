import os
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
        self.dirname = dirname
        self.database = dbees.make_db(gi_list)
        self.threads = threads
        self.barcodes = dict()
        self.status = None
        for i in range(num_barcodes):
            barcode = 'BC' + str(i)
            self.barcodes[barcode] = list()

    def query(self, filename):
        """
        :param filename: string, $(basename filename) stripped extension fastq
        function that:
        - prepares the magic-blast query
        - transform the sam output into bam
        - counts occurrences and calls self._stream to output everything
        - set the status to processing
        - reset the status to ready when finished
        """
        self.status = "processing"

        # launch the magicblast query for the specific file
        file_query = f'magicblast -query ./{filename} -db {self.database} -outfmt sam | ' \
                     f'samtools view -Sb -o {self.dirname}/bams/{filename}.bam -'
        magicblast_sam = subp.check_output(file_query, shell=True)

        self._stream()

        self.status = "ready"


    def _stream(self):
        """
        This funtion takes in bams from /bams/newbams
        for each file in the directory
        calls bammer.hit_counter(self.barcodes)
        yields the dictionary produced by hit_counter
        :return:
        """

        yield bammer.hit_counter(self.barcodes)