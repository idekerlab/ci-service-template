import unittest


class TestBaseService(unittest.TestCase):
    def test_say_hello(self):
        from ..apiv1.services.hello import HelloService

        data = {
            'name': 'John Doe'
        }

        result = HelloService.say_hello(data)
        message = result['message']
        self.assertIsNotNone(message)
        self.assertEqual(message, 'Hello John Doe!')
