# -*- coding: utf-8 -*-
"""
Created on Fri May  1 23:56:15 2020

@author: Subhankar
"""

ahs=[10,'subhankar']
ahs = ahs + [10] 
print(ahs)
b = ahs[0]
c = ahs[1]
'Hello\'world'

a='abcdefghijkl'
print(a)
len(a)
a[1:5]

n="sam"
p="p"+n[1:]
k="hhh"+"hhhjjj"
print(k)
print(2**2)
o=2**3
print(o)

d = "thank you"
d.split()

de = {"k1":1,"k2":2}
print(de["k1"])
dk = (1,2,3,4,1,1,1,4,5,6)
dk.count(1)
 


%%writefile test.txt
Hello there
how are You
Do YoU ReMeMbEr Me??

my_file=open('test.txt')
my_file.read()
my_file.seek(0)

my_text = my_file.read()
my_text
my_test = my_file.readlines()
my_test
my_file.close()
pwd                                 #wpath of working directory


%%writefile test2.txt
iron man
captain america
black panther
black widow
falcoln
loki
thor
hulk
antman
wasp
superman
spiderman

#Read only mode
with open('test2.txt',mode = 'r') as f:
    print(f.read())
with open('test2.txt',mode = 'a') as f:
    f.write('\nthanos')
with open('test3.txt',mode = 'w') as f:
    f.write('hi scratches heroes welcome')
    

tr=dir(__builtins__)
len(tr)
(int)(3/2)

