# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.views.generic import View, ListView
from app.models import Student, StudentGroup, StudentGroupDistribution, \
    GroupLead
from app.forms import UserProfileForm, StudentForm, \
    NewGroupForm, NewUserProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django_ajax.decorators import ajax

from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

AJAX_DECORATORS = [
        login_required,
        user_passes_test(lambda u: u.is_superuser),
        ajax
    ]


class Home(View):
    """Renders the home page."""
    template_name = 'app/index.html'

    def get(self, request):
        assert isinstance(request, HttpRequest)
        return render(request, self.template_name)


class Contact(View):
    """Renders the contact page."""
    template_name = 'app/contact.html'

    def get(self, request):
        assert isinstance(request, HttpRequest)
        context = {
            'title': 'Contact',
            'message': 'Your contact page.',
        }
        return render(request, self.template_name, context)


class About(View):
    """Renders the about page."""
    template_name = 'app/about.html'

    def get(self, request):
        assert isinstance(request, HttpRequest)
        context = {
            'title': 'About',
            'message': 'Your application description page.',
        }
        return render(request, self.template_name, context)


class GroupList(ListView):
    """Renders the page with a list of groups."""
    model = StudentGroup
    template_name = 'app/groups.html'


class GroupPage(View):
    """Renders the page of the group"""
    template_name = 'app/group.html'

    def get(self, request, group_id):
        group = get_object_or_404(StudentGroup, id=group_id)

        all_students = Student.objects.all()
        students = Student.objects.filter(
            id__in=[student.student_id for student in
                    StudentGroupDistribution.objects.filter(group_id=group_id)]
        )
        context = {
            'group': group,
            'students': students,
            'all_students': all_students,
        }
        return render(request, self.template_name, context)


@method_decorator(AJAX_DECORATORS, name='post')
class AddGroup(View):
    new_group_form = NewGroupForm

    def post(self, request):
        form = self.new_group_form(request.POST)
        if form.is_valid():
            new_group = form.save()
            new_group_row = str(
                render(request, 'app/groups_table_row.html',
                       {'group': new_group}).content
            ).replace('\\n', '')
            append_data = {
                '#group_list_table': new_group_row,
            }
            return {
                'append-fragments': append_data,
            }


@method_decorator(AJAX_DECORATORS, name='post')
class DellGroup(View):

    def post(self, request):
        try:
            group_id = request.POST['group_id']
        except KeyError:
            return

        try:
            group = StudentGroup.objects.get(id=group_id)
        except ObjectDoesNotExist:
            return

        group.delete()

        # exclude students in this group from table 'StudentGroupDistribution'
        distributions = StudentGroupDistribution.objects.filter(
            group_id=group_id
        )
        for distribution in distributions:
            distribution.delete()

        replace_data = {
            '#group_'+group_id+'_tr': '',
        }
        return {
            'fragments': replace_data,
        }


@method_decorator(AJAX_DECORATORS, name='post')
class RenameGroup(View):

    def post(self, request):
        try:
            group_id = request.POST['group_id']
            group_name = request.POST['group_name']
        except KeyError:
            return

        try:
            group = StudentGroup.objects.get(id=group_id)
        except ObjectDoesNotExist:
            return

        group.name = group_name
        group.save()

        replace_data = {
            '#group_name': '<h1 id="group_name">' + group_name + '</h1>',
        }
        return {
            'fragments': replace_data,
        }


@method_decorator(AJAX_DECORATORS, name='post')
class ExcludeStudent(View):

    def post(self, request):
        try:
            group_id = request.POST['group_id']
        except KeyError:
            return

        try:
            student_id = request.POST['student_id']
        except KeyError:
            return

        # exclude student in this group from table 'StudentGroupDistribution'
        distributions = StudentGroupDistribution.objects.filter(
            Q(group_id=group_id) & Q(student_id=student_id)
        )
        for distribution in distributions:
            distribution.delete()

        replace_data = {
            '#student_' + student_id + '_tr': '',
        }
        return {
            'fragments': replace_data,
        }


@method_decorator(AJAX_DECORATORS, name='post')
class AssignLeader(View):

    def post(self, request):
        try:
            group_id = request.POST['group_id']
        except KeyError:
            return

        try:
            student_id = request.POST['student_id']
        except KeyError:
            return

        try:
            group_lead = GroupLead.objects.get(group_id=group_id)
            group_lead.leader_id = student_id
            group_lead.save()
        except ObjectDoesNotExist:
            group_lead = GroupLead(group_id=group_id, leader_id=student_id)
            group_lead.save()
        student = Student.objects.get(id=student_id)

        replace_data = {
            '#group_leader': '<h3 id="group_leader">' +
                             student.get_full_instance_name() + '</h3>',
        }
        return {
            'fragments': replace_data,
        }


@method_decorator(AJAX_DECORATORS, name='post')
class DistributeStudent(View):

    def post(self, request):
        try:
            group_id = request.POST['group_id']
        except KeyError:
            return

        try:
            student_id = request.POST['student_id']
        except KeyError:
            return

        distributions = StudentGroupDistribution.objects.filter(
            Q(group_id=group_id) & Q(student_id=student_id)
        )
        if len(distributions) == 0:
            distribution = StudentGroupDistribution(group_id=group_id,
                                                    student_id=student_id)
            distribution.save()
        else:
            return

        student = Student.objects.get(id=student_id)

        new_student_row = str(
            render(request, 'app/student_table_row.html',
                   {'student': student}).content
        ).replace('\\n', '')
        append_data = {
            '#student_list_table': new_student_row,
        }
        return {
            'append-fragments': append_data,
        }


@method_decorator(AJAX_DECORATORS, name='post')
class DellStudent(View):

    def post(self, request):

        try:
            student_id = request.POST['student_id']
        except KeyError:
            return

        # delete student and appropriate user
        try:
            student = Student.objects.get(id=student_id)
        except ObjectDoesNotExist:
            pass
        user_id = student.user_id
        student.delete()
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            pass
        user.delete()

        replace_data = {
            '#student_' + student_id + '_tr': '',
        }
        return {
            'fragments': replace_data,
        }


class StudentList(ListView):
    model = Student
    template_name = 'app/students.html'


class StudentPage(View):
    """Renders the page of the student"""
    template_name = 'app/student.html'
    form = StudentForm
    user_form = UserProfileForm

    def get(self, request, student_id):

        student_data = get_object_or_404(Student, id=student_id)
        user_data = get_object_or_404(User, id=student_data.user_id)

        form = self.form(instance=student_data)

        context = {
            'form': form,
            'student': student_data,
            'email': user_data.username,
        }
        return render(request, self.template_name, context)

    def post(self, request, student_id):

        student_data = get_object_or_404(Student, id=student_id)
        user_data = get_object_or_404(User, id=student_data.user_id)

        form = self.form(request.POST, instance=student_data)
        user_form = self.user_form(request.POST, instance=user_data)
        if form.is_valid() and user_form.is_valid():
            if user_form.has_changed():
                user_data.username = user_form.cleaned_data['username']
                user_data.save()
            if form.has_changed():
                student_data.first_name = form.cleaned_data['first_name']
                student_data.middle_name = form.cleaned_data['middle_name']
                student_data.last_name = form.cleaned_data['last_name']
                student_data.bdate = form.cleaned_data['bdate']
                student_data.stud_id = form.cleaned_data['stud_id']
                student_data.save()

        context = {
            'form': form,
            'user_form': user_form,
            'student': student_data,
            'email': user_data.username,
        }
        return render(request, self.template_name, context)


class AddStudent(View):
    template_name = 'app/add_student.html'
    form = StudentForm
    user_form = NewUserProfileForm

    def get(self, request):

        form = self.form()

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):

        form = self.form(request.POST)
        user_form = self.user_form(request.POST)

        if form.is_valid() and user_form.is_valid():
            new_user = user_form.save()
            form.cleaned_data.update({
                'user_id': new_user.id
            })
            new_student = Student(**form.cleaned_data)
            new_student.save()
            return redirect('/students/')
        else:
            context = {
                'form': form,
                'user_form': user_form,
            }
            return render(request, self.template_name, context)


class TemplateTags(View):
    template_name = 'app/templatetags.html'

    def get(self, request):
        context = {
            'group': StudentGroup.objects.get(id=1),
            'student': Student.objects.get(id=1),
        }
        return render(request, self.template_name, context)
