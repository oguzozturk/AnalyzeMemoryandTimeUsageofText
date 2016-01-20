import sys
import re
import os
import psutil # if this makes an error, you need to install the psutil package on your system
import time

maxmem = 0
def showMemTime(when='Resources'):
  global maxmem
  # memory and time measurement
  process = psutil.Process(os.getpid())
  mem = process.memory_info().rss / float(2 ** 20)
  maxmem = max(maxmem, mem)
  ts = process.cpu_times()
  sys.stderr.write("{when:<20}: {mb:4.0f} MB (max {maxmb:4.0f} MB), {user:4.1f} s user, {system:4.1f} s system\n".format(
    when=when, mb=mem, maxmb=maxmem, user=ts.user, system=ts.system))
class NgramCounter:
   # constructor of Ngram as n=n tuple,m=m ending
  def __init__(self,n,m):
    # initialize storage dictionary (datatype of {} is 'dict')
    self.ngrams = {}
    self.n = n
    self.m = m

  def count(self, mylist = []):

    ngram = []
    

    for l in mylist:
      ngram.append(unicode(l, 'utf8')[-self.m:])

    t = tuple(ngram)
    if t not in self.ngrams:
      self.ngrams[t] = 1
    else:
      self.ngrams[t] += 1

  def display(self,k=5):
    showMemTime('begin display')

    ngram_freq = self.ngrams.items()
    showMemTime('after items')

    del (self.ngrams)

    print "sorting ..."
    ngram_freq.sort(key = lambda x:x[1], reverse = True)
    showMemTime('after sorting')

    print "creating output ..."
    for ngram, occurred in ngram_freq[0:k]:
      print "%d-ending %d-gram '" % \
        (self.m,self.n),
      print ", ".join(ngram),
      print "' occured %d times" % \
        (occurred)
def KMostFrequentNMGramsInFile(k,n,m,filename):

  # initialize Ngrambigram counter
  nc = NgramCounter(n,m)
  
  inputdata = open(filename,'r')
  
  for l in inputdata:

    inputwords = re.split(r' |\n',l)

    inputwords = filter(lambda x: x != '', inputwords)

    for idx in range(0,len(inputwords)):
      
      mylist=[]
      for i in reversed(range(0,n)):
        mylist.append(inputwords[idx-i])
      nc.count( mylist )

    del (inputwords)
    
  nc.display(k)

  del(nc)
def main():
  # make sure the user gave us a file to read
  if len(sys.argv) != 2:
    print "need one argument! (file to read from)"
    sys.exit(-1)

  #read system input for reading file=filename
  filename = sys.argv[1]

  showMemTime('begin') # let's observe where we use our memory and time

  KMostFrequentNMGramsInFile(30,2,2,filename)
  KMostFrequentNMGramsInFile(30,3,2,filename)
  KMostFrequentNMGramsInFile(30,4,2,filename)
  KMostFrequentNMGramsInFile(20,2,3,filename)
  KMostFrequentNMGramsInFile(20,3,3,filename)
  KMostFrequentNMGramsInFile(15,2,4,filename)
  KMostFrequentNMGramsInFile(15,3,4,filename)

main()
showMemTime('at the end')