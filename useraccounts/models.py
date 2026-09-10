from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta:
        managed = True   # 👈 change False to True
        db_table = "register"
