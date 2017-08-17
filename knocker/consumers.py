# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from channels import Group
#from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_connect(message):
    """
    Channels connection setup.
    Register the current client on the related Groups according to the language
    and according to the combination of language and username
    """
    # Accept the connection
    message.reply_channel.send({"accept": True})    
    
    prefix, language = message['path'].strip('/').split('/')
    grLangUser = Group('knocker-{0}-{1}'.format(language, 
                                                message.user.id))
    grLangUser.add(message.reply_channel)
    message.channel_session['knocker'] = language


@channel_session_user
def ws_receive(message):
    """
    Currently no-op
    """
    pass


@channel_session_user
def ws_disconnect(message):
    """
    Channels connection close.
    Deregister the client
    """
    language = message.channel_session['knocker']
    grLangUser = Group('knocker-{0}-{1}'.format(language, 
                                                message.user.id))
    grLangUser.discard(message.reply_channel)
    
