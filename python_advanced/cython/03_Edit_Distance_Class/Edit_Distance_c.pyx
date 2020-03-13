import numpy as np
cimport cython
cimport numpy as np


cdef class Edit_Distance_c():
    '''
    Computes the edit distance between two strings.
    
    Args:
        c_ins (int): Inserting cost for Edit Distance
        c_del (int): Deleting cost for Edit Distance
        c_rep (int): Replacing cost for Edit Distance
    
    Attributes:
        c_ins (int): Inserting cost for Edit Distance
        c_del (int): Deleting cost for Edit Distance
        c_rep (int): Replacing cost for Edit Distance
        
    
    '''
    cdef int c_ins
    cdef int c_del
    cdef int c_rep
    
    def __init__(self, int  c_ins=1,int c_del=1, int c_rep=1):
        self.c_ins = c_ins
        self.c_del = c_del
        self.c_rep = c_rep

    
    cpdef int evaluate(self,str str1, str str2):
        '''
        Function that calculates the edit distance between two strings. 
        It uses less memory because we only store 2 rows instead of the whole matrix 

        Args:
            str1: (String) First string
            str2: (String) Second string
        
        Returns:
            Edit distance between str1 and str2

        '''
        cdef int m = len(str1)
        cdef int n = len(str2)
        cdef int i,j,del_char, ins_char, rep_char

        # Create a array to memoize distance of previous computations (2 rows) 
        cdef np.ndarray[int,ndim=2] dist = np.zeros([2,m+1], dtype=np.int32)

        # When second string is empty then we remove all characters 
        for i in range(m+1):
            dist[0,i] = i


        # Fill the matrix for every character of the second string
        for i in range(1,n+1):
            #This loop compares the char from second string with first string characters 
            for j in range(m+1):
                #if first string is empty then we have to perform add character peration to get second string   
                if j==0:
                    dist[i%2,j] = i

                #if character from both string is same then we do not perform any operation. We take the diagonal value

                elif str1[j-1] == str2[i-1]:
                    dist[i%2,j] = dist[(i-1)%2,j-1]

                #if the characters are different, we take the minimum of the three edits and addd it with the cost
                else:
                    del_char = dist[(i-1)%2,j] + self.c_del #Delete
                    ins_char = dist[i%2,j-1] + self.c_ins #Insert
                    rep_char = dist[(i-1)%2,j-1] + self.c_rep #Replace

                    dist[i%2,j] = min(del_char, ins_char, rep_char)

        return dist[n%2,m]


