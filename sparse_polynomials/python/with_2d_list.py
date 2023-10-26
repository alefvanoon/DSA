import re

class SparsePolynomial:
    """
    A class to represent a sparse polynomial using a 2D list.
    Each term is represented as [coefficient, exponent].
    """

    def __init__(self, polynomial_str=""):
        # Initialize an empty 2D list to store the polynomial terms.
        self.terms = []
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
            # Use binary search to find the index to insert the new term.
            left, right = 0, len(self.terms) - 1
            while left <= right:
                mid = (left + right) // 2
                if self.terms[mid][1] == exponent:
                    self.terms[mid][0] += coefficient
                    break
                elif self.terms[mid][1] < exponent:
                    left = mid + 1
                else:
                    right = mid - 1
            else:
                # If the loop completes without finding a term with the same exponent, insert the new term.
                self.terms.insert(left, [coefficient, exponent])

    def evaluate(self, x):
        """
        Evaluate the polynomial for a given value of x.

        :param x: The value at which to evaluate the polynomial.
        :return: The result of the polynomial evaluation.
        """
        result = 0
        for coefficient, exponent in self.terms:
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
        i = 0  # Index for self.terms
        j = 0  # Index for other.terms

        while i < len(self.terms) and j < len(other.terms):
            coeff1, exp1 = self.terms[i]
            coeff2, exp2 = other.terms[j]

            if exp1 == exp2:
                result.add_term(coeff1 + coeff2, exp1)
                i += 1
                j += 1
            elif exp1 < exp2:
                result.add_term(coeff1, exp1)
                i += 1
            else:
                result.add_term(coeff2, exp2)
                j += 1

        # Append any remaining terms from self.terms and other.terms
        result += self.terms[i:] + other.terms[j:]

        return result

    def find_coefficient(self, n):
        """
        Return the coefficient of the term with exponent n.

        :param n: The exponent of the term to return.
        :return: A float coefficient for the term with exponent n.
        """
        # Use binary search to find the index to insert the new term.
        left, right = 0, len(self.terms) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.terms[mid][1] == n:
                return self.terms[mid][0]
            elif self.terms[mid][1] < n:
                left = mid + 1
            else:
                right = mid - 1
        # If the loop completes without finding a term with the same exponent, return 0.
        return 0

    def __str__(self):
        """
        Return a string representation of the polynomial.

        :return: A string representing the polynomial.
        """
        terms_str = [f"{coeff}x^{exp}" if exp > 0 else str(coeff) for coeff, exp in self.terms]
        terms_str.reverse()
        return " + ".join(terms_str)

# Example test:
polynomial_str1 = "2.1x^8 + 30x^9 + 3x + 10 + 10x^9 + 1 - 10"
sp1 = SparsePolynomial(polynomial_str1)
print(sp1)
print(sp1.find_coefficient(9))