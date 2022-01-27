from datetime import date, datetime
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    
    def validate(self, form):
        errors = {}
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length = 45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()

class GameManager(models.Manager):
    def game_validator(self, postData):
        errors = {}
        print(postData)
        if len(postData['title']) < 1:
                errors['title'] = "Game title must be entered"
        if len(postData['image']) < 1:
            errors['image'] = "image URL must be entered"
        if len(postData['release']) < 1:
            errors['release'] = "release date must be entered"
        if len(postData['description']) < 1:
                errors['description'] = "description must be entered"

        return errors

class Game(models.Model):

    title = models.CharField(max_length=255)
    image = models.ImageField(null = True, blank = True)
    release = models.DateField(datetime)
    description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = GameManager()


rating_choices = (
    ('1','1'),
    ('2', '2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
)

class Review(models.Model):
    creator = models.ForeignKey(User, related_name="has_created_reviews", on_delete=models.CASCADE)
    rating = models.CharField(max_length=6, choices=rating_choices, default='5', null=True)
    review = models.TextField()
    game_review = models.ForeignKey(Game, related_name="game_review", on_delete = models.CASCADE)

