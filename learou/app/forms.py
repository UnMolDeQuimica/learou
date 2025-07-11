from django import forms

from learou.app import models


class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = models.ProjectType
        fields = "__all__"


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = models.TaskType
        fields = "__all__"


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = models.TaskStatus
        fields = "__all__"


class LinkTypeForm(forms.ModelForm):
    class Meta:
        model = models.LinkType
        fields = "__all__"


class LinkForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = "__all__"


class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = "__all__"


class BibliographyTypeForm(forms.ModelForm):
    class Meta:
        model = models.BibliographyType
        fields = "__all__"


class BibliographyForm(forms.ModelForm):
    class Meta:
        model = models.Bibliography
        fields = "__all__"


class CheatSheetForm(forms.ModelForm):
    class Meta:
        model = models.CheatSheet
        fields = "__all__"


class TechnologyForm(forms.ModelForm):
    class Meta:
        model = models.Technology
        fields = "__all__"


class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = models.ProjectStatus
        fields = "__all__"


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"


class DiaryForm(forms.ModelForm):
    class Meta:
        model = models.Diary
        fields = "__all__"


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = models.DiaryEntry
        fields = "__all__"


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = models.Milestone
        fields = "__all__"
