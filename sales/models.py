from django.db import models

# Create your models here.
# TODO: implement Tests for models.


class Fruit(models.Model):
    """
    果物のモデル

    TODO: docstring
    """
    label = models.CharField(max_length=200, unique=True, help_text="果物の名称を記入してください")
    price = models.PositiveIntegerField(help_text="果物の単価を記入してください")

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        :return: 果物モデルを表す文字列を返す。
        """
        return "{} (単価：{})".format(self.label, self.price)


class Transaction(models.Model):
    """
    販売情報のモデル

    TODO: docstring
    """
    fruit = models.ForeignKey('Fruit', on_delete=models.CASCADE, help_text="果物を指定してください")
    num_items = models.PositiveIntegerField(help_text="個数を記入してください")
    amount = models.PositiveIntegerField(help_text="売り上げ金額を記入してください")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        """
        :return: 販売情報モデルを表す文字列を返す。
        """

        return "{} | {}個 | 合計{} | 販売日時{}".format(self.fruit, self.num_items, self.amount, self.created_at)


