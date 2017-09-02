from urllib import quote_plus
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post
from django.views.generic import (
                DeleteView, 
                UpdateView
                )

def post_create(request):
	if not request.user.is_active:
		return redirect("/login")

	islogin = True
	if not request.user.is_active:
		islogin = False

	user = request.user
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form,
		"islogin": islogin,
		"user": user
	}
	return render(request, "post_form.html", context)

def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	share_string = quote_plus(instance.content)
	userUrl = reverse_lazy("profiles:detail", kwargs={"username": request.user })
	autherUrl = reverse_lazy ("profiles:detail", kwargs={"username": instance.user })
	liked_count = instance.liked.all().count()
	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	islogin = True
	if not request.user.is_active:
		islogin = False
	isliked = False
	if request.user in instance.liked.all():
		isliked = True
    



	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
				parent_id = int(request.POST.get("parent_id"))
		except:
				parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	comments = instance.comments
	comment_count = comments.all().count()
	context = {
	    "slug": instance.slug,
		"title": instance.title,
		"auther": instance.user,
		"autherUrl": autherUrl,
		"user": request.user,
		"instance": instance,
		"islogin": islogin,
		"share_string": share_string,
		"comments": comments,
		"comment_form":form,
		"comment_count":comment_count,
		"userUrl": userUrl,
		"isliked": isliked,
		"liked_count": liked_count,
	}
	return render(request, "post_detail.html", context)


def post_list(request):
	queryset_list = Post.objects.all() #.order_by("-timestamp")
	user = request.user
	userUrl = reverse_lazy("profiles:detail", kwargs={"username": request.user })
	query = request.GET.get("q")
	islogin = True
	if not request.user.is_active:
		islogin = False

	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
		
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
   		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset, 
		"user": user,
		"islogin": islogin,
		"title": "Blog List",
		"page_request_var": page_request_var,
		"userUrl": userUrl,
		"islist": True
	
	}
	return render(request, "post_list.html", context)





def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	islogin = True
	if not request.user.is_active:
		islogin = False

    
	instance = get_object_or_404(Post, slug=slug)
	userUrl = reverse_lazy("profiles:detail", kwargs={"username": request.user })
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
		"islogin": islogin,
		"userUrl": userUrl
	}
	return render(request, "post_form.html", context)




def post_delete(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if not request.user == instance.user or not request.user.is_active:
		raise Http404
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("profiles:detail", username=request.user)











