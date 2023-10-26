import re

class SparsePolynomial:
    """
    A class to represent a sparse polynomial using a dictionary.
    Keys represent exponents, and values represent coefficients.
    """

    def __init__(self, polynomial_str=""):
        # Initialize an empty dictionary to store the polynomial terms.
        self.terms = {}
        if polynomial_str:
            self.parse_polynomial_string(polynomial_str)

    def parse_polynomial_string(self, polynomial_str):
        """
        Parse a polynomial string and add the terms to the polynomial.

        :param polynomial_str: The polynomial string to parse.
        """
        # Remove spaces from the input string.
        polynomial_str = polynomial_str.replace(" ", "")
        # Split the input string using '+' and '-' as delimiters.
        terms = re.split(r'(?=[-+])', polynomial_str)
        print(terms)
        for term in terms:
            term = term.strip()
            match = re.match(r'([-+]?\d*(?:\.\d+)?)x\^?(\d*)', term)
            if match:
                coefficient = float(match.group(1))
                exponent = int(match.group(2)) if match.group(2) else 1
            else:
                # If there's no 'x' in the term, it's a constant term (e.g., 9).
                coefficient = float(term)
                exponent = 0
            self.add_term(coefficient, exponent)

    def add_term(self, coefficient, exponent):
        """
        Add a new term to the polynomial.

        :param coefficient: The coefficient of the term.
        :param exponent: The exponent of the term.
        """
        if coefficient != 0:
            if exponent in self.terms:
                self.terms[exponent] += coefficient
            else:
                self.terms[exponent] = coefficient

    def evaluate(self, x):
        """
        Evaluate the polynomial for a given value of x.

        :param x: The value at which to evaluate the polynomial.
        :return: The result of the polynomial evaluation.
        """
        result = 0
        for exponent, coefficient in self.terms.items():
            result += coefficient * (x ** exponent)
        return result

    def __add__(self, other):
        """
        Add two sparse polynomials and return a new sparse polynomial.

        :param other: Another sparse polynomial to add.
        :return: A new sparse polynomial representing the sum.
        """
        if not isinstance(other, SparsePolynomial):
            raise TypeError("The 'other' object must be an instance of SparsePolynomial.")
        result = SparsePolynomial()
        for exponent, coefficient in self.terms.items():
            result.add_term(coefficient, exponent)
        for exponent, coefficient in other.terms.items():
            result.add_term(coefficient, exponent)
        return result

    def find_coefficient(self, n):
        """
        Return the coefficient of the term with exponent n.

        :param n: The exponent of the term to return.
        :return: A float coefficient the term with exponent n.
        """
        return self.terms[n]

    def __str__(self):
        """
        Return a string representation of the polynomial.

        :return: A string representing the polynomial.
        """
        terms_str = [f"{coeff}x^{exp}" if exp > 0 else str(coeff) for exp, coeff in self.terms.items()]
        return " + ".join(terms_str)

# Example test:
polynomial_str1 = "2.1x^8 + 30x^9 + 3x + 10 + 10x^9 + 1 - 10"
sp1 = SparsePolynomial(polynomial_str1)
print(sp1)
print(sp1.find_coefficient(9))
