from django.urls import re_path

from recSys import views

urlpatterns = [
    re_path(r'^menu/detail/(?P<menu_id>\d+)/$', views.menu_detail, name='menu_detail'),
    re_path(r'^menu/update/(?P<menu_id>\d+)/$', views.menu_update, name='menu_update'),
    re_path(r'^menu/delete/(?P<menu_id>\d+)/$', views.menu_delete, name='menu_delete'),
    re_path(r'^menu/food-type/$', views.food_type, name='food_type'),
    re_path(r'^menu/food-type/update/(?P<food_type_id>\d+)/$', views.food_type_update, name='food_type_update'),
    re_path(r'^menu/food-type/delete/(?P<food_type_id>\d+)/$', views.food_type_delete, name='food_type_delete'),
    re_path(r'^menu/add/$', views.menu_add, name='menu_add'),
    re_path(r'^menu/for-staff/$', views.menu_for_staff, name='menu_for_staff'),
    re_path(r'menu_by_em', views.get_menu_by_emotion, name='menu_by_em'),
    re_path(r'menu_like', views.menu_like, name='menu_like'),
    re_path(r'menu_dislike', views.menu_dislike, name='menu_dislike'),
    re_path(r'menu_review_recommendation', views.menu_review_recommendation, name='menu_review_recommendation'),
    re_path(r'^menu/$', views.main_list, name='menu'),
    re_path(r'^$', views.main_list, name='menu'),
    re_path(r'^user/(?P<username>[a-zA-Z0-9._]*)/$', views.user_profile, name='user_profile'),
    re_path(r'^user/(?P<username>[a-zA-Z0-9._]*)/editing/$', views.user_profile_editing, name='user_profile_editing'),
    re_path(r'^logout/', views.logout, name='logout'),
]

