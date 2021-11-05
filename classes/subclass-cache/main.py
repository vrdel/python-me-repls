#!/usr/bin/python3

from a import A
from b import B

def main():
    ac = A()
    ac.value = 'changed_classA_value'
    bc = B()

    print(bc.value)
    print(type(bc)) # class A here

if __name__ == '__main__':
    main()
