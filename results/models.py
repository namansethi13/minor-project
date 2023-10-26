from django.db import models

class Result(models.Model):
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    passout_year = models.CharField(max_length=100)
    shift = models.CharField(max_length=100)
    csv_file = models.FileField(upload_to="csv_files")

    def __str__(self):
        return f"{self.course} {self.semester}-{passout_year} shift:{self.shift}"
        
    def save(self, *args, **kwargs):
        self.csv_file.name = f"{self.course} {self.semester}-{self.passout_year} shift:{self.shift}.csv"
        super().save(*args, **kwargs)
