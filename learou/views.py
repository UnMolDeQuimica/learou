from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "home.html"


class Features(TemplateView):
    template_name = "features.html"


class LogOut(TemplateView):
    template_name = "registration/logout.html"
