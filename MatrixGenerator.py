import numpy

class MatrixGenerator:
    def __init__(self, n: int = 10, v: int = 7, a_min: float = 0.12, a_max: float = 0.22, beta1: float = 0.85, beta2: float = 1.0):
        self.n = n
        self.v = v
        self.a_min = a_min
        self.a_max = a_max
        self.beta1 = beta1
        self.beta2 = beta2

        self._validate_parameters()
    def _validate_parameters(self):
        if self.n <= 0:
            raise ValueError("n must be more than 0")
        if self.v <= 20:
            raise ValueError("v must be more than 20")
        if self.a_min >= self.a_max:
            raise ValueError("a_min must be less than a_max")
        if self.beta1 >= self.beta2:
            raise ValueError("beta1 must be less than beta2")
        if not (0.85 <= self.beta1 < self.beta2 <= 1.0):
                raise ValueError("beta1 and beta2 must be in range [0.85, 1.0]")
                
    def _init_small_experiment(self, distribution_type: str) -> Tuple[np.ndarray, np.ndarray]:
        a_vector = np.random.uniform(self.a_min, self.a_max, self.n) # сахаристость
        b_matrix = np.zeros((self.n, self.v))  # коэффициенты деградации (без дозаревания)
        
        if distribution_type == "uniform":  # равномерное распределение
            b_matrix = np.random.uniform(self.beta1, self.beta2, (self.n, self.v))
        elif distribution_type == "concentrated": # концентрированное распределение
            for i in range(self.n):
                max_delta = (self.beta2 - self.beta1) / 4   
                delta_i = np.random.uniform(0, max_delta) # δ_i
                
                beta1_i = np.random.uniform(self.beta1, self.beta2 - delta_i) # случайный подотрезок
                beta2_i = beta1_i + delta_i
                b_matrix[i, :] = np.random.uniform(beta1_i, beta2_i, self.v)  # коэффициенты для i-й партии
        
        return a_vector, b_matrix
    
    def GenerateMatrix(self):
        return 0