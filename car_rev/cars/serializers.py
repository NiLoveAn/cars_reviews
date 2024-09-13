from rest_framework import serializers
from .models import Country, Manufacturer, Car, Comment

class CommentSerializer(serializers.ModelSerializer):
    car_name = serializers.CharField(source='car.name', read_only=True)
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'email', 'car', 'created_at', 'comment', 'car_name']

    def validate_email(self, value):
        allowed = ['gmail.com', 'yandex.ru', 'mail.ru']
        for email in allowed:
            if value.endswith(email):
                return value
        raise serializers.ValidationError("Неверный формат email")

class CarSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacturer', 'start_year', 'end_year', 'comments', 'comment_count']

    def get_comment_count(self, obj):
        return obj.comments.count()

class ManufacturerSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)
    car_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'cars', 'car_count', 'comment_count']

    def get_car_count(self, obj):
        return obj.cars.count()

    def get_comment_count(self, obj):
        return sum(car.comments.count() for car in obj.cars.all())

class CountrySerializer(serializers.ModelSerializer):
    manufacturers = ManufacturerSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'manufacturers']