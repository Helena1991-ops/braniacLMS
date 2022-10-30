from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = [
            {
                'title': 'Новость 1',
                'preview': 'Превью к новости 1',
                'date': '2022-01-01'
            }, {
                'title': 'Новость 2',
                'preview': 'Превью к новости 2',
                'date': '2022-01-01'
            }, {
                'title': 'Новость 3',
                'preview': 'Превью к новости 3',
                'date': '2022-01-01'
            }, {
                'title': 'Новость 4',
                'preview': 'Превью к новости 4',
                'date': '2022-01-01'
            }, {
                'title': 'Новость 5',
                'preview': 'Превью к новости 5',
                'date': '2022-01-01'
            }
        ]
        return context_data
