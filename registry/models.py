from django.db import models


class Citizen(models.Model):

    first_name = models.CharField(
        max_length=100,
        db_index=True
    )

    last_name = models.CharField(
        max_length=100,
        db_index=True
    )

    national_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True
    )

    phone_number = models.CharField(
        max_length=13,
        db_index=True
    )

    father_name = models.CharField(
        max_length=100,
        db_index=True,
    )

    birth_date = models.DateField()

    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"