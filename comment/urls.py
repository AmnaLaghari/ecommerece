from django.urls import path
from django.contrib.auth.decorators import login_required
from comment.views.add_comment import AddComment

urlpatterns = [
    path('add/', login_required(AddComment.as_view(), login_url="login"), name="add_comment"),
]
