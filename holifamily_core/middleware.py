class NgrokBypassMiddleware:
    """
    Sets response headers and bypasses ngrok free interstitial splash/warning page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['ngrok-skip-browser-warning'] = 'true'
        return response
