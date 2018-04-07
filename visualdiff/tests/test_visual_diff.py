import os
from pathlib import Path

from visualdiff import vd

here = Path(os.path.abspath(os.path.dirname(__file__)))


class TestVisualDifferences:

    def test_didnt_change(self):
        assert not vd('http://example.com',
                      master_path=here / 'visualdiff_masters/example_same.png'
                      )

    def test_sshot_size(self):
        assert not vd('http://example.com',
                      width=2048, height=2048,
                      master_path=here / 'visualdiff_masters/example_big.png'
                      )

    def test_did_change(self):
        assert vd('http://example.com',
                  master_path=here / 'visualdiff_masters/example_changed.png'
                  )

    def test_interceptor(self):
        async def intercept_request(request):
            print(request.url)
            if 'forbidden' in request.url:
                await request.abort()
            else:
                await request.continue_()

        assert not vd('https://dbaron.org/dom/test/',
                      request_handler_func=intercept_request,
                      master_path=here / 'visualdiff_masters/dbaron_org.png'
                      )
