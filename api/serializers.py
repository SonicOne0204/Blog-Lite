from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from api.models import Post, SubPost


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user


class SubPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPost
        fields = ["title", "body", "post"]


class SubPostForPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPost
        fields = ["title", "body"]


class PostSerializer(serializers.ModelSerializer):
    subposts = SubPostForPostSerializer(many=True)
    likes = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "subposts", "likes", "views_count"]

    def create(self, validated_data):
        user = self.context["request"].user
        subposts_data = validated_data.pop("subposts", [])

        validated_data["author"] = user
        with transaction.atomic():
            post = Post.objects.create(**validated_data)

            for subpost_data in subposts_data:
                SubPost.objects.create(post=post, author=user, **subpost_data)

        return post

    def update(self, instance, validated_data):
        subposts_data = validated_data.pop("subposts", [])

        with transaction.atomic():
            for field in self.fields:
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
            instance.save()

            existing_ids = [sub.id for sub in instance.subposts.all()]
            sent_ids = []

            for subpost_data in subposts_data:
                subpost_id = subpost_data.get("id")
                if subpost_id and subpost_id in existing_ids:
                    subpost_data.pop("id")
                    subpost = SubPost.objects.get(id=subpost_id, post=instance)
                    for key, value in subpost_data.items():
                        setattr(subpost, key, value)
                    subpost.save()
                    sent_ids.append(subpost_id)
                else:
                    subpost = SubPost.objects.create(
                        post=instance, author=instance.author, **subpost_data
                    )
                    sent_ids.append(subpost.id)

            for subpost in instance.subposts.all():
                if subpost.id not in sent_ids:
                    subpost.delete()

        return instance
