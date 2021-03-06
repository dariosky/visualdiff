from visualdiff import vd


class TestVisualDifferences:
    common_options = dict(
        # master_should_exist=True,
        save_differences=True,
    )

    def test_didnt_change(self):
        assert not vd('http://example.com',
                      **self.common_options,
                      master_path='visualdiff_masters/example_same.png',
                      )

    def test_sshot_size(self):
        assert not vd('http://example.com',
                      **self.common_options,
                      width=2048, height=2048,
                      master_path='visualdiff_masters/example_big.png',
                      )

    def test_did_change(self):
        assert vd('http://example.com',
                  **{
                      **self.common_options,
                      'master_path': 'visualdiff_masters/example_changed.png',
                      'save_differences': False,
                  })

    def test_interceptor(self):
        async def intercept_request(request):
            if 'forbidden' in request.url:
                await request.abort()
            else:
                await request.continue_()

        assert not vd('http://httpbin.org/image/webp',
                      **self.common_options,
                      request_handler_func=intercept_request,
                      master_path='visualdiff_masters/reference.png',
                      )

    def test_send_cookies(self):
        assert not vd('http://httpbin.org/cookies',
                      **self.common_options,
                      cookies=[dict(name='cookie_is_set',
                                    value='YES',
                                    url='http://httpbin.org/')],
                      master_path='visualdiff_masters/cookies.png',
                      )
