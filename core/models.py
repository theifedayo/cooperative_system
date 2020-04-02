from django.db import models

# Create your models here.

class Sub(models.Model):
    doc = models.FileField(upload_to='zz/',blank=False, null=False)
    #name = models.CharField(max_length=22, blank=False, null=True)

    def __str__(self):
        return self.doc


class Subscriber(models.Model):
    id_no = models.IntegerField(null=False, unique=True)
    sub_name = models.CharField(max_length=30, blank=False, null=False)
    phone_no = models.IntegerField(blank=False, null=False)
    no_of_plot = models.IntegerField(blank=False, null=False)
    payable_amount = models.IntegerField(blank=False, null=False)
    payment_starting_date = models.CharField(max_length=12, blank=False, null=False)
    supposed_end_date = models.CharField(max_length=12, blank=False, null=False)
    amount_paid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Search(models.Model):
    s_word = models.CharField(max_length=30)

class Pop(models.Model):
    name = models.CharField(max_length=15)
