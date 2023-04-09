from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new"),
    
    path("listing/<int:id>", views.listing, name="listing"),
    path("post_comment/<int:producto_id>", views.post_comment, name="post_comment"),
    path("bid/<int:producto_id>", views.bid, name="bid"),
    path("categoryFilter", views.categoryFilter, name="categoryFilter"),
    path("watch_list_see", views.watch_list_see, name="watch_list_see"),
    path("watchList/<int:producto_id>", views.watchList, name="watchList"),
    path("closeListing/<int:producto_id>", views.closeListing, name="closeListing"),


]
