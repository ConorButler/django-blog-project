from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .models import Csstats
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def stats(request):
    context2 = {'csstats': Csstats.objects.all()}
    return render(request, 'blog/stats.html', context = context2)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user # this gets the current logged user and sets it as the instance of the form
        return super().form_valid(form) # sets the author before form_valid gets ran

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()  # this gets the object of the post we are currently updating
        if self.request.user == post.author: # makes sure the current (logged in) user is the author of the post
            return True
        return False # this will fail the test for the mixin and not allow the post to update

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # makes sure that only logged in users who authored the post can delete
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # gets the username from the url, or returns a 404
        return Post.objects.filter(author=user).order_by('-date_posted') # returns a list of posts filtered by the username we got from the url