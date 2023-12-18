from django.urls import path

from borrowing.views import (
    BorrowingDetailView,
    BorrowingCreateView,
    BorrowingReturnView,
    BorrowingListView,
)


urlpatterns = [

    path("<int:pk>/",
         BorrowingDetailView.as_view(),
         name="borrowing-detail",),

    path("",
         BorrowingListView.as_view(),
         name="borrowing-list",),

    path("<int:pk>/return/",
         BorrowingReturnView.as_view(),
         name="return-book"),

    path("create/",
         BorrowingCreateView.as_view(),
         name="borrowing-create",),
]


app_name = "borrowing"
