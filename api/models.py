from django.db import models

BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]


class Donor(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.blood_type})"



class BloodInventory(models.Model):
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, unique=True)
    units = models.IntegerField(default=0)

class BloodRequest(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    units_requested = models.IntegerField()
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
    ], default='Pending')

# class BloodRequest(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Fulfilled', 'Fulfilled'),
#         ('Rejected', 'Rejected'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
#     blood_type = models.CharField(max_length=3)
#     units_requested = models.PositiveIntegerField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
#     requested_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} requested {self.units_requested} units of {self.blood_type}"