from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Bulletin


def home(request):
    context = {
        'bulletins': Bulletin.objects.all()
    }
    return render(request, 'myboardapp/home.html', context)


class PostListView(ListView):
    model = Bulletin

    # <app>/<model>_<viewtype>.html
    template_name = 'myboardapp/home.html'

    # this variable <context_object_name> is passed to the template --> home.html
    context_object_name = 'bulletins_0'
    ordering = ['-date_created']

    paginate_by = 2



class UserPostListView(ListView):
    model = Bulletin
    # <app>/<model>_<viewtype>.html
    template_name = 'myboardapp/user_posts.html'
    # this variable <context_object_name> is passed to the template --> home.html
    context_object_name = 'bulletins_0'
    ordering = ['-date_created']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Bulletin.objects.filter(author=user).order_by('-date_created')



class PostDetailView(DetailView):
    model = Bulletin


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Bulletin
    fields = ['title', 'content', 'bulletin_category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# LoginRequiredMixin - only logged in user can update view
# UserPassesTestMixin - only author of the post can update it
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bulletin
    fields = ['title', 'content', 'bulletin_category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # get a bulletin which we are currently updating
        bulletin = self.get_object()
        # checking if the current user is the author of the post.
        if self.request.user == bulletin.author:  # self.request.user --> current user in the browser
            return True
        return False


# LoginRequiredMixin - only logged in user can delete view
# UserPassesTestMixin - only author of the post can delete it
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bulletin
    success_url = '/home'

    # checking if the user is an author
    def test_func(self):
        # get a bulletin which we are currently updating
        bulletin = self.get_object()
        # checking if the current user is the author of the post.
        if self.request.user == bulletin.author:  # self.request.user --> current user in the browser
            return True
        return False