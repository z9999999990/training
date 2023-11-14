#!/usr/bin/env python
# coding = utf-8


    
def reverse(a):
    b = str(a)
    c = b[::-1]
    d = int(c)

    if a == d :
        return True
    else:
        return False

def main():
    list = []
    for i in range(100, 1000):
        for j in range(100, 1000):
            if reverse(i*j):
                list.append(i*j)
            
    print(max(list))


if __name__ == "__main__" :
    main()
