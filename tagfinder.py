import hashlib
import urllib
import sys
from xml.etree.ElementTree import fromstring

def getFirstFrame(path):
    f = open(path, 'rb')
    data = f.read()
    first = 0
    for i in range(0, len(data)):
        ch = data[i]
        if ord(ch) == 0xff :
            ch2 = data[i+1]
            if ord(ch2) & 0xfb == 0xfb :
                first = i
                break

    frame = data[first:first + 102400 ]
    return frame

def getExceptid3(path):
    f = open(path, 'rb')
    data = f.read()
    id3size = ord(data[6]) << 21 | ord(data[7]) << 14 | ord(data[8]) << 7 | ord(data[9])
    id3size += 10
    print id3size

    return data[id3size:id3size+102400]


def searchTag(key):
    url = 'http://newlyrics.gomtv.com/xml/xml_searchtag.php?file_key=%s'%key
    data = urllib.urlopen(url)
    raw = data.read()
    print raw
    raw = raw.decode('euc-kr').encode('utf-8').replace('encoding="EUC-KR"', 'encoding="UTF-8"').replace("encoding='euc-kr'", "encoding='utf-8'")
    print raw
    parser = fromstring(raw)
    for item in parser.findall('item'):
        print item.get('title')
        print item.get('album')
        lyc = item.find('lyrics')
        if lyc != None :
            print lyc.text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage %s mp3path'%(sys.argv[0])
        sys.exit()
    print sys.argv[1]
    frame = getFirstFrame(sys.argv[1])
    hexdigest = hashlib.md5(frame).hexdigest()
    searchTag( hexdigest )
