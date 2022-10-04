from locust import HttpUser, between, task
from random import randint
from uuid import uuid4


class WebsiteUser(HttpUser):
    wait_time = between(2, 5)

    @task(2)
    def view_products(self):
        id = randint(2, 6)
        self.client.get(f'/store/products/?collection_id={id}', name='store/products')

    
    @task(4)
    def view_product(self):
        id = randint(1, 1000)
        self.client.get(f'/store/products/{id}/', name='/store/products/:id')


    @task(1)
    def add_to_cart(self):
        id = randint(1, 10)
        quantity = randint(3, 15)
        self.client.post(f'/store/carts/{self.cart_id}/items/', name='/store/carts/items', json={
            'product': id,
            'quantity': quantity,
        })

    
    @task(2)
    def users_me(self):
        self.client.get('/auth/users/me/', name='/auth/users/me', headers=self.headers)

    
    @task(1)
    def refresh_token(self):
        response = self.client.post('/auth/jwt/refresh/', name='/auth/jwt/refresh', json={
            'refresh': self.refresh
        })
        result = response.json()
        access = result['access']
        self.headers = {
            'Authorization': f'JWT {access}'
        }

    
    # @task(1)
    # def place_order(self):
    #     response = self.client.post('/store/orders/', name='/store/orders', json={
    #         'cart_id': self.cart_id,
    #     })
    #     if response.status == 400:
    #         pass
        


    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']

        # Register
        user = {
            'username': str(uuid4()),
            'password': str(uuid4()),
        }
        self.client.post('/auth/users/', name='/auth/store', json=user)
        response = self.client.post('/auth/jwt/create/', name='/auth/jwt/create', json=user)
        result = response.json()
        self.refresh = result['refresh']
        access = result['access']
        self.headers = {
            'Authorization': f'JWT {access}'
        }