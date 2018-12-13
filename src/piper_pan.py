__doc__ = """Main python file for calling and maintaining the pipeline. 

#THIS PIPELINE NEVER GROWS OLD (Besides maybe the tools used ^^)
Built with <3 by Bioinformatics Bachelor Class of 2015, La Sapienza, 2018
"""

import subprocess
import sys
import json


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


def shell_runner(cmd):
    # general function than takes a shell command and returns a list of strings with the output
    try:
        command = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
        command = command.decode("utf-8").split(sep="\n")
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
