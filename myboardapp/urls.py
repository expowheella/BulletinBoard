from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CommentCreateView,
    CommentListView,
    CommentDeleteView,
    accept,
    subscribe,
)
from . import views

urlpatterns = [
path('', PostListView.as_view(), name='home'),
path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

# Making link for each post by its primary key
    # pk - primary key
    # int - only expect to see integers
path('home/<int:pk>/', PostDetailView.as_view(), name='bulletin-detail'),
# and we also make a link in template to access this detail view:
    # {% url 'bulletin-detail' bulletin.id %}
    # 'bulletin-detail' --> name
    # bulletin.id --> <int:pk>
    # template should be names as: <app.name>_detail
# <h2><a class="article-title" href="{% url 'bulletin-detail' bulletin.id %}">{{ bulletin.title }}</a></h2>

path('home/new/', PostCreateView.as_view(), name='bulletin-create'),

path('home/<int:pk>/comment', CommentCreateView.as_view(), name='comment_create'),

path('home/comments', CommentListView.as_view(), name='comment_list'),

path('home/<int:pk>/update/', PostUpdateView.as_view(), name='bulletin-update'),

path('home/<int:pk>/delete/', PostDeleteView.as_view(), name='bulletin-delete'),

# accept comments where <int:pk> --> comment.id
path('home/comments/<int:pk>/accept', accept, name='comment-accept'),

# delete comments where <int:pk> --> comment.id
path('home/comments/<int:pk>/delete', CommentDeleteView.as_view(), name='comment-delete'),

# subscribe bulletins by category
path('<int:pk>/subscribe', subscribe, name='bulletin-subscribe'),
]