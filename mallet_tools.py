#!/usr/bin/python3
"""
Generic functions for processing MALLET output files
"""

def process_line(l):
    parts = l.split('\t')
    nr = int(parts[0])
    path = parts[1]
    weights = {}
    for i in range(2,len(parts),2):
        key, val = parts[i:i+2]
        weights[int(key)] = float(val)
    return (nr, path, weights)

def process_file(path):
    with open(path, 'r') as f:
        next(f)#skip first line
        return [process_line(l.rstrip('\n')) for l in f]
