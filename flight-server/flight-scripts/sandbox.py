import re

x = 'Column: 2, Row: 3'
if bool(re.search('(?<=Column:\s)[0-9]', x)) or bool(re.search('(?<=Row:\s)[0-9]', x)) is True:
    print(re.search('(?<=Column:\s)[0-9]', x).group(0))
    print(re.search('(?<=Row:\s)[0-9]', x).group(0))