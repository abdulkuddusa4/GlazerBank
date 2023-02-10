class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        pass

    def __call__(self, request):

        return self.get_response(request)


