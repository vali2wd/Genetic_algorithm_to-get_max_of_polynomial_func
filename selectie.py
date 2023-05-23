
class Polyfun():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def compute(self, x):
        return self.a * x ** 2 + self.b * x + self.c

# primeste o LISTA DE CROMOZOMI ca FLOAT

# chromo = [1 1.5 2.5]

# returneaza capetele intervalelor de selectie
# OUTPUT = [0.000000
# 0.266666
# 0.633333
# 1.000000]
def boundaries(polycoef=[], chromo=[]):
    polyfun = Polyfun(polycoef[0], polycoef[1], polycoef[2])
    chromocomputed = list(map(polyfun.compute, chromo))

    # print(*chromocomputed)
    F = sum(chromocomputed)
    # print(F)

    interval_boundaries = [0]
    for i in range(len(chromocomputed)):
        interval_boundaries.append(
            (sum(chromocomputed[:i + 1]) / F).__round__(6)
        )

    return interval_boundaries


if __name__ == '__main__':
    polycoef = list(map(int, input().split()))
    n = int(input())
    chromo = list(map(float, input().split()))
    # how to print wiht precision
    #
    print(*boundaries(polycoef, chromo), sep='\n')
