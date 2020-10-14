def slices(s, *args):
    position = 0
    for length in args:
        yield s[position:position + length]
        position += length
