class Currency(object):
    "Represent a currency"
    def __init__(self,name,symbol,factor):
        self.name = name
        self.symbol = symbol
        self.factor = factor

    def convert_amount_to_base_currency(self, aNumber):
        return aNumber * self.factor

    def convert_amount_from_base_currency(self, aNumber):
        return aNumber / self.factor

    def __repr__(self):
        return self.name

class Money(object):
    "Represent an amount of money"
    def __init__(self,amount,currency):
        self.amount = amount
        self.currency = currency

    def base_currency_amount(self):
        return self.currency.convert_amount_to_base_currency(self.amount)

    def __add__(self, anAmountOfMoney):
        amount = self.base_currency_amount() + anAmountOfMoney.base_currency_amount()
        amount = self.currency.convert_amount_from_base_currency(amount)
        return Money(amount, self.currency)

    def __sub__(self, anAmountOfMoney):
        amount = self.base_currency_amount() - anAmountOfMoney.base_currency_amount()
        amount = self.currency.convert_amount_from_base_currency(amount)
        return Money(amount, self.currency)

    def __mul__(self, aNumber):
        return Money(self.amount * aNumber, self.currency)

    def __truediv(self, aNumber):
        return Money(self.amount / aNumber, self.currency)

    def __repr__(self):
        return '{} {}'.format(self.currency.symbol, self.amount)

dolar = Currency('dolar', 'U$S',1)
pesos = Currency('pesos (Arg)', '$',1/40)
one_dolar = Money(1,dolar)
one_peso = Money(1,pesos)
    