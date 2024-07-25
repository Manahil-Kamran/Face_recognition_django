from django.db import models

class AdminLogin(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # True if active, False otherwise
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.CharField(max_length=256, default='Admin', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)  # Auto-fill with current timestamp

    class Meta:
        db_table = "admin_login"
class PersonRegistration(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    full_name = models.CharField(max_length=256, null=True, blank=True)
    cnic = models.CharField(max_length=256, null=True, blank=True)
    department_name = models.CharField(max_length=256, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)  # Auto-fill with current timestamp

class FaceCoding(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    person_id = models.ForeignKey(PersonRegistration, on_delete=models.CASCADE)  # Foreign key to PersonRegistration
    face_feature = models.TextField(null=True, blank=True)
    blob_face_feature = models.BinaryField(null=True, blank=True)  # To store binary data
    img_url = models.CharField(max_length=256, null=True, blank=True)
    is_current = models.BooleanField(default=False)  # Indicates if this is the current face feature
    time_sent = models.DateTimeField(auto_now_add=True)  # Auto-fill with current timestamp
    date_created = models.DateTimeField(auto_now_add=True)  # Auto-fill with current timestamp

class PersonAttend(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    person_id = models.ForeignKey(PersonRegistration, on_delete=models.CASCADE)  # Foreign key to PersonRegistration
    face_feature = models.TextField(null=True, blank=True)
    blob_face_feature = models.BinaryField(null=True, blank=True)  # To store binary data
    img_url = models.CharField(max_length=256, null=True, blank=True)
    camera_id = models.CharField(max_length=256, null=True, blank=True)
    time_sent = models.DateTimeField(auto_now_add=True)  # Auto-fill with current timestamp
    date_created = models.DateTimeField(auto_now_add=True)  # Auto-fill with current timestamp
    T1 = models.IntegerField(default=0)  # Default value of 0
    T2 = models.IntegerField(default=0)  # Default value of 0
    T3 = models.IntegerField(default=0)  # Default value of 0
    score = models.IntegerField(default=0)  # Default value of 0
    is_moved = models.BooleanField(default=False)  # Default value of False
