from Hadamard import HadamardMatrix
from Matrix import Matrix
from Vector import Vector

from copy import deepcopy as copy
from random import randint

class HSSS():
    """ Secret-Sharing scheme based on Hadamard matrix. """
    def __init__(self, H, n):
        """ 
            H - Hadamard matrix,
            n - number of participants
        """
        
        H.check()
        if len(H) < n-1:
            raise Exception("Error: dimension of a matrix is less than number of participants")

        self.H = H
        self.n = n
        self.C = H.get_code()
        self.G = H.get_generator()
        self.D1, self.D3 = H.get_scheme()

    def cover(self, s):
        G0 = self.G.get_col(0).list()
        z = [randint(-100, 100) for i in range(len(G0))]
        sm = 0
        for i in range(len(G0)):
            sm += G0[i] * z[i]

        if sm != 0:
            for i in range(len(G0)):
                if G0[i] != 0:
                    sm -= G0[i] * z[i]
                    z[i] = G0[i]
                    break

        z = Matrix([z])
        u = z * self.G
        return u


def test():
    n = int(input())
    m = HadamardMatrix.new(n=n)
    for i in range(n):
        s = input()
        l = [[1, -1][j!='+'] for j in s]
        m[i] = Vector(l)

    scheme = HSSS(m, n-3)

    u = scheme.cover(123)
    print(u)

if __name__ == "__main__":
    test()
