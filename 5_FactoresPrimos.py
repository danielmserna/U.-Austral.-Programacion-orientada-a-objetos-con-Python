import unittest

def is_prime(n):
    if n <= 1:
        result = False
    else:
        result = True
    for div in range(2, n):
        if n % div == 0:
            result = False
            break;
    return result

def primes_to(n):
    primes = []
    for x in range(2, n+1):
        if is_prime(x):
            primes.append(x)
    return primes

def prime_factors(n):
    result = []
    for div in primes_to(n):
        while n % div == 0:
            result.append(div)
            n /= div
    return result

class IsPrimeTestCase(unittest.TestCase):

    def test_is_prime_1(self):
        result = is_prime(1)
        self.assertFalse(result)

    def test_is_prime_2(self):
        result = is_prime(2)
        self.assertTrue(result)

    def test_is_prime_3(self):
        result = is_prime(3)
        self.assertTrue(result)

    def test_is_prime_4(self):
        result = is_prime(4)
        self.assertFalse(result)

    def test_is_prime_5(self):
        result = is_prime(5)
        self.assertTrue(result)

    def test_is_prime_6(self):
        result = is_prime(6)
        self.assertFalse(result)

    def test_is_prime_7(self):
        result = is_prime(7)
        self.assertTrue(result)

class PrimesToTestCase(unittest.TestCase):

    def test_primes_to_1(self):
        result = primes_to(1)
        self.assertEqual([],result)

    def test_primes_to_2(self):
        result = primes_to(2)
        self.assertEqual([2],result)

    def test_primes_to_3(self):
        result = primes_to(3)
        self.assertEqual([2,3],result)

    def test_primes_to_4(self):
        result = primes_to(4)
        self.assertEqual([2,3],result)

    def test_primes_to_5(self):
        result = primes_to(5)
        self.assertEqual([2,3,5],result)

    def test_primes_to_6(self):
        result = primes_to(6)
        self.assertEqual([2,3,5],result)

    def test_primes_to_7(self):
        result = primes_to(7)
        self.assertEqual([2,3,5,7],result)


class PrimeFactorsTestCase(unittest.TestCase):

    def test_prime_factors_of_1(self):
        result = prime_factors(1)
        self.assertEqual([],result)

    def test_prime_factors_of_2(self):
        result = prime_factors(2)
        self.assertEqual([2],result)

    def test_prime_factors_of_4(self):
        result = prime_factors(4)
        self.assertEqual([2,2],result)

    def test_prime_factors_of_6(self):
        result = prime_factors(6)
        self.assertEqual([2,3],result)

    def test_prime_factors_of_12(self):
        result = prime_factors(12)
        self.assertEqual([2,2,3],result)

    def test_prime_factors_of_91(self):
        result = prime_factors(9)
        self.assertEqual(2,len(result))
        self.assertIn(7, result)
        self.assertIn(13, result)

if __name__ == '__main__':
    unittest.main()