from django.urls import path
from apis.views import MyHomeListView

urlpatterns = [
    path("myhome/", MyHomeListView.as_view(), name="myhome-list"),
]
