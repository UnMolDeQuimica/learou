from django.contrib import admin
from learou.app.models import (
    TaskType,
    TaskStatus,
    Task,
    LinkType,
    Link,
    Review,
    Author,
    BibliographyType,
    Bibliography,
    CheatSheet,
    Technology,
    ProjectType,
    ProjectStatus,
    Project,
    Diary,
    DiaryEntry,
    CustomModelNameCollection,
    CustomModelName,
    Milestone,
)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin): ...


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin): ...


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin): ...


@admin.register(LinkType)
class LinkTypeAdmin(admin.ModelAdmin): ...


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin): ...


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin): ...


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin): ...


@admin.register(BibliographyType)
class BibliographyTypeAdmin(admin.ModelAdmin): ...


@admin.register(Bibliography)
class BibliographyAdmin(admin.ModelAdmin): ...


@admin.register(CheatSheet)
class CheatSheetAdmin(admin.ModelAdmin): ...


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin): ...


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin): ...


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin): ...


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin): ...


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin): ...


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin): ...


@admin.register(CustomModelNameCollection)
class CustomModelNameCollectionAdmin(admin.ModelAdmin): ...


@admin.register(CustomModelName)
class CustomModelNameAdmin(admin.ModelAdmin): ...


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin): ...
