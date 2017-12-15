from datetime import date


class Ledger(object):
    """
    TODO: docstring
    this should hold all transactions for that date.
    """

    def __init__(self):
        self.date = date.today()
        self.total = 0  # TODO: Get amount from items instead
        self.transactions = dict()

    def add_transactions(self, transactions):
        """
        TODO docstring
        :param transactions:
        :return:
        """
        # Summarize transaction stats (num of sold items, amount) into Ledger instance
        for transaction in transactions:
            if transaction.fruit in self.transactions.keys():
                self.transactions[transaction.fruit].num_items += transaction.num_items
                self.transactions[transaction.fruit].amount += transaction.amount

            else:
                self.transactions[transaction.fruit] = transaction

    def update_total(self):
        """
        TODO docstring
        :return:
        """
        total = 0
        for item in self.transactions.values():
            total += item.amount
        self.total = total

    def set_date(self, dt):
        """
        TODO docstring
        :param dt:
        :return:
        """
        self.date = dt

    def __str__(self):
        """
        TODO docstring
        :return:
        """
        msg = ""
        for fruit, transaction in self.transactions.items():
            msg += "{fruit}: {amount}円({num_items}) ".format(fruit=fruit.label, amount=transaction.amount,
                                                             num_items=transaction.num_items)
        return msg


