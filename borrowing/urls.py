from django.urls import path, include
from rest_framework import routers

from .views import BorrowingReturnView

urlpatterns = [

]


urlpatterns += [
    path('borrowings/<int:pk>/return/', BorrowingReturnView.as_view(), name='return_book'),
]


app_name = "borrowing"
