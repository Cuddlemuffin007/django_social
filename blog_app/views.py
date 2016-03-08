from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView

from blog_app.models import UserProfile, Blog, Follower


class AppUserCreationForm(UserCreationForm):
    age = forms.IntegerField()


class Home(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = AppUserCreationForm

    def form_valid(self, form):
        user_object = form.save()
        user_age = form.cleaned_data.get('age')
        UserProfile.objects.create(user=user_object, age=user_age)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login_view')


class UserListView(ListView):
    model = UserProfile

    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = UserProfile.objects.get(user=self.request.user)
        followed = current_user.followers.all()
        context['followed'] = [follower.follower_name for follower in followed]

        return context


class BlogCreateView(CreateView):
    model = Blog
    fields = ['body']

    def form_valid(self, form):
        blog_object = form.save(commit=False)
        blog_object.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_posts')


class MyPostsView(ListView):
    model = Blog
    template_name = 'blog_app/my_post_list.html'

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)


class BlogListView(ListView):
    model = Blog
    template_name = 'blog_app/user_blog_list.html'

    def get_queryset(self):
        return Blog.objects.filter(user=self.kwargs['pk'])


class MyFollowingListView(ListView):
    model = UserProfile
    template_name = 'blog_app/my_following_list.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = UserProfile.objects.get(user=self.request.user)
        current_user_following = current_user.followers.all()
        user_profile_dict = {
            following: UserProfile.objects.get(user__username=following.follower_name)
            for following in current_user_following
        }
        context['user_profiles'] = user_profile_dict

        return context


def follow_user(request, user_id):
    user_to_follow = UserProfile.objects.get(user=user_id)
    current_user = UserProfile.objects.get(user=request.user)
    if not current_user.followers.filter(follower_name=user_to_follow.user).exists():
        current_user.followers.add(Follower.objects.create(follower_name=user_to_follow.user))

    return HttpResponseRedirect('/my_posts')

