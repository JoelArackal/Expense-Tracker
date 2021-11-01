from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    expense = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField()
    Date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return str(self.description)[:5]
