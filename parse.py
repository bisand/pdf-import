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

pdf = open("test.pdf", "r").read()
regex = r"(.?)stream(.|\n)BT(?P<text>.*?)ET(.|\n)endstream"
regex2 = r".*Tm \((?P<text>.*)\) Tj"

matches = re.finditer(regex, pdf, re.DOTALL)
try:
    matchesEnum = enumerate(matches, start=1)
    for matchNum, match in matchesEnum:
        print ("{group}".format(group = match.group("text")))
        # TODO: Parse single result lines to remove pdf keywords.


except:
    pass

print("Finish!")
