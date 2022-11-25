# import sys
# s = sys.stdin
# sp = [x.strip() for x in sys.stdin]
# print(sp)
# st = []
# for i in range(0, len(sp) - 2, 4):
#     st += [sp[i + 1] + ' ' + sp[i + 2]]
# print(", ".join(st))
from requests import get

print(get('http://localhost:5000/api/news/q').json())