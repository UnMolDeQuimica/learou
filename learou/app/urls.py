from django.urls import include, path
from rest_framework import routers

from learou.app import views

urlpatterns = [
    path("task_type/", views.TaskTypeListView.as_view()),
    path("task_status/", views.TaskStatusListView.as_view()),
    path("task/", views.TaskListView.as_view()),
    path("link_type/", views.LinkTypeListView.as_view()),
    path("link/", views.LinkListView.as_view()),
    path("review/", views.ReviewListView.as_view()),
    path("author/", views.AuthorListView.as_view()),
    path("bibliography_type/", views.BibliographyTypeListView.as_view()),
    path("bibliography/", views.BibliographyListView.as_view()),
    path("cheatsheet/", views.CheatSheetListView.as_view()),
    path("technology/", views.TechnologyListView.as_view()),
    path("project_type/", views.ProjectTypeListView.as_view()),
    path("project_status/", views.ProjectStatusListView.as_view()),
    path("project/", views.ProjectListView.as_view()),
    path("diary/", views.DiaryListView.as_view()),
    path("diary_entry/", views.DiaryEntryListView.as_view()),
]
