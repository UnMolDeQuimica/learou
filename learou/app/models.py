from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractType(models.Model):
    """
    Abstract class used as a template to create type classes such as
    'SourceType', 'TaskType', etc. in order to avoid boilerplate.
    """

    class Meta:
        abstract = True

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    icon = models.ImageField(verbose_name=_("Image"), blank=True, null=True)
    model_custom_name = models.CharField(
        verbose_name=_("Model custom name"), blank=True
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.model_custom_name:
            self.name = self.__class__.__name__

        super().save(*args, **kwargs)


class TaskType(AbstractType):
    """
    Handles the task types such as feature, documentation, etc.
    """

    ...


class TaskStatus(AbstractType):
    """
    Tracks the different task status such as in progress, done, etc.
    """

    ...


class Task(models.Model):
    """
    Adds tasks to a different project, making it easy to track it's progress
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    # TODO: Think if I need to add a default value to this
    # See: https://www.geeksforgeeks.org/python/setting-default-value-for-foreign-key-attribute-in-django/
    status = models.ForeignKey(
        TaskStatus,
        verbose_name=_("Status"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    task_type = models.ForeignKey(
        TaskType,
        verbose_name=_("Type"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)


class LinkType(AbstractType):
    """
    Tracks the different Link types
    """

    ...


class Link(models.Model):
    """
    Stores url data
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    url = models.URLField(verbose_name=_("Link"), blank=False, unique=False)

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    """
    When some bibliography/author/technology, etc. is checked, a review of the bibligraphy can be added.
    For example, whena  video or a tutorial is followed, a user can review it,
    leave their thoughts about it etc.
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Author(AbstractType):
    """Tracks the authors of a bibliography"""

    ...
    review = models.ManyToManyField(Review, verbose_name=_("Review"))


class BibliographyType(AbstractType):
    """
    Tracks the different bibliography types (paper, video, etc.)
    """

    ...


class Bibliography(models.Model):
    """
    Links to the source of the information
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    authors = models.ManyToManyField(Author, verbose_name=_("Authors"))
    publication_date = models.DateField(
        verbose_name=_("Publication date"), blank=True, null=True
    )
    extra_data = models.TextField(verbose_name=_("Extra data"), blank=True, null=True)
    review = models.ManyToManyField(Review, verbose_name=_("Review"))
    link = models.ManyToManyField(Link, verbose_name=_("Link"))

    def __str__(self):
        return str(self.name)


class CheatSheet(models.Model):
    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    bibliography = models.ManyToManyField(Bibliography, verbose_name=_("Bibliography"))
    review = models.ManyToManyField(Review, verbose_name=_("Review"))
    link = models.ManyToManyField(Link, verbose_name=_("Link"))


class Technology(models.Model):
    """
    Stores the information about a technology
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    bibliography = models.ManyToManyField(Bibliography, verbose_name=_("Bibliography"))
    review = models.ManyToManyField(Review, verbose_name=_("Review"))
    link = models.ManyToManyField(Link, verbose_name=_("Link"))
    cheat_sheet = models.ManyToManyField(CheatSheet, verbose_name=_("Cheat Sheet"))

    def __str__(self):
        return str(self.name)


class ProjectType(AbstractType): ...


class ProjectStatus(AbstractType): ...


class Project(models.Model):
    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    project_type = models.ForeignKey(
        ProjectType, verbose_name=_("Project Type"), on_delete=models.CASCADE
    )
    project_status = models.ForeignKey(
        ProjectStatus, verbose_name=_("Project Status"), on_delete=models.CASCADE
    )
    review = models.ManyToManyField(Review, verbose_name=_("Review"))
    link = models.ManyToManyField(Link, verbose_name=_("Link"))
    bibliography = models.ManyToManyField(Bibliography, verbose_name=_("Bibliography"))
    tasks = models.ManyToManyField(Task, verbose_name=_("Task"))
    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return str(self.name)


class Diary(models.Model):
    """
    Stores the information about a diary
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    review = models.ManyToManyField(Review, verbose_name=_("Review"))
    link = models.ManyToManyField(Link, verbose_name=_("Link"))
    bibliography = models.ManyToManyField(Bibliography, verbose_name=_("Bibliography"))
    tasks = models.ManyToManyField(Task, verbose_name=_("Task"))
    project = models.ManyToManyField(Project, verbose_name=_("Project"))
    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return str(self.name)


class DiaryEntry(models.Model):
    """
    Stores the information about a diary entry
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    diary = models.ManyToManyField(Diary, verbose_name=_("Diary"))
    review = models.ManyToManyField(Review, verbose_name=_("Review"))
    link = models.ManyToManyField(Link, verbose_name=_("Link"))
    bibliography = models.ManyToManyField(Bibliography, verbose_name=_("Bibliography"))
    tasks = models.ManyToManyField(Task, verbose_name=_("Task"))
    project = models.ManyToManyField(Project, verbose_name=_("Project"))
    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return str(self.name)
