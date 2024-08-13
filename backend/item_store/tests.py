from django.test import TestCase
from rest_framework.test import APITestCase, APIClient, api_settings
import math
from datetime import date

from item_store.models import Basket, Customer, Order, OrderNumber, Review
from products.models import Product

# Create your tests here.

def assert_print(req,cond):
    if not cond:
        print(req.status_code,req.json())
    assert(cond)

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
        
    def test_get_reviews_by_product(self):
        product : Product = Product.objects.get(name="Pen")
        response = self.client.get("/reviews/"+str(product.id)+"/") #type: ignore
        body = response.json()
        assert(response.status_code==200)
        assert(body['count']==3)
        
        PAGE_SIZE : int = api_settings.PAGE_SIZE # type: ignore
        page_count = math.ceil(body['count']/PAGE_SIZE)
        last_page_review_count = body['count']%PAGE_SIZE
        
        for i in range(1,page_count):
            response = self.client.get("/reviews/"+str(product.id)+"/?page="+str(i)) #type: ignore
            assert(response.status_code==200)
            body = response.json()
            body = body['results']
            assert(len(body)==PAGE_SIZE)
            for item in range(PAGE_SIZE):
                assert(body[0]['product']['id']==product.id) # type: ignore
                
            
        response = self.client.get("/reviews/"+str(product.id)+"/?page="+str(page_count)) # type: ignore
        assert(response.status_code==200)
        body = response.json()
        body = body['results']
        assert(len(body)==last_page_review_count)
        for item in range(last_page_review_count):
            assert(body[0]['product']['id']==product.id) # type: ignore

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
        
class BasketTestCase(APITestCase):
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
        super(BasketTestCase,cls).setUpClass()
        user = Customer.objects.get(username='test', email='testuser@testuser.com')
        user.set_password('testpassword123')
        # Remember to save the model to the database
        user.save()
        cls.user = user
        cls.client = APIClient()
        cls.customer_id = user.id # type: ignore
        
    def setUp(self):
        self.client.login(username='test',password='testpassword123')
        
    def tearDown(self):
        self.client.logout()
        
    def test_list_basket_items(self):
        response = self.client.get("/baskets/")
        body = response.json()
        items = list(Basket.objects.filter(customer__username='test'))
        for i,basket_item in enumerate(body['results']):
            assert(basket_item['customer']==self.customer_id)
            url = basket_item['product']
            response = self.client.get(url)
            product = response.json()
            assert(product['id'] == items[i].product.id) # type: ignore
    
    def test_get_basket_item(self):
        product_id = 3
        response = self.client.get(f"/baskets/{product_id}/")
        item = Basket.objects.get(customer__username="test", product_id=product_id)
        json = response.json()
        assert(json['id']==item.id) # type: ignore
        assert(json['customer']['username']==item.customer.username)
        assert(json['quantity']==item.quantity)
        assert(json['product']['id']==item.product.id) # type: ignore
        
    def test_add_item_to_basket_with_invalid_quantity(self):
        request_json = {
            'product' : 2,
            'quantity' : 0
        }
        response = self.client.post(f"/baskets/", data = request_json)
        assert(response.status_code==500)
        
    def test_add_new_item_to_basket(self):
        request_json = {
            'product' : 2,
            'quantity' : 4
        }
        response = self.client.post(f"/baskets/", data = request_json)
        assert(response.status_code==200)
        json = response.json()
        assert(json['success']==True)
        item : Basket = Basket.objects.get(customer=self.user , product__id=request_json['product'])
        assert(item.quantity == request_json['quantity'])
        
    def test_add_current_item_to_basket(self):
        request_json = {
            'product' : 3,
            'quantity' : 4
        }
        response = self.client.post(f"/baskets/", data = request_json)
        assert(response.status_code==200)
        json = response.json()
        assert(json['success']==True)
        
    def test_add_current_item_to_basket_above_stock(self):
        request_json = {
            'product' : 1,
            'quantity' : 461
        }
        response = self.client.post(f"/baskets/", data = request_json)
        product = Product.objects.get(id = 1)
        assert(response.status_code==400)
        json = response.json()
        assert(json['non_field_errors'][0]=="Not enough of product Book in stock")
        assert(product.stock == 460)
        
    def test_delete_item_from_basket(self):
        product_id = 1
        response = self.client.delete(f"/baskets/{product_id}/")
        assert(response.status_code==200)
        json = response.json()
        assert(json['success'] == True)
        assert(json['detail'] == "Item removed from basket")
        assert(Basket.objects.filter(product__id = 1).exists()==False)
        
    def test_delete_non_existent_item_from_basket(self):
        product_id = 2
        response = self.client.delete(f"/baskets/{product_id}/")
        assert(response.status_code==404)
        json = response.json()
        assert(json['detail'] == "No Basket matches the given query.")
        
    def test_empty_basket(self):
        response = self.client.delete(f"/baskets/")
        assert_print(response, response.status_code==200)
        json = response.json()
        assert_print(response, json['detail'] == "All items removed from basket")
        assert(Basket.objects.filter(customer__username='test').exists()==False)
    
    def test_increase_current_item_in_basket(self):
        request_json = {
            "quantity" : 6
        }
        product_id = 3
        
        response = self.client.patch(f"/baskets/{product_id}/", data = request_json)
        assert(response.status_code==200)
        json = response.json()
        assert(json['detail']=="Product pencil quantity increased")
        assert(Basket.objects.get(customer__username='test', product__id=product_id).quantity==6)
    
    def test_decrease_current_item_in_basket(self):
        
        request_json = {
            "quantity" : 4
        }
        product_id = 3
        
        response = self.client.patch(f"/baskets/{product_id}/", data = request_json)
        assert(response.status_code==200)
        json = response.json()
        assert(json['detail']=="Product pencil quantity decreased")
        assert(Basket.objects.get(customer__username='test', product__id=product_id).quantity==4)
        
    def test_remove_negative_amount_from_basket(self):
        request_json = {
            "quantity" : -1
        }
        product_id = 3
        
        response = self.client.patch(f"/baskets/{product_id}/", data = request_json)
        assert(response.status_code==400)
        json = response.json()
        assert(json['non_field_errors'][0]=="Can not have a negative quantity of an item.")
        
    def test_remove_all_of_current_item_in_basket(self):
        request_json = {
            "quantity" : 0
        }
        product_id = 3
        
        response = self.client.patch(f"/baskets/{product_id}/", data = request_json)
        assert(response.status_code==200)
        json = response.json()
        
        assert_print(response,json['detail']=="Product pencil quantity decreased")
        assert(Basket.objects.filter(customer__username='test', product__id=product_id).exists()==False)
        
    def test_keep_current_item_quantity_in_basket(self):
        request_json = {
            "quantity" : 5
        }
        product_id = 3
        
        response = self.client.patch(f"/baskets/{product_id}/", data = request_json)
        assert(response.status_code==200)
        json = response.json()
        assert(json['detail']=="Product pencil quantity unchanged")
        assert(Basket.objects.get(customer__username='test', product__id=product_id).quantity==5)
        
class OrderTestCase(APITestCase):
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
        super(OrderTestCase,cls).setUpClass()
        user = Customer.objects.get(username='test', email='testuser@testuser.com')
        user.set_password('testpassword123')
        # Remember to save the model to the database
        user.save()
        
        cls.user = user
        cls.client = APIClient()
        cls.customer_id = user.id # type: ignore
        
    def setUp(self):
        self.client.login(username='test',password='testpassword123')
        
    def tearDown(self):
        self.client.logout()
        
    def test_view_orders(self):
        response = self.client.get("/orders/")
        json = response.json()['results']
        orders = list(OrderNumber.objects.filter(customer__username='test').order_by("-date"))
        assert(len(json) == 2)
        for i in range(len(json)):
            assert(json[i]['date'] == str(orders[i].date))
            assert(json[i]['customer']['username']==orders[i].customer.username) # type: ignore
    
    def test_view_order(self):
        date = "2024-06-21"
        order_number = 17
        response = self.client.get(f"/orders/{date}/{order_number}/")
        json = response.json()
        json = json['results']
        items = list(Order.objects.filter(order_number=order_number))
        
        for i,item in enumerate(json):
            assert(item['order_number'] == order_number)
            assert(item['product']['id'] == items[i].product.id) # type: ignore
            assert(item['quantity'] == items[i].quantity)
            
    
    def test_make_order(self):
        basket_items = list(Basket.objects.filter(customer__username='test').order_by("product__id"))
        prev_stock = [item.product.stock for item in basket_items]
        response = self.client.post("/orders/")
        d = date.today()
        assert(response.status_code==200)
        
        order_number = OrderNumber.objects.get(date=d)
        assert(str(order_number.date) == str(d))
        
        orders = list(Order.objects.filter(order_number = order_number).order_by("product__id"))
        
        for i, item in enumerate(orders):
            assert(basket_items[i].product.id == orders[i].product.id) # type: ignore
            assert(orders[i].product.stock == (prev_stock[i] - orders[i].quantity))
            
        assert(Basket.objects.filter(customer__username='test').count()==0)
        
    def test_make_invalid_order(self):
        basket_before = Basket.objects.filter(customer__username='test').order_by("product__id")
        book = basket_before.get(product__name="Book")
        book.quantity = 500
        book.save()
        pen = Basket(
            customer = Customer.objects.get(username="test"),
            product = Product.objects.get(name="Pen"),
            quantity = 1000
        )
        pen.save()
        prev_stock = [item.product.stock for item in basket_before]
        order_count_before = OrderNumber.objects.filter(customer__username = "test").count()
        response = self.client.post("/orders/")
        assert(response.status_code==500)
        json = response.json()
        assert(len(json) == 2)
        assert("Not enough of Book in stock" in json)
        assert("Not enough of Pen in stock" in json)
        
        basket_after = list(Basket.objects.filter(customer__username='test').order_by("product__id"))
        # Make sure product stock stays the same
        for i, item in enumerate(basket_after):
            assert(basket_after[i].product.stock == basket_before[i].product.stock)
            
        assert(len(basket_after)==basket_before.count())
            
        
        