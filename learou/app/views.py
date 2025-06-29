from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    DetailView,
    FormView,
    UpdateView,
)
from django.contrib import messages

from learou.app import models, forms

# Base and generic classes


class GenericListView(ListView):
    model = None
    model_name = None
    template_name = "app/base_list.html"
    context_object_name = "objects"

    def get_queryset(self):
        if not self.model:
            raise Exception("No model provided")

        return self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        if not self.model_name:
            raise Exception("No model name provided")
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["model_name"] = self.model_name
        return context


class PermissionsMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to edit")

        self.list_url = f"{self.base_url}_list"
        self.update_url = f"{self.base_url}_update"
        self.detail_url = f"{self.base_url}_detail"
        self.create_url = f"{self.base_url}_create"
        self.delete_url = f"{self.base_url}_delete"
        self.success_url = self.detail_url
        return super().dispatch(request, *args, **kwargs)


class BaseViewMixin:
    base_url = ""
    list_url = f"{base_url}_list"
    update_url = f"{base_url}_update"
    detail_url = f"{base_url}_detail"
    create_url = f"{base_url}_create"
    delete_url = f"{base_url}_delete"
    success_url = detail_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] = f"{self.base_url}_list"
        context["update_url"] = f"{self.base_url}_update"
        context["detail_url"] = f"{self.base_url}_detail"
        context["create_url"] = f"{self.base_url}_create"
        context["delete_url"] = f"{self.base_url}_delete"
        return context


class HTMXTemplateMixin:
    htmx_template_name = None
    template_name = "app/base_detail.html"
    context_object_name = "object"
    htmx_template_name = "app/partials/base_fields.html"

    def get_template_names(self):
        if self.request.htmx and self.htmx_template_name:
            return [self.htmx_template_name]
        return super().get_template_names()

    def form_valid(self, form):
        is_create = not bool(getattr(self, "object", None) and self.object.pk)
        response = super().form_valid(form)

        if not self.request.htmx:
            return response
        if is_create:
            redirect_url = reverse(f"{self.base_url}_detail", args=[self.object.pk])
            htmx_response = HttpResponse()
            htmx_response["HX-Redirect"] = redirect_url
            return htmx_response

        context = {
            self.context_object_name: self.object,
            "list_url": f"{self.base_url}_list",
            "update_url": f"{self.base_url}_update",
            "detail_url": f"{self.base_url}_detail",
            "create_url": f"{self.base_url}_create",
            "delete_url": f"{self.base_url}_delete",
        }
        return render(self.request, self.template_name, context)

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={"pk": self.object.pk})


class DeleteViewMixin(PermissionsMixin, HTMXTemplateMixin, DeleteView):
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_delete_form.html"

    def get_success_url(self):
        return reverse(self.base_url + "_list")

    def form_valid(self, form):
        if not self.request.htmx:
            return super().form_valid(form)

        self.delete(self.request)

        return HttpResponse(headers={"HX-Redirect": self.get_success_url()})


# ------------------
# BASE VIEWS
# ------------------


class BaseProjectTypeViewMixin(BaseViewMixin):
    model = models.ProjectType
    base_url = "project_type"


class BaseTaskViewMixin(BaseViewMixin):
    model = models.Task
    base_url = "task"


class BaseLinkTypeViewMixin(BaseViewMixin):
    model = models.LinkType
    base_url = "link_type"


class BaseLinkViewMixin(BaseViewMixin):
    model = models.Link
    base_url = "link"


class BaseReviewViewMixin(BaseViewMixin):
    model = models.Review
    base_url = "review"


class BaseAuthorViewMixin(BaseViewMixin):
    model = models.Author
    base_url = "author"


class BaseBibliographyTypeViewMixin(BaseViewMixin):
    model = models.BibliographyType
    base_url = "bibliography_type"


class BaseBibliographyViewMixin(BaseViewMixin):
    model = models.Bibliography
    base_url = "bibliography"


class BaseCheatSheetViewMixin(BaseViewMixin):
    model = models.CheatSheet
    base_url = "cheatsheet"


class BaseTechnologyViewMixin(BaseViewMixin):
    model = models.Technology
    base_url = "technology"


class BaseProjectViewMixin(BaseViewMixin):
    model = models.Project
    base_url = "project"


class BaseProjectStatusViewMixin(BaseViewMixin):
    model = models.ProjectStatus
    base_url = "project_status"


class BaseDiaryViewMixin(BaseViewMixin):
    model = models.Diary
    base_url = "diary"


class BaseDiaryEntryViewMixin(BaseViewMixin):
    model = models.DiaryEntry
    base_url = "diary_entry"


class BaseTaskTypeViewMixin(BaseViewMixin):
    model = models.TaskType
    base_url = "task_type"


class BaseTaskStatusViewMixin(BaseViewMixin):
    model = models.TaskStatus
    base_url = "task_status"


# ------------------
# LIST VIEWS
# ------------------


class TaskListView(BaseTaskViewMixin, GenericListView):
    model_name = "Tasks"


class LinkTypeListView(BaseLinkTypeViewMixin, GenericListView):
    model_name = "Link Type"


class LinkListView(BaseLinkViewMixin, GenericListView):
    model_name = "Link"


class ReviewListView(BaseReviewViewMixin, GenericListView):
    model_name = "Review"


class AuthorListView(BaseAuthorViewMixin, GenericListView):
    model_name = "Author"


class BibliographyTypeListView(BaseBibliographyTypeViewMixin, GenericListView):
    model_name = "Bibliography Type"


class BibliographyListView(BaseBibliographyViewMixin, GenericListView):
    model_name = "Bibliography"


class CheatSheetListView(BaseCheatSheetViewMixin, GenericListView):
    model_name = "Cheat Sheet"


class TechnologyListView(BaseTechnologyViewMixin, GenericListView):
    model_name = "Technology"


class ProjectTypeListView(BaseProjectTypeViewMixin, GenericListView):
    model_name = "Project Type"


class ProjectStatusListView(BaseProjectStatusViewMixin, GenericListView):
    model_name = "Project Status"


class ProjectListView(BaseProjectViewMixin, GenericListView):
    model_name = "Project"


class DiaryListView(BaseDiaryViewMixin, GenericListView):
    model_name = "Diary"


class DiaryEntryListView(BaseDiaryEntryViewMixin, GenericListView):
    model_name = "Diary Entry"


class TaskTypeListView(BaseTaskTypeViewMixin, GenericListView):
    model_name = "Task Type"


class TaskStatusListView(BaseTaskStatusViewMixin, GenericListView):
    model_name = "Task Status"


