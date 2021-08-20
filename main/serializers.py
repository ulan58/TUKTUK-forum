from rest_framework import serializers

from .models import Post, PostImage, Reply, Category, Comment, Rating, Likes


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'author', 'created_at', 'text',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True).data
        action = self.context.get('action')
        ReplySerializer.action = action
        if action == 'list':
            representation['replies'] = instance.replies.count()
        elif action == 'retrieve':
            representation['replies'] = ReplySerializer(instance.replies.all(), many=True).data
        return representation

    def create(self, validated_data):   # for saving imgs with postman
        request = self.context.get('request')
        images_data = request.FILES
        # print(images_data)
        post = Post.objects.create(author=request.user, **validated_data)
        for image in images_data.getlist('images'):
            PostImage.objects.create(image=image,
                                     problem=post)
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            PostImage.objects.create(
                image=image,
                post=instance
            )
        return instance


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    class Meta:
        model = Reply
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)
        action = self.action
        # print("Reply", action)
        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(
                instance.comments.all(), many=True
            ).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
        )
        return reply


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user,
            **validated_data
        )
        return comment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        # print("Comment", action)
        if action == 'list':
            representation['inner_comments'] = instance.comments.count()
        return representation


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'posts')

    def create(self, validated_data):
        request = self.context.get('request')
        rating, user = Rating.objects.update_or_create(
            posts=validated_data.get('posts', None),
            author=request.user,
            star=validated_data.get("star", None)
        )
        return rating


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        ads = validated_data.get('liked_posts')

        if Likes.objects.filter(author=user, liked_posts=ads):
            return Likes.objects.get(author=user, liked_posts=ads)
        else:
            return Likes.objects.create(author=user, liked_posts=ads)
