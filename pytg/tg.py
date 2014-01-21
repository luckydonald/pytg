# -*- coding: utf-8 -*-
from types import GeneratorType
from datetime import datetime
from utils import *
from regex import *

@coroutine
def dialog_list(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{print_message}' in line or '{end_print_message}' in line or \
               '{user_status}' in line or '{service_message}' in line:
                continue
            m = unread_user.search(clear_prompt(remove_color(line)).strip())
            if m:
                if m.group('uid'):
                    user, uid = m.group('user'), m.group('uid')
                    cmduser = user.replace(' ', '_')
                else:
                    user, cmduser, uid = None, None, m.group('user')
                unread = m.group('unread')
                arg = {'type': 'dialog_list_user', 'uid': uid, 'user': user, 'cmduser': cmduser, 'unread': unread}
                target.send(arg)
                continue
            m = unread_chat.search(clear_prompt(remove_color(line)).strip())
            if m:
                if m.group('gid'):
                    group, gid = m.group('group'), m.group('gid')
                    cmdgroup = group.replace(' ', '_')
                else:
                    group, cmdgroup, gid = None, None, m.group('group')
                unread = m.group('unread')
                arg = {'type': 'dialog_list_group', 'gid': gid, 'group': group, 'cmdgroup': cmdgroup, 'unread': unread}
                target.send(arg)
    except GeneratorExit:
        pass

@coroutine
def chat_info(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        arg = {}
        while True:
            line = (yield)
            if '{print_message}' in line or '{end_print_message}' in line or \
               '{user_status}' in line or '{service_message}' in line:
                continue
            m = chat_info_header.search(clear_prompt(remove_color(line)).strip())
            if m:
                if m.group('gid'):
                    group, gid = m.group('group'), m.group('gid')
                    cmdgroup = group.replace(' ', '_')
                else:
                    group, cmdgroup, gid = None, None, m.group('group')
                arg = {'type': 'chat_info', 'group': group,
                    'cmdgroup': cmdgroup, 'gid': gid}
                target.send(arg)
                continue
            m = chat_info_body.search(clear_prompt(remove_color(line)).strip())
            if m and len(arg) > 0:
                if m.group('uid'):
                    user, uid = m.group('user'), m.group('uid')
                    cmduser = user.replace(' ', '_')
                else:
                    user, usercmd, uid = None, None, m.group('user')
                if m.group('iuid'):
                    iuser, iuid = m.group('iuser'), m.group('iuid')
                    cmdiuser = iuser.replace(' ', '_')
                else:
                    iuser, cmdiuser, iuid = None, None, m.group('iuser')
                timestamp = datetime(int(m.group('yr')), int(m.group('mth')),
                    int(m.group('day')), int(m.group('hr')),
                    int(m.group('min')), int(m.group('sec')))
                arg = {
                    'type': 'chat_info_member', 'group': group, 'gid': gid,
                    'user': user, 'cmduser': cmduser, 'uid': uid,
                    'iuser': iuser, 'cmdiuser': cmdiuser, 'iuid': uid,
                    'timestamp': timestamp
                }
                target.send(arg)
                arg = {}
    except GeneratorExit:
        pass

@coroutine
def user_info(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        header_found = False
        while True:
            line = (yield)
            if '{print_message}' in line or '{end_print_message}' in line or \
               '{user_status}' in line or '{service_message}' in line or \
               'unread' in line:
                continue
            m = user_info_header.search(clear_prompt(remove_color(line)).strip())
            if m:
                header_found = True
                continue
            m = user_info_peerid.search(clear_prompt(remove_color(line)).strip())
            if m and header_found:
                arg = {'type': 'user_info', 'uid': m.group('peerid')}
                continue
            m = user_info_realname.search(clear_prompt(remove_color(line)).strip())
            if m and header_found:
                arg['user'] = m.group('realname')
                arg['cmduser'] = arg['user'].replace(' ', '_')
                continue
            m = user_info_phone.search(clear_prompt(remove_color(line)).strip())
            if m and header_found:
                arg['phone'] = m.group('phone')
                target.send(arg)
                header_found = False
    except GeneratorExit:
        pass

@coroutine
def user_status(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{user_status}' not in line:
                continue
            m = user_status_data.search(clear_prompt(remove_color(line)).strip())
            if m:
                user, uid, status = m.group('user'), m.group('uid'), m.group('status')
                if not uid:
                    uid, user = user, None
                arg = {
                    'type': 'user_status', 'uid': uid, 'user': user, 'status': status
                }
                target.send(arg)
    except GeneratorExit:
        pass

@coroutine
def contact_list(target):
    try:
        while True:
            line = (yield)
            if '{print_message}' in line or '{end_print_message}' in line or \
               '{user_status}' in line or '{service_message}' in line or \
               'unread' in line:
                continue
            m = contact_list_data.search(clear_prompt(remove_color(line)).strip())
            if m:
                arg = {
                    'type': 'contact_list', 'uid': m.group('uid'),
                    'user': m.group('user'), 'cmduser': m.group('cmduser'),
                    'phone': m.group('phone')
                }
                target.send(arg)
    except GeneratorExit:
        pass

@coroutine
def message(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{print_message}' not in line or '{end_print_message}' not in line:
                continue
            m = print_message_data.search(clear_prompt(remove_color(line)).strip())
            if m:
                arg = {
                    'type': 'message', 'msgid': m.group('msgid'),
                    'timestamp': m.group('timestamp'),
                    'message': m.group('message'), 'media': None
                }
                tmpchat, tmpuser = m.group('chat'), m.group('user')
                arg['peer'] = 'group' if tmpchat else 'user'
                if tmpchat:
                    if '#' in tmpchat:
                        arg['group'], arg['gid'] = tmpchat.split('#')
                        arg['cmdgroup'] = arg['group'].replace(' ', '_')
                    else:
                        arg['group'], arg['cmdgroup'], arg['gid'] = None, None, tmpchat
                if '#' in tmpuser:
                    arg['user'], arg['uid'] = tmpuser.split('#')
                    arg['cmduser'] = arg['user'].replace(' ', '_')
                else:
                    arg['user'], arg['cmduser'], arg['uid'] = None, None, tmpuser
                if arg['peer'] == 'user':
                    arg['ownmsg'] = True if m.group('dir') == '«««' else False
                if m.group('media'):
                    if 'photo' in m.group('media'):
                        tmp = m.group('media').split(' ', 1)
                        arg['media'] = {'type': tmp[0], 'caption': None}
                        if len(tmp) == 2:
                            arg['media'] = {'caption': tmp[1]}
                    elif 'video' in m.group('media') or \
                        'audio' in m.group('media') or \
                        'contact' in m.group('media'):
                        arg['media'] = {'type': m.group('media')}
                    elif 'document' in m.group('media'):
                        arg['media'] = {'type': 'document', 'caption': None, 'mime': None}
                        tmp = m.group('media').split(':')
                        try:
                            arg['media']['caption'] = tmp[0].split(' ', 1)[1]
                        except IndexError:
                            pass
                        try:
                            arg['media']['mime'] = tmp[1].strip().split(' ', 1)[1]
                        except IndexError:
                            pass
                    elif 'geo' in m.group('media'):
                        arg['media'] = {'type': 'geo', 'link': m.group('geolink')}
                target.send(arg)
    except GeneratorExit:
        pass

@coroutine
def service_message(target):
    if type(target) is not GeneratorType:
        raise TypeError('target must be GeneratorType')
    try:
        while True:
            line = (yield)
            if '{service_message}' not in line or '{service_message}' not in line:
                continue
            m = service_message_data.search(clear_prompt(remove_color(line)).strip())
            if m:
                arg = {
                    'type': 'service_message', 'msgid': m.group('msgid'),
                    'timestamp': m.group('timestamp'),
                    'message': m.group('message'), 'action': m.group('action'),
                }
                if m.group('gid'):
                    arg['group'], arg['gid'] = m.group('group'), arg('gid')
                    arg['cmdgroup'] = arg['group'].replace(' ', '_')
                else:
                    arg['group'], arg['cmdgroup'], arg['gid'] = None, None, m.group('group')
                if m.group('uid'):
                    arg['user'], arg['uid'] = m.group('user'), arg('uid')
                    arg['cmduser'] = arg['user'].replace(' ', '_')
                else:
                    arg['user'], arg['cmduser'], arg['uid'] = None, None, m.group('user')
                if arg['action'] == 'changed title to':
                    arg['actionarg'] = m.group('arg')
                else:
                    tmp = m.group('arg').split('#')
                    if len(tmp) == 2:
                        arg['actionarg'] = {'user': None, 'uid': tmp[1]}
                    else:
                        arg['actionarg'] = {'user': tmp[1], 'uid': tmp[2]}
                target.send(arg)
    except GeneratorExit:
        pass
