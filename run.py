from werkzeug.middleware.proxy_fix import ProxyFix

from app import create_app

app = create_app()


class PrefixMiddleware:
    """Honors an X-Forwarded-Prefix header set by a reverse proxy that mounts
    this app under a subpath (e.g. refreshinc.org/labs), so url_for() generates
    correctly-prefixed links. No-op when the header is absent (local dev)."""

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        prefix = environ.get("HTTP_X_FORWARDED_PREFIX", "")
        if prefix:
            environ["SCRIPT_NAME"] = prefix
            path_info = environ.get("PATH_INFO", "")
            if path_info.startswith(prefix):
                environ["PATH_INFO"] = path_info[len(prefix):]
        return self.wsgi_app(environ, start_response)


app.wsgi_app = ProxyFix(PrefixMiddleware(app.wsgi_app), x_for=1, x_proto=1, x_host=1)

if __name__ == "__main__":
    app.run(debug=True)
