from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



# Create your models here.
# Model: info about data
# Migration: SQL information used to create table
# Make-migration generates files (migrations aka sql equivalent of a model)



class Profile(models.Model):
    """Links User to User attributes"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True, null=False)
    user_id = 1
    MBTI_CHOICES = [
        # ('DB', 'shown')
        ('TBD', 'To Be Determined'),
        ('INFP', 'INFP'),
        ('INFJ', 'INFJ'),
        ('INTP', 'INTP'),
        ('INTJ', 'INTJ'),
        ('ISFP', 'ISFP'),
        ('ISFJ', 'ISFJ'),
        ('ISTP', 'ISTP'),
        ('ISTJ', 'ISTJ'),
        ('ENFP', 'ENFP'),
        ('ENFJ', 'ENFJ'),
        ('ENTP', 'ENTP'),
        ('ENTJ', 'ENTJ'),
        ('ESFP', 'ESFP'),
        ('ESFJ', 'ESFJ'),
        ('ESTP', 'ESTP'),
        ('ESTJ', 'ESTJ')
        ]
    user_mbti = models.CharField(
        max_length=4,
        choices=MBTI_CHOICES,
        default=None,
        blank=True, null=True)
    childhood_hobbies = models.TextField("",
                                         blank=True, null=True)

    # def __str__(self):
    #     """return string representation of profile"""
    #     return self.user_mbti


    def get_absolute_url(self):
        username = self.user.objects.get(self.user.username)
        return reverse("home:create-profile", args=[username])



class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    entry = models.TextField()



class Suggestion(models.Model):
    """Suggestions submitted by people"""

    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.text


# class Blog(models.Model):
#     title = models.CharField(max_length=200)
#     entry = models.TextField()
#     last_modified = models.DateTimeField(auto_now_add=True)
#     img = models.ImageField(upload_to="images/")
#
#     # renames the instances of the model
#     # with their title name
#     def __str__(self):
#         return self.title



class ToDoList(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse("home:list2", args=[self.id])

    def __str__(self):
        return self.name


class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    complete = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "home:list2", args=[str(self.todolist.id)]
        )

    def __str__(self):
        return f"{self.text}"

