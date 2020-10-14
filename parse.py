import sys
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
regexPage = r"(.?)stream(.|\n)BT(?P<page>.*?)ET(.|\n)endstream"
regexText = r"\((?P<text>.*)\)\s?Tj"

matches = re.finditer(regexPage, pdf, re.DOTALL)

matchesEnum = enumerate(matches, start=1)

for matchNum, match in matchesEnum:
    pageText = match.group("page")
    subMatches = re.finditer(regexText, pageText, re.MULTILINE)
    subMatchesEnum = enumerate(subMatches, start=1)

    for subMatchNum, subMatch in subMatchesEnum:
        subGroupText = subMatch.group("text")
        subText = "{group}".format(group=subGroupText)
        print(subText)


print("Finish!")
