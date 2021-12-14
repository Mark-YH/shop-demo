# coding: UTF-8
"""
Created on 2021/12/14

@author: Mark Hsu
"""
from shopping_site_demo.settings import LOCAL_DEBUG, BASE_DIR
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.models import User
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
import json


class GoogleAccountManager:
    credentials = None
    SCOPES = [
        'openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]
    API_SERVICE_NAME = 'oauth2'
    API_VERSION = 'v2'

    def __init__(self):
        # When running in production *do not* leave this option enabled.
        if LOCAL_DEBUG:
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    @staticmethod
    def credentials_to_dict(credentials):
        return {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}

    @staticmethod
    def get_client_secret():
        if LOCAL_DEBUG:
            with open(os.path.join(BASE_DIR, 'config.json'), 'r') as file:
                data = file.read()
            return json.loads(data)

        config = os.environ.get('CLIENT_SECRET')
        return json.loads(config)

    def authorize(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(self.get_client_secret(), scopes=self.SCOPES)
        flow.redirect_uri = request.scheme + '://' + request.META['HTTP_HOST'] + '/oauth2callback/'
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        request.session['state'] = state
        return redirect(authorization_url)

    def callback(self, request):
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = request.session['state']

        flow = google_auth_oauthlib.flow.Flow.from_client_config(self.get_client_secret(), scopes=self.SCOPES,
                                                                 state=state)
        flow.redirect_uri = request.scheme + '://' + request.META['HTTP_HOST'] + '/oauth2callback/'

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        flow.fetch_token(code=request.GET['code'])

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials
        request.session['credentials'] = self.credentials_to_dict(credentials)

        return redirect('/login/google/')

    def login(self, request):
        if 'credentials' not in request.session:
            return redirect('/authorize/')

        # Load credentials from the session.
        credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])

        service = googleapiclient.discovery.build(self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials)

        info = service.userinfo()

        service.close()
        # Save credentials back to session in case access token was refreshed.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        request.session['credentials'] = self.credentials_to_dict(credentials)

        userinfo = info.get().execute()
        try:
            user = User.objects.get(username=userinfo['email'])
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth.login(request, user=user)
        else:
            try:
                user = User.objects.create_user(username=userinfo['email'])
                auth.login(request, user=user)
            except Exception as e:
                print(e)
        return redirect('/shop/')
