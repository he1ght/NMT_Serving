import sys

with open(sys.argv[1], 'br') as f:
    lines = f.readlines()
    print(lines[0])
    with open(sys.argv[2], 'bw') as of:
        of.write(lines[0])
    # for line in lines:
    #     print(line)