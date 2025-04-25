from django.urls import path
from .views import management_agents_view


app_name = 'call_center'

urlpatterns = [
    path(r'management-agents/', management_agents_view, name='management_agents'),
]
