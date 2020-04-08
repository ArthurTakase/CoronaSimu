logs = [[1, 454, 1959, 1, 1], [2, 453, 1959, 2, 1], [3, 453, 1959, 3, 0], [4, 453, 1959, 3, 0], [4, 453, 1959, 3, 0]]

immu = []
mort = []


for i in range(len(logs)):
    immu.append(logs[i][2])
    mort.append(logs[i][3])

print(immu, mort)
