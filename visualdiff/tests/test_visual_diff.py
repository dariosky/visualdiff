import os

from visualdiff import vd

base_master_path = os.path.abspath(os.path.dirname(__file__))


class TestVisualDifferences:

    def test_didnt_change(self):
        assert not vd('http://example.com',
                      master_path=os.path.join(
                          base_master_path,
                          'visualdiff_masters/example_same.png'
                      ))

    def test_did_change(self):
        assert vd('http://example.com',
                  master_path=os.path.join(
                      base_master_path,
                      'visualdiff_masters/example_changed.png'
                  ))

    def test_interceptor(self):
        async def intercept_request(request):
            print(request.url)
            if 'forbidden' in request.url:
                await request.abort()
            else:
                await request.continue_()

        assert not vd('https://dbaron.org/dom/test/',
                      request_handler_func=intercept_request,
                      master_path=os.path.join(
                          base_master_path,
                          'visualdiff_masters/dbaron_org.png'
                      )
                      )
