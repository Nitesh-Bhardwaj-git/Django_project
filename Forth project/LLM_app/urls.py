from django.urls import path
from .views import (
    CourseList, CourseDetail,
    CourseCreate, CourseUpdate, CourseDelete,
    EnrollView,
)

urlpatterns = [
    path("",              CourseList.as_view(),   name="course-list"),
    path("course/<int:pk>/",        CourseDetail.as_view(),  name="course-detail"),
    path("course/add/",             CourseCreate.as_view(),  name="course-add"),
    path("course/<int:pk>/edit/",   CourseUpdate.as_view(),  name="course-edit"),
    path("course/<int:pk>/delete/", CourseDelete.as_view(),  name="course-delete"),
    path("course/<int:pk>/enroll/", EnrollView.as_view(),    name="course-enroll"),
]
