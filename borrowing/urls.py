from django.urls import path

from borrowing.views import (
    BorrowingSerializer,
    BorrowingListView,
    BorrowingDetailView,
)

from .views import BorrowingReturnView

from .views import BorrowingReturnView

urlpatterns = [
    path("borrowings_list/",
         BorrowingListView.as_view(),
         name="borrowing-list"),

    path("borrowing_list/<int:pk>/",
         BorrowingDetailView.as_view(),
         name="borrowing-detail"),

    path('borrowings/<int:pk>/return/',
         BorrowingReturnView.as_view(),
         name='return_book'),
]


app_name = "borrowing"
