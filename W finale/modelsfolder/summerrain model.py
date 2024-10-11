from django.db import models
import calendar

# Create your models here.
class staff(models.Model):
    position_choices = [
        ("SrMng", "Senior Manager"),
        ("Mng", "Manager"),
        ("SrEngr", "Senior Engineer"),
        ("JrEngr", "Junior Engineer")
    ]
    
    working_region_choices = [
        ("Yangon", "Yangon"),
        ("Mandalay", "Mandalay")
    ]
    
    Name = models.CharField(max_length=100)
    NRC_id = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=100)
    position = models.CharField(max_length=100, choices=position_choices)
    birthday = models.DateField()
    father_name = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    address_no = models.CharField(max_length=100)
    address_street = models.CharField(max_length=100)
    address_quarter = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)
    address_state = models.CharField(max_length=100)
    working_region = models.CharField(max_length=100, choices=working_region_choices)
    start_date = models.DateField()
    resign_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.Name
    
    def get_position_display(self):
        """
        Returns the human-readable label for the position choice.
        """
        for key, label in self.position_choices:
            if key == self.position:
                return label
        return self.position  # Return the key itself if not found
    
    # Put default value 0 ||||||
class salary(models.Model):
    date = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowance = models.DecimalField(max_digits=10, decimal_places=2)
    travelling_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    leadership_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    remark = models.CharField(max_length=255)
    staff = models.ForeignKey('staff', on_delete=models.CASCADE)

    @property
    def total_salary(self):
        return self.basic_salary + self.allowance + self.travelling_allowance + self.leadership_allowance

    @property
    def month(self):
        return calendar.month_name[self.date.month]

    @property
    def year(self):
        return self.date.year
    
    def __str__(self):
        return f"{self.staff} : {self.month}, {self.year}"
    
class PastExperience(models.Model):
    staff = models.ForeignKey('staff', on_delete=models.CASCADE)
    year_of_exp = models.IntegerField(null=True)
    position = models.CharField(max_length=20, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.staff.Name}'s past experience in {self.year_of_exp} years as {self.position}"
    
class DailyAttendance(models.Model):
    date = models.DateField(unique=True)
    staff = models.ManyToManyField(staff)
    def __str__(self):
        return f"{self.date}"  