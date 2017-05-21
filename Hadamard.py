from Matrix import Matrix
from Vector import Vector

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

    def get_code(h):
        pass

    def get_generator(h):
        pass

    def get_scheme(h):
        pass



def test():
    m = HadamardMatrix.new(n=4, m=4)
    m[0] = Vector.read(" 1  1  1  1")
    m[1] = Vector.read(" 1 -1  1 -1")
    m[2] = Vector.read(" 1  1 -1 -1")
    m[3] = Vector.read(" 1 -2 -1  1")

    print(m)
    print(m.check())

if __name__ == "__main__":
    test()


