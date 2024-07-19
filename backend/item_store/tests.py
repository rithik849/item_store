from django.test import TestCase
from rest_framework.test import APITestCase, APIClient, api_settings
import math

from item_store.models import Customer, Review
from products.models import Product

# Create your tests here.


class ReviewTestCase(APITestCase):
    fixtures = [
        "products/fixtures/products.json",
        "item_store/fixtures/basket.json",
        "item_store/fixtures/customer.json",
        "item_store/fixtures/ordernumber.json",
        "item_store/fixtures/order.json",
        "item_store/fixtures/review.json"
    ]
    
    @classmethod
    def setUpClass(cls):
        super(ReviewTestCase,cls).setUpClass()
        user,val = Customer.objects.get_or_create(username='test', email='testuser@testuser.com')
        user.set_password('testpassword123')
        # Remember to save the model to the database
        user.save()
        cls.user = user

        
    # 403 is unauthorised
        
    def setUp(self):
        self.client = APIClient()
        product = Product.objects.get(name="Pen")
        review,t = Review.objects.get_or_create(customer=self.user,product=product,rating=3,comment="This is a good pen.")
        review.save()
    
    def tearDown(self):
        self.client.logout()
        
    def test_get_reviews(self):
        PAGE_SIZE : int = api_settings.PAGE_SIZE # type: ignore
        review_count = Review.objects.all().count()
        page_count = math.ceil(review_count/PAGE_SIZE)
        last_page_review_count = review_count%PAGE_SIZE
        
        for i in range(1,page_count):
            response = self.client.get("/reviews/?page="+str(i))
            assert(response.status_code==200)
            body = response.json()
            assert(len(body['results'])==PAGE_SIZE)
            
        response = self.client.get("/reviews/?page="+str(page_count))
        assert(response.status_code==200)
        body = response.json()
        assert(len(body['results'])==last_page_review_count)
    
    def test_get_review(self):
        product : Product = Product.objects.get(name="Pen")
        response = self.client.get("/reviews/test/"+str(product.id)+"/") #type: ignore
        body = response.json()
        assert(response.status_code==200)
        assert(body['customer']['username'] == 'test')
        assert(body['product']['id'] == product.id) # type: ignore

    def test_create_review(self):
        # Check unauthenticated users cannot create reviews
        product : Product = Product.objects.get(name="Book")
        response = self.client.post("/reviews/",data={"customer":self.user.id, "product" : product.id, "rating" : 3, "comment" : "Test review"}) # type: ignore
        assert(response.status_code==403)
        
        # Check creating a review
        authenticated = self.client.login(username='test',password='testpassword123')
        assert(authenticated==True)
        response = self.client.post("/reviews/",data={"customer":self.user.id, "product" : product.id, "rating" : 3, "comment" : "Test review"}) # type: ignore
        assert(response.status_code==200)
        
        # Check we can only have one review per product for a given user
        response = self.client.post("/reviews/",data={"customer":self.user.id, "product" : product.id, "rating" : 3, "comment" : "Test review"}) # type: ignore
        assert(response.status_code==400)
    
    def test_destroy_review(self):
        pen : Product = Product.objects.get(name="Pen")
        # Test only authenticated users can delete reviews
        response = self.client.delete(f"/reviews/{self.user.username}/{pen.id}/") # type: ignore
        assert(response.status_code==403)
        # Test we can delete a review
        self.client.login(username='test',password='testpassword123')
        response = self.client.delete(f"/reviews/{self.user.username}/{pen.id}/") # type: ignore
        assert(response.status_code==200)
        # Test we can only delete our own review
        response = self.client.delete(f"/reviews/rithik/2/") # type: ignore
        body = response.json()
        assert(response.status_code==403)
        assert(body['detail']=="You do not have permission to perform this action.")