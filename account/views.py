from urllib.parse import urlencode, quote_plus

from authlib.integrations.base_client import OAuthError
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def login(request):
    return oauth.auth0.authorize_redirect(
        request,
        request.build_absolute_uri(reverse('account:callback')),
    )


def callback(request):
    try:
        token = oauth.auth0.authorize_access_token(request)
        request.session["user"] = token

        user = get_user_model().objects.filter(email=token["userinfo"]["email"]).first()
        if not user:
            user = get_user_model().objects.create(
                email=token["userinfo"]["email"],
                name=token["userinfo"]["name"],
                is_active=True,
            )

        auth.login(request, user)

        return redirect(request.build_absolute_uri(reverse('account:home')))
    except OAuthError as e:
        print(str(e))
        return redirect(request.build_absolute_uri(reverse('account:login')))


def logout(request):
    auth.logout(request)

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("account:login")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus
        )
    )


def home(request):
    if request.user.is_authenticated:
        return HttpResponse('Authenticated')
    return HttpResponse('Ok')
