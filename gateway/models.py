from django.db import models

class InfoModel(models.Model):
    no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()

class TxModel(models.Model):
    tx_id = models.ForeignKey(InfoModel,on_delete=models.CASCADE)


