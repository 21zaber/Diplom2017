from Hadamard import HadamardMatrix, solve_sole
from Matrix import Matrix
from Vector import Vector

from copy import deepcopy as copy
from random import randint



class HSSS():
    """ Secret-Sharing scheme based on Hadamard matrix. """
    def __init__(self, H):
        """ 
            H - Hadamard matrix,
            n - number of participants
        """
        
        H.check()

        self.H = H
        self.C = H.get_code()
        self.G = H.get_generator()
        self.D1, self.D3 = H.get_scheme()

    def cover(self, s):
        G0 = self.G.get_col(0).list()
        z = [randint(-100000, 100000)/100 for i in range(len(G0))]
        sm = -s

        for i in range(len(G0)):
            sm += G0[i] * z[i]

        if sm != 0:
            for i in range(len(G0)):
                if G0[i] != 0:
                    sm -= G0[i] * z[i]
                    z[i] = -sm
                    break
        z = Matrix([z])
        u = z * self.G
        return u.list()[1:]

    def _recover(self, parts):
        a = Matrix.new(n=len(parts)+1)
        for i in range(len(parts)):
            a[i] = self.G.get_col(parts[i][0]).list()
        a[-1] = self.G.get_col(0).list()
        a = a.transpose()
        x = solve_sole(a)
        s = sum([x[i] * parts[i][1] for i in range(len(x))])

        return s

    def _check_parts(self, parts):
        t = Matrix([self.D1.get_col(i[0]).list() for i in parts])
        t = [sum(t.get_col(i).list()) for i in range(len(t[0]))]
        t = [int(i > 0) for i in t]
        return len(t) == sum(t)

    def recover(self, parts):
        """ parts = [(i1, Ui1), (i2, Ui2), ...] """

        if not self._check_parts(parts):
            raise Exception("Error: that parts cannot recover secret")

        return self._recover(parts)



def test():
    n = int(input())
    m = HadamardMatrix.new(n=n)
    for i in range(n):
        s = input()
        l = [[1, -1][j!='+'] for j in s]
        m[i] = Vector(l)

    scheme = HSSS(m)

    print("H: ")
    print(m)
    secret = randint(0, 100000)
    print("secret:", secret)
    u = scheme.cover(secret)
    print("u: ")
    print(u)
    print()
    print("C {}x{}".format(len(scheme.C), len(scheme.C[0])))
    print(scheme.C)
    print("D1 {}x{}".format(len(scheme.D1), len(scheme.D1[0])))
    print(scheme.D1)
    print("G {}x{}".format(len(scheme.G), len(scheme.G[0])))
    print(scheme.G)
    print()

    for i in range(10000):
        user_idx = set()
        parts_size = randint(2, 14)
        while len(user_idx) < parts_size:
            user_idx.add(randint(0, n-2))
        parts = [(i+1, u[i]) for i in user_idx]
        s = scheme._recover(parts)
        if abs(s - secret) < 0.0001:
            if not scheme._check_parts(parts):
                print("Error")
                print(parts)

if __name__ == "__main__":
    test()
