#!/usr/bin/python

import _thread
import time
import subprocess

# Define a function for the thread
def pri( threadName, delay):
    time.sleep(delay)
    subprocess.call(["python","dora","client"])
    print("client stopped")

def print_time( threadName, delay):
    subprocess.call(["python","dora","server"])
    print("server thread is about to stoppppppppppppppppppppppppppppppppppppppppppppppppp")

# Create two threads as follows
try:
   #_thread.start_new_thread(call_core, ("working" ))
   _thread.start_new_thread( pri, ("Thread-2", 30, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print("Error: unable to start thread")

while 1:
   pass
