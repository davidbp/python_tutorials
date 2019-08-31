
# author: David Buchaca Prats
import csv
import re
import time

# INPUT: busquedas_filtered.csv
# OUTPUT: queries_no_accents.csv that is clean.
		# The new csv contains 2 columns: 
		# query   times_query_appeared

path = 'busquedas_filtered.csv'

f= open(path,'r')
csvfile = open(path,'r')

d = csv.reader(csvfile,delimiter=',')
D ={}

start = time.time();

for row in d:
	query = row[0].lower()
	if len(query.split())>16: # Queries with more than 16 words are discarted
		pass
	else:
		query = query.strip()           # remove white spaces and tab (\t) at beginning and end
		query = re.sub(' +',' ',query)  # more than 1 space is converted to 1 space
		query = re.sub('\t',' ',query)  # tab to normal space
		query = re.sub(" +"," ",query)  # more than 1 space to 1 space
		query =	re.sub('" +','"',query) # " codigo civil "-> "codigo civil "
		query = re.sub(' +"','"',query) # " codigo civil " -> " codigo civil"
		# remove accents is done below
		query = re.sub('á','a',query)
		query = re.sub('é','e',query)
		query = re.sub('í','i',query)
		query = re.sub('ó','o',query)
		query = re.sub('ú','u',query)
		if query in D:
			D[query] = D[query] + 1
		else:
			D[query] = 1

time.time() - start

import operator

#data.sort(key=operator.itemgetter(1),reverse=True)

D2={}
for key in D:
	if D[key]<3: # Eliminate queries that has been done < 3 times
		pass
	else:
		D2[key]=D[key]

queries = [ [word,D[word]] for (pos,word) in sorted( zip(D2.values(),D2.keys()),reverse=True ) ]

with open("queries_no_accents.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(queries)
