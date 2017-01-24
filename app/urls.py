# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

import app.views as views
from django.conf.urls import url

from datetime import datetime
from app.forms import CustomAuthenticationForm, CustomPasswordChangeForm
from app.views import Home, About, Contact, GroupList, GroupPage, \
    StudentList, StudentPage, AddStudent, AddGroup, DellGroup, RenameGroup, \
    TemplateTags, ExcludeStudent, AssignLeader, DistributeStudent, DellStudent
# from app.models import *
from django.contrib.auth.views import login, logout,\
    password_change, password_change_done


urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^contact$', Contact.as_view(), name='contact'),
    url(r'^about$', About.as_view(), name='about'),
    url(r'^login', login,
        {
            'template_name': 'app/login.html',
            'authentication_form': CustomAuthenticationForm,
            'extra_context':
                {
                    'title': 'Login, please',
                    'year': datetime.now().year,
                }
        }, name='login'),
    url(r'^logout$', logout,
        {
            'next_page': '/'
        }, name='logout'),
    url(r'^password_change/$', password_change,
        {
            'template_name': 'app/password_change.html',
            'password_change_form': CustomPasswordChangeForm,
            'extra_context':
                {
                    'title': 'You can change your password'
                }
        }, name='password_change'),
    url(r'^password_change/done/$', password_change_done,
        {
            'template_name': 'app/password_change_done.html',
        }, name='password_change_done'),

    url(r'^groups/$', GroupList.as_view(), name='groups'),
    url(r'^group/(?P<group_id>[0-9]+)/$', GroupPage.as_view(),
        name='group'),
    # ajax methods
    url(r'^addgroup/$', AddGroup.as_view(), name='add_group'),
    url(r'^delgroup/$', DellGroup.as_view(), name='del_group'),
    url(r'^renamegroup/$', RenameGroup.as_view(), name='rename_group'),
    url(r'^excludestudent/$', ExcludeStudent.as_view(), name='exclude_student'),
    url(r'^assignleader/$', AssignLeader.as_view(), name='assign_leader'),
    url(r'^distributestudent/$', DistributeStudent.as_view(),
        name='distribute_student'),
    url(r'^dellstudent/$', DellStudent.as_view(), name='del_student'),

    url(r'^students/$', StudentList.as_view(), name='students'),
    url(r'^student/(?P<student_id>[0-9]+)/$',
        StudentPage.as_view(), name='student'),
    url(r'^addstudent/$', AddStudent.as_view(), name='add_student'),

    url(r'^templatetags/$', TemplateTags.as_view(), name='tags'),

    # url(r'^profile/$', views.profile, name='profile'),
    # url(r'^apps$', views.apps, name='apps'),
    # url(r'^clients$', views.clients, name='clients'),
    # url(r'^search', views.search, name='search'),
    # url(r'^statistic/$', views.statistic, name='statistic'),
    # url(r'^archive/$', views.archive, name='archive'),
    # url(r'^reviews/$', views.reviews, name='reviews'),
    # url(r'^addreview/$', views.add_review, name='add_review'),
    # url(r'^addapp/$', views.add_app, name='add_app'),
    # # url(r'^result/$', views.render_result, name='result'),
    # url(r'^sync_clients$', views.sync_clients, name='sync_clients'),
    # url(r'^update_client_balance', views.update_client_balance),
    # url(r'^clients/(?P<client_id>[0-9]+)/$', views.client_profile,
    #     name='client_profile'),
    # url(r'^filter_clients$', views.filter_clients,
    #     name='filter_clients'),
    # url(r'^clients_next_page$', views.clients_next_page,
    #     name='clients_next_page'),
]

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
