from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint, Q


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

    def __str__(self):
        return str(self.name)

    @classmethod
    def model_name(cls):
        from learou.app.models import CustomModelNameCollection, CustomModelName

        custom_collection_qs = CustomModelNameCollection.objects.filter(is_active=True)

        if not custom_collection_qs:
            return cls.__name__

        custom_collection = custom_collection_qs.first()

        custom_model_name_qs = CustomModelName.objects.filter(
            model=cls.__name__, custom_model_name_collection=custom_collection
        )

        if not custom_model_name_qs:
            return cls.__name__

        return custom_model_name_qs.first().name


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


class Task(AbstractType):
    """
    Adds tasks to a different project, making it easy to track it's progress
    """

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


class Link(AbstractType):
    """
    Stores url data
    """

    url = models.URLField(verbose_name=_("Link"), blank=False, unique=False)

    def __str__(self):
        return str(self.name)


class Review(AbstractType):
    """
    When some bibliography/author/technology, etc. is checked, a review of the bibligraphy can be added.
    For example, whena  video or a tutorial is followed, a user can review it,
    leave their thoughts about it etc.
    """

    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Author(AbstractType):
    """Tracks the authors of a bibliography"""

    ...
    review = models.ManyToManyField(Review, verbose_name=_("Review"), blank=True)


class BibliographyType(AbstractType):
    """
    Tracks the different bibliography types (paper, video, etc.)
    """

    ...


class Bibliography(AbstractType):
    """
    Links to the source of the information
    """

    authors = models.ManyToManyField(Author, verbose_name=_("Authors"), blank=True)
    publication_date = models.DateField(
        verbose_name=_("Publication date"), blank=True, null=True
    )
    extra_data = models.TextField(verbose_name=_("Extra data"), blank=True, null=True)
    review = models.ManyToManyField(Review, verbose_name=_("Review"), blank=True)
    link = models.ManyToManyField(Link, verbose_name=_("Link"), blank=True)

    def __str__(self):
        return str(self.name)


class CheatSheet(AbstractType):
    """
    Used to summarize the useful tips or procedures from a review.
    """

    bibliography = models.ManyToManyField(
        Bibliography, verbose_name=_("Bibliography"), blank=True
    )
    review = models.ManyToManyField(Review, verbose_name=_("Review"), blank=True)
    link = models.ManyToManyField(Link, verbose_name=_("Link"), blank=True)


class Technology(AbstractType):
    """
    Stores the information about a technology
    """

    bibliography = models.ManyToManyField(
        Bibliography, verbose_name=_("Bibliography"), blank=True
    )
    review = models.ManyToManyField(Review, verbose_name=_("Review"), blank=True)
    link = models.ManyToManyField(Link, verbose_name=_("Link"), blank=True)
    cheat_sheet = models.ManyToManyField(
        CheatSheet, verbose_name=_("Cheat Sheet"), blank=True
    )

    def __str__(self):
        return str(self.name)


class ProjectType(AbstractType):
    """
    Describes the different project types:
        - Reading a book.
        - Creating an app.
        - Learning a new skill
        - ...
    """

    ...


class ProjectStatus(AbstractType):
    """
    Describes the status of a project:
        - In progress
        - New
        - To Be Done
        - ...
    """

    ...


class Project(AbstractType):
    """
    A project is something you want to achieve.
    Maybe making an app or reading a book or
    learning to play a new song.
    """

    project_type = models.ForeignKey(
        ProjectType,
        verbose_name=_("Project Type"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project_status = models.ForeignKey(
        ProjectStatus,
        verbose_name=_("Project Status"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    review = models.ManyToManyField(Review, verbose_name=_("Review"), blank=True)
    link = models.ManyToManyField(Link, verbose_name=_("Link"), blank=True)
    bibliography = models.ManyToManyField(
        Bibliography, verbose_name=_("Bibliography"), blank=True
    )
    tasks = models.ManyToManyField(Task, verbose_name=_("Task"), blank=True)
    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateField(verbose_name=_("Updated at"), auto_now=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subproject",
        verbose_name=_("Parent"),
    )

    def __str__(self):
        return str(self.name)


class Diary(AbstractType):
    """
    Stores the information about a diary
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    review = models.ManyToManyField(Review, verbose_name=_("Review"), blank=True)
    link = models.ManyToManyField(Link, verbose_name=_("Link"), blank=True)
    bibliography = models.ManyToManyField(
        Bibliography, verbose_name=_("Bibliography"), blank=True
    )
    tasks = models.ManyToManyField(Task, verbose_name=_("Task"), blank=True)
    project = models.ManyToManyField(Project, verbose_name=_("Project"), blank=True)
    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return str(self.name)


class DiaryEntry(AbstractType):
    """
    Stores the information about a diary entry
    """

    name = models.CharField(
        verbose_name=_("Name"), max_length=255, blank=False, unique=True
    )
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    diary = models.ManyToManyField(Diary, verbose_name=_("Diary"), blank=True)
    review = models.ManyToManyField(Review, verbose_name=_("Review"), blank=True)
    link = models.ManyToManyField(Link, verbose_name=_("Link"), blank=True)
    bibliography = models.ManyToManyField(
        Bibliography, verbose_name=_("Bibliography"), blank=True
    )
    tasks = models.ManyToManyField(Task, verbose_name=_("Task"), blank=True)
    project = models.ManyToManyField(Project, verbose_name=_("Project"), blank=True)
    created_at = models.DateField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return str(self.name)


class CustomModelNameCollection(AbstractType):
    """
    Used to customize the models naming
    """

    is_active = models.BooleanField(
        verbose_name="Is active", default=False, blank=False, null=False
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("is_active",),
                condition=Q(is_active=True),
                name="unique_active_value",
            )
        ]


class CustomModelName(AbstractType):
    MODELS = (
        ("AbstractType", "Abstract Type"),
        ("TaskType", "Task Type"),
        ("TaskStatus", "Task Status"),
        ("Task", "Task"),
        ("LinkType", "Link Type"),
        ("Link", "Link"),
        ("Review", "Review"),
        ("Author", "Author"),
        ("BibliographyType", "Bibliography Type"),
        ("Bibliography", "Bibliography"),
        ("CheatSheet", "Cheat Sheet"),
        ("Technology", "Technology"),
        ("ProjectType", "Project Type"),
        ("ProjectStatus", "Project Status"),
        ("Project", "Project"),
        ("Diary", "Diary"),
        ("DiaryEntry", "Diary Entry"),
        ("CustomModelNameCollection", "Custom Model Name Collection"),
        ("CustomModelName", "Custom Model Name"),
    )
    model = models.CharField(
        verbose_name="Model", blank=False, null=False, choices=MODELS
    )
    custom_model_name_collection = models.ForeignKey(
        to=CustomModelNameCollection, on_delete=models.CASCADE, blank=False, null=False
    )

    class Meta:
        unique_together = ("model", "custom_model_name_collection")

    def __str__(self):
        return f"{self.custom_model_name_collection.name} - {self.model}"
