from django.urls import path

from borrowing.views import (
    BorrowingListView,
    BorrowingDetailView, BorrowingCreateView,
)

from .views import BorrowingReturnView


urlpatterns = [
    path("borrowing_list/", BorrowingListView.as_view(), name="borrowing-list"),
    path(
        "borrowing_list/<int:pk>/",
        BorrowingDetailView.as_view(),
        name="borrowing-detail",
    ),
    path(
        "borrowings/<int:pk>/return/", BorrowingReturnView.as_view(), name="return_book"
    ),
    path(
        "borrowings/", BorrowingCreateView.as_view(), name="borrowing-create"
    ),
]


app_name = "borrowing"
