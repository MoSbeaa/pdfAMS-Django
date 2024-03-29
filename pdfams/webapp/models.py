from django.db import models

class Record(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    Full_name = models.CharField(max_length=256)
    Date_of_birth = models.DateField()
    SIN = models.CharField(max_length=20)
    Date_of_hire = models.DateField()
    Address = models.CharField(max_length=256)
    City = models.CharField(max_length=256)
    Zip = models.CharField(max_length=256)
    State = models.CharField(max_length=256)
    Home_phone = models.CharField(max_length=20)
    Cell_phone = models.CharField(max_length=20)
    # married
    # single
    Spouse_name = models.CharField(max_length=256)
    Em_name = models.CharField(max_length=256)
    Em_relationship = models.CharField(max_length=256)
    Date = models.DateField()

    def __str__(self):
        return self.Full_name
