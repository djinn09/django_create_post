from django.urls import path
from blog import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/new/", views.PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path(
        "post/<int:pk>",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
]
