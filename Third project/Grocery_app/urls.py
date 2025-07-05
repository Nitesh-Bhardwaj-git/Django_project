from django.urls import path
from .views import ItemList, ItemCreate, ItemUpdate, ItemDelete

urlpatterns = [
    path("",           ItemList.as_view(),   name="item-list"),
    path("create/",    ItemCreate.as_view(), name="item-create"),
    path("<int:pk>/",  ItemUpdate.as_view(), name="item-update"),
    path("<int:pk>/delete/", ItemDelete.as_view(), name="item-delete"),
]
