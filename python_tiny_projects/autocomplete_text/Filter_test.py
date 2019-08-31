
# author: David Buchaca Prats

import csv

# INPUT: test.csv database 
# OUTPUT: busquedas_filtered.csv file containing 
        # all the queries done in the vlex search engine with the 
        # number of documents associated to the query.

path = 'test.csv'

f= open(path,'r')
data=[]	
#f.readline() # takes out header
csvfile = open(path,'r')

d = csv.reader(csvfile,delimiter=',')

for row in d:
	if row[2]=="": # if there is no document in the vlex database skip
		pass
	else:
		if int(row[2]) > 1: # in case there is at least 1 document retrieve
			if row[1]=="":  # if the search is empty do not retrieve
				pass
			else:
				data.append([row[1].lower(),int(row[2])])

with open("busquedas_filtered.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data)

Ngrams_by_freq = [word for (pos,word) in sorted( zip(Ngrams.values(),Ngrams.keys()),reverse=True ) ]




