from django.db import models
from django.contrib.auth.models import User, AbstractUser, Permission

class Instance(models.Model):
    admin = models.CharField(max_length=128, unique=False)
    name = models.CharField(max_length=128, unique=True)
    stage = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"

class UserProfile(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    user_types = (('Student','Student'), ('Supervisor', 'Supervisor'), ('Admin', 'Admin'), ('Superadmin', 'Superadmin'))
    user_type = models.CharField(max_length=10, choices=user_types, default='Student')

    def __str__(self):
        return str(self.user)

class Project(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.PROTECT)
    supervisor = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    title = models.CharField(max_length=128, unique=False)
    description = models.TextField()
    tags = models.TextField()
    seSuitable = models.BooleanField(default=True)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)

    created_by = supervisor.name

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Preference(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    student = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    preferenceNo = models.IntegerField(default=0)

class Algorithm(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    size = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    profile = models.CharField(max_length=128)
    degree = models.IntegerField(default=0)

class Allocation(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.PROTECT)
    student = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)