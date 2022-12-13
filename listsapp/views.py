from datetime import datetime
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import Category, User
from .models import List, ListItem, Follow
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    lists = List.objects.all()
    paginator = Paginator(lists, 10)
    page_number = request.GET.get('page')
    listObjs = paginator.get_page(page_number)
    return render(request, "listsapp/index.html", {
        "list" : listObjs,
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "listsapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "listsapp/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "listsapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "listsapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "listsapp/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def create_list(request):
    title = request.POST.get('title', False)
    data = request.POST.get('public', False)
    if data == "yes":
        public = True
    else:
        public = False

    new_list = List.objects.create(
        title = title,
        creator = request.user,
        timestamp = datetime.now(),
        public = public
    )
    new_list.save()
    
    # Create new Category object
    new_category = Category.objects.create(
        title = request.POST.get('category', False),
        lists = new_list
    )
    new_category.save()
    return render(request, "listsapp/edit_list.html", {
        "list" : new_list
    })

@login_required(login_url='/login')
def create_list_item(request, id):

    target = List.objects.filter(id=id).first()
    rawContent = json.loads(request.body)
    content = rawContent["content"]

    newListItem = ListItem.objects.create(content = content, timestamp = datetime.now(), completed = False)
    newListItem.save()

    target.listitems.add(newListItem)
    target.save()

    return JsonResponse({},status = 201)

def edit_list(request, id):
    list = List.objects.filter(id=id).first()
    users = User.objects.all()
    return render(request, "listsapp/edit_list.html", {
        "list" : list,
        "users" : users
    })

def profile(request, id):
    target = User.objects.filter(id=id).first()
    lists = List.objects.filter(creator = target).all()
    paginator = Paginator(lists, 10)
    page_number = request.GET.get('page')
    listObjs = paginator.get_page(page_number)

    return render(request, "listsapp/profile.html", {
        "Lists" : listObjs,
        "target" : target
    })

def category(request):
    categories = Category.objects.all()
    
    empty_arr=[]
    for i in categories:
        if i.title not in empty_arr:
            empty_arr.append(i.title)

    return render(request, "listsapp/category_select.html", {
        "categories" : categories,
        "array" : empty_arr
    })
    

def category_individual(request, title):
    catObjects = Category.objects.filter(title = title).all()
    lists = List.objects.filter(id__in=catObjects.values('lists_id')).order_by('-timestamp')
    paginator = Paginator(lists, 10)
    page_number = request.GET.get('page')
    listObjs = paginator.get_page(page_number)

    return render(request, "listsapp/category_individual.html",{
        "lists": listObjs,
        "title": title
    })

def delete_list(request, id):
    List.objects.filter(id=id).delete()

    return JsonResponse({},status = 201)

def delete_list_item(request, id):
    print("views.py delete item function is running")
    listitem = ListItem.objects.filter(id=id).delete()
    

    return JsonResponse({},status = 201)

def follow_list(request, id):
    listToFollow = List.objects.filter(id=id).first()
    followObj = Follow.objects.filter(user = request.user, following = listToFollow).first()

    if followObj:
        followObj.delete()
        return JsonResponse({"data":False},status = 201)

    else:
        newFollow = Follow.objects.create(user=request.user, following = listToFollow)
        newFollow.save()
        return JsonResponse({"data":True},status = 201)

def get_follow(request, id):
    listToFollow = List.objects.filter(id=id).first()
    followObj = Follow.objects.filter(user = request.user, following = listToFollow).first()
    followBool = False
    if followObj:
        followBool = True
        return JsonResponse({"data":followBool},status = 201)
    else:
        followBool = False
        return JsonResponse({"data":followBool},status = 201)



@login_required(login_url='/login')
def follow_view(request):
    follow = Follow.objects.filter(user = request.user).all()
    lists = List.objects.filter(id__in=follow.values('following_id'))
    paginator = Paginator(lists, 10)
    page_number = request.GET.get('page')
    listObjs = paginator.get_page(page_number)

    return render(request, "listsapp/follow_view.html",{
        "lists" : listObjs
    })
    
def complete_list_item(request, id):
    listItem = ListItem.objects.filter(id=id).first()
    checkbox = listItem.completed

    if checkbox is True:
        listItem.completed = False
    elif checkbox is False:
        listItem.completed = True
    listItem.save()
    
    
    return JsonResponse({
        "listItem" : listItem.serialize()
    })


def check_complete(request, id):
    listItem = ListItem.objects.filter(id=id).first()

    return JsonResponse({
        "listItem" : listItem.serialize()
    })
    

