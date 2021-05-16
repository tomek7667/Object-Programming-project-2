def get_width():
    with open("World/temp.conf", 'r') as f:
        sizes = eval(f.readline())
        return int(sizes[0])


def get_height():
    with open("World/temp.conf", 'r') as f:
        sizes = eval(f.readline())
        return int(sizes[1])
