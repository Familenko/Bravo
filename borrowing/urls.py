from django.urls import path

from borrowing.views import (
    BorrowingSerializer,
    BorrowingListView,
    BorrowingDetailView,
)

from .views import BorrowingReturnView

urlpatterns = [
    path("borrowings_list/", BorrowingListView.as_view(), name="borrowing-list"),
    path(
        "borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"
    ),
]



app_name = "borrowing"
