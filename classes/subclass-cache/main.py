#!/usr/bin/python3

from a import A
from b import B

def main():
    ac = A()
    print(ac.value)
    ac.value = 'changed_classA_value'
    print(ac.value)
    bc = B()

    print(bc.value)


if __name__ == '__main__':
    main()
