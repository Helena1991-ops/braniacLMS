from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView, View
from mainapp.models import News, Course, Lesson, CourseTeacher, CourseFeedback
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from mainapp.forms import CourseFeedbackForm
from django.template.loader import render_to_string
from config import settings
from django.core.cache import cache
from mainapp import tasks


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def post(self,args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_to_email.delay(message_body, message_from)

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))


class CoursesListView(ListView):
    template_name = 'mainapp/courses_list.html'
    model = Course
    paginate_by = 3




class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)
    # template_name = 'mainapp/news.html'


#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['object_list'] = News.objects.filter(deleted=False)
#         return context_data

class NewsDetailView(DetailView):
    model = News


# class NewsDetail(TemplateView):
#     template_name = 'mainapp/news_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['object'] = get_object_or_404(News, pk=self.kwargs.get('pk'))
#         return context_data


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["course_object"] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context_data["lessons"] = Lesson.objects.filter(course=context_data["course_object"])
        context_data["teachers"] = CourseTeacher.objects.filter(course=context_data["course_object"])
        feedback_list_key = context_data["course_object"].pk
        cached_feedback_list = cache.get(feedback_list_key)

        if cached_feedback_list is None:
            context_data["feedback_list"] = CourseFeedback.objects.filter(course=context_data["course_object"])
            cache.set(feedback_list_key, context_data["feedback_list"], timeout=300)
            # Archive object for tests --->
            # import pickle
            #
            # with open(f"mainapp/fixtures/005_feedback_list_{feedback_list_key}.bin", "wb") as outf:
            #     pickle.dump(context_data["feedback_list"], outf)
            # # <--- Archive object for tests
        else:
            context_data["feedback_list"] = cached_feedback_list

        if self.request.user.is_authenticated:
            context_data["feedback_form"] = CourseFeedbackForm(
                course=context_data["course_object"],
                user=self.request.user
            )



        return context_data


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def from_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})


class LogView(UserPassesTestMixin, TemplateView):

    template_name = "mainapp/log_view.html"


    def test_func(self):
        return self.request.user.is_superuser


    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:  # first 1000 lines
                    break
                log_slice.insert(0, line)  # append at start

            context_data["logs"] = log_slice
        return context_data


class LogDownloadView(UserPassesTestMixin, View):


    def test_func(self):
        return self.request.user.is_superuser


    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
