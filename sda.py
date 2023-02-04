def sadsd():
    k1 = ['20', '3', '8', '23', '31', '22', '30']
    k2 = ['20']
    return k1, k2


if __name__ == '__main__':
    k1= sadsd()
    print(k1)
    if isinstance(k1, tuple):
        print("tuple")
    else:
        print("not tuple")
