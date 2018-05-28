from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^regUser$', views.regUser),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^system$', views.system),
    url(r'^addUserType$', views.addUserType),
    url(r'^addUserGroup/(?P<userID>\d+)$', views.addUserGroup),
    url(r'^user/(?P<userID>\d+)$', views.user),
    url(r'^services/(?P<userID>\d+)$', views.services),
    url(r'^addMealType$', views.addMealType),
    url(r'^addMeal/(?P<userID>\d+)$', views.addMeal),
    url(r'^addBuilding/(?P<userID>\d+)$', views.addBuilding),
    url(r'^addParking/(?P<userID>\d+)$', views.addParking),
    url(r'^deleteGroup/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteGroup),
    url(r'^deleteMeal/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteMeal),
    url(r'^deleteBuilding/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteBuilding),
    url(r'^deleteParking/(?P<userID>\d+)/(?P<noID>\d+)$', views.deleteParking),
    url(r'^updatePhone/(?P<userID>\d+)$', views.updatePhone),
    url(r'^updateExtNum/(?P<userID>\d+)$', views.updateExtNum),
    url(r'^updatePersonEmail/(?P<userID>\d+)$', views.updatePersonEmail),
]
