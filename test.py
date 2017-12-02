#conda execute
#env:
# - python >=3
# - subprocess
import subprocess
from subprocess import check_output
from subprocess import call
from subprocess import check_call
from subprocess import Popen
from subprocess import PIPE
import time

#print check_output("dir", shell=True)
#for x in xrange(0, 1):
"""
	#create file for each iteration
	arg1 = "echo"
	arg2 = "test%s" %x
	arg3 = ">"
	arg4 = "file%s.txt" %x
	arg = [arg1, arg2, arg3, arg4]
	Popen(arg, shell=True)
	
	#command = "echo text%s>file%s.txt" %(x,x)


	#set up commands
	branch = 'git branch %s > NUL' %arg4
	checkout = 'git checkout %s > NUL' %arg4
	add = 'git add -A > NUL'
	commit = 'git commit -m "%s" > NUL' %arg2
	tag = 'git tag "user%s" > NUL' %x

	start_time = time.time()
"""
branch = 'python dora client'
r1 = Popen(branch, shell=True)
	#r2 = Popen(checkout, shell=True)
	#r2 = Popen(add, shell=True)
	#r3 = Popen(commit, shell=True)
	#r4 = Popen(tag, shell=True)


#end_time = time.time() - start_time

result = ""
	#parse the results to one var
print(result.join(str(r1.poll())))
	#result.join(str(r2.poll()))
	#result.join(str(r3.poll()))
	#result.join(str(r4.poll()))


	#call('echo %s >> time.txt' %end_time, shell=True)
	#print result on a new line or the same line, every
	#line will have a 1000 result
	#if (x%1000)== 0:
	#	call('echo %s >> results.txt' %result, shell=True)
	#else:
	#	call('echo|set /p="%s " >> results.txt' %result, shell=True)

	


