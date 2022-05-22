from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(sum('post_rating')) * 3
        comment_rating = self.comment_set.all().aggregate(sum('comment_rating'))
        news_comment_rating = Post.objects.filter(author=self).values('comments__comment_rating')
        self.user_rating = post_rating + comment_rating + news_comment_rating
        self.save

        return f'{self.user_rating}'


class Category(models.Model):
    category_names = models.CharField(max_length=255, unique=True)


article = "AT"
news = "NW"

POST_TYPE = [
    (article, "Статья"),
    (news, "Новости"),
]


class Post(models.Model):

    news_type = models.CharField(
        max_length=2,
        choices=POST_TYPE,
        default=article)
    creation_date = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=225)
    post_text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        preview_text = 124 if len(self.post_text) > 124 else len(self.post_text)
        return self.post_text[:preview_text]+'...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
