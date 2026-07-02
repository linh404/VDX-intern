class Account:
    bank_name = 'Pythonic Bank'

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def __str__(self):
        return f'Account for {self.owner} with balance {self.balance}'

    def __repr__(self):
        return f"Account(owner='{self.owner}', balance={self.balance})"

    @staticmethod
    def is_valid_amount(amount):
        return amount > 0

    @classmethod
    def change_bank(cls, new_name):
        cls.bank_name = new_name

class SavingsAccount(Account):

    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        bonus = amount * self.interest_rate
        self.balance += amount + bonus
        return self.balance

def main():
    acc1 = Account('Alice', 1000)
    acc2 = Account('Bob', 2000)
    print('Class Attribute vs Instance Attribute:')
    print('Class attr via class:', Account.bank_name)
    print('Class attr via instance 1:', acc1.bank_name)
    print('Class attr via instance 2:', acc2.bank_name)
    acc1.bank_name = 'Alice Bank'
    print('After shadowing class attribute in instance 1:')
    print('acc1.bank_name:', acc1.bank_name)
    print('acc2.bank_name:', acc2.bank_name)
    print('Account.bank_name:', Account.bank_name)
    Account.change_bank('Global Pythonic Bank')
    print('After classmethod change:')
    print('acc1.bank_name:', acc1.bank_name)
    print('acc2.bank_name:', acc2.bank_name)
    print('Account.bank_name:', Account.bank_name)
    print('---')
    print('Method binding check:')
    print('Bound method object:', acc2.deposit)
    print('Unbound method function:', Account.deposit)
    print('Equivalence proof of calls:')
    acc2.deposit(500)
    print('After normal call:', acc2.balance)
    Account.deposit(acc2, 500)
    print('After manual binding call:', acc2.balance)
    print('---')
    print('Overriding:')
    savings = SavingsAccount('Charlie', 1000, 0.05)
    savings.deposit(100)
    print('Overridden deposit output (1000 + 100 + 5 bonus):', savings.balance)
    print('---')
    print('String representations:')
    print('str(acc2):', str(acc2))
    print('repr(acc2):', repr(acc2))
    print('---')
    print('Static method:')
    print('Is 100 valid?', Account.is_valid_amount(100))
    print('Is -50 valid?', Account.is_valid_amount(-50))
if __name__ == '__main__':
    main()
