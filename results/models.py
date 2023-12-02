from django.db import models

class Result(models.Model):
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    passout_year = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)
    xlsx_file = models.FileField(upload_to="xlsx_files/")

    def __str__(self):
        return f"{self.course}_{self.semester}-{self.passout_year}_shift{self.shift}"
        
    def save(self, *args, **kwargs):
        self.xlsx_file.name = f"{self.course}_{self.semester}-{self.passout_year}_shift{self.shift}.xlsx"
        super().save(*args, **kwargs)


class Subject(models.Model):
    course = models.CharField(max_length=100)
    subject= models.CharField(max_length=100,null=True,blank=True)
    code = models.CharField(max_length=100)
    credit = models.IntegerField()
    is_not_university = models.BooleanField(default=False)
    semester = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.course} {self.code}"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)