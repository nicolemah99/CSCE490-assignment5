from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listings/<str:listingID>", views.listing, name="listing"),
    path(("comment/<str:listingID>"), views.comment, name="comment"),
    path(("bid/<str:listingID>"), views.bid, name="bid"),
    path(("bycategory/<str:categoryChosen>"), views.bycategory, name="bycategory"),
    path(("addtowatchlist/<str:listingID>"), views.addtowatchlist, name="addtowatchlist"),
    path(("removefromwatchlist/<str:listingID>"), views.removefromwatchlist, name="removefromwatchlist"),
    path(("closeBidding/<str:listingID>"), views.closeBidding, name="closeBidding"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
