import sys
import math

def get_mtype_by_fname(fname: str) -> str:  # 'Возвращает  найденный MIME  тип или 'UNKNOWN'
    unknown_mtype = 'UNKNOWN'
    if '.' not in fname:
        return unknown_mtype
    ext = fname.split('.')[-1]
    mime_mapping.get(ext.upper(), fname)

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    mime_mapping[ext.upper()] = mt

for i in range(q):
    fname = input()
    print(get_mtype_by_fname(fname))