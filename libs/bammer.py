from src.piper_pan import shell_runner

def hit_counter(barcodes):
    counts = dict()
    for k in barcodes.keys():
        paths = barcodes[k]
        genomes = dict()
        for i in paths:
            print(i)
            command = f"samtools view {i}  | cut -f 3"
            list_gi = shell_runner(command)
            list_gi = list_gi[:-1]
            print(list_gi)
            for gi in list_gi:
                if gi == '*':
                    gi = 'unmapped'
                current = genomes.setdefault(gi, 0)
                genomes[gi] = current+1
        counts[k] = genomes
    return(counts)

