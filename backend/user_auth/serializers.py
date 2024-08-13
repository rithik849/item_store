from django.contrib.auth.hashers import make_password
from rest_framework import routers, serializers, viewsets
from item_store.models import Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password as default_password_validation

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
        exclude = ['password']
        
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
        # for attr,value in validated_data.items():
        #     instance[attr] = value
        instance.username = validated_data.get('username',instance.username)
        instance.email = validated_data.get('email',instance.email)
        instance.save()
        return instance
    
class UpdatePasswordSerializer(BaseSerializer):
    queryset = Customer.objects.all()
    password = serializers.CharField(max_length=255,required=True, validators=[default_password_validation]
                                         , error_messages = {"required" : "Password is unspecified", "blank": "Password can not be blank."}
                                         )
    confirm_password = serializers.CharField(max_length=255,required=True
                                             , error_messages = {"required" : "Confirm Password is unspecified", "blank": "Confirm Password can not be blank."}
                                             )
    
    class Meta:
        model = Customer
        fields = ['password', 'confirm_password']
        extra_kwargs = {
            "password": {"error_messages" : {"required" : "Password is unspecified", "blank": "Password can not be blank."}},
            "confirm_password": {"error_messages" : {"required" : "Confirm password is unspecified", "blank": "Confirm password can not be blank."}}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def update(self, instance : Customer, validated_data):
        instance.password = make_password(validated_data['password'])
        instance.save()
        return instance
    
    
class LogInSerializer(BaseSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    class Meta:
        model = Customer
        fields = ['username','password']
    
    # def validate(self, attrs):
    #     user_obj = None
    #     username = attrs['username']
    #     password = attrs['password']
    #     if username and password:
    #         try:
    #             user_obj = Customer.objects.get(username=username)
    #             if not user_obj.check_password(password):
    #                 raise Exception
    #         except:
    #             raise serializers.ValidationError('Incorrect username or password')
        # return attrs
    
class SignUpSerializer(BaseSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Customer.objects.all(),message='Username already in use. Please choose another username.')]
    )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Customer.objects.all(),message='An account with this email already exists. Please choose another email.')]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[default_password_validation])
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
