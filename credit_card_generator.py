#! /usr/bin/env python

'''
|-------------------+--------------------------------------+---------------------------|
| Credit card brand | Bank identification number prefix    | Credit card number length |
|-------------------+--------------------------------------+---------------------------|
| American Express  | 34 or 37                             |                        15 |
| Discover Card     | 6011, 622126-622925, 644-649, 65     |                        16 |
| Mastercard        | 51-55                                |                        16 |
| Visa              | 4                                    |                  13 or 16 |
| Visa Electron     | 4026, 417500, 4508, 4844, 4913, 4917 |                        16 |
|-------------------+--------------------------------------+---------------------------|

For more details on algorithms used in this page 
visit: http://en.wikipedia.org/wiki/Luhn_algorithm

Luhn algorithm
==============
1. From the rightmost digit, which is the check digit, moving left,
double the value of every second digit; if the product of this
doubling operation is greater than 9 (e.g., 8 x 2 = 16), then sum the
digits of the products (e.g., 16: 1 + 6 = 7, 18: 1 + 8 = 9).

2. Take the sum of all the digits.

3. If the total modulo 10 is equal to 0 (if the total ends in zero)
then the number is valid according to the Luhn formula; else it is not
valid.


Check Digit
===========
1. Compute the sum of the digits.
2. Multiply by 9.
3. The last digit is the check digit.

'''

import random

class CreditCard(object):
    def __init__(self, brand, prefix_id, length):
        '''
        brand: string containing 'visa', 'master card' ... etc.
        prefix_id: should be an int or a list of ints
        length: number of digits on the credit card. an int or list of ints.
        '''
        self.brand = brand
        self.prefix_id = prefix_id
        self.length = length

    def next(self, prefix_id_picker=random.randint):
        if isinstance(self.prefix_id, int):
            cc = [int(_) for _ in str(self.prefix_id)]
        else:
            cc = [int(_) for _ in str(self.prefix_id[
                prefix_id_picker(0, len(self.prefix_id)-1)])]

        cc.extend([random.randint(0,9) for _ in range(self.length - len(cc) - 1)])

        #cc = [random.randint(0,9) for _ in range(self.length - 1)]
        cc.append(self.calculate_check_digit(cc))
        return '%s: %s' % (self.brand, ''.join([str(_) for _ in cc]))

    def calculate_check_digit(self, cc):
        # Find the indexes of the numbers we should double
        should_double = [x for x in range(self.length-1)[::-2]]

        # clone
        doubled_and_added = cc[:]

        # see note above for luhn algorithm
        for _ in should_double:
            doubled_and_added[_] = 0
            for x in [int(char) for char in str(cc[_] * 2)]:
                doubled_and_added[_] += x

        sum = reduce(lambda x,y: x+y, doubled_and_added, 0)
        return int(str(sum*9)[-1])

class CreditCards(object):
    cards = [
        CreditCard('American Express', [34, 37], 15),
        CreditCard('Mastercard', range(51, 56), 16),
        CreditCard('Visa', 4, 16)
    ]

    def next(self):
        return self.cards[random.randint(0, len(self.cards)-1)].next()

if __name__ == '__main__':
    print CreditCards().next()
