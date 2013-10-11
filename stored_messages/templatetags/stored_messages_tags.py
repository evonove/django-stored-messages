from django import template

from ..models import Inbox


register = template.Library()


@register.inclusion_tag("stored_messages/stored_messages_list.html", takes_context=True)
def stored_messages_list(context, num_elements=10):
    """
    Renders a list of stored messages for the current user
    """
    if "user" in context:
        user = context["user"]
        if user.is_authenticated():
            return {
                "messages": Inbox.objects.select_related("message").filter(user=user)[:num_elements]
            }
