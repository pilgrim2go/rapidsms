#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.utils.translation.trans_real import translation
from .base import MessageBase
from ..conf import settings


class OutgoingMessage(MessageBase):
    """
    """

    def __init__(self, *args, **kwargs):
        self.in_reply_to = kwargs.pop('in_reply_to', None)
        super(OutgoingMessage, self).__init__(*args, **kwargs)
        self.sent = False

    @property
    def language(self):
        """
        Return the language which this message will be sent in. If
        possible, this is fetched from the recipient Contact model.
        Otherwise, it defaults to the ``LANGUAGE_CODE`` setting.
        """

        if self._connection.contact is not None:
            if self._connection.contact.language:
                return self._connection.contact.language

        return settings.LANGUAGE_CODE

    def append(self, template, **kwargs):
        self._parts.append((template, kwargs))

    def _render_part(self, template, **kwargs):
        t = translation(self.language)
        tmpl = t.gettext(template)
        return tmpl % kwargs

    # @property
    # def text(self):
    #     return unicode(" ".join([
    #         self._render_part(template, **kwargs)
    #         for template, kwargs in self._parts
    #     ]))

    @property
    def date(self):
        return self.sent_at

    def send(self):
        """
        Raises an exception to help developers upgrade legacy code to use
        the new interface for sending messages.
        """
        # TODO decide if this API is deprecated and add a
        #   deprecation warning if so
        from rapidsms.router import send
        send(self.text, self.connection)
        self.sent = True
