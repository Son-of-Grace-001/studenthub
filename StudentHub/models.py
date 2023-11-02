from django.db import models

# Faculty Model
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='faculty/')

    def __str__(self):
        return self.name

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='department/')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#Level model 
class Level(models.Model):
    level = models.CharField(max_length=20)
    image = models.ImageField(upload_to = 'level/')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    dept = models.CharField(max_length=100)
    def __str__(self):
        return self.dept
    
# Course Model
class Course(models.Model):
    img  = models.ImageField(upload_to='course/')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    description = models.TextField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Year(models.Model):
    year = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    img = models.ImageField(upload_to = 'year/')
    def __str__(self):
        return self.year

# Past Questions Model
class Material(models.Model):
    option = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    files = models.FileField(upload_to='past_questions/')
    img = models.FileField(upload_to='past_questions/')
    year = models.ForeignKey(Year, on_delete = models.CASCADE)

    def __str__(self):
        return self.option
