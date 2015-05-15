import unittest


class TestBaseService(unittest.TestCase):

    def setUp(self):
        from api_v1.resource_base import BaseResource
        self.service = BaseResource()

    def test_get(self):
        get_result = self.service.get()
        self.assertIsNotNone(get_result)
        self.assertEqual(get_result[1], 200)
        print(get_result[0])
        message = get_result[0]['message']
        self.assertIsNotNone(message)

    def __dummy_function(self):
        pass

    def test_submit(self):
        data = {}
        # TODO Add redis mock for testing
        # self.service.submit(self.__dummy_function, data, result_type=RESULT_FILE)
