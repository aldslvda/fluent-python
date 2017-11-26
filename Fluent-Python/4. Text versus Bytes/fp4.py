
def eg_4_1():
    s = 'café'
    print(len(s))
    b = s.encode('utf8')
    print(b, len(b))
    print(b.decode('utf8'))
