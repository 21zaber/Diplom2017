from Hadamard import HadamardMatrix, solve_sole
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
        print("z: ")
        print(z)
        print()
        z = Matrix([z])
        u = z * self.G
        return u.list()[1:]

    def _recover_part(selfi, G, parts):
        print("recover_part")
        print("G: ", G, sep='\n')
        a = Matrix.new(n=len(parts)+1)
        for i in range(len(parts)):
            a[i] = G.get_col(parts[i][0]).list()
        a[-1] = G.get_col(0).list()
        a = a.transpose()
        print("a: ", a, sep='\n')

        x = solve_sole(a)
        print("x: ", x, sep='\n')

        s = sum([x[i] * parts[i][1] for i in range(len(x))])

        return s

    def recover(self, parts):
        """ parts = [(i1, Ui1), (i2, Ui2), ...] """

       #if parts[0][0] != 1 or parts[1][0] != 2:
       #    raise Exception("Error: first two participants must be 1 and 2.")

        s = self._recover_part(self.G, parts)
        
       #G = copy(self.G)
       #for i in range(len(G)):
       #    G[i][0] = G[i][2] - G[i][0] - G[i][1]
       #
       #s2 = self._recover_part(G, parts[2:])

        print("s: ", s)
        #print("s2: ", s2)
        return s



def test():
    n = int(input())
    m = HadamardMatrix.new(n=n)
    for i in range(n):
        s = input()
        l = [[1, -1][j!='+'] for j in s]
        m[i] = Vector(l)

    scheme = HSSS(m, n-1)

    print("H: ")
    print(m)
    u = scheme.cover(123)
    print("u: ")
    print(u)
    print()
    print("C")
    print(scheme.C)
    print("G {}x{}".format(len(scheme.G), len(scheme.G[0])))
    print(scheme.G)
    print()
    print()

    users = [3,4,6, 9, 12]
   #users = [5,7,9]
   #users = [8,10,11]
   #users = list(range(2, 11))
    users = list(range(4))

   #s = scheme.recover([(i+1, u[i]) for i in [0,1] + users])
    s = scheme.recover([(i+1, u[i]) for i in users])
    print(s)

if __name__ == "__main__":
    test()
