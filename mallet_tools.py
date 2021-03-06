"""
Generic functions for parsing MALLET files
"""

def process_file(path):
    """
    parse a MALLET inferencer output file
    returns a list of tuples with structure:
    (id, filepath, {5: 0,362865, ...})
    """
    def parse_line(l):
        parts = l.split('\t')
        nr = int(parts[0])
        path = parts[1].lstrip('file:')
        weights = {}
        for i in range(2, len(parts), 2):
            key, val = parts[i:i+2]
            weights[int(key)] = float(val)
        return (nr, path, weights)
    with open(path, 'r') as f:
        next(f)#skip first line
        return [parse_line(l.rstrip('\n')) for l in f]

def parse_topicfile(path):
    """
    parse a MALLET trainingset "keys.txt"-file
    returns a list of tuples with structure:
    (id, ?, ["water", "wind", "ocean", ...])
    """
    def parse_line(l):
        parts = l.split('\t')
        return (int(parts[0]), float(parts[1]), list(parts[2:]))
    with open(path, 'r') as f:
        return [parse_line(l.rstrip('\n')) for l in f]
