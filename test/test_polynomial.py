from shamir.polynomial import Polynomial

MODSZ = 208351617316091241234326746312124448251235562226470491514186331217050270460481
EVALUATE_AT_EIGHT = [3684728771, 241773850901, 308087426778, 572692230111, 182571175610]
EVALUATE_AT_ONE = [17629, 56534, 55522, 54020, 57237]


class TestPolynomial:

    def get_polynomials(self):
        polynomials = [
            # 9x⁹ + 28x⁸ + 901x⁷ + 321x⁶ + 982x⁵ + 123x⁴ + 932x³ + 2318x² + 780x + 11235
            [11235, 780, 2318, 932, 123, 982, 321, 901, 28, 9],
            # 395x⁹ +  9777x⁸ + 10945x⁷ + 6364x⁶ + 3071x⁵ + 611x⁴ + 3960x³ + 2525x² + 7609x + 11277
            [11277, 7609, 2525, 3960, 611, 3071, 6364, 10945, 9777, 395],
            # 1617x⁹ + 5033x⁸ + 1743x⁷ + 10565x⁶ + 4879x⁵ + 6705x⁴ + 9970x³ + 4195x² + 3213x + 7602
            [7602, 3213, 4195, 9970, 6705, 4879, 10565, 1743, 5033, 1617],
            # 3171x⁹ + 8005x⁸ + 5082x⁷ + 6906x⁶ + 8676x⁵ + 7927x⁴ + 1603x³ + 7589x² + 4566x + 495
            [495, 4566, 7589, 1603, 7927, 8676, 6906, 5082, 8005, 3171],
            # 426x⁹ + 6260x⁸ + 8483x⁷ + 8896x⁶ + 6219x⁵ + 10107x⁴ + 3059x³ + 1822x² + 91x + 11874
            [11874, 91, 1822, 3059, 10107, 6219, 8896, 8483, 6260, 426]
        ]

        return list(map(lambda p: Polynomial(p), polynomials))

    def get_points(self):
        points = [
            # 2x³ + 3x² + 2x + 6
            [(1, 13), (2, 38), (3, 93), (4, 190)],
            # 94x² + 166x + 1234
            [(2, 1942), (4, 3402), (5, 4414)],
            # -3x² + 6x + 5
            [(1, 8), (2, 5), (3, -4)],
            # 2x³ - x² - 6x + 15
            [(-3, -30), (-2, 7), (0, 15), (1, 10)]
        ]
        return (points, [6, 1234, 5, 15])


    def test_evaluate(self):
        polynomials = self.get_polynomials()
        for i in range(len(polynomials)):
            evaluate_at_eight = polynomials[i].evaluate(8, MODSZ)
            evaluate_at_one = polynomials[i].evaluate(1, MODSZ)
            assert (evaluate_at_eight == EVALUATE_AT_EIGHT[i])
            assert (evaluate_at_one == EVALUATE_AT_ONE[i])

    def test_lagrange(self):
        points, results = self.get_points()
        for i in range(len(points)):
            k = Polynomial.lagrange(points[i], 0, MODSZ)
            assert (results[i] == k)

