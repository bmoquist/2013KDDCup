'''
Created on Dec 7, 2013

@author: Bryant Moquist
'''

import numpy as np

class dup:
    def __init__(self,list1,list2):
        self.dlist = []
        self.dlist.append(list1)
        self.dlist.append(list2)

def makegraph(list1):
    cendict = {}
    lcen = []
    length = 0
    
    for i in range(0,len(list1)):
        a = cen(list1[i],list1)
        for j in range(0,len(a)):            
            temp = sum(len(s) for s in a[j].name)
            if(temp>length):
                length = temp
                lcen = a[j]
            else:
                continue

        cendict[list1[i]]=lcen
        length = 0
        lcen = ""
    
    inverse = {}
    for k, v in cendict.iteritems():
        inverse[v] = inverse.get(v, [])
        inverse[v].append(k)
    
    l1 = []

    for i in inverse:
        l1.append(inverse[i])

    return l1

        
#Returns Common Extended Name List
def cen(current,duplist):
    cenlist = []
    for i in duplist:
        if(checknames(current.name,i.name)):
            cenlist.append(i)
        else:
            continue
    cenlist = sorted(cenlist,reverse=True, key=lambda nstr: len(nstr.name))
   
    return cenlist

#Check if two names are CEN
def checknames(basename,lname):
    l1 = len(basename)
    l2 = len(lname)
    count =0
    #Basename larger than the list name --> cannot be common extended name
    if(l1>l2):
        return False
    
    #All elements must be the same if the lists are the same size
    if(l1==l2):
        for i in basename:
            for j in lname:
                if(len(i)<=len(j)):
                    if(i==j[0:len(i)]):
                        count+=1
                        break
                    else:
                        continue                    
                else:
                    if(i[0:len(j)]==j):
                        count+=1
                        break
                    else:
                        continue                    
                    
    #Lists not the same size: Check is all elements are in the list or if all are in the list plus 1 prefix
    count=0
    
    for i in basename:
        for j in lname:
            if(len(i)<=len(j)):
                if(i==j[0:len(i)]):
                    count+=1
                    break
                else:
                    continue
            else:
                if(i[0:len(j)]==j):
                    count+=1
                    break
                else:
                    continue
                
    #All of the base name elements are in the list name
    if(count==l1):
        return True
    else:
        return False
