from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name


urlpatterns = [
    path('contacts.html/', views.ContactsView.as_view()),
    path('courses_list.html/', views.CoursesListView.as_view()),
    path('doc_site.html/', views.DocSiteView.as_view()),
    path('', views.IndexView.as_view()),
    path('login.html/', views.LoginView.as_view()),
    path('news.html/', views.NewsView.as_view()),

]

