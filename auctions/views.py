import datetime
import django
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.http import Http404
# a bit sloppy to "import *"; with visual studio, it's easy to list the methods you need
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
    # more consistent would be "categoryID" rather than "categoryChosen". 
    # more bullet-proof: get_object_or_404(Category, categoryID)
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
    # wrong - this view is returning a list of Listings that are in the 
    # users watchlist. it MUST not have any side-effects. You should delete
    # from the watch list when the auction is closed. 
    for item in watchlist:
        if item.listing.active == 0:
            listingToDelete = Listing.objects.get(id=item.listing.id)
            # shouldn't the following be a .get()? 
            Watchlist.objects.filter(user=user, listing = listingToDelete).delete()

    watchlist = Watchlist.objects.filter(user=user)

    return render(request,"auctions/watchlist.html", {"watchlist": watchlist})


def addtowatchlist(request,listingID):
    if request.method == "POST":
        # more bullet proof get_object_or_404..
        item = Listing.objects.get(id=listingID)
        user = request.user
        if Watchlist.objects.filter(user=user, listing = item).exists():
            messages.error(request, f"{item.name} already in watchlist")
        else:
            watchItem = Watchlist(user=user, listing = item)
            watchItem.save()
            messages.success(request, f"{item.name} successfully added to watchlist")
    # correct to redirect! like with the removefromwatchlist, not sure how this is called
    # with method!=POST unless a user goes into URL bar and types 'https://.../removefromwatchlist/10'
    # If so, you are probably correct to redirect to the listing page
    return redirect("listing", listingID = listingID)

def api_toggle_watchlist(request,listingID):
    if request.method == "POST":
        item = Listing.objects.get(id=listingID)
        user = request.user
        if Watchlist.objects.filter(user=user, listing = item).exists():
            Watchlist.objects.filter(user=user, listing = item).delete()
            newstate = "off"
        else:
            watchItem = Watchlist(user=user, listing = item)
            watchItem.save()
            newstate = "on"
    return JsonResponse({'current_value': newstate})


def removefromwatchlist(request,listingID):
    if request.method == "POST":
        # more bullet proof get_object_or_404..
        item = Listing.objects.get(id=listingID)
        user = request.user
        Watchlist.objects.filter(user=user, listing = item).delete()
        messages.success(request, f"{item.name} deleted")
        watchlist = Watchlist.objects.filter(user=request.user)
        # on success, you should redirct back to the listing page, 
        # like you do in the addtowatchlist. or you can redirect to
        # the watchlist page, but you should not be rendering.
    # in your app, you are only called by a POST. Not sure what the right
    # thing to do when method != POST. 
    return render(request,"auctions/watchlist.html", {"watchlist": watchlist})


def listing(request,listingID):
    # more bullet-proof to say: item=get_object_or_404(Listing, id=listingID)
    item = Listing.objects.get(id=listingID)
    allComments = Comment.objects.filter(listing = listingID)
    owner = False
    inWatchlList=False # consistent with your style for owner flag
    if request.user.is_authenticated:
        inWatchlist = Watchlist.objects.filter(user=request.user, listing= item).exists()
        if item.user == request.user:
            owner = True

    # # The following line causes system to crash when viewing a listing that has no big
    # winningBid = Bid.objects.get(listing=item, bidPrice= item.currentBid)

    # # cleaner: winning = (winningBid.user == request.user)
    # if winningBid.user == request.user:
    #     winning = True
    # else:
    #     winning = False
    try:
        winningBid = Bid.objects.get(listing=item, bidPrice= item.currentBid)
        winning = (request.user == winningBid.user)
    except:
        winning = False
    

    # keep in moind that this page might be called when a listing has just been closed,
    # so the listing.html needs to be aware of this fact (and look at item.active to hid
    # some things like the bid button)
    return render(request, "auctions/listing.html",{"item":item, "commentForm": NewComment, 'bidForm': NewBid, 'allComments': allComments, "inWatchlist": inWatchlist, "owner": owner, "winning":winning})

def closeBidding(request, listingID):
    # more bullet proof...
    item = Listing.objects.get(id = listingID)
    item.active = 0
    item.finalBid = item.currentBid
    item.save()
    # here is where you'd remove from the watchlist, if that is the behavior you
    # want in your app; but don't do the renmovig in the innocuous display of the watchlinst page!
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


def bid0(request, listingID):
    item = Listing.objects.get(id=listingID)
    currentbid = item.currentBid
    # this should be done AFTER the form.is_valid() returns true. 
    # moreover, needs to be done after you test for method==POST
    bidSubmitted = float(request.POST['bidPrice'])

    if request.method == "POST":
        if bidSubmitted <= currentbid:
            messages.error(request, "Bid must be more than current bid.")
        else:
            # you should not store the bidSubmitted until you check that form.is_valid() is true. 
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

def bid(request, listingID):
    item = get_object_or_404(Listing, id=listingID)

    if request.method == "POST":
        form = NewBid(request.POST)
        if form.is_valid():
            bidSubmitted = float(form.cleaned_data['bidPrice'])
            if bidSubmitted <= item.currentBid:
                messages.error(request, "Bid must be more than current bid.")
            else:
                item.currentBid = bidSubmitted
                item.save()
                messages.success(request, "Bid Successful, you are currently winning this bid.")
                obj = form.save(commit=False)
                obj.user = request.user
                obj.listing = item
                obj.save()
        else:
            messages.error(request, f'Errors on form: {form.errors}')
    return redirect('listing', listingID = listingID)