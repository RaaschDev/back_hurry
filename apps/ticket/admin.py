from django.contrib import admin
from .models import TicketModel, TicketSale, SaleT

admin.site.register(TicketSale)
admin.site.register(TicketModel)
admin.site.register(SaleT)
