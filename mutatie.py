def mutatie(bitlist = str, idx_of_mutations = []):
    for i in idx_of_mutations:
        if bitlist[i] == '0':
            bitlist[i] = '1'
        else:
            bitlist[i] = '0'

    return ''.join(bitlist)

if __name__ == '__main__':
    l, k = map(int, input().split())
    bitlist = list(input())
    idx_of_mutations = list(map(int, input().split()))
    print(mutatie(bitlist, idx_of_mutations))