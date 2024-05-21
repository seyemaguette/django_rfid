from django.db import models

# Create your models here.
class UID(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    def __str__(self):
            return f"{self.uid}"
    




class Etudiant(models.Model):
    name = models.CharField(max_length=50, null=True)
    codePermenant = models.CharField(max_length=50, null=True)
    uid = models.CharField(max_length=20, unique=True, null=True)
    fingerprint_id = models.CharField(max_length=20, unique=True,null=True)
    

    def __str__(self):
        return f"{self.name}"

# class Etudiant(models.Model):
#         name =models.CharField(max_length=50, null=True )
#         # uid_id = models.ForeignKey(UID,  on_delete=models.CASCADE)
#         uid = models.CharField(max_length=20, unique=True)
        
#         def __str__(self):
#             return f"{self.name}"