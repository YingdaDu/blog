from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from .forms import UserLoginForm, UserRegisterForm
from .models import UserProfile
# Create your views here.
User = get_user_model()

class UserDetailView(DetailView):
    template_name = 'user_detail.html'
    queryset = User.objects.all()
    
    def get_object(self):
        return get_object_or_404(
                    User, 
                    username__iexact=self.kwargs.get("username")
                    )
    def get_context_data(self, *args, **kwargs):
        islogin = True
        if not self.request.user.is_active:
            islogin = False

        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        userUrl = reverse_lazy("profiles:detail", kwargs={"username": self.request.user })
        following = UserProfile.objects.is_following(self.request.user, self.get_object())
        isCurrentUser = False
        if self.get_object() == self.request.user: 
            isCurrentUser = True
        context['following'] = following
        context['userUrl'] = userUrl
        context['islogin'] = islogin
        context['user'] = self.request.user 
        context['isCurrentUser'] = isCurrentUser
        return context


class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated():
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)
        

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if request.user.is_authenticated():
            return redirect("/posts/")
        # redirect
    return render(request, "form.html", {"form":form, "title": title})



def register_view(request):
    print(request.user.is_authenticated())
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/posts/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/posts/")