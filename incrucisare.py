def incrucisare(chromoA, chromoB, idx_of_crossover):
    pickA = chromoA[idx_of_crossover:]
    pickB = chromoB[idx_of_crossover:]
    newChromoA = chromoA[:idx_of_crossover] + pickB
    newChromoB = chromoB[:idx_of_crossover] + pickA

    return newChromoA, newChromoB

if __name__ == '__main__':
    n = int(input())
    chromoA = input()
    chromoB = input()
    idx_of_crossover = int(input())
    print(*incrucisare(chromoA, chromoB, idx_of_crossover), sep = '\n')