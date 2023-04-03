from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import HomeView, CollectionExplorer, RoadMapView, NftGalleryView
from NftDashboard import views

urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    path("", CollectionExplorer.as_view(), name="collection_explorer"),
    path("road-map", RoadMapView.as_view(), name="roadmap"),
    path("gallery", NftGalleryView.as_view(), name="gallery"),
    # path('', LandingPage.as_view(), name='landing-page'),
]
