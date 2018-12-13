from src.piper_pan import shell_runner


def hit_counter(barcodes):
    """
    :param barcodes: a dict {barcode:list of the paths of bam files}
    :return: a dict {barcodes:{genome:#hits,..., unmapped:#hits}}
        """
    counts = dict()
    for k in barcodes.keys():
        paths = barcodes[k]
        genomes = dict()
        for i in paths:
            command = f"samtools view {i}  | cut -f 3"
            list_gi = shell_runner(command)
            for gi in list_gi:
                if gi == '*':
                    gi = 'unmapped'
                current = genomes.setdefault(gi, 0)
                genomes[gi] = current + 1
        counts[k] = genomes
    return (counts)


def merge_bam(barcodes):
    """
    :param barcodes: a dict {barcode:list of the paths of bam files}
    :return: a dict {barcode:path to the file of merged bams}
    """
    barcodes_merged = dict()
    for k in barcodes.keys():
        paths_to_bam = ' '.join(barcodes[k])
        command = f"samtools merge -f {k}_merged.bam {paths_to_bam} | readlink -f {k}_merged.bam"  # readlink -f returns the path of the file
        path_to_merged = shell_runner(command)
        barcodes_merged[k] = path_to_merged
    return barcodes_merged


def hit_counter_from_list(filenames, barcode):
    """
    :param filenames: all files from a single barcode - just the same hit_counter but for a list of filenames
    :param barcode: the barcode associated to our experiment
    :return: a dict {genome:hits}
    """
    genomes = dict()
    for name in filenames:
        command = f"samtools view ./{barcode}/bams/{name}.bam  | cut -f 3"
        list_ids = shell_runner(command)
        for hit in list_ids:
            if hit == '*': hit = 'unmapped';
            current = genomes.setdefault(hit, 0)
            genomes[hit] += current + 1
    return genomes
