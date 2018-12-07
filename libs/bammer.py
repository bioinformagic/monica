from src.piper_pan import shell_runner

def hit_counter(barcodes):
    counts = dict()
    for k in barcodes.keys():
        paths = barcodes[k]
        genomes = dict()
        for i in paths:
            command = f"samtools view {i}  | cut -f 3"
            list_gi = shell_runner(command)
            list_gi = list_gi[:-1]
            for gi in list_gi:
                if gi == '*':
                    gi = 'unmapped'
                current = genomes.setdefault(gi, 0)
                genomes[gi] = current+1
        counts[k] = genomes
    return(counts)


def merge_bam(barcodes):
    barcodes_merged = dict()
    for k in barcodes.keys():
        paths_to_bam = ' '.join(barcodes[k])
        command = f"samtools merge -f {k}_merged.bam {paths_to_bam} | readlink -f {k}_merged.bam"   #readlink -f returns the path of the file
        path_to_merged = shell_runner(command)
        barcodes_merged[k] = path_to_merged[:-1]
    return barcodes_merged

