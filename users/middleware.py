from django.utils import timezone


class LastVisitedPageMiddleware:
    """
    Stores the last meaningful page visited by an authenticated user.
    """

    EXCLUDED_PATHS = (
        "/logout/",
        "/signup/",
        "/password-reset/",
        "/admin/",
        "/static/",
        "/media/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if (
            request.user.is_authenticated
            and request.method == "GET"
            and not any(request.path.startswith(path) for path in self.EXCLUDED_PATHS)
        ):

            request.session["last_page"] = {
                "url": request.get_full_path(),
                "context": request.resolver_match.view_name if request.resolver_match else "",
                "timestamp": timezone.now().isoformat(),
            }

        return self.get_response(request)