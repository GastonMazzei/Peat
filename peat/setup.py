from multiprocessing import cpu_count
from sys import exit
from os import remove

def exiter():
  print('INVALID ANSWER...')
  exit(1)
  return

def intro():
  mssg_0 = """

--------------------------------------------------------------------------------------------------------------------
...Hi. Welcome to Peat, the Intel-Optimized Tensorflow dockerization with CPU & Memory constraints configurator... |
-------------------------------------------------------------------------------------------------------------------|                                                                                                                   
                 TLDR: You'll have to answer 4 questions before the script begins                                  |
                                                                                                                   |  
--------------------------------------------------------------------------------------------------------------------
LONG TEXT:                                                                                                         |
If you have an Intel core (post 2000-smth ?2012? e.g. i7) AND a non-NVIDIA GPU then the Intel-Optimized-Tensorflow |
is the best way to accelerate your calculations. A modern implementation that does not require messy installations |
is available (and encouraged by Intel themselves) via an OS-Independent method call 'Dockerization'.               |
A non memory-&-CPU constrained out-of-the-box Dockerization may lead to a 100% core-utilization which makes running|
other tasks with the script in the background plainly-impossible.                                                  |
The aim of this script is to (1) allow users manually-set Core & Memory limits, and (2) run pythonic scripts that  |
use Tensorflow making use of the Intel Architecture Optimization                                                   |
--------------------------------------------------------------------------------------------------------------------
* Author isnt related to Google, Nvidia, Intel, Tensorflow or Python. github.com/GastonMazzei for comments or Bugs!
          """

  Q_1 = '\nQuestion 1 of 4: do you want to set limit values for RAM memory? (y/n)'
  m_1 = '(format: gigas)               e.g. "answer: 4.5"'
  Q_2 = '\nQuestion 2 of 4: do you want to set limit values for SWAP memory? (y/n)'
  m_2 = '(format: gigas)               e.g. "answer: 4.5"'
  Q_3 = '\nQuestion 3 of 4: do you want to set limit values for Number Of Cores? (y/n)'
  m_3 = '(format: number)               e.g. "answer: 2"'
  Q_4 = '\nQuestion 4 of 4: do you want to set limit values for Power per Core (%)? (y/n)'
  m_4 = '(format: percentage)               e.g. "answer: 60"'
  Q_v = [Q_1, Q_2, Q_3, Q_4]
  m_v = [m_1, m_2, m_3, m_4]
  info_names = ['ram', 'swap', 'coresn', 'coresp']
  info = {}

  def request_1(q):
    print(q)
    answ = input("Your answer: ")    
    #print(answ)
    return answ
  
  def request_2(m):
    print(m)
    answ = input("Your answer: ")    
    #print(answ)
    return answ

  def protector(answ):
    if answ.lower() in ['y','1','yes','true']:
      return True
    elif answ.lower() in ['n','0','no','false']:  
      return False
    else: 
      exiter()
      return
  
  print(mssg_0)
  for x in range(4):
    if protector(request_1(Q_v[x])):
      info[info_names[x]] = request_2(m_v[x])  
  return info

def set_manually(**kwargs):
  txt_0 = """
version: '2.4'
services:
  IntOptim:
    image: intel/intel-optimized-tensorflow
    build:
      context: .
      dockerfile: Dockerfile-IntOptim
    volumes:
      - "../:/workdir"
      - "./:/extras"
    #mem_limit: 4000m #RAM
    #memswap_limit: 4000m #RAM+SWAP
    #cpu_percent: 50 #WINDOWS
    #cpu_count: 4 #WINDOWS
    #cpus: 2 #LINUX
    #cpuset: 0,1,2,3 #LINUX
    restart: on-failure
volumes:
    uploads:
  """
  ind = 11
  txt_1 = txt_0.split('\n')
  if 'ram' in kwargs.keys():
    txt_1[ind] = f'    mem_limit: {int(1000*float(kwargs["ram"]))}m'
    if 'swap' in kwargs.keys():
      txt_1[ind+1] = f'    memswap_limit: {int(1000*float(kwargs["ram"])+1000*float(kwargs["swap"]))}m'
  else:
    if 'swap' in kwargs.keys():
      print('cannot limit swap without limiting RAM... swap restriction will be ignored')
  if 'coresn' in kwargs.keys():
    txt_1[ind+3] = f'    cpu_count: {int(kwargs["coresn"])}'
    if kwargs["coresn"]!='1':
      txt_1[ind+5] = f'    cpuset: {str(list(range(int(kwargs["coresn"]))))[1:-1].replace(" ","")}' 
    else:
      txt_1[ind+5] = f'    cpuset: "0"' 
    if 'coresp' in kwargs.keys(): 
      txt_1[ind+2] = f'    cpu_percent: {int(kwargs["coresp"])}'
      txt_1[ind+4] = f'    cpus: {round(float(kwargs["coresp"])/100*float(kwargs["coresn"]),2)}'
  elif 'coresp' in kwargs.keys():
    txt_1[ind+2] = f'    cpu_percent: {int(kwargs["coresp"])}'
    txt_1[ind+4] = f'    cpus: {round(float(kwargs["coresp"])/100*cpu_count(),2)}'
  try: remove('docker-compose.yml')
  except FileNotFoundError: pass
  f = open('docker-compose.yml','w')
  for line in txt_1:
    f.write(line)
    f.write('\n')
  f.close()
     



set_manually(**intro())
print('.\n..\n...')
mssg_end = """
_______________________________________________________________
.............SUCCESSFULLY DEFINED THE PARAMETERS!..............|
                                                               |
Now starting the "main.py" script inside an Intel-Optimized    |
Memory & CPU constrained Docker Container                      |
_______________________________________________________________|
"""
print(mssg_end)

# CHECK MKL IS ON
#docker-compose run IOP bash task.sh --rm
#task.sh is 
#python -c "import tensorflow; print(tensorflow.pywrap_tensorflow.IsMklEnabled())"


















