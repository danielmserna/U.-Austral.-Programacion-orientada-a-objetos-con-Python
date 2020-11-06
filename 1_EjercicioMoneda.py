
class Currency(object):
    "Represent a currency"
    def __init__(self,name,symbol):
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return self.name

class Money(object):
    "Represent an amount of money"
    def __init__(self,amount,currency):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return '{} {}'.format(self.currency.symbol, self.amount)

dolar = Currency('dolar', 'U$S')
pesos = Currency('pesos (Arg)', '$')
one_dolar = Money(1,dolar)
one_peso = Money(1,pesos)