from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Bulletin, Comment, CategoryModel
from django.urls import reverse_lazy
from .forms import CommentForm
from .filter import CommentFilter
import django.dispatch
from django.contrib.auth.decorators import login_required


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
        # username is passed from url
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Bulletin.objects.filter(author=user).order_by('-date_created')


class PostDetailView(DetailView):
    model = Bulletin


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Bulletin
    fields = ['title', 'content', 'bulletin_category', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user  # self.object = form.save()
        return super().form_valid(form)  # return super().form_valid(form)

    success_url = reverse_lazy('home')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # fields = '__all__'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.bulletin_id = self.kwargs['pk']  # self.object = form.save()
        form.instance.username = self.request.user
        return super().form_valid(form)  # return super().form_valid(form)

    success_url = reverse_lazy('home')


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


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    # <app>/<model>_<viewtype>.html
    template_name = 'myboardapp/comment_list.html'
    context_object_name = 'comments' # we use it in template as {% for comment in comments %}
    ordering = ['-date_added']
    paginate_by = 3
    # form_class = CommentForm
    myFilter = CommentFilter()

    def get_queryset(self):
        user_id = self.request.user.id # get logged-in user id because he is an author of his own posts
        return Comment.objects.filter(bulletin__author_id=user_id).order_by('-date_added')  #filtering current user's bulletins and looking up the comments under these bulletins


    # filtered content
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
            # self.request.GET - get-запрос в котором указанны данные из фильтра
            # queryset=self.get_queryset()) - это отфильтрованный кверисет экземпларов модели self -> bulletin


        return context

# deleting comments
# 1. Create CommentDeleteView
# 2. Create comment_confirm_delete.html template
# 3. Add a link to delete a comment into comment_list.html template
# 4. Create route in urls.py file
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('comment_list')




# declare a signal
accepted = django.dispatch.Signal()

# when we push "Accept" button at the template, it is routed to 'comment-accept' in urls.py
# then, it calls accept function --> which sends 'accepted' signal ----> look signals.py file
def accept(request, **kwargs):

    accepted.send(sender=Comment.__class__, **kwargs) # sending signal, where Comment model is sender argument
        # means that any changes with Comment model will send signal

    return redirect('/home/comments')


# отправка писем для подписчиков по категориям
@login_required
def subscribe(request, **kwargs):
    print(kwargs['pk'])
    pk = kwargs['pk']  # 0 то же самое можно записать, как: pk = kwargs.get('pk')

    my_post = Bulletin.objects.get(id=pk).bulletin_category
    print(my_post)

    # находим объекты категории, с которыми связан данный пост,
    # и добавляем текущего пользователя в поле subscribers моделей
    CategoryModel.objects.get(id=my_post.id).subscribers.add(request.user)

    subscribers = CategoryModel.objects.filter(subscribers=request.user)
    print(f"subscribed categories={subscribers.values()}")
    #

    print('Эта новость относится к категории:', subscribers.last())
    print(subscribers)

    print('Вы подписаны на следующие категории: ', end='')
    for i in Bulletin.objects.filter(bulletin_category__subscribers=request.user.id): print(i, end='    ')
    print("")
    return redirect('/')