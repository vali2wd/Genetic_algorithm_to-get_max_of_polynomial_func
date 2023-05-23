import bisect
import copy
import random
import sys
sys.stdout = open('GeneticOutput.txt', 'w')
def incrucisare_2_chromo(chromoA, chromoB, idx_of_crossover):
    pickA = chromoA[idx_of_crossover:]
    pickB = chromoB[idx_of_crossover:]
    newChromoA = chromoA[:idx_of_crossover] + pickB
    newChromoB = chromoB[:idx_of_crossover] + pickA

    return newChromoA, newChromoB
class Chromosome():
    def __init__(self, binary_str, left_boundary, f_left_boundary, probabilitate_selectie = 0):
        self.binar = binary_str
        self.left_boundary = left_boundary
        self.f_left_boundary = f_left_boundary
        self.probabilitate_selectie = probabilitate_selectie

    #setter for left_boundary
    def set_left_boundary(self, left_boundary):
        self.left_boundary = left_boundary

    #setter for f_left_boundary
    def set_f_left_boundary(self, f_left_boundary):
        self.f_left_boundary = f_left_boundary

    # getter for binary_str
    def get_binary_str(self):
        return self.binar

    #setter for binary_str
    def set_binary_str(self, binary_str):
        self.binar = binary_str



    def __str__(self):
        return f'{self.binar} x={self.left_boundary.__round__(6)} f={self.f_left_boundary}'

    def repr_probabilitati_selectie(self):
        return 'probabilitate ' + str(self.probabilitate_selectie)

class PolyFun():
    a = 0
    b = 0
    c = 0

    @classmethod
    def set_coefficients(cls, a, b, c):
        cls.a = a
        cls.b = b
        cls.c = c

    @classmethod
    def compute(cls, x):
        return cls.a * x ** 2 + cls.b * x + cls.c


class Codificare():
    def __init__(self, a, b, precision):
        self.a = a
        self.b = b
        self.precision = precision
        self.l = bin((b - a) * (10 ** precision))[2:].__len__()
        self.discretion = (b - a) / (2 ** self.l)

    def compute(self, x, operation='TO'):
        if operation == 'TO':
            x = float(x)
            return bin(int((x - self.a) / self.discretion))[2:].zfill(self.l)
            # return bin(((x - self.a) / self.discretion).__round__(0))
        elif operation == 'FROM':
            # make x int from binary
            x = int(x, 2)
            # ia un BINAR si imi zice LEFT BOUNDARY-ul lui
            return self.a + x * self.discretion
        else:
            raise ValueError('Invalid operation')


class GeneticPolyDetermination():
    def __init__(self, file):
        file = open(file, 'r')
        self.dimensiunea_populatiei = int(file.readline())
        self.a, self.b = map(int, file.readline().split())

        self.coef_polinom = list(map(int, file.readline().split()))
        PolyFun.set_coefficients(self.coef_polinom[0], self.coef_polinom[1], self.coef_polinom[2])

        self.precizie = int(file.readline())
        self.recombinare = int(file.readline())/100
        self.mutatie = int(file.readline())/100
        self.nr_generatii = int(file.readline())

        self.lungime_biti = bin((self.b - self.a) * (10 ** self.precizie))[2:].__len__()

        self.codificareManager = Codificare(self.a, self.b, self.precizie)

        # print(self.dimensiunea_populatiei)
        # print(self.a, self.b)
        # print(self.coef_polinom)
        # print(self.precizie)
        # print(self.recombinare)
        # print(self.mutatie)
        # print(self.nr_generatii)
        # print(self.lungime_biti)

        self.populatie = []
        # initializare cromozomi
        for binar in self.generate_population(self.dimensiunea_populatiei):
            left_boundary = self.codificareManager.compute(binar, 'FROM')
            f_de_x = PolyFun.compute(left_boundary)
            self.populatie.append(Chromosome(binar, left_boundary, f_de_x))




        self.calc_probabilitati_selectie()
        for i in self.populatie:
            i.repr_probabilitati_selectie()

        self.intervale_selectie = []
        self.set_intervale_prob_selectie()



    def retrieve_max(self):
        return max(self.populatie, key=lambda x: x.f_left_boundary)

    def set_at_min(self, chromo):

        idx = self.populatie.index(min(self.populatie, key=lambda x: x.f_left_boundary))
        print("idx: ", idx, "chromo: ", chromo)
        self.populatie[idx] = copy.deepcopy(chromo)

    def print_epoch_max(self):
        print('Maximul din populatie: ', max(self.populatie, key=lambda x: x.f_left_boundary))
    def print_intervale_selectie(self):
        print("STARTOF Intervale probabilitati selectie: ----------------------------")
        print(*self.intervale_selectie)
        print("ENDOF Intervale probabilitati selectie: ----------------------------")
    def print_populatie(self):
        print("STARTOF Populatia: ----------------------------")
        for idx, i in enumerate(self.populatie):
            print(idx,': ',i, sep='')
        print("ENDOF Populatia: ----------------------------")
    def print_probabilitati_selectie(self):
        print("STARTOF Probabilitati selectie: ----------------------------")
        for idx, i in enumerate(self.populatie):
            print('cromozom ' + str(idx + 1) + ' '+ i.repr_probabilitati_selectie(), sep='')
        print("ENDOF Probabilitati selectie: ----------------------------")

    def calc_probabilitati_selectie(self):
        suma = sum([i.f_left_boundary for i in self.populatie])
        for i in self.populatie:
            i.probabilitate_selectie = i.f_left_boundary / suma

    def set_intervale_prob_selectie(self):
        self.intervale_selectie = [0]
        for i in range(1, len(self.populatie)):
            a = sum([j.probabilitate_selectie for j in self.populatie[:i]])
            self.intervale_selectie.append(a)
        self.intervale_selectie.append(1.0)

    def selectie(self):
        print("STARTOF Selectie: ---------------------------------")
        new_population = []
        for _ in range(20):
            u = random.uniform(0, 1)
            # binary search in self.intervale_selectie using library
            # cautare binara lui u generat aleator in intervalele de selectie
            idx = bisect.bisect_left(self.intervale_selectie, u)
            # print(idx)
            x = copy.deepcopy(self.populatie[idx-1])
            new_population.append(x)
            print('u=',u, 'selectam cromozomul ', idx)
        self.populatie = new_population
        print('Dupa selectie:')

        # REFRESH PROBABILITATI SELECTIE SI INTERVALE
        # DUPA SELECTIE
        self.calc_probabilitati_selectie()
        self.set_intervale_prob_selectie()

        self.print_populatie()
        print("ENDOF Selectie: ---------------------------------")



    def incrucisare(self):
        # max from self.populatie by f_left_boundary
        # pentru criterul elitismului se salveaza maximul, nu este supus altor modificari
        # IAU MAXIM SI IL PUN IN LOCUL MINIMULUI DUPA CE DAU CROSSOVER
        # maxim = copy.deepcopy(max(self.populatie, key=lambda x: x.f_left_boundary))
        print('STARTOF Incrucisare: ---------------------------------')
        new_population_binaries = []
        last_tagged = -1
        print('Probabilitate de incrucisare: ', self.recombinare)
        for i in range(20):
            new_population_binaries.append(self.populatie[i].binar)
            u = random.uniform(0, 1)
            print(i,': ',self.populatie[i].binar, 'u=',u, f'<{self.recombinare} participa' if u < self.recombinare else '')
            if u < self.recombinare:
                if last_tagged == -1:
                    last_tagged = i
                else:
                    # incrucisare
                    print('Incrucisare intre: ', last_tagged, i)
                    # 1. alegem un punct de incrucisare
                    punct_incrucisare = random.randint(1, self.lungime_biti - 1)
                    print('Punct de incrucisare: ', punct_incrucisare)
                    print('Inainte de incrucisare: ', self.populatie[last_tagged].binar, self.populatie[i].binar)
                    # 2. facem incrucisarea
                    copyA = copy.deepcopy(self.populatie[last_tagged].binar)
                    copyB = copy.deepcopy(self.populatie[i].binar)
                    self.populatie[last_tagged].set_binary_str(copyA[:punct_incrucisare] + copyB[punct_incrucisare:])
                    self.populatie[i].set_binary_str(copyB[:punct_incrucisare] + copyA[punct_incrucisare:])
                    print('Dupa incrucisare: ', self.populatie[last_tagged].binar, self.populatie[i].binar)

                    # UPDATE VALORILOR FIINDCA S+AU MODIFICAT
                    self.populatie[last_tagged].f_left_boundary = self.codificareManager.compute(self.populatie[last_tagged].binar, 'FROM')
                    self.populatie[last_tagged].f_left_boundary = PolyFun.compute(self.populatie[last_tagged].f_left_boundary)
                    self.populatie[i].f_left_boundary = self.codificareManager.compute(self.populatie[i].binar, 'FROM')
                    self.populatie[i].f_left_boundary = PolyFun.compute(self.populatie[i].f_left_boundary)
                    last_tagged = -1
        print('ENDOF Incrucisare: ---------------------------------')


        self.calc_probabilitati_selectie()
        self.set_intervale_prob_selectie()
        # print(maxim)
        # get idx of min in self.populatie by f_left_boundary
        # min_idx = self.populatie.index(min(self.populatie, key=lambda x: x.f_left_boundary))

        # self.populatie[min_idx] = copy.deepcopy(maxim)
        print('Dupa incrucisare:')
        self.print_populatie()


    def mutatie_cromozomi(self):
        print('STARTOF Mutatie: ---------------------------------')
        for i in range(len(self.populatie)):
            u = random.uniform(0, 1)
            if u <= self.mutatie:
                print("Se modifica cromozomul ", i)
                print('Inainte de mutatie: ', self.populatie[i].binar)
                random_point_of_mutation = random.randint(0, self.lungime_biti - 1)
                print('Punct de mutatie: ', random_point_of_mutation)

                binar_list = list(self.populatie[i].binar)
                binar_list[random_point_of_mutation] = '1' if binar_list[random_point_of_mutation] == '0' else '0'
                self.populatie[i].binar = ''.join(binar_list)

                self.populatie[i].left_boundary = self.codificareManager.compute(self.populatie[i].binar, 'FROM')
                self.populatie[i].f_left_boundary = PolyFun.compute(self.populatie[i].left_boundary)
                print('Dupa mutatie: ', self.populatie[i].binar)

        self.calc_probabilitati_selectie()
        self.set_intervale_prob_selectie()
        print('ENDOF Mutatie: ---------------------------------')
















    def generate_population(self, amt):
        population = []

        for i in range(amt):
            x = random.getrandbits(self.lungime_biti)
            population.append(
                bin(x)[2:].zfill(self.lungime_biti)
            )

        return population

    def mean_fitness(self):
        return sum([i.f_left_boundary for i in self.populatie]) / len(self.populatie)



if __name__ == '__main__':
    geneticPolyDetermination = GeneticPolyDetermination('HWGenetici.txt')
    for i in range(100):
        print("EPOCA ", i+1, ":---------------------------------- ")
        geneticPolyDetermination.print_populatie()
        geneticPolyDetermination.print_probabilitati_selectie()
        geneticPolyDetermination.print_intervale_selectie()
        maxim = geneticPolyDetermination.retrieve_max()
        print("MAXIM FITNESS", maxim)
        print("MEAN FITNESS", geneticPolyDetermination.mean_fitness())
        geneticPolyDetermination.selectie()
        geneticPolyDetermination.incrucisare()
        geneticPolyDetermination.mutatie_cromozomi()
        geneticPolyDetermination.set_at_min(maxim)
        geneticPolyDetermination.print_epoch_max()
        geneticPolyDetermination.print_populatie()

    # OUTPUT REDIRECTIONAT CATRE GENETICOUTPUT>TXT
    sys.stdout.close()