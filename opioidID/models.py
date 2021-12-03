from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Credential(models.Model):
    credential = models.CharField(max_length=20, primary_key=True, db_column="credential")
    prescriber = models.ForeignKey('Prescriber', on_delete=models.CASCADE, null=False, db_column="prescribernpi")
    class Meta:
        db_table = "prescriber_credential"
        managed = False

    def __str__(self):
        return self.prescriber.first_name + " " + self.prescriber.last_name + " - " + self.credential

class Drug(models.Model):

    drug_name = models.CharField(max_length=30, primary_key=True, db_column="drugname")
    is_opioid = models.BooleanField(null=False, db_column="isopioid")

    class Meta:
        db_table = "drug"
        managed = False

    def __str__(self):
        return self.drug_name

class DrugPrescriber(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    quantity = models.IntegerField(null=False, db_column="quantity")
    drug = models.ForeignKey('Drug', null=False, db_column="drugname", on_delete=models.CASCADE)
    prescriber = models.ForeignKey('Prescriber', null=False, db_column="prescribernpi", on_delete=models.CASCADE)
    class Meta:
        db_table = "drug_prescriber"
        managed = False

    def __str__(self):
        return self.prescriber.first_name + " " + self.prescriber.last_name + " - " + self.drug.drug_name

class Prescriber(models.Model):

    npi = models.IntegerField(primary_key=True, db_column="npi", null=False)
    first_name = models.CharField(max_length=11, db_column="firstname", null=False)
    last_name = models.CharField(max_length=11, db_column="lastname", null=False)
    gender = models.CharField(max_length=1, db_column="gender", null=False)
    state = models.ForeignKey("State", db_column="state", null=False, on_delete=models.PROTECT)
    drugs = models.ManyToManyField(Drug, through=DrugPrescriber)
    class Meta:
        db_table = "prescriber"
        managed = False


    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + str(self.npi) + ")"

class State(models.Model):

    state_name = models.CharField(max_length=19, null=False, db_column="statename")
    state_abbrev = models.CharField(max_length=2, primary_key=True, db_column="stateabbrev")
    population = models.IntegerField(null=False, db_column="population")
    deaths = models.IntegerField(null=False, db_column="deaths")

    class Meta:
        db_table = "state"
        managed = False
    
    def __str__(self):
        return self.state_name