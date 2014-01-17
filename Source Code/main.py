'''
Created on Dec 1, 2013

@author: Bryant Moquist
'''
import csv
import compare as cp
import duplicateops as dp
import re
import string

class nstr:
    def __init__(self,namelist,authorid):
        self.name = namelist
        self.aid = authorid

if __name__ == '__main__':
    
    #Build the Chinese/Korean dictionary
    chinese = set()
    with open('chineselist.csv','rU') as f:
        reader = csv.reader(f,delimiter=",")
        for row in reader:
            r = row[0]
            chinese.add(r)
    print('Chinese/Korean dictionary successfully created.')

    #Build the ban list (other potentials: sum, yam,lung,to,he,bang)
    ban = set(['tom','ban','jim','sam','hew','bach','hay','dan','roe','long','tow','man','dam','mac','van','moon','den','ben','shaw','ham','ka','joe'])
    print('Ban list built.')
    
    #Read in the author's names
    master = {}
    author = {}
    paperauthor = set([])
    cnames=[]
    onames=[]
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    #Read in and standardize names from Paper-Author file
    #authorid is row[1] and author name is row[2]
    with open('PaperAuthor.csv','rb') as f:
        reader = csv.reader(f, delimiter=',')
        reader.next()
        for row in reader:
            paperauthor.add(int(row[1]))

    print('PaperAuthor.csv set created.  Set length is: ' +str(len(paperauthor)))
    
    #Read in and standardize names from Author file: 
    with open('Author.csv','rb') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            aid = int(row[0])
            
            #If the author does not appear in the paper author set, assume the author is unique
            if(aid not in paperauthor):
                master[aid] = [aid]  
                continue
            
            #Process authors that appear in paperauthor
            x = row[1].lower()
            s=re.split(r'\s|-', x)
            for i in range(0,len(s)):
                s[i]=regex.sub('', s[i])  
            #Hash the standardized string as a tuple to the author id
            author[aid]=s     

        #Determine if the word is Chinese or Not
        for k in author:
            s = author[k]           
            words=len(s)
            oneletter=0
            shortwords=0
            chinesecount=0
        
            for i in s:
                length=len(i)
                if(length==1):
                    oneletter+=1
                if(i in chinese and i not in ban):
                    chinesecount+=1  
                                        
            if(oneletter==words):
                onames.append(nstr(s,k))
            if((words-chinesecount)<2 and chinesecount>0):
                cnames.append(nstr(s,k))
            else:
                onames.append(nstr(s,k))
    
    #Print the Chinese lists
    print('The length of Chinese/Korean list is: '+str(len(cnames)))
    print('The length of the non-Chinese/Korean list is: ' +str(len(onames)))
    print('Deleting author dictionary')
    del author
    print('Author dictionary deleted')
    print('The length of master is: '+str(len(master)))

    print('Finding Chinese/Korean duplicates')
    cunique = []
    cduplist = []
    flag = 0
    count = 0            

    #Find duplicates
    while(cnames):
        count+=1
        if(count%500==0):
            print(count)
        candidate = cnames.pop()
        #Check if the candidate belongs to an existing duplicate
        for i in range(0,len(cduplist)):
            if(flag):
                break
            for j in cduplist[i].dlist:
                if(cp.compare(candidate.name,j.name)):
                    cduplist[i].dlist.append(candidate)
                    flag=1
                    break
                else:
                    continue
        
        #Check if the candidate is in the main list
        if(not flag):
            for k in range(0,len(cnames)):
                if(cp.compare(candidate.name,cnames[k].name)):
                    flag=1
                    duplicate = dp.dup(candidate,cnames[k])
                    cduplist.append(duplicate)
                    cnames.pop(k)
                    break
        if(not flag):
            cunique.append(candidate)
        
        flag=0
        
    #Split over-matched Chinese names
    print('Checking Chinese/Korean duplicates for over-matching')
    count = 0
    newcduplist = []
    
    for i in range(0,len(cduplist)):
        if(count%100==0):
            print(count)
        temp = dp.makegraph(cduplist[i].dlist)
        for j in temp:
            newcduplist.append(j)
        count+=1
    
    
    #Match Western name duplicates
    print('Finding Western name duplicates')
    ounique = []
    oduplist = []
    flag = 0
    count = 0            

    #Find duplicates
    while(onames):
        count+=1
        if(count%500==0):
            print(count)
        candidate = onames.pop()
        #Check if the candidate belongs to an existing duplicate
        for i in range(0,len(oduplist)):
            if(flag):
                break
            for j in oduplist[i].dlist:
                if(cp.compare(candidate.name,j.name)):
                    oduplist[i].dlist.append(candidate)
                    flag=1
                    break
                else:
                    continue
        
        #Check if the candidate is in the main list
        if(not flag):
            for k in range(0,len(onames)):
                if(cp.compare(candidate.name,onames[k].name)):
                    flag=1
                    duplicate = dp.dup(candidate,onames[k])
                    oduplist.append(duplicate)
                    onames.pop(k)
                    break
        if(not flag):
            ounique.append(candidate)
        
        flag=0
        
    #Split over-matched Chinese names
    print('Checking Western duplicates for over-matching')
    count = 0
    newoduplist = []
    
    for i in range(0,len(oduplist)):
        if(count%100==0):
            print(count)
        temp = dp.makegraph(oduplist[i].dlist)
        for j in temp:
            newoduplist.append(j)
        count+=1
    
    #Put into master dictionary
    #Western unique names
    for i in ounique:
        master[i.aid]=[i.aid]    
    
    #Western duplicates
    for i in newoduplist:
        for j in i:
            master[j.aid]=[]
            for k in i:
                master[j.aid].append(k.aid)
                            
    #Chinese unique names
    for i in cunique:
        master[i.aid]=[i.aid]
    
    #Chinese duplicates
    for i in newcduplist:
        for j in i:
            master[j.aid]=[]
            for k in i:
                master[j.aid].append(k.aid)
    
    #Write master dictionary to CSV file
    print('Writing the CSV file.')
    header = ['AuthorId,DuplicateAuthorIds']
    with open ('output.csv','wb') as csvfile:
        fwriter = csv.writer(csvfile,delimiter='\n',quoting=csv.QUOTE_NONE)
        fwriter.writerow(header)
        for i in master:
            dups = ''
            for j in master[i]:
                dups=dups+" "+str(j)
            dups=dups.strip()
            row1 = [str(i)+","+dups]
            fwriter.writerow(row1)   

