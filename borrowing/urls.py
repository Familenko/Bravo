from django.urls import path

from borrowing.views import (
    BorrowingDetailView,
    BorrowingCreateView,
    BorrowingReturnView
)


urlpatterns = [
    path(
        "borrowings/<int:pk>/",
        BorrowingDetailView.as_view(),
        name="borrowing-detail",
        methods=["get"]
    ),

    path(
        "borrowings/",
        BorrowingDetailView.as_view(),
        name="borrowing-list",
        methods=["get"]
    ),

    path(
        "borrowings/<int:pk>/return/",
        BorrowingReturnView.as_view(),
        name="return_book"
    ),
    path(
        "borrowings/",
        BorrowingCreateView.as_view(),
        name="borrowing-create",
        methods=["post"]
    ),
]


app_name = "borrowing"
