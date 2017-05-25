from Matrix import Matrix
from Vector import Vector

from copy import deepcopy as copy

def gauss(a):
    n = len(a)
    m = len(a[0])

    rows = [i for i in range(n)]

    for i in range(min(m, n)):
        mx = i
        for j in range(i, n):
            if abs(a[j][i]) > abs(a[mx][i]):
                mx = j
        if abs(a[mx][i]) < 0.00001:
            continue
        a[mx], a[i] = a[i], a[mx]
        rows[mx], rows[i] = rows[i], rows[mx]

        for j in range(i+1, n):
            koef = a[j][i] / a[i][i]
            for k in range(i, m):
                a[j][k] -= a[i][k] * koef

    return Matrix(a), rows

def solve_sole(a, debug=False):
    n = len(a)
    m = len(a[0])

    if debug:
        print("SoLE:")
        for i in a:
            s = ''
            for j in range(m-1):
                s += "{}*x{} + ".format(i[j], j)

            s = s[:-2] + " = {}".format(i[-1])
            print(s)

    
    a, _ = gauss(a)
    print()
    print(a)
    x = [0 for i in range(m-1)]
    for i in range(min(m-2,n-1), -1, -1):
        if abs(a[i][i]) > 0.0001:
            x[i] = a[i][-1] / a[i][i] 
            for j in range(i):
                a[j][-1] -= a[j][i] / a[i][i] * a[i][-1]

    return Vector(x)

def get_basis(a):
    elems = copy(a)
    a, rows = gauss(a)
    G = Matrix.new(n=0)
    for i in range(len(a)):
        if abs(a[i]) > 0.0001:
            G.append(elems[rows[i]])

    return G


class HadamardMatrix(Matrix):

    def check(h):
        """ Check matrix for Hadamard. """

        n = len(h)

        if n < 1 or n != len(h[0]):
            raise Exception("Error: Nonsuare or empty Matrix")

        for i in h:
            for j in i:
                if j not in [-1,  1]:
                    raise Exception("Error: Wrong element {}".format(j))
        
        t = h.transpose()
        m = h * t
        e = Matrix.E(n) * n

        if e != m:
            raise Exception("Error: Matrix isn't Hadamard")

        return True

    def normalize(h):
        return h

    def get_code(h):
        elems = [tuple(i) for i in h] + [tuple(i) for i in h * -1]
        elems = list(set(elems))

        C = Matrix.new(n=len(elems), m = len(h))

        for i in range(len(elems)):
            C[i] = Vector([(1-j)/2 for j in elems[i]])

        return C

    def get_generator(h):
        a = h.get_code()
        
        G = get_basis(a)[:len(h)//2]

       #G, _ = gauss(G)
       #
       #print(G)
       #
       #for i in range(len(G)-1, -1, -1):
       #    for j in range(i+1, len(G[0])):
       #        G[i][j] /= G[i][i]
       #
       #    G[i][i] = 1
       #    
       #    for j in range(i):
       #        for k in range(i+1, len(G[0])):
       #            G[j][k] -= G[j][i] * G[i][k]
       #
       #        G[j][i] = 0

        return Matrix(G)

    def _get_generator(h):
        a = h.get_code()
        elems = copy(a)
        n = len(a)
        m = len(a[0])
        rows = [i for i in range(n)]

        for i in range(m):
            mx = i
            for j in range(i, n):
                if abs(a[j][i]) > abs(a[mx][i]):
                    mx = j
            if abs(a[mx][i]) < 0.00001:
                continue
            a[mx], a[i] = a[i], a[mx]
            rows[mx], rows[i] = rows[i], rows[mx]

            for j in range(i+1, n):
                koef = a[j][i] / a[i][i]
                for k in range(i, m):
                    a[j][k] -= a[i][k] * koef
        print("======")
        print(a)
        print("======")

        G = Matrix.new(n=0, m=0)
        for i in range(n):
            if abs(a[i]) > 0.0001:# and len(G) < m:
                G.append(elems[rows[i]])

        return G

    def get_scheme(h):
        hn = h.normalize()

        hn = HadamardMatrix(hn[1:])

        C = hn.get_code()
        D1 = Matrix.new(n=0, m=0)
        for i in C:
            if i[0] == 1:
                D1.append(Vector(i))
        D2 = Matrix.new(n=0, m=0)
        for i in D1:
            if i[1] == 1:
                D2.append(Vector(i))
        D3 = Matrix.new(n=0, m=0)
        for i in D2:
            if i[2] == 1:
                D3.append(Vector(i))

        return (D1, D3)

def test():
    n = int(input())
    m = HadamardMatrix.new(n=n)
    for i in range(n):
        s = input()
        print(s)
        l = [[1, -1][j!='+'] for j in s]
        m[i] = Vector(l)

    print("Tested matrix: ")
    print(m)
    print("Check passed: ", m.check())
    print("Code: ")
    print(m.get_code())
    g = m.get_generator()
    print("Generator matrix: {}x{}".format(len(g), len(g[0])))
    print(g)
    print("Scheme matrixes: ")
    D1, D3 = m.get_scheme()
    print("D1:")
    print(D1)
    print("D3:")
    print(D3)

if __name__ == "__main__":
    test()


