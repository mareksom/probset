from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .decorators import allowed_user_required
from .helpers import (
    get_redir_path, get_redir_arg, get_paginator, get_redir_field,
    check_allow_for_user, users_impersonable
)
from .signals import session_begin, session_end

try:
    # Django 1.5 check
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


@allowed_user_required
def impersonate(request, uid):
    ''' Takes in the UID of the user to impersonate.
        View will fetch the User instance and store it
        in the request.session under the '_impersonate' key.

        The middleware will then pick up on it and adjust the
        request object as needed.
    '''
    new_user = get_object_or_404(User, pk=uid)
    if check_allow_for_user(request, new_user):
        request.session['_impersonate'] = new_user.id
        request.session.modified = True  # Let's make sure...
        # can be used to hook up auditing of the session
        session_begin.send(
            sender=None,
            impersonator=request.user,
            impersonating=new_user,
            request=request
        )
    return redirect('accounts-users')


def stop_impersonate(request):
    ''' Remove the impersonation object from the session
    '''
    impersonating = request.session.pop('_impersonate', None)
    if impersonating is not None:
        request.session.modified = True
        session_end.send(
            sender=None,
            impersonator=request.impersonator,
            impersonating=impersonating,
            request=request
        )
    return redirect('accounts-users')
