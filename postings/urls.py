from django.urls      import path
from postings.views   import PostingView, CommentView, CommentDeleteView

urlpatterns = [
    path('', PostingView.as_view()),
    path('/comments', CommentView.as_view()),
    path('/comments/<int:comment_id>', CommentDeleteView.as_view())
]