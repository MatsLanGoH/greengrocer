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
    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        """
        :return: 果物モデルを表す文字列を返す。
        """
        return "{} (単価：{})".format(self.label, self.price)


