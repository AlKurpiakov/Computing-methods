import numpy

class MatrixGenerator:
    def __init__(self, params):
        self._params = params

    def GenerateMatrix(self, size=5, min_val=1, max_val=100):
        """
        Генерирует случайную матрицу размера size x size.
        """
        return numpy.random.randint(min_val, max_val, (size, size))