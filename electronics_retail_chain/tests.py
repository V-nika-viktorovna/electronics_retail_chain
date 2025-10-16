from django.contrib.auth.models import Group
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from users.models import User

from .models import NetworkLink, Product
from .serializers import (NetworkLinkDetailSerializer, NetworkLinkSerializer,
                          ProductSerializer)


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="test44@mail.ru", password='password', username="test44@mail.ru")
        moders_group, created = Group.objects.get_or_create(name="moders")
        self.user.groups.set([moders_group.id])
        self.product = Product.objects.create(name="Test product")
        self.client.force_authenticate(user=self.user)

    def test_list_products(self):
        response = self.client.get(reverse("electronics_retail_chain:product-list"))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve_product(self):
        response = self.client.get(reverse("electronics_retail_chain:product-detail", kwargs={"pk": self.product.pk}))
        product = Product.objects.get(pk=self.product.pk)
        serializer = ProductSerializer(product)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_product(self):
        data = {"name": "New product"}
        response = self.client.post(reverse("electronics_retail_chain:product-list"), data=data)

        self.assertEqual(response.status_code, 201)
        new_product = Product.objects.latest('id')
        self.assertEqual(new_product.name, "New product")
        self.assertEqual(new_product.created_by, self.user)

    def test_update_product(self):
        updated_data = {"name": "Updated name"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse("electronics_retail_chain:product-detail",
                                           kwargs={"pk": self.product.pk}), data=updated_data)

        self.assertEqual(response.status_code, 200)
        updated_product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(updated_product.name, "Updated name")

    def test_delete_product(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("electronics_retail_chain:product-detail",
                                              kwargs={"pk": self.product.pk}))

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=self.product.pk)


class NetworkLinkViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="test44@mail.ru", password='password', username="test44@mail.ru")
        moders_group, created = Group.objects.get_or_create(name="moders")
        self.user.groups.set([moders_group.id])
        self.network_link = NetworkLink.objects.create(name="Test link", country="USA")
        self.client.force_authenticate(user=self.user)

    def test_list_network_links(self):
        response = self.client.get(reverse("electronics_retail_chain:networklink-list"))
        links = NetworkLink.objects.all()
        serializer = NetworkLinkSerializer(links, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], serializer.data)

    def test_filtered_list_network_links(self):
        response = self.client.get(f"{reverse('electronics_retail_chain:networklink-list')}?\
                                   country={self.network_link.country}")
        filtered_links = NetworkLink.objects.filter(country=self.network_link.country)
        serializer = NetworkLinkSerializer(filtered_links, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve_network_link(self):
        response = self.client.get(reverse("electronics_retail_chain:networklink-detail",
                                           kwargs={"pk": self.network_link.pk}))
        link = NetworkLink.objects.get(pk=self.network_link.pk)
        serializer = NetworkLinkDetailSerializer(link)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_network_link(self):
        data = {"name": "New link", "country": "Canada", "level": "Завод"}
        response = self.client.post(reverse("electronics_retail_chain:networklink-list"), data=data)

        self.assertEqual(response.status_code, 201)
        new_link = NetworkLink.objects.latest('id')
        self.assertEqual(new_link.name, "New link")
        self.assertEqual(new_link.created_by, self.user)

    def test_update_network_link(self):
        updated_data = {"name": "Updated link", "country": "Mexico", "level": "Завод"}
        response = self.client.put(reverse("electronics_retail_chain:networklink-detail",
                                           kwargs={"pk": self.network_link.pk}), data=updated_data)

        self.assertEqual(response.status_code, 200)
        updated_link = NetworkLink.objects.get(pk=self.network_link.pk)
        self.assertEqual(updated_link.name, "Updated link")
        self.assertEqual(updated_link.country, "Mexico")

    def test_delete_network_link(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("electronics_retail_chain:networklink-detail",
                                              kwargs={"pk": self.network_link.pk}))

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(NetworkLink.DoesNotExist):
            NetworkLink.objects.get(pk=self.network_link.pk)
