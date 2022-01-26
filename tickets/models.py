from django.db import models

# Create your models here.


class Tickets(models.Model):
    ticket_id = models.IntegerField()
    ticket_num = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    service_id = models.CharField(max_length=200)
    service_name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200, blank=True,null=True)
    ticket_date = models.DateField()
    stand_time = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)
    waite_stand_time = models.IntegerField(blank=True,null=True)
    waite_start_time = models.IntegerField(blank=True,null=True)
    is_active = models.BooleanField()

    def __str__(self):
        return self.ticket_num


