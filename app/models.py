"""
Definition of models.
"""
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Student(models.Model):
    """Model for student"""
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    user = models.OneToOneField(User,
                                verbose_name='User',
                                help_text='point appropriate user',
                                on_delete=models.SET_NULL,
                                blank=True, null=True)
    first_name = models.CharField('* Name',
                                  help_text='enter your name here',
                                  max_length=30)
    middle_name = models.CharField('Middle name',
                                   help_text='enter your middle name here',
                                   max_length=50, blank=True, default='')
    last_name = models.CharField('Last name',
                                 help_text='enter your last name here',
                                 max_length=50, blank=True, default='')
    bdate = models.DateField('Birthday',
                             help_text='pick your birthday',
                             blank=True, null=True)
    stud_id = models.CharField('Student id',
                               help_text='enter your student id number',
                               max_length=16, blank=True,
                               default='', unique=True)

    def get_full_name(self):
        return ' '.join([self.last_name,
                         self.first_name,
                         self.middle_name])

    def get_full_instance_name(self):
        full_name = ' '.join([self.last_name,
                              self.first_name,
                              self.middle_name])
        try:
            user = User.objects.get(id=self.user_id)
            if user.username != '':
                username = '(' + user.username + ')'
            else:
                username = ''
        except ObjectDoesNotExist:
            username = '(no appropriate user)'
        return '{} {}'.format(full_name, username)

    def __str__(self):
        return self.get_full_instance_name()


class StudentGroup(models.Model):
    """Model for an instance of student Group """
    class Meta:
        verbose_name = 'Group of students'
        verbose_name_plural = 'Student groups'

    name = models.CharField('* Name',
                            help_text='enter group name here',
                            max_length=50, unique=True)

    def get_len(self):
        students = StudentGroupDistribution.objects.filter(group_id=self.id)
        return '{}'.format(len(students))

    def get_leader(self):
        try:
            leader = GroupLead.objects.get(group_id=self.id)
            leader = Student.objects.get(id=leader.leader_id)
        except ObjectDoesNotExist:
            leader = 'none'
        return leader

    def get_full_instance_name(self):
        students = StudentGroupDistribution.objects.filter(group_id=self.id)
        return '{}, ({} members)'.format(self.name, len(students))

    def __str__(self):
        return self.get_full_instance_name()


class StudentGroupDistribution(models.Model):
    """Model for distribution of students in groups"""
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    group = models.ForeignKey(StudentGroup,
                              verbose_name='* Group',
                              help_text='pick a group to assign a student for',
                              on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student,
                                verbose_name='* Student',
                                help_text='pick a student',
                                on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            group = StudentGroup.objects.get(id=self.group_id)
            group = group.get_full_instance_name()
        except ObjectDoesNotExist:
            group = 'group deleted'

        try:
            student = Student.objects.get(id=self.student_id)
            student = student.get_full_instance_name()
        except ObjectDoesNotExist:
            student = 'student deleted'

        return '{}, {}'.format(group, student)


class GroupLead(models.Model):
    """Model for group leaders"""
    class Meta:
        verbose_name = 'Group leader'
        verbose_name_plural = 'Group leaders'

    group = models.ForeignKey(StudentGroup,
                              verbose_name='* Group',
                              help_text='pick a group to assign a leader for',
                              on_delete=models.SET_NULL, null=True)
    leader = models.ForeignKey(Student,
                               verbose_name='* Leader',
                               help_text='pick a leader from a students',
                               on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            group = StudentGroup.objects.get(id=self.group_id)
            group = group.get_full_instance_name()
        except ObjectDoesNotExist:
            group = 'group deleted'

        try:
            leader = Student.objects.get(id=self.leader_id)
            leader = leader.get_full_instance_name()
        except ObjectDoesNotExist:
            leader = 'student deleted'

        return '{}, {}'.format(group, leader)
