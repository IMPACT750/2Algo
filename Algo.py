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
    symbole_prec = None

    for i in range(n):
        if symbole_prec is None or C[i] != symbole_prec:
            gain = B * T[i]
        else:
            gain = A * T[i]

        if gain > 0:
            gain_total += gain
            indices_visites.append(i)
            symbole_prec = C[i]

    return gain_total, indices_visites


def parcours_optimal_naif(T, C, A, B):
    memorisation = {}

    def parcours_optimal_recursif(i, symbole_prec):
        if i == 0:
            return B * T[0]
        if i in memorisation:
            return memorisation[i]

        gain_max = parcours_optimal_recursif(i - 1, symbole_prec)
        for j in range(i):
            gain = parcours_optimal_recursif(j, symbole_prec) + (A if C[i] == C[j] else B) * T[i]
            gain_max = max(gain_max, gain)

        memorisation[i] = gain_max
        return gain_max

    return parcours_optimal_recursif(len(T) - 1, None)





def parcours_optimal_top_down(T, C, A, B):
    memo = {}

    def parcours_optimal_recursif(i, symbole_prec):
        if i == len(T):
            return 0

        if (i, symbole_prec) in memo:
            return memo[(i, symbole_prec)]

        gain = B * T[i] if symbole_prec is None or C[i] != symbole_prec else A * T[i]
        gain_visite = gain + parcours_optimal_recursif(i + 1, C[i])
        gain_passage = parcours_optimal_recursif(i + 1, symbole_prec)

        memo[(i, symbole_prec)] = max(gain_visite, gain_passage)

        return memo[(i, symbole_prec)]

    return parcours_optimal_recursif(0, None)




def parcours_optimal_bottom_up(T, C, A, B):
    n = len(T)
    dp = [0] * n
    indices_visites = []

    dp[0] = B * T[0]
    indices_visites.append(0)

    for i in range(1, n):
        gain_max = dp[i - 1]
        index_a_visiter = -1
        for j in range(i):
            gain = dp[j] + (A if C[i] == C[j] else B) * T[i]
            if gain > gain_max:
                gain_max = gain
                index_a_visiter = j

        if index_a_visiter != -1:
            dp[i] = gain_max
            indices_visites.append(i)
        else:
            dp[i] = dp[i - 1]

    return dp[-1], indices_visites




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
