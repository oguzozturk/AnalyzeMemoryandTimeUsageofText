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

class BigramCounter:
  def __init__(self):
    # initialize storage dictionary (datatype of {} is 'dict')
    self.bigrams = {}

  def count(self, word1, word2):
    # make bigram (datatype of (,) is 'tuple')
    bigram = (unicode(word1, 'utf8')[-3:],unicode(word2, 'utf8')[-3:])
    # increase count for this bigram by one
    if bigram not in self.bigrams:
      # if it was not yet in the dictionary
      self.bigrams[bigram] = 1
    else:
      # if it was already in the dictionary
      self.bigrams[bigram] += 1

  def display(self):
    showMemTime('begin display')

    # build list of all frequencies and bigrams
    bigram_freq = self.bigrams.items()
    showMemTime('after items')

    # sort that list by frequencies (i.e., second field), descending
    print "sorting ..."
    bigram_freq.sort(key = lambda x:x[1], reverse = True)
    showMemTime('after sorting')

    # iterate over the first five (or less) elements
    print "creating output ..."
    for bigram, occurred in bigram_freq[0:5]:
      print "3-ending bigram '%s' '%s' occured %d times" % \
        (bigram[0], bigram[1], occurred)

class TrigramCounter:
  def __init__(self):
    # initialize storage dictionary (datatype of {} is 'dict')
    self.trigrams = {}
    self.m = 2

  def count(self, word1, word2, word3):
    # make bigram (datatype of (,) is 'tuple')
    trigram = (unicode(word1, 'utf8')[-self.m:],unicode(word2, 'utf8')[-self.m:],unicode(word3, 'utf8')[-self.m:])
    # increase count for this bigram by one
    if trigram not in self.trigrams:
      # if it was not yet in the dictionary
      self.trigrams[trigram] = 1
    else:
      # if it was already in the dictionary
      self.trigrams[trigram] += 1

  def display(self):
    showMemTime('begin display')

    # build list of all frequencies and trigrams
    trigram_freq = self.trigrams.items()
    showMemTime('after items')

    # sort that list by frequencies (i.e., second field), descending
    print "sorting ..."
    trigram_freq.sort(key = lambda x:x[1], reverse = True)
    showMemTime('after sorting')

    # iterate over the first five (or less) elements
    print "creating output ..."
    for trigram, occurred in trigram_freq[0:5]:
      print "%d-ending trigram '%s' '%s' '%s' occured %d times" % \
        (self.m, trigram[0], trigram[1], trigram[2], occurred)

# this is our main function
def main():
  # make sure the user gave us a file to read
  if len(sys.argv) != 2:
    print "need one argument! (file to read from)"
    sys.exit(-1)
  filename = sys.argv[1]

  showMemTime('begin') # let's observe where we use our memory and time

  # read input file
  print "reading from file "+filename
  inputdata = open(filename,'r').read()
  showMemTime('after reading')

  # split on all newlines and spaces
  print "splitting"
  inputwords = re.split(r' |\n',inputdata)
  showMemTime('after splitting')

  # remove empty strings
  inputwords = filter(lambda x: x != '', inputwords)
  showMemTime('after filtering')

  # initialize bigram counter
  bc = BigramCounter()
  tc = TrigramCounter()

  # go through all words
  print "going over words"
  for idx in range(0,len(inputwords)):
    # let's show resources after all 50 K words
    if idx % 50000 == 49999:
      showMemTime('while counting')

    # count bigram if we can look back one character
    if idx >= 1:
      bc.count( inputwords[idx-1], inputwords[idx] )

    # count trigram if we can look back two characters
    if idx >= 2:
      tc.count( inputwords[idx-2], inputwords[idx-1], inputwords[idx] )

  showMemTime('after counting')
  print "bigrams:"
  bc.display()
  print "trigrams:"
  tc.display()

main()
showMemTime('at the end')
