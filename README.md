# AnalyzeMemoryandTimeUsageofText


The program ‘analyze.py’ reads a ﬁle, splits it into words, 
counts which pair of word endings of length 3 occurs how often, and which triple of word endings of length 3 occurs how often, 
and then displays the most frequent pairs and triples of word endings.

The program ‘analyzeRefactor1NGram.py’ reads a ﬁle, splits it into words, 
counts which pair of word endings of length n occurs how often, and which n of word endings of length m occurs how often, 
and then displays the most frequent pairs and n of word endings.

The program ‘analyzeRefactor2Delete.py’  reduce the memory usage by deleting data 
when it is no longer needed (with the ‘del’ keyword). 

The program ‘analyzeRefactor3Iterator.py’  I create a function ‘def displayKMostFrequentNMGramsInFile(k,n,m,ﬁlename)’ 
which opens the ﬁle, creates a n-gram counter class for m, counts the n-grams, and
then prints the k most frequent n-grams (reuse the code in ‘analyzeRefactor3Iterator’). 
f = open(filename,’r’) 
for line in f: 
- do everything you need to do with ’line’ here 
- (for example counting bigrams/trigrams)
- the line data will be deleted automatically by python
by changing method of read file I decrease memory and time usage
