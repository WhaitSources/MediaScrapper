import os
import sys
import getopt
import requests
from bs4 import BeautifulSoup

def usage():
    print("\n\tUsage : " + sys.argv[0] + " -u http://exemple.com -e png,mp4 -o")
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:e:o:')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()

    url = ""
    ext = []
    outDir = ""
    for o,a in opts:
        if o in ("-u", "--url"):
            url = a
        elif o in ("-e", "--extensions"):
            ext = a.split(',')
        elif o in ("-o", "--output"):
            outDir = a
    if url == "" or ext == [] or outDir == "":
        usage()
        sys.exit()
    

    print("\n=> Checking url : " + url)
    print("=> Looking for extensions : " + ', '.join(map(str, ext)) + '\n')
    
    scraper(url, ext, outDir)

def scraper(url, ext, out):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    medias_link = []
    for link in soup.find_all('img'):
        if any(e in link.get("src") for e in ext):
            linkMedia = link.get("src")
            if '?' in link.get("src"):
                linkMedia = link.get("src").split("?")[0]
            medias_link.append(linkMedia)

    print("[+] Found " + str(len(medias_link)) + " medias.")

    if not os.path.isdir(out):
        try:
            os.mkdir(out)
        except OSError:
            print ("Creation of the output directory failed")
        else:
            print ("Successfully created the output directory")

    print("[+] Downloading medias..\n")

    i = 0
    for media in medias_link:
        url = url + '/' if url[-1] != '/' else url 
        try:
            r_media = requests.get(url + media)
        except:
            break
        localMediaPath = out + '/' + str(i) + '_' + media.split('/')[-1]
        print("[*] Downloading " + media + "...")
        file = open(localMediaPath, "wb")
        file.write(r_media.content)
        file.close()
        i = i + 1

    print("\n/!\\ Script done running. /!\\")
if __name__ == "__main__":
    main()
