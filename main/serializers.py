from rest_framework import serializers

from .models import Car, CarImage, Comment, Brand


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ('image', )

    def _get_image_url(self, instance):
        if instance.image:
            url = instance.image.url
            return 'localhost:8000' + url

    def to_representation(self, instance):
        representation = super(CarImageSerializer, self).to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class CarSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES
        author = request.user
        car = Car.objects.create(author=author, **validated_data)
        for image in images.getlist('images'):
            CarImage.objects.create(image=image, car=car)
        return car

    def update(self, instance, validated_data):
        request = self.context.get('request')
        images = request.FILES
        for key,val in validated_data.items():
            setattr(instance, key, val)
        if images.getlist('new_images'):
            instance.images.all().delete()
            for image in images.getlist('new_images'):
                CarImage.objects.create(image=image, car=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = CarImageSerializer(instance.images.all(), many=True).data
        # representation['likes'] = instance.likes.count()
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.comments.count()
        else:

            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        author = self.context.get('request').user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment
    #
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['likes'] = instance.likes.count()
    #     return representation


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'

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
        represantation = super().to_representation(instance)
        represantation['image'] = self._get_image_url(instance)
        return represantation


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'



