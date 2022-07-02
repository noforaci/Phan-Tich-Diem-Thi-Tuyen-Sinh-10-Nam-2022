import re
import ssl
import subprocess
import pandas as pd
import html
import string

#Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

preRe0 = 'curl -F "sobaodanh='
preRe1 = '" diemthi.hcm.edu.vn/Home/Show'
num = 9000

column = {'Ten':[], 'Ngay sinh': [],'SBD':[], 'Toan':[], 'Ngu van':[], 'Ngoai ngu':[], 'Chuyen':[]}
raw = {'Ten':[''], 'Ngay sinh': [''],'SBD':[''], 'Toan':[0], 'Ngu van':[0], 'Ngoai ngu':[0], 'Chuyen':[0]}

analyst = pd.DataFrame(column)

def reset():
    raw['Toan'] = [0]
    raw['Ngu van'] = [0]
    raw['Ngoai ngu'] = [0]
    raw['Chuyen'] = [0]
    raw['Ten'] = ['']
    raw['Ngay sinh'] = ['']

while True:
    s = preRe0 + str(num) + preRe1
    result = subprocess.check_output(s)

    data = result.decode('utf-8')
    data = str(data)

    raw['SBD'][0] = str(num)

    getDate = re.findall('[0-9]?[0-9]/[0-9]?[0-9]/[0-9]{4}', data)
    raw['Ngay sinh'][0] = getDate[0]

    getInfo = re.findall('[A-ZÂĐÊÔƯƠ]+.+\r', data)

    sName = html.unescape(getInfo[11]).replace("\r","")
    raw['Ten'][0] = sName

    getInfo[12] = html.unescape(getInfo[12])
    sMark = s = re.findall('[-]?[0-9]?[0-9][.]?[0-9]?[0-9]?', getInfo[12])

    raw['Ngu van'][0] = sMark[0]
    raw['Ngoai ngu'][0] = sMark[1]
    raw['Toan'][0] = sMark[2]

    if(len(sMark) == 4):
        raw['Chuyen'][0] = sMark[3]

    
    new_row = pd.DataFrame(raw)
    analyst = pd.concat([analyst, new_row])

    num += 1
    print(num-8999)
    if (num == 9572): break
    reset()

analyst.to_csv("tuyensinhTHPT.csv")