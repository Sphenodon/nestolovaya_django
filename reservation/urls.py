from django.urls import re_path

from reservation import views

urlpatterns = [
    re_path(r'show_reservation', views.show_reservation, name='show_reservation'),
    re_path(r'delete_reservation', views.delete_reservation, name='delete_reservation'),
    re_path(r'reserve_table', views.reserve_table, name='reserve_table'),
    re_path(r'^add-table/$', views.reservation_add_table, name='reservation_add_table'),
    re_path(r'^table/change/(?P<table_id>\d+)/$', views.reservation_change_table, name='reservation_change_table'),
    re_path(r'^delete-table/(?P<table_id>\d+)/$', views.reservation_delete_table, name='reservation_delete_table'),
    re_path(r'^$', views.main_list, name='reservation'),
]
