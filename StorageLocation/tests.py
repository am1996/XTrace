from django.test import TestCase
from StorageLocation.models import StorageLocation
# Create your tests here.

# Test cases for StorageLocation views and models will be added here

class StorageLocationModelTest(TestCase):
    def setUp(self):
        # Set up a StorageLocation instance for testing
        self.storage_location = StorageLocation.objects.create(
            name="Test Storage Location",
            gln="12431a2345678",
            sub_location="Bin A1",
            location_type="physical",
            address="123 Test Street, Test City",
            is_active=True
        )

    def test_storage_location_creation(self):
        # Test that the StorageLocation instance was created successfully
        self.assertEqual(self.storage_location.name, "Test Storage Location")
        self.assertEqual(self.storage_location.gln, "12431a2345678")
        self.assertEqual(self.storage_location.sub_location, "Bin A1")
        self.assertEqual(self.storage_location.location_type, "physical")
        self.assertEqual(self.storage_location.address, "123 Test Street, Test City")
        self.assertEqual(self.storage_location.is_active, True)

class StorageLocationViewTest(TestCase):
    def setUp(self):
        # Set up a StorageLocation instance for testing views
        self.storage_location = StorageLocation.objects.create(
            name="Test Storage Location",
            gln="12431a2345678",
            sub_location="Bin A1",
            location_type="physical",
            address="123 Test Street, Test City",
            is_active=True
        )

    def test_storage_location_index_view(self):
        # Test the index view for StorageLocation
        response = self.client.get('/web/storage_location/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Storage Location")

    def test_storage_location_details_view(self):
        # Test the details view for StorageLocation
        response = self.client.get(f'/web/storage_location/{self.storage_location.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Storage Location")




