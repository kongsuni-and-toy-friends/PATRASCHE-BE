import re

pw = "URe1I1pdl0"
pattern = "^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9]+$"
print(bool(re.match(pattern, pw)))


