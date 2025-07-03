from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    DetailView,
    UpdateView,
)

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
    model_name = ""

    EXCLUDED_FIELDS = ["id", "name", "description"]

    def get_all_fields(self):
        if not getattr(self, "object", None):
            return

        model_fields = {}
        for field in self.model._meta.fields:
            if field.name in self.EXCLUDED_FIELDS:
                continue

            if field.many_to_one or field.one_to_one:
                model_fields[field.verbose_name] = getattr(self.object, field.name, "-")
            else:
                model_fields[field.verbose_name] = (
                    field.value_from_object(self.object) or "-"
                )

        return model_fields

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] = f"{self.base_url}_list"
        context["update_url"] = f"{self.base_url}_update"
        context["detail_url"] = f"{self.base_url}_detail"
        context["create_url"] = f"{self.base_url}_create"
        context["delete_url"] = f"{self.base_url}_delete"
        context["model_name"] = self.model_name
        model_fields = self.get_all_fields()
        if model_fields:
            context["model_fields"] = model_fields
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
        try:
            is_create = not bool(getattr(self, "object", None) and self.object.pk)
            response = super().form_valid(form)

            if not self.request.htmx:
                return response

            if is_create:
                return self.create_response()

            return self.update_response()
        except Exception as request_error:
            messages.warning(self.request, f"An error occurred: {request_error}")
            messages.info(
                self.request,
                "Before trying again, check if your item was created or updated",
            )
            redirect_url = self.request.headers["Referer"]
            htmx_response = HttpResponse()
            htmx_response["HX-Redirect"] = redirect_url

            return htmx_response

    def get_success_url(self):
        return reverse_lazy(self.success_url, kwargs={"pk": self.object.pk})

    def create_response(self):
        redirect_url = reverse(f"{self.base_url}_detail", args=[self.object.pk])
        htmx_response = HttpResponse()
        htmx_response["HX-Redirect"] = redirect_url
        messages.success(self.request, "Your item was successfully created!")

        return htmx_response

    def update_response(self):
        context = {
            self.context_object_name: self.object,
            "list_url": f"{self.base_url}_list",
            "update_url": f"{self.base_url}_update",
            "detail_url": f"{self.base_url}_detail",
            "create_url": f"{self.base_url}_create",
            "delete_url": f"{self.base_url}_delete",
        }

        messages.success(self.request, "Your item was successfully updated!")
        return render(self.request, self.template_name, context)


class DeleteViewMixin(PermissionsMixin, HTMXTemplateMixin, DeleteView):
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_delete_form.html"

    def get_success_url(self):
        return reverse(self.base_url + "_list")

    def form_valid(self, form):
        try:
            if not self.request.htmx:
                return super().form_valid(form)

            self.delete(self.request)
            messages.success(self.request, "The deletion was succesful")
            return HttpResponse(headers={"HX-Redirect": self.get_success_url()})

        except Exception as request_error:
            messages.warning(self.request, f"An error occurred: {request_error}")
            messages.info(
                self.request,
                "Before trying again, check if your item was deleted",
            )
            redirect_url = self.request.headers["Referer"]
            htmx_response = HttpResponse()
            htmx_response["HX-Redirect"] = redirect_url

            return htmx_response


# ------------------
# BASE VIEWS
# ------------------


class BaseProjectTypeViewMixin(BaseViewMixin):
    model = models.ProjectType
    base_url = "project_type"
    model_name = "Tasks"


class BaseTaskViewMixin(BaseViewMixin):
    model = models.Task
    base_url = "task"
    model_name = "Task"


class BaseLinkTypeViewMixin(BaseViewMixin):
    model = models.LinkType
    base_url = "link_type"
    model_name = "Link Type"


class BaseLinkViewMixin(BaseViewMixin):
    model = models.Link
    base_url = "link"
    model_name = "Link"


class BaseReviewViewMixin(BaseViewMixin):
    model = models.Review
    base_url = "review"
    model_name = "Review"


class BaseAuthorViewMixin(BaseViewMixin):
    model = models.Author
    base_url = "author"
    model_name = "Author"


class BaseBibliographyTypeViewMixin(BaseViewMixin):
    model = models.BibliographyType
    base_url = "bibliography_type"
    model_name = "Bibliography Type"


class BaseBibliographyViewMixin(BaseViewMixin):
    model = models.Bibliography
    base_url = "bibliography"
    model_name = "Bibliography"


class BaseCheatSheetViewMixin(BaseViewMixin):
    model = models.CheatSheet
    base_url = "cheatsheet"
    model_name = "Cheat Sheet"


class BaseTechnologyViewMixin(BaseViewMixin):
    model = models.Technology
    base_url = "technology"
    model_name = "Technology"


class BaseProjectViewMixin(BaseViewMixin):
    model = models.Project
    base_url = "project"
    model_name = "Project"


class BaseProjectStatusViewMixin(BaseViewMixin):
    model = models.ProjectStatus
    base_url = "project_status"
    model_name = "Project Status"


class BaseDiaryViewMixin(BaseViewMixin):
    model = models.Diary
    base_url = "diary"
    model_name = "Diary"


class BaseDiaryEntryViewMixin(BaseViewMixin):
    model = models.DiaryEntry
    base_url = "diary_entry"
    model_name = "Diary Entry"


class BaseTaskTypeViewMixin(BaseViewMixin):
    model = models.TaskType
    base_url = "task_type"
    model_name = "Task Type"


class BaseTaskStatusViewMixin(BaseViewMixin):
    model = models.TaskStatus
    base_url = "task_status"
    model_name = "Task Status"


# ------------------
# LIST VIEWS
# ------------------


class TaskListView(BaseTaskViewMixin, GenericListView): ...


class LinkTypeListView(BaseLinkTypeViewMixin, GenericListView): ...


class LinkListView(BaseLinkViewMixin, GenericListView): ...


class ReviewListView(BaseReviewViewMixin, GenericListView): ...


class AuthorListView(BaseAuthorViewMixin, GenericListView): ...


class BibliographyTypeListView(BaseBibliographyTypeViewMixin, GenericListView): ...


class BibliographyListView(BaseBibliographyViewMixin, GenericListView): ...


class CheatSheetListView(BaseCheatSheetViewMixin, GenericListView): ...


class TechnologyListView(BaseTechnologyViewMixin, GenericListView): ...


class ProjectTypeListView(BaseProjectTypeViewMixin, GenericListView): ...


class ProjectStatusListView(BaseProjectStatusViewMixin, GenericListView): ...


class ProjectListView(BaseProjectViewMixin, GenericListView): ...


class DiaryListView(BaseDiaryViewMixin, GenericListView): ...


class DiaryEntryListView(BaseDiaryEntryViewMixin, GenericListView): ...


class TaskTypeListView(BaseTaskTypeViewMixin, GenericListView): ...


class TaskStatusListView(BaseTaskStatusViewMixin, GenericListView): ...


# ------------------
# UPDATE VIEWS
# ------------------


class ProjectTypeUpdateView(
    BaseProjectTypeViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    UpdateView,
):
    form_class = forms.ProjectTypeForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form.html"


class TaskUpdateView(
    BaseTaskViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.TaskForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form.html"


class LinkTypeUpdateView(
    BaseLinkTypeViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.LinkForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form.html"


class LinkUpdateView(
    BaseLinkViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.LinkForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form.html"


class ReviewUpdateView(
    BaseReviewViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.ReviewForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class AuthorUpdateView(
    BaseAuthorViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.AuthorForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class BibliographyTypeUpdateView(
    BaseBibliographyTypeViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    UpdateView,
):
    form_class = forms.BibliographyForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class BibliographyUpdateView(
    BaseBibliographyViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    UpdateView,
):
    form_class = forms.BibliographyForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class CheatSheetUpdateView(
    BaseCheatSheetViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    UpdateView,
):
    form_class = forms.CheatSheetForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class TechnologyUpdateView(
    BaseTechnologyViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    UpdateView,
):
    form_class = forms.TechnologyForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class ProjectStatusUpdateView(
    BaseProjectStatusViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    UpdateView,
):
    form_class = forms.ProjectStatusForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class ProjectUpdateView(
    BaseProjectViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.ProjectForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class DiaryUpdateView(
    BaseDiaryViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.DiaryForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class DiaryEntryUpdateView(
    BaseDiaryEntryViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    UpdateView,
):
    form_class = forms.DiaryEntryForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form."


class TaskTypeUpdateView(
    BaseTaskTypeViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.TaskTypeForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form.html"


class TaskStatusUpdateView(
    BaseTaskStatusViewMixin, HTMXTemplateMixin, PermissionsMixin, UpdateView
):
    form_class = forms.TaskStatusForm
    template_name = "app/partials/base_fields.html"
    htmx_template_name = "app/partials/base_form.html"


# ------------------
# DETAIL VIEWS
# ------------------


class ProjectTypeDetailView(
    BaseProjectTypeViewMixin, HTMXTemplateMixin, DetailView
): ...


class TaskDetailView(BaseTaskViewMixin, HTMXTemplateMixin, DetailView): ...


class LinkTypeDetailView(
    BaseLinkTypeViewMixin, HTMXTemplateMixin, PermissionsMixin, DetailView
): ...


class LinkDetailView(
    BaseLinkViewMixin, HTMXTemplateMixin, PermissionsMixin, DetailView
): ...


class ReviewDetailView(
    BaseReviewViewMixin, HTMXTemplateMixin, PermissionsMixin, DetailView
): ...


class AuthorDetailView(
    BaseAuthorViewMixin, HTMXTemplateMixin, PermissionsMixin, DetailView
): ...


class BibliographyTypeDetailView(
    BaseBibliographyTypeViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    DetailView,
): ...


class BibliographyDetailView(
    BaseBibliographyViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    DetailView,
): ...


class CheatSheetDetailView(
    BaseCheatSheetViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    DetailView,
): ...


class TechnologyDetailView(
    BaseTechnologyViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    DetailView,
): ...


class ProjectStatusDetailView(
    BaseProjectStatusViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    DetailView,
): ...


class ProjectDetailView(
    BaseProjectViewMixin, HTMXTemplateMixin, PermissionsMixin, DetailView
): ...


class DiaryDetailView(
    BaseDiaryViewMixin, HTMXTemplateMixin, PermissionsMixin, DetailView
): ...


class DiaryEntryDetailView(
    BaseDiaryEntryViewMixin,
    HTMXTemplateMixin,
    PermissionsMixin,
    DetailView,
): ...


class TaskTypeDetailView(BaseTaskTypeViewMixin, HTMXTemplateMixin, DetailView): ...


class TaskStatusDetailView(BaseTaskStatusViewMixin, HTMXTemplateMixin, DetailView): ...


# ------------------
# CREATE VIEWS
# ------------------


class TaskTypeCreateView(
    BaseTaskTypeViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.TaskTypeForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class TaskStatusCreateView(
    BaseTaskStatusViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.TaskStatusForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class TaskCreateView(
    BaseTaskViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.TaskForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class LinkTypeCreateView(
    BaseLinkTypeViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.LinkTypeForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class LinkCreateView(
    BaseLinkViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.LinkForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class ReviewCreateView(
    BaseReviewViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.ReviewForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class AuthorCreateView(
    BaseAuthorViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.AuthorForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class BibliographyTypeCreateView(
    BaseBibliographyTypeViewMixin, HTMXTemplateMixin, CreateView
):
    form_class = forms.BibliographyTypeForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class BibliographyCreateView(
    BaseBibliographyViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.BibliographyForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class CheatSheetCreateView(
    BaseCheatSheetViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.CheatSheetForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class TechnologyCreateView(
    BaseTechnologyViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.TechnologyForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class ProjectTypeCreateView(
    BaseProjectTypeViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.ProjectTypeForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class ProjectStatusCreateView(
    BaseProjectStatusViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.ProjectStatusForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class ProjectCreateView(
    BaseProjectViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.ProjectForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class DiaryCreateView(
    BaseDiaryViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.DiaryForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


class DiaryEntryCreateView(
    BaseDiaryEntryViewMixin, HTMXTemplateMixin, PermissionsMixin, CreateView
):
    form_class = forms.DiaryEntryForm
    template_name = "app/base_detail.html"
    htmx_template_name = "app/partials/base_form.html"


# ------------------
# DELETE VIEWS
# ------------------


class TaskTypeDeleteView(BaseTaskTypeViewMixin, DeleteViewMixin): ...


class TaskStatusDeleteView(BaseTaskStatusViewMixin, DeleteViewMixin): ...


class TaskDeleteView(BaseTaskViewMixin, DeleteViewMixin): ...


class LinkTypeDeleteView(BaseLinkTypeViewMixin, DeleteViewMixin): ...


class LinkDeleteView(BaseLinkViewMixin, DeleteViewMixin): ...


class ReviewDeleteView(BaseReviewViewMixin, DeleteViewMixin): ...


class AuthorDeleteView(BaseAuthorViewMixin, DeleteViewMixin): ...


class BibliographyTypeDeleteView(BaseBibliographyTypeViewMixin, DeleteViewMixin): ...


class BibliographyDeleteView(BaseBibliographyViewMixin, DeleteViewMixin): ...


class CheatSheetDeleteView(BaseCheatSheetViewMixin, DeleteViewMixin): ...


class TechnologyDeleteView(BaseTechnologyViewMixin, DeleteViewMixin): ...


class ProjectTypeDeleteView(BaseProjectTypeViewMixin, DeleteViewMixin): ...


class ProjectStatusDeleteView(BaseProjectStatusViewMixin, DeleteViewMixin): ...


class ProjectDeleteView(BaseProjectViewMixin, DeleteViewMixin): ...


class DiaryDeleteView(BaseDiaryViewMixin, DeleteViewMixin): ...


class DiaryEntryDeleteView(BaseDiaryEntryViewMixin, DeleteViewMixin): ...
