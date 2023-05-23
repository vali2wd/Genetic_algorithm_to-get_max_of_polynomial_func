class Codificare():
    def __init__(self, a, b, precision):
        self.a = a
        self.b = b
        self.precision = precision
        self.l = bin((b - a) * (10 ** precision))[2:].__len__()
        self.discretion = (b - a) / (2 ** self.l)

    def compute(self, x, operation='TO'):

        # ia un FLOAT si imi zice in care interval de discretizare e
        # DAR IN BINAR
        if operation == 'TO':
            x = float(x)
            return bin(int((x - self.a) / self.discretion))[2:].zfill(self.l)
            # return bin(((x - self.a) / self.discretion).__round__(0))

        # ia un BINAR si imi zice LEFT BOUNDARY-ul lui
        elif operation == 'FROM':
            # make x int from binary
            x = int(x, 2)

            return self.a + x * self.discretion
        else:
            raise ValueError('Invalid operation')


if __name__ == '__main__':

    a, b = map(int, input().split())
    precision = int(input())
    n = int(input())

    codificare = Codificare(a, b, precision)

    for i in range(n):
        operation = input()
        x = input()
        print(codificare.compute(x, operation))
