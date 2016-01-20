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
  def __init__(self,n,m):
    # initialize storage dictionary (datatype of {} is 'dict')
    self.ngrams = {}
    self.n = n
    self.m = m


  def count(self, mylist = []):
      # make bigram (datatype of (,) is 'tuple')
    ###############################
    # get mylist in for and split last m char, then appends it new ngram list
    ###############################
    ngram = []
    for l in mylist:
      ngram.append(unicode(l, 'utf8')[-self.m:])

    ###############################
      # convert the list to tuple
      ###############################
    t = tuple(ngram)

    # increase count for this bigram by one
    if t not in self.ngrams:
      # if it was not yet in the dictionary
      self.ngrams[t] = 1
    else:
      # if it was already in the dictionary
      self.ngrams[t] += 1

  def display(self):
    showMemTime('begin display')

    # build list of all frequencies and trigrams
    ngram_freq = self.ngrams.items()
    showMemTime('after items')
    del (self.ngrams)
    # sort that list by frequencies (i.e., second field), descending
    print "sorting ..."
    ngram_freq.sort(key = lambda x:x[1], reverse = True)
    showMemTime('after sorting')

    # iterate over the first five (or less) elements
    print "creating output ..."
    for ngram, occurred in ngram_freq[0:5]:
      print "%d-ending %d-gram '" % \
        (self.m,self.n),
      print ", ".join(ngram),
      print "' occured %d times" % \
        (occurred)

# this is our main function
def main():

  # make sure the user gave us a file to read
  if len(sys.argv) != 4:
    print "need one argument! (file to read from)"
    sys.exit(-1)
  filename = sys.argv[1]
  ###############################
  # get n and m from user as parameter
  # n is tuple size and m is last end char num
  ###############################
  n = int(sys.argv[2])
  m = int(sys.argv[3])

  showMemTime('begin') # let's observe where we use our memory and time

  # read input file
  print "reading from file "+filename

  # initialize Ngrambigram counter
  nc = NgramCounter(n,m)

  inputdata = open(filename,'r')

  ###############################
  # read file and start iteration line by line,
  # and do the counting stuff in the for loop
  ###############################

  for l in inputdata:

    showMemTime('after reading')

    # split on all newlines and spaces
    print "splitting"
    inputwords = re.split(r' |\n',l)

    showMemTime('after splitting')

    # remove empty strings
    inputwords = filter(lambda x: x != '', inputwords)

    showMemTime('after filtering')


    # go through all words
    print "going over words"
    for idx in range(0,len(inputwords)):
      # let's show resources after all 50 K words
      if idx % 50000 == 49999:
        showMemTime('while counting')

      # count Ngramcounter if we can look back n-1 characters
      mylist=[]
        ###############################
      # get n words(0 to n-1) from the inputwords list,
      # and append it to the list 'mylist' which i have created 2 lines above
      ###############################
      for i in reversed(range(0,n)):
        mylist.append(inputwords[idx-i])
            ###############################
      # call count function of 'nc' ngramCounter with mylist parameter
      ###############################
      nc.count(mylist)
    ###############################################deleting
    del(inputwords)
    del(mylist)
    del(idx)

  showMemTime('after counting')
  print "ngrams:"
  nc.display()

  ####################################
  del(nc)

main()

showMemTime('at the end')