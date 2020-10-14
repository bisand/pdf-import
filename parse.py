import re
import zlib

def slices(s, *args):
    position = 0
    for length in args:
        yield s[position:position + length]
        position += length

data = slices('Dette er en test', 6, 3, 3, 10)

for d in data:
    print(d)

pdf = open("some_doc.pdf", "rb").read()
stream = re.compile(rb'.*?FlateDecode.*?stream(.*?)endstream', re.S)

for s in stream.findall(pdf):
    s = s.strip(b'\r\n')
    try:
        print(zlib.decompress(s))
        print("")
    except:
        pass