
import csv
from google_images_download import google_images_download
response = google_images_download.googleimagesdownload() 
import os
import shutil
import shutil
import logging
import threading
from numpy import random
import sys
import unidecode
import unicodedata

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


NUM_THREADS = 40


pro10 = ['163.172.152.52:8811','178.62.193.19:3128','104.248.86.193:8080','136.243.14.107:3128','138.68.165.154:3128','138.68.165.154:8080','138.68.161.14:8080','188.213.25.26:80','185.234.37.207:80','207.154.231.211:3128']
pro20 = ['142.93.130.169:8118','138.68.173.29:3128','138.68.173.29:8080','138.68.161.14:3128','138.68.165.154:3128','138.68.165.154:8080','138.68.161.14:8080','188.226.141.211:8080','188.226.141.127:3128','188.226.141.61:8080','188.226.141.61:3128','188.226.141.211:3128','188.226.141.127:8080','192.81.223.236:3128','178.62.193.19:3128','163.172.169.167:3129','176.9.75.42:3128','46.4.96.137:3128','82.196.11.105:8080','34.90.113.143:3128']
pro20 =['176.9.119.170:8080','138.68.173.29:3128','138.68.173.29:8080','176.9.75.42:8080','138.68.161.14:3128','138.68.165.154:3128','138.68.165.154:8080','138.68.161.14:8080','188.226.141.211:8080','188.226.141.127:3128','188.226.141.61:8080','163.172.136.226:8811','178.62.193.19:3128','178.62.232.215:8080','139.59.169.246:8080','188.226.141.61:3128','46.4.96.137:3128','51.158.98.121:8811','188.226.141.127:8080','188.226.141.211:3128']
profinal = ['157.245.196.253:8080','138.197.102.119:80','137.117.98.253:8080','138.68.240.218:3128','138.197.204.55:3128','45.55.27.161:3128','198.199.120.102:3128','192.241.245.207:8080','45.55.27.15:8080','192.241.245.207:3128','198.199.120.102:8080','23.101.203.138:3128','35.235.75.244:3128','34.90.113.143:3128','198.199.119.119:3128','35.247.83.89:3128','198.199.119.119:8080','142.93.8.181:8888','138.197.222.35:3128','138.197.104.219:3128','138.197.222.35:8080','157.245.205.81:8080','157.245.193.82:8080','138.68.24.145:3128','45.55.27.15:3128','45.55.23.78:3128','45.55.23.78:8080','199.19.254.164:8080','34.213.184.205:3128','157.245.207.190:8080','157.245.207.112:8080','138.197.204.55:8080','138.68.41.90:3128','157.245.211.139:8080','165.22.101.123:8080','138.68.41.90:8080','67.205.174.209:3128','45.55.27.161:8080','157.245.4.94:3128','138.68.24.145:8080','157.230.35.68:8080','157.245.4.94:8080','157.245.52.134:8080','34.73.123.161:8080','45.55.9.218:3128','50.235.28.146:3128','162.243.108.141:8080','165.22.199.231:3128','138.68.240.218:8080','157.245.197.232:8080','157.245.52.211:8080','209.90.63.108:80','162.243.108.129:3128','45.55.9.218:8080','67.205.132.241:8080','67.205.174.209:8080','165.22.254.99:3128','165.22.254.99:8080','157.245.197.92:8080','157.245.204.7:8080','162.243.108.161:3128','67.205.149.230:8080','167.71.138.113:8080','157.245.52.229:8080','162.243.108.161:8080','167.88.117.209:8080']

path = '/home/pc/Desktop/threading/result'
path_proxies = 'proxies.txt'
proxies = []

def load_proxies():
    with open(path_proxies, mode='r') as fp:
        line = fp.readline()
        while line:
            proxies.append(line)
            line = fp.readline()
    # Listing all the files in the dir
    print(len(proxies))
    return proxies

def scrap_Google(pro,mydict,missing):
    res = []
    errors=[]

    ## scrapping only missing
    for key in mydict.items():
        change = False
        id2 = key[0]
        name = key[1]
        folder=''
        if (id2 in missing):
            logging.debug('ID: ' + str(key[0]))
            u = unidecode.unidecode(name)
            keyword = u +  " musician"
            arguments = {"keywords": keyword,"limit":1,"print_urls":False,"aspect_ratio":"square"}  
            try: 
                change = False
                a,b = response.download(arguments)
                lis = [v for k,v in a.items()]
                oldPath = lis[0][0]
                os.rename(oldPath, "/home/pc/Desktop/threading/result/"+str(id2)+".jpg") 
                st = oldPath
                st = st.split('/')
                folder = st[len(st)-2]
                #shutil.rmtree('/home/pc/Desktop/work2/downloads/' + folder)
                continue
            except:
                change = True
                logging.debug('ERROR ID: ' + str(id2) +  str(sys.exc_info()[0]))
                if ('SystemExit' in str(sys.exc_info()[0]) ):
                    print('entrei change')
                    missing = calc_missing()
                    r = random.choice(len(profinal))
                    pro = proxies[r]
                errors.append(id2)
                #shutil.rmtree('/home/pc/Desktop/work2/downloads/' + keyword)
                continue
    try:
        f = open("erros.txt", "a")
        g = open("finish.txt", "a")
        f.write(str(errors))
        g.write("thread: " + str(sup) + "-" + str(inf) + "finished")
        f.close()
        g.close()
        logging.debug('FINISHED THREAD SCRAPPING')
    except:
        logging.debug('erro gravado em ficeiro')


def calc_missing():
    files = []
    missing = []
    for r, d, f in os.walk(path):
        for file in f:
            file = file.split('.')
            file = file[0]
            files.append(file)
    #checking those who miss
    for i in range(30000):
        if not (str(i) in files):
            missing.append(i)
    return missing

def getIds():
    mydict = []
    # reading all the ids from de CSV
    with open('celeb.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {int(rows[0]):rows[1] for rows in reader}
    # Listing all the files in the dir
    return mydict

def main():
    threads=[]
    missing=[]
    while(True):
        mydict = getIds()
        missing = calc_missing()
        #random.shuffle(profinal)
        load_proxies()
        print('proxies aqui',len(proxies))
        val = len(proxies)
        r = random.choice(val)
        if (len(missing)>0):
            print('Size of missing',len(missing))
            scrap_Google(proxies[r],mydict,missing,proxies)
        else:
            print('HYUURRY u did it')
            return


main()
