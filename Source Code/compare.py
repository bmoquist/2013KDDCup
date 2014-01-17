'''
Created on Dec 7, 2013

@author: Bryant Moquist
'''

def compare(list1,list2):
    l1 = len(list1)
    l2 = len(list2)
    counter=0
    missing = 'missingword'

    if(l1<=l2):
        small=list1
        large=set(list2)
    else:
        small=list2
        large=set(list1)
    
    #Both strings are exactly the same
    if(l1==l2):
        
        for i in small:
            if i in large:
                counter+=1
            else:
                missing = i
                continue
        
        if(counter==l1):
            return True

        #Check for prefix based on missing word if only word is not matching and 
        if(counter==(len(small)-1) and l1>2):
            for i in large:  
                if(len(missing)<=len(i)): 
                    if(missing==i[0:len(missing)]):
                        return True
                else:
                    if(missing[0:len(i)]==i):
                        return True
                
    
    #Check if the shorter list is a subset of the larger
    counter=0
    if(l1!=l2):
        for i in small:
            if i in large:
                counter+=1
            else:
                missing = i
                continue
        
        if(counter==len(small)):
            return True
        
        #Check for prefix based on missing word if only 1 word is not matching
        if(counter==(len(small)-1) and l1>2 and l2>2):
            for i in large:       
                if(len(missing)<=len(i)): 
                    if(missing==i[0:len(missing)]):
                        return True
                else:
                    if(missing[0:len(i)]==i):
                        return True    
    return False


            
                    
    
    