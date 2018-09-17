x = lambda d: "".join([chr(ord(x) ^ 0x6e) for x in d])
with open("CC_traffic.txt") as f:
    content = f.readlines()
    for line in content:
        print(x(line))
