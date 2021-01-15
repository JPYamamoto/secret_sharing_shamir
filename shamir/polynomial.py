class Polynomial:

    def __init__(self, coefficients):
        self.coefficients = coefficients


    def evaluate(self, x, prime):
        result = 0

        for coefficient in reversed(self.coefficients):
            result = ((result * x)  + coefficient) % prime

        return result

    @staticmethod
    def lagrange(points, x, prime):
        at_zero = 0

        for i in range(len(points)):
            x_i, y_i = points[i]
            at_zero = (prime + at_zero + Polynomial.multiply_points(points, x_i, x, i, y_i, prime)) % prime

        return at_zero


    @staticmethod
    def multiply_points(points, x_i, x, i, y_i, prime):
        polynom = []

        for j in range(len(points)):
            if (j == i):
                continue

            numerator = (x - points[j][0]) % prime
            denominator = (x_i - points[j][0]) % prime
            inverse_d = Polynomial.mod_inverse(denominator, prime)
            polynom.append(numerator * inverse_d)

        result = 1
        for k in range(len(polynom)):
            result *= polynom[k]

        return result * y_i


    @staticmethod
    def mod_inverse(denominator, prime):
        return pow(denominator, prime-2, prime)
