import re


pattern = r"^[^:]+(?:\s+[^:]+)*\s*:\s*[-+][0-9]+$"

def test():
    string = None
    while string!='end':
        string = input()
        print(re.match(pattern, string))

test()
