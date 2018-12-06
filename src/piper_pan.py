__doc__="""Main python file for calling and maintaining the pipeline. 

#THIS PIPELINE NEVER GROWS OLD
"""

import subprocess
from subprocess import PIPE
import sys

def read_MK_info():

    # function to read the directory information of the user_conf (json)
    return None

def run_deepbinner(args, inp_folder):
    #Function to run deepbinner from bash --> giving with it selected args
    #deepbinner command creator
    return None


def shell_runner(cmd):
    try:
        command = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
        command = command.decode("utf-8").split(sep="\n")
        return command
    except subprocess.CalledProcessError as e:
        print(e.ouput)
        sys.exit(1)

