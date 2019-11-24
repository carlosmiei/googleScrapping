
import csv
from google_images_download import google_images_download
response = google_images_download.googleimagesdownload() 
import os
import shutil
import shutil
import logging
import threading
import sys
import unidecode
import unicodedata
from numpy import random
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


NUM_THREADS = 5

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


def scrap_Google(sup,inf,pro,missing,mydict,profinal):
    res = []
    errors=[]

    ## scrapping only missing
    for key in mydict.items():
        change = False
        id2 = key[0]
        name = key[1]
        folder=''
        if ((id2 in missing) and (id2 >= sup) and (id2 < inf)):

            logging.debug('ID: ' + str(key[0]))
            u = unidecode.unidecode(name)
            keyword = u +  " musician"

            arguments = {"keywords": keyword,"limit":1,"print_urls":False,"aspect_ratio":"square","proxy":pro}  
            try: 
                change = False
                a,b = response.download(arguments)
                lis = [v for k,v in a.items()]
                oldPath = lis[0][0]
                os.rename(oldPath, "/home/pc/Desktop/threading/result/"+str(id2)+".jpg") 
                st = oldPath
                st = st.split('/')
                folder = st[len(st)-2]
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
                continue
            finally:
                shutil.rmtree('/home/pc/Desktop/threading/downloads/' + keyword)

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
    while(True):
        mydict = getIds()
        missing = calc_missing()
        #random.shuffle(proxies)
        load_proxies()
        if (len(missing)>0):
            print('Size of missing',len(missing))
            for i in range(NUM_THREADS):
                inf = 6000*i
                sup = inf+6000  
                t = threading.Thread(name='t'+str(i),target=scrap_Google, args=(inf,sup,proxies[i],missing,mydict,proxies))
                threads.append(t)
                t.start()
            #for x in threads:
            #    x.join()
        else:
            print('HYUURRY u did it')
            return

main()