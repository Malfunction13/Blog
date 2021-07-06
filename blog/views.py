from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# #these below is a function based view - the below ahs same purpose as PostListView
# def home(request):
#     context = {
#         "posts": Post.objects.all()
#     }
#
#     return render(request, 'blog/home.html', context)


# the below is a class-based view
class PostListView(ListView):  # this example uses custom names and doesnt follow the naming convention
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # shows newest entries first with the - sign
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))  # limit results to the selected user only

        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):  # this example follows the naming convention and doesnt require template_name etc
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):  # mixins are added to the far left
    model = Post
    fields = ['title', 'content']
    login_url = 'login'  # this will help the Mixin methods know where to redirect when user is not logged in

    def form_valid(self, form):  # override the method that comes with CreateView
        form.instance.author = self.request.user  # sets the author of the instance of the form to the current user
        # this runs the form_valid() in the parent class, although it would've ran anyway

        return super().form_valid(form) # the difference is now the author is set to the current logged user

    def handle_no_permission(self):
        messages.info(self.request, message='You need to log in before posting!')

        return super(PostCreateView, self).handle_no_permission()


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # mixins are added to the far left
    model = Post
    fields = ['title', 'content']
    login_url = 'login'  # this will help the Mixin methods know where to redirect when user is not logged in

    def form_valid(self, form):  # override the method that comes with CreateView
        form.instance.author = self.request.user  # sets the author of the instance of the form to the current user
        # this runs the form_valid() in the parent class, although it would've ran anyway

        return super().form_valid(form)  # the difference is now the author is set to the current logged user

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.info(self.request, message='You need to log in before updating a post!')

        else:
            if not self.test_func():
                messages.info(self.request, message='You can update only own posts!')

        return super(PostUpdateView, self).handle_no_permission()

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:

            return True

        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # in case of successful deletion redirects to home

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:

            return True

        return False

    def handle_no_permission(self):

        if not self.request.user.is_authenticated:
            messages.info(self.request, message='You need to log in before deleting a post!')

        else:
            if not self.test_func():
                messages.info(self.request, message='You can delete only own posts!')

        return super(PostDeleteView, self).handle_no_permission()


def about(request):

    return render(request, 'blog/about.html', {'title': "About Page"})

