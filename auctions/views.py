import decimal
from operator import itemgetter
from unicodedata import category
import django
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.contrib import messages

from auctions.models import *

from auctions.forms import NewBid, NewComment, NewListing


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {'listings': listings})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    return render(request,"auctions/categories.html")


def createlisting(request):
    if request.POST:
        form = NewListing(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("index")
    return render(request,"auctions/createlisting.html", {"form": NewListing})

def watchlist(request):
    return render(request,"auctions/watchlist.html")

from django.http import Http404

def listing(request,listingID):
    item = Listing.objects.get(id=listingID)
    allComments = Comment.objects.filter(listing = listingID)

    return render(request, "auctions/listing.html",{"item":item, "commentForm": NewComment, 'bidForm': NewBid, 'allComments': allComments})

def comment(request, listingID):

    if request.method == "POST":
        form = NewComment(request.POST)
        if form.is_valid():
            form.save()
    
        return redirect('listing', listingID = listingID)

def bid(request, listingID):
    item = Listing.objects.get(id=listingID)
    currentbid = item.currentBid
    bidSubmitted = float(request.POST['bidPrice'])

    if request.method == "POST":
        if bidSubmitted <= currentbid:
            messages.error(request, "Bid must be more than current bid.")
        else:
            item.currentBid = bidSubmitted
            item.save()
            form = NewBid(request.POST)
            if form.is_valid():
                messages.success(request, "Bid Successful, you are currently winning this bid.")
                form.save()

    return redirect('listing', listingID = listingID)