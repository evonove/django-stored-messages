from __future__ import unicode_literals

from django import template

from ..models import Inbox, MessageArchive


register = template.Library()


@register.inclusion_tag("stored_messages/stored_messages_list.html", takes_context=True)
def stored_messages_list(context, num_elements=10):
    """
    Renders a list of unread stored messages for the current user
    """
    if "user" in context:
        user = context["user"]
        if user.is_authenticated():
            qs = Inbox.objects.select_related("message").filter(user=user)
            return {
                "messages": qs[:num_elements],
                "count": qs.count(),
            }


@register.assignment_tag(takes_context=True)
def stored_messages_count(context):
    """
    Renders a list of unread stored messages for the current user
    """
    if "user" in context:
        user = context["user"]
        if user.is_authenticated():
            return Inbox.objects.select_related("message").filter(user=user).count()


@register.inclusion_tag("stored_messages/stored_messages_list.html", takes_context=True)
def stored_messages_archive(context, num_elements=10):
    """
    Renders a list of archived messages for the current user
    """
    if "user" in context:
        user = context["user"]
        if user.is_authenticated():
            qs = MessageArchive.objects.select_related("message").filter(user=user)
            return {
                "messages": qs[:num_elements],
                "count": qs.count(),
            }
