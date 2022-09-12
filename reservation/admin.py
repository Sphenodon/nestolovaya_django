from django.contrib import admin

from reservation.models import Table, Reservation


class TableModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']
    list_editable = []

    class Meta:
        model = Table


class ReservationModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'table', 'date_of_creation', 'date_of_reservation', 'time_of_reservation']
    list_display_links = ['user']
    list_filter = ['user_id', 'table_id', 'date_of_creation', 'date_of_reservation', 'time_of_reservation']
    search_fields = ['user_id', 'table_id', 'date_of_creation', 'date_of_reservation', 'time_of_reservation']
    list_editable = []

    class Meta:
        model = Reservation


admin.site.register(Table, TableModelAdmin)
admin.site.register(Reservation, ReservationModelAdmin)
