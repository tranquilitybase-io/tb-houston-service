import json
import sys

inp = []

line = sys.stdin.readline()
while (line):
    inp.append(line)
    line = sys.stdin.readline()

lines = "".join(inp)
lines.rstrip()

oj = json.loads(lines)
print(oj['key'])
