import os
import libs.dbees as dbees
import libs.bammer as bammer
from src.piper_pan import shell_runner, stop_deepbinner

MAGIC_BLAST = 'magicblast -query ./%s.fastq -db %s -splice F -outfmt sam | samtools view -B -o %s/bams/%s.bam -'


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
                 num_barcodes=12,
                 max_hours=48,
                 ):

        self.dirname = dirname
        self.database = dbees.make_db(gi_list)
        self.threads = threads
        self.barcodes = dict()
        self.status = None
        self.time = max_hours
        self.running_processes = list()
        for i in range(num_barcodes):
            barcode = 'BC' + str(i)
            self.barcodes[barcode] = list()

    def query(self, filename, barcode):
        """
        :param filename: string, $(basename filename .fastq) stripped extension fastq
        function that:
        - prepares the magic-blast query
        - transform the sam output into bam
        - counts occurrences and calls self._stream to output everything
        - set the status to processing
        - reset the status to ready when finished
        """
        self.status = "processing"

        # launch the magicblast query for the specific file
        # -splice F cause it is not freaking RNA
        file_query = f'magicblast -query ./{filename}.fastq -db {self.database} -splice F -outfmt sam | ' \
                     f'samtools view -B -o {self.dirname}/bams/{filename}.bam -'

        shell_runner(file_query)

        # add filename to the list of barcodes
        self.barcodes[barcode].append(filename)

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

    def end_realtime(self):
        """
        checks if experiment is over (by self.status), then merge_bams into 12 different bams
        :return:
        """
        if self.status == "finished":
            bammer.merge_bams(self.barcodes)
            stop_deepbinner()
            stop_albacore()
        else:
            print("Can close a running experiment, try to STOP it first.")
