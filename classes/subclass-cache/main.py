#!/usr/bin/python3

from a import A
from b import B

def main():
    ac = A()
    print(ac.value)
    ac.value = 'changed_classA_value'
    bc = B()

    print(bc.value)
    ac.value = 'changed_secondtime_classA_value'
    print(bc.value)
    bc.cvalue = 'changed_classB_value'
    print(ac.value)
    print(bc.cvalue)


if __name__ == '__main__':
    main()
