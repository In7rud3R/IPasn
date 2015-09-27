import numpy as np
import subprocess
import socket
import re
import os

InputFile = 'Input.txt' # Input File with IPs and Hostnames

# Set the files and/or paths
IPListFile = 'IPList.txt'
IP_ASN_File = 'IP-ASN.txt'
IP_ASN_err = 'IP-ASN-Error.txt'

try:
    os.remove(IPListFile)
except:
    print IPListFile + ' does not exist'
fopen = open(IPListFile, 'a')

InputFile = np.genfromtxt(InputFile,delimiter=",",usecols=[0],dtype=None)

regex = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
for i in range(0,len(InputFile)):
    result = regex.match(InputFile[i])

    if not result:
        addr = socket.gethostbyname(InputFile[i])
        save_results = str(addr) + "\n"
        fopen.write(save_results)
    else:
        save_results = InputFile[i] + "\n"
        fopen.write(save_results)

fopen.close()

IPList = np.genfromtxt(IPListFile,delimiter=",",usecols=[0],dtype="S16")

def reverseIP(address):
    temp = address.split(".")
    convertedAddress = str(temp[3]) +'.' + str(temp[2]) + '.' + str(temp[1]) +'.' + str(temp[0])
    return convertedAddress

# Open the Output Files
try:
    os.remove(IP_ASN_File)
except:
    print IP_ASN_File + ' does not exist'
f1 = open(IP_ASN_File, 'a')
try:
    os.remove(IP_ASN_err)
except:
    print IP_ASN_err + ' does not exist'
f2 = open(IP_ASN_err, 'a')

#Start at 1 in the IPList to skip the header
for i in range(0,len(IPList)):
    IP_reversed = reverseIP(IPList[i])
    querycmd1 = IP_reversed + '.origin.asn.cymru.com'
    response1 = subprocess.Popen(['dig', '-t', 'TXT', querycmd1, '+short'], stdout=subprocess.PIPE).communicate()[0]
    response1List = response1.split('|')
    ASN = response1List[0].strip('" ')
    querycmd2 = 'AS' + ASN + '.asn.cymru.com'
    response2 = subprocess.Popen(['dig', '-t', 'TXT', querycmd2, '+short'], stdout=subprocess.PIPE).communicate()[0]
    response2List = response2.split('|')
    IP = IPList[i]
    if len(response2List) < 4:
        #No Response or other error
        print '*' * 5, IP,response2
        error_string = IP+','+response2
        f2.write(error_string)
    else:
        #Valid Response, Log only first if multiple responses
        ISP = response2List[4].replace('"', '')
        Network = response1List[1].strip()
        Country = response1List[2].strip()
        Registry = response1List[3].strip()
        save_string = IP+' | '+Country+' | '+ASN+' | '+ISP
        f1.write(save_string)

try:
    os.remove(IPListFile)
except:
    print IPListFile + ' does not exist'

f1.close()
f2.close()
