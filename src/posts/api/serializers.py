from rest_framework import serializers 
from accounts.api.serializers import UserSerializer
from posts.models import Post
from django.core.urlresolvers import reverse
from django.utils.timesince import timesince

class PostModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) #write_only
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'title',
            'timestamp',
            'image',
            'date_display',
            'timesince',
            'url',
            'likes',
            'comments',
           
        ]

    def get_comments(self, obj):
        return obj.comments.all().count()

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_url(self, obj):
        return reverse("posts:detail", kwargs={"slug": obj.slug})

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

