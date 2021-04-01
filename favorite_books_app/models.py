from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def create_validator(self, reqPost):
        errors = {}
        if len(reqPost['first_name']) < 2:
            errors['first_name'] = "First name must be at least 3 characters"
        if len(reqPost['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 3 characters"
        if len(reqPost['email']) < 6:
            errors['email'] = "Email must be at least 7 characters"
        if len(reqPost['password']) < 8:
            errors['password'] = "Password must be at least 9 characters"
        if reqPost['password'] != reqPost['password_conf']:
            errors['match'] = "Passwords do no match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPost['email']):
            errors['regex'] = "Email is in wrong format"
        users_with_email = User.objects.filter(email=reqPost['email'])
        if len(users_with_email) >= 1:
            errors['dep']: "Email taken, please create another one"
        return errors

class BookManager(models.Manager):
    def book_validator(self, reqPost):
        errors = {}
        if len(reqPost['book_title']) < 1:
            errors['book_title'] = "Title is required"
        if len(reqPost['book_desc']) < 5:
            errors['book_desc'] = "Description must be at least 5 characters"
        return errors


class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="uploaded_books", on_delete = models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()