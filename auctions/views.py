import datetime
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
from django.http import Http404
from auctions.models import *
from auctions.forms import *


def index(request):
    #Check for active listings here, compare todays date with dateBidEnd 
    listings = Listing.objects.all()
    for l in listings:
        endDate = l.dateBidEnd
        today = datetime.date.today()

        if endDate < today:
            Listing.objects.filter(id=l.id).update(active=0)
    
    activeListings = Listing.objects.filter(active=1)
        
    return render(request, "auctions/index.html", {'activeListings': activeListings})


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
    allCategories = Category.objects.all()
    return render(request,"auctions/categories.html", {"allCategories": allCategories})

def bycategory(request,categoryChosen):
    category = Category.objects.get(name=categoryChosen)
    allListings = Listing.objects.filter(category = category, active = 1)
    
    return render(request,"auctions/byCategory.html", {"allListings":allListings, "category": category})


def createlisting(request):
    if request.POST:
        form = NewListing(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
        return redirect("index")
    return render(request,"auctions/createlisting.html", {"form": NewListing})


def watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)

    for item in watchlist:
        if item.listing.active == 0:
            listingToDelete = Listing.objects.get(id=item.listing.id)
            Watchlist.objects.filter(user=user, listing = listingToDelete).delete()

    watchlist = Watchlist.objects.filter(user=user)
    
    return render(request,"auctions/watchlist.html", {"watchlist": watchlist})


def addtowatchlist(request,listingID):
    if request.method == "POST":
        item = Listing.objects.get(id=listingID)
        user = request.user
        if Watchlist.objects.filter(user=user, listing = item).exists():
            messages.error(request, f"{item.name} already in watchlist")
        else:
            watchItem = Watchlist(user=user, listing = item)
            watchItem.save()
            messages.success(request, f"{item.name} successfully added to watchlist")
    return redirect("listing", listingID = listingID)

def removefromwatchlist(request,listingID):
    if request.method == "POST":
        item = Listing.objects.get(id=listingID)
        user = request.user
        Watchlist.objects.filter(user=user, listing = item).delete()
        messages.success(request, f"{item.name} deleted")
        watchlist = Watchlist.objects.filter(user=request.user)
    return render(request,"auctions/watchlist.html", {"watchlist": watchlist})


def listing(request,listingID):
    item = Listing.objects.get(id=listingID)
    allComments = Comment.objects.filter(listing = listingID)
    owner = False
    if request.user.is_authenticated:
        inWatchlist = Watchlist.objects.filter(user=request.user, listing= item).exists()
        if item.user == request.user:
            owner = True
    else:
        inWatchlist = False

    return render(request, "auctions/listing.html",{"item":item, "commentForm": NewComment, 'bidForm': NewBid, 'allComments': allComments, "inWatchlist": inWatchlist, "owner": owner})

def closeBidding(request, listingID):
    item = Listing.objects.get(id = listingID)
    item.active = 0
    item.finalBid = item.currentBid
    item.save()
    messages.success(request, "You have successfully closed the bidding.")
    return redirect('listing', listingID = listingID)


def comment(request, listingID):

    if request.method == "POST":
        form = NewComment(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.listing = Listing.objects.get(id=listingID)
            obj.save()
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
                obj = form.save(commit=False)
                obj.user = request.user
                obj.listing = Listing.objects.get(id=listingID)
                obj.save()

    return redirect('listing', listingID = listingID)