import sys
import re
import zlib
import tools

# Testing purposes only
data = tools.slices('Dette er en test', 6, 3, 3, 10)

for d in data:
    print(d)

# Main program
encodings = ["utf-8", "ISO-8859-1", "windows-1250", "windows-1252"]
regexPage = r"(.?)stream(.|\n)BT(?P<page>.*?)ET(.|\n)endstream"
regexText = r"\((?P<text>.*)\)\s*?Tj"

for e in encodings:
    try:
        with open("test.pdf", "r", encoding=e) as strm:
            pdf = strm.read()

    except UnicodeDecodeError:
        print('got unicode error with %s , trying different encoding' % e)
    else:
        print('opening the file with encoding:  %s ' % e)

        matches = re.finditer(regexPage, pdf, re.DOTALL)

        matchesEnum = enumerate(matches, start=1)

        for matchNum, match in matchesEnum:
            pageText = match.group("page")
            subMatches = re.finditer(regexText, pageText, re.MULTILINE | re.IGNORECASE)
            subMatchesEnum = enumerate(subMatches, start=1)

            for subMatchNum, subMatch in subMatchesEnum:
                subGroupText = subMatch.group("text")
                subText = "{group}".format(group=subGroupText)
                print(subText)
        break

print("Finish!")
