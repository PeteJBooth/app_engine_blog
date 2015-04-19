from google.appengine.api import users

def gauth(request):
    """
    Get any google user info associated with the current session.
    """
    user = users.get_current_user()
    context = {}
    if user:
        context['user_authenticated'] = True
        context['user_admin'] = users.is_current_user_admin()
        context['user_nickname'] = user.nickname()
    else:
        context['user_authenticated'] = False

    context['logout_url']  = users.create_logout_url('/')
    context['login_url'] = users.create_login_url('/')

    return context