from django.urls import path
from django.contrib.auth.decorators import login_required
from comment.views.add_comment import AddComment
from comment.views.edit_comment import EditComment
from comment.views.delete_comment import DeleteComment

urlpatterns = [
    path('add/', login_required(AddComment.as_view(), login_url="login"), name="add_comment"),
    path('edit/<int:pk>/', login_required(EditComment.as_view(), login_url="login"), name="edit_comment"),
    path('delete/<int:pk>/', login_required(DeleteComment.as_view(), login_url="login"), name="delete_comment"),
]
