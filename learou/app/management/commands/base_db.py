from django.core.management.base import BaseCommand
from learou.app.models import (
    TaskType,
    TaskStatus,
    BibliographyType,
    ProjectStatus,
)


class Command(BaseCommand):
    def create_task_types(self):
        TaskType.objects.get_or_create(name="Feature", description="Feature")
        TaskType.objects.get_or_create(
            name="Documentation", description="Documentation"
        )
        TaskType.objects.get_or_create(name="Improvement", description="Improvement")
        TaskType.objects.get_or_create(name="Fix", description="Fix")

    def create_task_status(self):
        TaskStatus.objects.get_or_create(name="New", description="New")
        TaskStatus.objects.get_or_create(name="In progress", description="In progress")
        TaskStatus.objects.get_or_create(name="Done", description="Done")
        TaskStatus.objects.get_or_create(name="Blocked", description="Blocked")

    def create_bibliography_type(self):
        BibliographyType.objects.get_or_create(name="Book", description="Book")
        BibliographyType.objects.get_or_create(name="Article", description="Article")
        BibliographyType.objects.get_or_create(name="Paper", description="Paper")
        BibliographyType.objects.get_or_create(name="Web page", description="Web page")
        BibliographyType.objects.get_or_create(name="Video", description="Video")

    def create_project_status(self):
        ProjectStatus.objects.get_or_create(name="New", description="New")
        ProjectStatus.objects.get_or_create(
            name="In progress", description="In progress"
        )
        ProjectStatus.objects.get_or_create(name="Finished", description="Finished")
        ProjectStatus.objects.get_or_create(
            name="Under maintainment", description="Under maintainment"
        )
        ProjectStatus.objects.get_or_create(name="Abandoned", description="Abandoned")

    def handle(self, *args, **kwargs):
        self.create_task_types()
        self.create_task_status()
        self.create_bibliography_type()
        self.create_project_status()
