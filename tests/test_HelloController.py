
if __name__ == '__main__':
    from.HttpTestCase import HttpTestCase
else:
    from HttpTestCase import HttpTestCase


class TestHelloController(HttpTestCase):
    def test_homepage(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertTrue('"message": "pong"' in str(response.body))
