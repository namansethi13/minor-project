from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True , default="")
    no_of_semesters = models.IntegerField()
    abbreviation = models.CharField(max_length=20)
    shift = models.CharField(max_length=20,default="Morning")


    def __str__(self):
        return self.abbreviation

class Result(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
    semester = models.CharField(max_length=100)
    passout_year = models.CharField(max_length=100)
    xlsx_file = models.FileField(upload_to="xlsx_files/")

    def __str__(self):
        return f"{self.course}_{self.semester}-{self.passout_year}_shift{self.shift}"
        
    def save(self, *args, **kwargs):
        self.xlsx_file.name = f"{self.course}_{self.semester}-{self.passout_year}_shift{self.shift}.xlsx"
        super().save(*args, **kwargs)

@receiver(pre_delete, sender=Result)
def delete_xlsx_file(sender, instance, **kwargs):
    
    if instance.xlsx_file:
        if os.path.isfile(instance.xlsx_file.path):
            os.remove(instance.xlsx_file.path)


class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject= models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=100)
    credit = models.IntegerField()
    is_not_university = models.BooleanField(default=False)
    semester = models.CharField(max_length=100,null=True,blank=True)
    is_practical = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return f"{self.course} {self.code}"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
