__doc__="""Main python file for calling and maintaining the pipeline. 

#THIS PIPELINE NEVER GROWS OLD
"""

import subprocess
from subprocess import PIPE

def read_MK_info():

    # function to read the directory information of the user_conf (json)
    return somedata

def run_deepbinner(args, inp_folder):
    #Function to run deepbinner from bash --> giving with it selected args
    #deepbinner command creator



def shell_runner(cmd):
    command = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stderr=PIPE, stdout=PIPE)
    return  command.communicate()