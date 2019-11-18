from django.db import models
from datetime import date
from datetime import datetime 


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    join_date = models.DateField(auto_now_add=True)
    registration_date = models.DateField(default=datetime.strptime("01-01-1970","%d-%m-%Y"),help_text="date registration")
    name = models.CharField(max_length=200, help_text="Enter username")
    email = models.EmailField(max_length=200, help_text="Enter you email")
    
    guest_status = (
        ('0','user is guest'),
        ('1', 'registered user')
    )
    guest = models.CharField(max_length=1,choices=guest_status,blank=False)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=200,default=str(datetime.now()),blank=False, help_text="Enter task name")

    def __str__(self):
        return "{0}: {1}".format(str(self.id),str(self.task_name))

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=False)
    action_status = (
        ('0','view'),
        ('1','sumbit'),
        ('2','closed')
    )
    action_id = models.CharField(max_length=1,choices=action_status,blank=False,help_text="action status")
    target_id = models.ForeignKey('Tasks', on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0}: {1}: {2}".format(str(self.id),str(self.target_id),self.time)


