
# author: David Buchaca Prats

import re


def autocomplete(q,queries):
    start = time.time();
    q = q.lower()
    q = re.sub('á','a',q)
    q = re.sub('é','e',q)
    q = re.sub('í','i',q)
    q = re.sub('ó','o',q)
    q = re.sub('ú','u',q)
    q = re.sub('...')
    q = q.split() # now q is a list
    n = len(q)
    max = 0
    for query in queries:
        Q = query[0].split()
        if len(q)> len(Q):
            pass
        else:
            for num,w in enumerate(q):
                if w in Q[num][0:len(w)]:
                    if num == len(q)-1:
                        max = max + 1
                        print query[0]
                    else:
                        pass
                else:
                    break
            if max ==4:
                print 'time needed: ', time.time() - start
                break
    if max ==0:
        print 'time needed: ', time.time() - start



def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]