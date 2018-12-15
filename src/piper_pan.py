__doc__ = """Main python file for calling and maintaining the pipeline. 

#THIS PIPELINE NEVER GROWS OLD (Besides maybe the tools used ^^)
Built with <3 by Bioinformatics Bachelor Class of 2015, La Sapienza, 2018
"""

import subprocess
import sys
import json
import os


#debug

import random
#debug end

def read_MK_info(conf_file='/opt/ONT/MinKNOW/conf/user_conf'):
    #Reads data from the user_conf file of the MiniKnow application (Optoinal conf_file can be loaded)
    with open(conf_file) as json_data:
        conf_params = json.load(json_data)

    return conf_params['user']['output_dirs']['base']['value0']


def run_deepbinner(experiment, cpuonly):
    #Method for initiating deepbinner that assembles the code and starts the process
    basecommand = "deepbinner realtime"
    in_dir = read_MK_info()
    out_dir = experiment.dirname
    if cpuonly:
        gpu = "0"
    else:
        gpu = "1"

    command = basecommand+" --indir "+in_dir+" --outdir "+out_dir+" --rapid "+" --device_count "+gpu
    shell_runner_realtime(experiment.running_processes,"DeepBinner", command)
    # Function to run deepbinner from bash --> giving with it selected args
    # deepbinner command creator
    return None



def run_chiron():

    return None

def shell_runner(cmd):
    # general function than takes a shell command and returns a list of strings with the output
    try:
        command = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
        command = command.decode("utf-8").strip().split(sep="\n")
        return command
    except subprocess.CalledProcessError as e:
        print(e.ouput)
        sys.exit(1)


def shell_runner_realtime(processlist, application, cmd):
    # realtime running of bash commands and saving the process object to the experiment class so it can be canceled afterwards
    try:
        processlist.append([application,subprocess.Popen(cmd,shell=True, executable='/bin/bash')])
        # run commmand and add a list object to the experiment.process with [PID,AppName,ProcessObj]
    except subprocess.CalledProcessError as e:
        print(e.ouput)
        sys.exit(1)

def shell_realtime_stopper(processlist):
    #Read all the objects form the experiment class that holds the processes and ends them.
    for process_info in processlist:
        try:
            process_info[1].kill()
            processlist.pop(process_info)

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            print(e.ouput)
            sys.exit(1)

    return None


def albacore_watchdog():
    #
    #function that checks if the files of this
    return None

def albacore_runner():
    # get all the directories in the directory (check also for new ones) and run an instance of albacore
    # while albacore watchdog returns true rerun the finished albacore instance
    return None


def test_wd_albacore(directory, experiment=None):
    f5_basecalled = []
    output = []
    procdir = os.path.join(directory,"processing")
    os.makedirs(procdir,exist_ok=True)
    while experiment.status == "processing":

        #loop for one run of basecaller (taking snapshot of current de-multiplexed folder)
        #reset the processing data in the beginning of the loop
        processing = []

        #get difference between files created from DeepBinner and Files that got already basecalled
        diff_files = set(get_files(directory)) - set(f5_basecalled)

        for file in diff_files:
            os.symlink(os.path.join(directory,file),os.path.join(procdir,file))
            processing.append(file)
            #for each not basecalled file create a symlink in the processing dir and add it to the processing list

        #run the albacore runner function that returns a list of the processed files by albacore
        proc_fq = albacore_runner(experiment.dirname)
        f5_basecalled = f5_basecalled + processing
        #prepare output as couple of fast5 and corresponding fastq files
        output.append([processing,proc_fq])

        #cleanup the symlinks in the processing directory (maybe delete)
        for link in get_files(procdir):
            os.remove(os.path.join(procdir,link))

    return output

# def test_lowest(fname,dir,dbim):
#     #imitated DB and create new files outside processing
#
#     shell_runner(("touch %s/db_%s") % (dbim, fname))
#     shell_runner(("touch %s/db_%s") % (dbim, fname+1))
#     curr_files = get_files(dir)
#     #imitate albacore dir => target dir
#     for i in random.sample(range(100),3):
#         shell_runner(("touch %s/bc_%s") % (dir,i))
#     shell_runner("sleep 2")
#     #return created files
#     output = list(set(get_files(dir)) - set(curr_files))
#
#     return output

def get_files(directory):
    for _, _, files in os.walk(directory):
        return files

if __name__ == '__main__':
    test_dir =  '/Users/jan.delshad/Documents/Uni/S5_BPP/test/1'
    print(test_wd_albacore(test_dir))