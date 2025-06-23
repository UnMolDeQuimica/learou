from django.views.generic import ListView

from learou.app import models

class TaskTypeListView(ListView):
    queryset = models.TaskType.objects.all()


class TaskStatusListView(ListView):
    queryset = models.TaskStatus.objects.all()


class TaskListView(ListView):
    queryset = models.Task.objects.all()
    context_object_name = "tasks"


class LinkTypeListView(ListView):
    queryset = models.LinkType.objects.all()


class LinkListView(ListView):
    queryset = models.Link.objects.all()


class ReviewListView(ListView):
    queryset = models.Review.objects.all()


class AuthorListView(ListView):
    queryset = models.Author.objects.all()


class BibliographyTypeListView(ListView):
    queryset = models.BibliographyType.objects.all()


class BibliographyListView(ListView):
    queryset = models.Bibliography.objects.all()


class CheatSheetListView(ListView):
    queryset = models.CheatSheet.objects.all()


class TechnologyListView(ListView):
    queryset = models.Technology.objects.all()


class ProjectTypeListView(ListView):
    queryset = models.ProjectType.objects.all()


class ProjectStatusListView(ListView):
    queryset = models.ProjectStatus.objects.all()


class ProjectListView(ListView):
    queryset = models.Project.objects.all()


class DiaryListView(ListView):
    queryset = models.Diary.objects.all()


class DiaryEntryListView(ListView):
    queryset = models.DiaryEntry.objects.all()
