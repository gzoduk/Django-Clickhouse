from django.contrib import admin
from .models import Users, Tasks, Events

#admin.site.register(Users)
#admin.site.register(Tasks)
#admin.site.register(Events)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id','join_date','registration_date','name','email')
    ordering = ('-id',)

admin.site.register(Users,UsersAdmin)

class TasksAdmin(admin.ModelAdmin):
    list_display = ('id','task_name')
    ordering = ('-id',)

admin.site.register(Tasks,TasksAdmin)

class EventsAdmin(admin.ModelAdmin):
    list_display = ('id','time','action_id','target_id','user_id')
    ordering = ('-id',)

admin.site.register(Events,EventsAdmin)