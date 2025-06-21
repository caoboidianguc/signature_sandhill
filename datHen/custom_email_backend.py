
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend
import ssl
import certifi

class EmailBackend(DjangoEmailBackend):
    @property
    def ssl_context(self):
        # Use getattr to safely check _ssl_context, defaulting to None if undefined
        if getattr(self, '_ssl_context', None) is None:
            # Create an SSL context with certifi's CA bundle
            self._ssl_context = ssl.create_default_context(cafile=certifi.where())
            # Load client certificate chain only if both files are provided
            if self.ssl_certfile and self.ssl_keyfile:
                self._ssl_context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
        return self._ssl_context