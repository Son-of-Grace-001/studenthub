from django.contrib import admin

# Register your models here.
from . models import Faculty
from . models import Department
from . models import Level
from . models import Course
from . models import Material
from . models import Year


admin.site.register (Faculty)
admin.site.register (Department)
admin.site.register (Level)
admin.site.register (Course)
admin.site.register (Material)
admin.site.register (Year)

