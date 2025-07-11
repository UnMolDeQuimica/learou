from django.urls import path

from learou.app import views


def make_view_url(view, view_type=None, extra_url=""):
    return path(
        f"{view.base_url}/{extra_url}",
        view.as_view(),
        name=f"{view.base_url}_{view_type}",
    )


list_views = [
    views.TaskTypeListView,
    views.TaskStatusListView,
    views.TaskListView,
    views.LinkTypeListView,
    views.LinkListView,
    views.ReviewListView,
    views.AuthorListView,
    views.BibliographyTypeListView,
    views.BibliographyListView,
    views.CheatSheetListView,
    views.TechnologyListView,
    views.ProjectTypeListView,
    views.ProjectStatusListView,
    views.ProjectListView,
    views.DiaryListView,
    views.DiaryEntryListView,
    views.MilestoneListView,
]

list_urls = [make_view_url(view=view, view_type="list") for view in list_views]

detail_views = [
    views.TaskTypeDetailView,
    views.TaskStatusDetailView,
    views.TaskDetailView,
    views.LinkTypeDetailView,
    views.LinkDetailView,
    views.ReviewDetailView,
    views.AuthorDetailView,
    views.BibliographyTypeDetailView,
    views.BibliographyDetailView,
    views.CheatSheetDetailView,
    views.TechnologyDetailView,
    views.ProjectTypeDetailView,
    views.ProjectStatusDetailView,
    views.ProjectDetailView,
    views.DiaryDetailView,
    views.DiaryEntryDetailView,
    views.MilestoneDetailView,
]

detail_urls = [
    make_view_url(view=view, view_type="detail", extra_url="<int:pk>/")
    for view in detail_views
]

update_views = [
    views.TaskTypeUpdateView,
    views.TaskStatusUpdateView,
    views.TaskUpdateView,
    views.LinkTypeUpdateView,
    views.LinkUpdateView,
    views.ReviewUpdateView,
    views.AuthorUpdateView,
    views.BibliographyTypeUpdateView,
    views.BibliographyUpdateView,
    views.CheatSheetUpdateView,
    views.TechnologyUpdateView,
    views.ProjectTypeUpdateView,
    views.ProjectStatusUpdateView,
    views.ProjectUpdateView,
    views.DiaryUpdateView,
    views.DiaryEntryUpdateView,
    views.MilestoneUpdateView,
]

update_urls = [
    make_view_url(view=view, view_type="update", extra_url="<int:pk>/edit/")
    for view in update_views
]

create_views = [
    views.TaskTypeCreateView,
    views.TaskStatusCreateView,
    views.TaskCreateView,
    views.LinkTypeCreateView,
    views.LinkCreateView,
    views.ReviewCreateView,
    views.AuthorCreateView,
    views.BibliographyTypeCreateView,
    views.BibliographyCreateView,
    views.CheatSheetCreateView,
    views.TechnologyCreateView,
    views.ProjectTypeCreateView,
    views.ProjectStatusCreateView,
    views.ProjectCreateView,
    views.DiaryCreateView,
    views.DiaryEntryCreateView,
    views.MilestoneCreateView,
]

create_urls = [
    make_view_url(view=view, view_type="create", extra_url="create/")
    for view in create_views
]

delete_views = [
    views.TaskTypeDeleteView,
    views.TaskStatusDeleteView,
    views.TaskDeleteView,
    views.LinkTypeDeleteView,
    views.LinkDeleteView,
    views.ReviewDeleteView,
    views.AuthorDeleteView,
    views.BibliographyTypeDeleteView,
    views.BibliographyDeleteView,
    views.CheatSheetDeleteView,
    views.TechnologyDeleteView,
    views.ProjectTypeDeleteView,
    views.ProjectStatusDeleteView,
    views.ProjectDeleteView,
    views.DiaryDeleteView,
    views.DiaryEntryDeleteView,
    views.MilestoneDeleteView,
]

delete_urls = [
    make_view_url(view=view, view_type="delete", extra_url="<int:pk>/delete/")
    for view in delete_views
]
urlpatterns = list_urls + update_urls + detail_urls + create_urls + delete_urls
