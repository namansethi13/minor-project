from django.db import models

class Result(models.Model):
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    passout_year = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)
    xlsx_file = models.FileField(upload_to="xlsx_files/")

    def __str__(self):
        return f"{self.course} {self.semester}-{self.passout_year} shift:{self.shift}"
        
    def save(self, *args, **kwargs):
        self.xlsx_file.name = f"{self.course} {self.semester}-{self.passout_year} shift:{self.shift}.xlsx"
        super().save(*args, **kwargs)
