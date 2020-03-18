import json
import sys

input = []

line = sys.stdin.readline()
while (line): 
    input.append(line)
    line = sys.stdin.readline()

lines = "".join(input)
lines.rstrip()

oj = json.loads(lines)
print(oj['id'])
