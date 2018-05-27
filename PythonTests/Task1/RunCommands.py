# Eric Lynch https://github.com/mxmstr

import os, time
from subprocess import Popen, PIPE


sudo_password = 'your_password' # Specify system password
processes = []
commands = [
    'sleep 3',
    'ls -l /',
    'find /',
    'sleep 4',
    'find /usr',
    'date',
    'sleep 5',
    'uptime'
]


# Open a process for each command w/ admin privileges
for command in commands:
    p = Popen(['sudo', '-S'] + [command], stdin=PIPE, stderr=PIPE, universal_newlines=True)
    p.communicate(sudo_password + '\n')[1]
    processes.append([p, command, None])


# Wait for each process to terminate
start = time.time() * 1000
num_processes = 0

while(num_processes < len(processes)):
    
    for process in processes:
        
        if process[0].poll() is not None and process[2] is None:
            elapsed = (time.time() * 1000 - start)
            #print(elapsed)
            process[2] = elapsed
            num_processes += 1
            

# Log timestamps
print()
print('Total time:', sum(round(p[2], 2) for p in processes))
print('Average time:', sum(round(p[2], 2) for p in processes) / len(processes))
print('Max time:', max(round(p[2], 2) for p in processes))
print('Min time:', min(round(p[2], 2) for p in processes))

for num, process in enumerate(processes):
    
    print()
    print('Command', num + 1)
    print('Text:', process[1])
    print('Elapsed time:', round(process[2], 2), 'ms')
            
        