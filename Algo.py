import sys

sys.setrecursionlimit(10000)

def lire_fichier(nom_fichier):
    T = []
    C = []
    with open(nom_fichier, 'r') as file:
        for line in file:
            values = line.strip().split()
            T.append(int(values[0]))
            C.append(int(values[1]))
    return T, C


def strategie_gloutonne(T, C, A, B):
    n = len(T)
    indices_visites = []
    gain_total = 0

    for i in range(n):
        if i == 0 or C[i] != C[i - 1]:
            gain = B * T[i]
        else:
            gain = A * T[i]

        if gain > 0:
            gain_total += gain
            indices_visites.append(i)

    return gain_total, indices_visites


def parcours_optimal_naif(T, C, A, B):
    memorisation = {}

    def parcours_optimal_recursif(i, symbol_prec):
        if i == 0:
            return B * T[0]
        if i in memorisation:
            return memorisation[i]

        max_gain = parcours_optimal_recursif(i - 1, symbol_prec)
        for j in range(i):
            if C[i] == C[j]:
                gain = parcours_optimal_recursif(j, symbol_prec) + A * T[i]
            else:
                gain = parcours_optimal_recursif(j, symbol_prec) + B * T[i]
            max_gain = max(max_gain, gain)

        memorisation[i] = max_gain
        return max_gain

    return parcours_optimal_recursif(len(T) - 1, None)


def parcours_optimal_top_down(T, C, A, B):
    memo = {}

    def parcours_optimal_recursif(i, symbole_prec):
        if i == len(T):
            return 0

        if (i, symbole_prec) in memo:
            return memo[(i, symbole_prec)]

        if symbole_prec is None or C[i] != symbole_prec:
            gain = B * T[i]
        else:
            gain = A * T[i]

        gain_visite = gain + parcours_optimal_recursif(i + 1, C[i])
        gain_passage = parcours_optimal_recursif(i + 1, symbole_prec)

        memo[(i, symbole_prec)] = max(gain_visite, gain_passage)

        return memo[(i, symbole_prec)]

    return parcours_optimal_recursif(0, None)


def parcours_optimal_bottom_up(T, C, A, B):
    n = len(T)
    memo = [0] * n
    indices = []

    memo[0] = B * T[0]
    indices.append(0)

    for i in range(1, n):
        max_gain = memo[i - 1]
        visit_index = -1
        for j in range(i):
            if C[i] == C[j]:
                gain = memo[j] + A * T[i]
            else:
                gain = memo[j] + B * T[i]
            if gain > max_gain:
                max_gain = gain
                visit_index = j

        if visit_index != -1:
            memo[i] = max_gain
            indices.append(i)
        else:
            memo[i] = memo[i - 1]

    return memo[-1], indices


def main():
    # Exemple 1
    T = [9, 7, 8, 7, 10, 7]
    C = [2, 1, 1, 4, 4, 2]
    A = -2
    B = 5

    print("Exemple 1 gloutonne :", strategie_gloutonne(T, C, A, B))
    print("Exemple 1 naif :", parcours_optimal_naif(T, C, A, B))
    print("Exemple 1 top down :", parcours_optimal_top_down(T, C, A, B))
    print("Exemple 1 bottom up:", parcours_optimal_bottom_up(T, C, A, B))

    # Exemple 2
    T = [3, 9, 2, 7, 3, 1]
    C = [2, 2, 5, 4, 2, 1]
    A = 2
    B = -5
    print("Exemple 2 gloutonne:", strategie_gloutonne(T, C, A, B))
    print("Exemple 2 gloutonne:", parcours_optimal_naif(T, C, A, B))
    print("Exemple 2 top down :", parcours_optimal_top_down(T, C, A, B))
    print("Exemple 2 bottom up:", parcours_optimal_bottom_up(T, C, A, B))


    # Avec le fichier MP.txt
    T, C = lire_fichier('MP.txt')
    A,B = -3, 7
    print("Résultat Stratégie Gloutonne:", strategie_gloutonne(T, C, A, B))
    print("Résultat Parcours Optimal Naif:", parcours_optimal_naif(T, C, A, B))
    print("Résultat Parcours Optimal Top-Down:", parcours_optimal_top_down(T, C, A, B))
    print("Résultat Parcours Optimal Bottom-Up:", parcours_optimal_bottom_up(T, C, A, B))

if __name__ == "__main__":
    main()
