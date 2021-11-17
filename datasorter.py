import sys
import os
import math
import random


#while True:
    #try:
        #doalli = input("Sort all data (y/n): ")
        #doall = False
        #if "y" in doalli.lower():
        #    doall = True
        #if "n" in dollai.lower():
        #    doall = False
    #except:
    #    print("Command not recognized, please try again")

while True:
    try:
        emailonlyi = input(" (y/n): ")
        emailonly = False
        if "y" in emailonlyi.lower():
            emailonly = True
        if "n" in emailonlyi.lower():
            emailonly = False
    except:
        print("Command not recognized, please try again")

print("Email only mode: "+str(emailonly))


file = open("all_leads.txt","r")
allleads = file.readlines()
file.close()

if emailonly == True:
    theleads = []
    for lead in allleads:
        theleads.append(str(lead.split(":")[2].strip().replace("\r","").replace("\n","")+"\n"))

    file = open("outputleads.txt", "w")
    file.writelines(theleads)
    file.close()
        
else:
    theleads = []
    for lead in allleads:
        if "NAN" in lead.split(":")[2]:
            theleads.append(lead)

    file = open("outputleads.txt", "w")
    file.writelines(theleads)
    file.close()    
