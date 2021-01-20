class Polynomial:
    """Polynomial related methods.
    A polynomial is described by a list of its coefficient, where
    the entry at index i is the coefficient of x^i.
    """

    def __init__(self, coefficients):
        self.coefficients = coefficients


    def evaluate(self, x, prime):
        """Horner's method.
        This method allows the evaluation of a polynomial of degree n
        with only n multiplications and n additions (arithmetic operation).
        This is optimal, since there are polynomials of degree n that cannot be evaluated
        with fewer arithmetic operations.

        Args:
            x: The number in which we will evaluate the polynomial.
            prime: The prime number which will apply the module operation.
        """
        result = 0

        for coefficient in reversed(self.coefficients):
            result = ((result * x)  + coefficient) % prime

        return result

    @staticmethod
    def lagrange(points, x, prime):
        """Lagrange polynomials are used for polynomial interpolation.
        For a given list of points (x_j , y_j) with all differents x_j values for all x_j in the list,
        the Lagrange interpolation polynomial is the polynomial of lowest degree that assumes at each value x_j
        the corresponding value y_j, so that the functions coincide at each point.

        Args:
            points: List of tuples representing points in the plane, which pass through the polynomial.
            x: List of tuples representing points in the plane, which pass through the polynomial.
            prime: The prime number which will apply the module operation.
        """
        at_zero = 0

        for i in range(len(points)):
            x_i, y_i = points[i]
            at_zero = (prime + at_zero + Polynomial.multiply_points(points, x_i, x, i, y_i, prime)) % prime

        return at_zero


    @staticmethod
    def multiply_points(points, x_i, x, i, y_i, prime):
        """We calculate the interpolation polynomial of Lagrange in x_i.

        Args:
            points: List of tuples representing points in the plane, which pass through the polynomial.
            x_i: The point at which we are making the interpolation of the polynomial.
            i: Index
            y_i: f(x_i)
            prime: The prime number which will apply the module operation.
        """
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
        """We neet to get the multiplicative inverse of denominator
        in the field Z_p, for this reason we must implement the Fermat's
        little theorem.
        Fermat's little theorem states that if p is a prime number, then
        for any integer a, the number a^p − a is an integer multiple of p.

        Args:
            denominator: The number to which we should get your multiplicative inverse in the field Z_p.
            prime: The prime number which will help us to get the multiplicative inverse.
        """
        return pow(denominator, prime-2, prime)
