from django.urls      import path
from postings.views   import PostingView, PostingListView

urlpatterns = [
    path('', PostingView.as_view()),
    path('<int:produt_id>', PostingListView.as_view())
]