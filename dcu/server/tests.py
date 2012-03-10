from django.test import TestCase
import module_loader

class ModuleLoaderTest(TestCase):
    def test(self):
        """
        Test return False if not errors.
        """
        self.assertEqual(module_loader.test("homer", 1), False)
