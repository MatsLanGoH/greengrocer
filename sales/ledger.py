from datetime import date


class Ledger:
    """
    販売情報を登録し、合計金額、売上、内訳を返すためのクラス
    """

    def __init__(self):
        self.date = date.today()
        self.total = 0
        self.transactions = dict()

    def add_transactions(self, transactions):
        """
        Ledgerに販売情報を登録する

        :param transactions: Transactionのリスト
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
        Ledgerに登録されている販売情報から合計金額を更新する
        """
        total = 0
        for item in self.transactions.values():
            total += item.amount
        self.total = total

    def set_date(self, ledger_date):
        """
        Ledgerの年月日を設定する

        :param ledger_date: 年月日 ex. datetime.date(2017, 12, 24)
        """
        self.date = ledger_date

    def __str__(self):
        """
        Ledgerに登録されている販売情報の内訳（登録商品の種類、数、累計）を返す

        :return: 文字列（販売情報の内訳）
        """
        msg = ""
        for product, transaction in self.transactions.items():
            msg += "{product}: {amount}円({num_items}) ".format(product=product.label, amount=transaction.amount,
                                                               num_items=transaction.num_items)
        return msg
