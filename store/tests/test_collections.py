from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework import status
import pytest
from model_bakery import baker

from store.models import Collection, Product

User = get_user_model()


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.fixture
def update_collection(api_client):
    collection_queryset = baker.make(Collection)
    # baker.make(Product, collection=collection_queryset, _quantity=10)
    def do_update_collection(collection):
        return api_client.put(f'/store/collections/{collection_queryset.id}/', collection)
    return do_update_collection


@pytest.fixture
def delete_collection(api_client):
    collection_queryset = baker.make(Collection)
    def do_delete_collection(if_has_product=False):
        if if_has_product:
            baker.make(Product, collection=collection_queryset, _quantity=10)
        return api_client.delete(f'/store/collections/{collection_queryset.id}/')
    return do_delete_collection
    


@pytest.mark.django_db
class TestCreateCollection:
    """User must be authenticated and (superuser or (admin and have add_collection permission))."""


    def test_if_user_is_anonymous_return_401(self, create_collection):
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_if_user_is_not_admin_return_403(self, api_client, create_collection):
        api_client.force_authenticate(user={})
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        

    def test_if_user_does_not_have_permission_return_403(self, api_client, create_collection):
        api_client.force_authenticate(user=User(is_staff=True, id=99999))
        response =create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        

    def test_if_user_has_permission_and_data_is_invalid_return_400(self, api_client, create_collection):
        user = User.objects.create(is_staff=True, id=99999)
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get(content_type=content_type, codename='add_collection')
        user.user_permissions.add(permission)
        api_client.force_authenticate(user=user)
        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        

    def test_if_user_is_superuser_and_data_is_invalid_return_400(self, api_client, create_collection):
        api_client.force_authenticate(user=User(is_staff=True, is_superuser=True, id=99999))
        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        

    def test_if_user_is_superuser_and_data_is_valid_return_201(self, api_client, create_collection):
        api_client.force_authenticate(user=User(is_staff=True, is_superuser=True, id=99999))
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        

    def test_if_user_has_permission_and_data_is_valid_return_201(self, api_client, create_collection):
        user = User.objects.create(is_staff=True, id=99999)
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get(content_type=content_type, codename='add_collection')
        user.user_permissions.add(permission)
        api_client.force_authenticate(user=user)
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        baker.make(Product, collection=collection, _quantity=10)

        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 10,
        }


    def test_if_collections_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        baker.make(Product, collection=collection, _quantity=10)

        response = api_client.get('/store/collections/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                'id': collection.id,
                'title': collection.title,
                'products_count': 10,
            }
        ]



@pytest.mark.django_db
class TestUpdateCollection:
    """User must be authenticated and (superuser or (admin and have change_collection permission))."""


    def test_if_user_is_anonymous_return_401(self, update_collection):
        response = update_collection({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_if_user_is_not_admin_return_403(self, api_client, update_collection):
        api_client.force_authenticate(user={})
        response = update_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        

    def test_if_user_does_not_have_permission_return_403(self, api_client, update_collection):
        api_client.force_authenticate(user=User(is_staff=True, id=99999))
        response =update_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
        

    def test_if_user_has_permission_and_data_is_invalid_return_400(self, api_client, update_collection):
        user = User.objects.create(is_staff=True, id=99999)
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get(content_type=content_type, codename='change_collection')
        user.user_permissions.add(permission)
        api_client.force_authenticate(user=user)
        response = update_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        

    def test_if_user_is_superuser_and_data_is_invalid_return_400(self, api_client, update_collection):
        api_client.force_authenticate(user=User(is_staff=True, is_superuser=True, id=99999))
        response = update_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
        

    def test_if_user_is_superuser_and_data_is_valid_return_200(self, api_client, update_collection):
        api_client.force_authenticate(user=User(is_staff=True, is_superuser=True, id=99999))
        response = update_collection({'title': 'a'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0
        

    def test_if_user_has_permission_and_data_is_valid_return_200(self, api_client, update_collection):
        user = User.objects.create(is_staff=True, id=99999)
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get(content_type=content_type, codename='change_collection')
        user.user_permissions.add(permission)
        api_client.force_authenticate(user=user)
        response = update_collection({'title': 'a'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestDestroyCollection:
    """User must be authenticated and (superuser or (admin and have delete_collection permission))."""


    def test_if_user_is_anonymous_return_401(self, delete_collection):
        response = delete_collection()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        

    def test_if_user_is_not_admin_return_403(self, api_client, delete_collection):
        api_client.force_authenticate(user={})
        response = delete_collection()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        

    def test_if_user_does_not_have_permission_return_403(self, api_client, delete_collection):
        api_client.force_authenticate(user=User(is_staff=True, id=99999))
        response =delete_collection()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        

    def test_if_user_has_permission_and_collection_has_product_return_400(self, api_client, delete_collection):
        user = User.objects.create(is_staff=True, id=99999)
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get(content_type=content_type, codename='delete_collection')
        user.user_permissions.add(permission)
        api_client.force_authenticate(user=user)
        response = delete_collection(True)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        

    def test_if_user_is_superuser_and_collection_has_product_return_400(self, api_client, delete_collection):
        api_client.force_authenticate(user=User(is_staff=True, is_superuser=True, id=99999))
        response = delete_collection(True)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        

    def test_if_user_is_superuser_and_collection_has_no_product_return_204(self, api_client, delete_collection):
        api_client.force_authenticate(user=User(is_staff=True, is_superuser=True, id=99999))
        response = delete_collection()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        

    def test_if_user_has_permission_and_collection_has_no_product_return_204(self, api_client, delete_collection):
        user = User.objects.create(is_staff=True, id=99999)
        content_type = ContentType.objects.get_for_model(Collection)
        permission = Permission.objects.get(content_type=content_type, codename='delete_collection')
        user.user_permissions.add(permission)
        api_client.force_authenticate(user=user)
        response = delete_collection()

        assert response.status_code == status.HTTP_204_NO_CONTENT