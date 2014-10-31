#! /usr/bin/env python
"""
Created on Sep 10, 2014

@author syekabathula@paypal.com

Sreekanth Yekabathula

"""

#These are needed by the multiprocessing scheduler
from multiprocessing import Queue
import multiprocessing
import commands
import sys
import logger
import time
import subprocess

#These are specific jobs requirement
import os
import re

 
def RunCommand (fullCmd, logfile, statuslog):
    try:

        pid = subprocess.Popen(fullCmd , stdout=subprocess.PIPE, shell=True)
        output, errors = pid.communicate()
        exitcode = pid.returncode

        #Writing to Status log
        logger.logger(statuslog, "command is " + fullCmd, "debug")
        logger.logger(statuslog, "EXITCODE: " + str(exitcode), "critical")
        logger.logger(statuslog, "STDOUT: " + str(output), "info")
        logger.logger(statuslog, "STDERR: " + str(errors), "error")

        #Writing to package log
        logger.logger(logfile, "command is " + fullCmd, "debug")
        logger.logger(logfile, "EXITCODE: " + str(exitcode), "critical")
        logger.logger(logfile, "STDOUT: " + str(output), "info")
        logger.logger(logfile, "STDERR: " + str(errors), "error")

        return output
    except:
        return "Error executing command %s" %(fullCmd)

        
class Queue(multiprocessing.Process):
 
    def __init__(self,
            request_queue,
            result_queue,
            statuslog,
          ):
        # base class initialization
        multiprocessing.Process.__init__(self)
        self.request_queue = request_queue
        self.result_queue = result_queue
        self.statuslog = statuslog
        self.kill_received = False
 
    def run(self):
        while (not (self.kill_received)) and (self.request_queue.empty()==False):
            try:
                job = self.request_queue.get_nowait()
            except:
                break
            (logfile,runCmd) = job
            rtnVal = RunCommand(runCmd, logfile, self.statuslog)
            self.result_queue.put(rtnVal)

            
def execute(jobs, statuslog, num_processes=2):
    # load request queue
    request_queue = multiprocessing.Queue()
    for job in jobs:
        request_queue.put(job)
 
    # create a queue to store the results
    result_queue = multiprocessing.Queue()
 
    # spawn workers
    worker = []
    for i in range(num_processes):
        worker.append(Queue(request_queue, result_queue, statuslog))
        worker[i].start()
    
    # collect the results from the queue
    results = []
    while len(results) < len(jobs): #Beware - if a job hangs, then the whole program will hang
        result = result_queue.get()
        results.append(result)
    results.sort() # The tuples in result are sorted according to the first element - the jobid
    return (results) 

 
#MAIN 
if __name__ == "__main__":
    
    starttime = time.time() #Code to measure time
    #Test jobs
    jobs = [('ls.log','ls'), ('pwd.log','pwd'), ('lsltr.log', 'ls -ltr')]

    # run
    numProcesses = 10
    #Test Run
    results = execute(jobs, 'jobstatus.log', numProcesses) #job list and number of worker processes

    print "Time taken = %f" %(time.time()-starttime) #Code to measure time

