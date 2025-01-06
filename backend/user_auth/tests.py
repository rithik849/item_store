
from django.contrib.auth.hashers import make_password
from django.test import TransactionTestCase, TestCase, Client
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, api_settings, RequestsClient
from rest_framework.viewsets import reverse
from item_store.models import Customer
from django.contrib.auth import get_user
# Create your tests here.

class CustomerAuthTestCase(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super(CustomerAuthTestCase,cls).setUpClass()
        cls.user,val = Customer.objects.get_or_create(username='test', email='testuser@testuser.com')
        cls.user.set_password('testpassword123')
        cls.id = cls.user.id # type: ignore
        # Remember to save the model to the database
        cls.user.save()
        
        user = Customer.objects.create(username='user2' , email='johndoe@gmail.com')
        user.save()
        
        
    def setUp(self):
        self.client = APIClient()
        pass
    
    def tearDown(self):
        self.client.logout()
        pass

    def test_logout_view_access_not_authenticated(self):
        response = self.client.post('/customers/logout/',data = None)
        assert(response.status_code==403)  # type: ignore
    
    def test_logout_view_authenticated(self):
        val= self.client.login(username='test',password='testpassword123')
        response = self.client.post('/customers/logout/', data = None)
        assert(response.status_code==200) # type: ignore
        self.client.logout()
    
    
    def test_login_view_access_not_authenticated(self):
        response = self.client.post('/customers/login/', data={'username':'test', 'password':'testpassword123'}, format='json')
        assert(response.status_code==200)
        self.client.logout()
        
    def test_login_view_access_authenticated(self):
        val = self.client.login(username='test',password='testpassword123')
        assert(val==True)
        response = self.client.post('/customers/login/', data={'username':'test', 'password':'testpassword123'}, format='json')
        self.client.logout()
    
    def test_login_view_wrong_credentials(self):
        response = self.client.post('/customers/login/', data={'username':'test_wrong_username', 'password':'testpassword123'}, format='json')
        assert(response.status_code==401)
        response = self.client.post('/customers/login/', data={'username':'test', 'password':'test_wrong_password'}, format='json')
        assert(response.status_code==401)
        response = self.client.post('/customers/login/', data={'username':'test_wrong_username', 'password':'test_wrong_password'}, format='json')
        assert(response.status_code==401)
    
    def test_change_details_view(self):
        val = self.client.login(username='test',password='testpassword123')
        response = self.client.post('/customers/change-details/', data= {'username' : 'user2'})
        assert(response.status_code==400)
        response = self.client.post('/customers/change-details/', data= {'username' : 'user3'})
        assert(response.status_code==200)
        self.user = Customer.objects.get(id=self.id)
        assert(self.user.username=='user3')
        response = self.client.post('/customers/change-details/', data= {'email' : 'johndoe@gmail.com'})
        assert(response.status_code==400)
        response = self.client.post('/customers/change-details/', data= {'email' : 'user3@gmail.com'})
        assert(response.status_code==200)
        self.user = Customer.objects.get(id=self.id)
        assert(self.user.email=='user3@gmail.com')
        response = self.client.post('/customers/change-details/', data= {'username' : 'test', 'email' : 'testuser@testuser.com'})
        self.user = Customer.objects.get(id=self.id)
        assert(self.user.email=='testuser@testuser.com' and self.user.username=='test')
    
    def test_change_password_view(self):
        val = self.client.login(username='test',password='testpassword123')
        new_password = 'newpassword123'
        response = self.client.patch('/customers/change-password/', data= {'password' : new_password, 'confirm_password' : new_password})
        self.client.logout()
        val = self.client.login(username='test',password=new_password)
        assert(val==True)
        
    def test_change_password_invalid_view(self):
        val = self.client.login(username='test',password='testpassword123')
        new_password = 'newpassword123'
        response = self.client.patch('/customers/change-password/', data= {'password' : new_password, 'confirm_password' : 'differemt'})
        assert(response.status_code == 400)
        self.client.logout()
        val = self.client.login(username='test',password=new_password)
        assert(val==False)
        
    def test_signup_view(self):
        create_user = {
            'username' : 'newuser',
            'email' : 'newuser@gmail.com',
            'password' : 'newpassword123',
            'password2' : 'newpassword123'
        }
        response = self.client.post('/customers/register/', data = create_user )
        json = response.json()
        assert(response.status_code==200)
        assert(Customer.objects.filter(username=create_user['username']).exists() == True)
        user = get_user(self.client)
        assert(user.is_authenticated==True)
        assert(json['user']['username'] == create_user['username'])
        assert(json['user']['email'] == create_user['email'])
        self.client.logout()
        
        create_user_invalid = {
            'username' : 'newuser',
            'email' : 'newuser@gmail.com',
            'password' : 'newpassword123',
            'password2' : 'newpassword'
        }
        response = self.client.post('/customers/register/', data = create_user_invalid )
        assert(response.status_code!=200)
        user = get_user(self.client)
        assert(user.is_authenticated==False)