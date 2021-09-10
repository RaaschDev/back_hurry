from django.contrib import admin
from .models import Category, EventModel, EventTypeModel, EventAnalitc
from apps.consumable.models import Consumable
from apps.ticket.models import TicketModel

admin.site.register(Category)
admin.site.register(EventTypeModel)


class EventAnalitcInline(admin.TabularInline):
    model = EventAnalitc
    fields = ('event', 'investment',
              'billing', 'profit')
    readonly_fields = ('event', 'investment',
                       'billing', 'profit')


class ConsumableInline(admin.TabularInline):
    model = Consumable
    fields = ('description', 'consumable_type',
              'price', 'quantity', 'img', 'event')
    extra = 1


class TicketInline(admin.TabularInline):
    model = TicketModel
    fields = ('description', 'batch',
              'price', 'quantity', 'gender', 'status', 'event')
    extra = 1


@admin.register(EventModel)
class EventModelAdmin(admin.ModelAdmin):
    inlines = [
        ConsumableInline,
        TicketInline,
        EventAnalitcInline
    ]
    list_display = ('id', 'description', 'date',
                    'start', 'event_type', 'category', 'status')
    list_display_links = ('description',)
    list_filter = ('event_type', 'category', 'status')
