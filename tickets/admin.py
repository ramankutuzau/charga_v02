from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Tickets

class TicketsAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('_name',)}
    list_display = ('ticket_id', 'ticket_num', 'status', 'service_id', 'service_name','user_name','stand_time','start_time')
    # list_editable = ('is_active',)

 # t = Tickets(ticket_id=ticketID, ticket_num=ticketNum, status=status,
 #                        service_id=serviceID, service_name=serviceName,user_name=userName,
 #                        stand_time=standTime, start_time=startTime)


admin.site.register(Tickets,TicketsAdmin)