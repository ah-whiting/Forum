from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Topic, Comment
from apps.login.models import User

def root(request):
    # if not 'id' in request.session:
    #     return redirect('/login')
    context = {
        "topics" : Topic.objects.all()
    }
    return render(request, 'forum/index.html', context)

def new_topic(request):
    return render(request, 'forum/newTopic.html')

def create_topic(request):
    if not 'id' in request.session:
        return redirect('/login')
    # if request.method != "POST":
    #     return redirect('topics/new')
    e = Topic.objects.validator(request.POST)
    if len(e) > 0:
        for key, value in e.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/topics/new')
    top = Topic.objects.create(
        title = request.POST["title"],
        message = request.POST["message"],
        created_by = User.objects.get(id = request.session["id"])
    )
    Comment.objects.create(
        message = top.message,
        created_by = top.created_by,
        topic = top
    )
    return redirect('/')

def show_topic(request, id):
    page = 1
    page_count = 10
    comment_count = Topic.objects.get(id = id).comments.count()
    if "page" in request.GET:
        page = int(request.GET["page"])
    context = {
        "topic" : Topic.objects.get(id = id),
        "comments" : Topic.objects.get(id = id).comments.all()[page_count*(page-1): page_count*page],
        "last_page": comment_count // page_count + (comment_count % page_count > 0)
    }
    return render(request, 'forum/showTopic.html', context)

def delete_topic(request, id):
    if not 'id' in request.session:
        return redirect('/login')
    topic = Topic.objects.get(id=id)
    if request.session["id"] == topic.created_by.id:
        topic.delete()
    else:
        messages.error(request, "You do not have permission for that action")
    return redirect("/")

def create_comment(request, id):
    if not 'id' in request.session:
        return redirect('/login')
    Comment.objects.create(
        topic = Topic.objects.get(id=id),
        message = request.POST["message"],
        created_by = User.objects.get(id = request.session["id"])
    )
    return redirect(f'/topics/{id}')
    
def update_comment(request, id):
    if not 'id' in request.session:
        return redirect('/login')
    comment = Comment.objects.get(id = id)
    comment.message = request.POST["message"]
    comment.save()
    return redirect(f"/topics/{comment.topic.id}")

def delete_comment(request, id):
    if not 'id' in request.session:
        return redirect('/login')
    comment = Comment.objects.get(id = id)
    if comment.created_by.id == request.session["id"]:
        comment.message = "[comment deleted]"
        comment.is_active = False
        comment.save()
    else: 
        messages.error(request, "You do not have permission for that action")
    return redirect(f"/topics/{comment.topic.id}")