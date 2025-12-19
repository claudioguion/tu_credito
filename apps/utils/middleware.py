

class ApiSecurityMiddleware:
    """
    We're hadling both CSP and Permissions Policy together.
    Both can be easily adjusted in here.
    This should only affect the '/api/' endpoints. Admin should be fine.
    I'm taking this approach because it's cleaner than CSP library.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith("/api/docs"):
            # Creating a condition on CSP so that /api/docs can render properly
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
            )
        elif request.path.startswith("/api/"):
            # Content Security Policy
            response["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self'; "
                "img-src 'self' data:; "
                "connect-src 'self'; "
                "font-src 'self'; "
                "frame-src 'none';"
            )

            # Permissions Policy
            response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        return response
