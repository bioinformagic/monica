import subprocess
import os
import xml.etree.ElementTree as parXML
import wget

class GoodOvernight():
    def  __init__(self):
        pass

    def unmapped_extractor(exp_output, unmapped_path): #this creates fasta files over unmapped bam sequences
        list_bam_files = []
        for file in os.listdir(exp_output):
            if file.endswith('.bam'):
                list_bam_files.append(file)
        for element in list_bam_files:
            subprocess.Popen('samtools fasta -f 4 ' + exp_output + '/' + element + ' > ' + unmapped_path + '/' + element[:-4] + '_unmapped.fasta',shell=True)

    def biomarter(list):
        wget.download('https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.xml?method=db2db&format=row&input=geneid&inputValues=' + ','.join(list) + '&outputs=refseqgenomicgi')#This line of code downloads from db2db a xml file  with a specific filename
        #that is biodbnetRestApi.xml
        file = 'biodbnetRestApi.xml'
        root = parXML.parse(file).getroot() #this line initializes the xml file so to be parsed
        levels = root.findall('.//item')
        ee = dict()
        for level in levels:
            GeneId = level.find('InputValue').text
            Transformed = filter(None, str(level.find('RefSeqGenomicGI').text).split('//'))
            ee[GeneId] = Transformed
        #the previous for loop for every level so 'Gene' we may have 1 or different outputs from the sitethat are stored into Transformed and I create a dictionary knowing this datas
        with open(file[:-4] + '_biomarter_output.txt', 'w') as out:
            for gene in ee.keys():
                for value in ee[gene]:
                    out.write(gene + ' ' + value + '\n')
        os.remove(file)
        #This creates a txt file as Gene and Ids

#example GoodOvernight.unmapped_extractor('/home/pepsi/Documents/Università/Bioinformatics2/mapped', '/home/pepsi/Documents/Università/Bioinformatics2/unmapped')
#example GoodOvernight.biomarter([])

    def master_blaster():

    """Blast the unmapped reads and returns the GenBank IDs"""

        id_list = []
        # os.chdir("~Desktop/unmmaped_fasta")
        blasting = subprocess.call("ls *.fa | parallel 'blastn -query {} -db nt -remote -num_alignments 1 -outfmt 6 -out {.}.out'", shell = True)
        get_id = subprocess.call("cut -f 2 *.out > list_ids.txt", shell = True)
        with open("list_ids.txt") as file:
            output = [id_list.append(line.strip()) for line in file]

        return id_list
    
    
if __name__ == "__main__":
    goodOvernight = GoodOvernight()
        
        
