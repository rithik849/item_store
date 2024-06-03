from rest_framework import routers, serializers, viewsets
from item_store.models import Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# # Serializers define the API representation.
# class CustomerTokenPairSerializer(TokenObtainPairSerializer):
#     class Meta:
#         model = Customer
#         fields = ['url', 'username', 'email', 'password']
    
#     @classmethod
#     def get_token(cls, user : Customer):
#         token = super(CustomerTokenPairSerializer, cls).get_token(user)
#         token['username'] = user.username
#         token['email'] = user.email
#         return token
    
# class CustomerTokenRefreshSerializer(TokenRefreshSerializer):
#     class Meta:
#         model = Customer
#         fields = ['url', 'username', 'email', 'password']

class BaseSerializer(serializers.ModelSerializer):
    queryset=Customer.objects.all()
    class Meta:
        model = Customer
        fields = ['username','email','password']
        
class UpdateDetailsSerializer(BaseSerializer):
    queryset = Customer.objects.all()
    
    class Meta:
        model = Customer
        fields = ['username','email']
        
    def validate_username(self, value):
        instance : Customer = self.instance # type: ignore
        if value == instance.username:
            return value
        elif self.queryset.filter(username=value).exists():
            raise serializers.ValidationError('username '+str(value)+' already exists')
        return value
        
    def validate_email(self,value):
        instance : Customer = self.instance # type: ignore
        if value == instance.email:
            return value
        elif self.queryset.filter(email=value).exists():
            raise serializers.ValidationError('email '+str(value)+' already exists')
        return value
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            instance[attr] = value
        instance.save()
        return instance
    
class UpdatePasswordSerializer(BaseSerializer):
    queryset = Customer.objects.all()
    new_password = serializers.CharField(max_length=255,required=True)
    confirm_password = serializers.CharField(max_length=255,required=True)
    
    class Meta:
        model = Customer
        fields = ['new_password', 'confirm_password']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def update(self, instance, validated_data):
        for attr,value in validated_data.items():
            instance[attr] = value
        instance.save()
        return instance
    
    
class LogInSerializer(BaseSerializer):
    email = serializers.EmailField()
    
    class Meta:
        model = Customer
        fields = ['email','password']
    
    def validate(self, attrs):
        print(attrs)
        user_obj = None
        email = attrs['email']
        password = attrs['password']
        if email and password:
            user_obj = Customer.objects.get(email=email)
            if (not user_obj) or (not user_obj.check_password(password)):
                raise serializers.ValidationError('Incorrect email or password')
        return attrs
    
class SignUpSerializer(BaseSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Customer.objects.all(),message='Username already in use. Please choose another username.')]
    )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Customer.objects.all(),message='An account with this email already exists. Please choose another email.')]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Customer
        fields = ['username','email','password','password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        
        user = Customer.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
