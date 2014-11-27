# -*- coding: utf-8 -*-
from __future__ import generators
from types import GeneratorType
from datetime import datetime
from .utils import coroutine, clear_prompt, remove_color
from .regex import unread_user,unread_chat,chat_info_header,chat_info_body,user_info_realname,user_info_peerid,user_info_header,user_info_phone,print_message_data,contact_list_data,user_status_data,service_message_data

@coroutine
def dialog_list(target):
	"""
	Get the dialog list.
	:param target:
	:raise TypeError:
	"""
	if type(target) is not GeneratorType:
		raise TypeError('target must be GeneratorType')
	try:
		while True:
			line = (yield)
			# this next line will let the regex search inside multi-line messages?
			if '{print_message}' in line or '{end_print_message}' in line or \
							'{user_status}' in line or '{service_message}' in line:
				continue
			m = unread_user.search(clear_prompt(remove_color(line)).strip())
			if m:
				if m.group('userid'):
					user, userid = m.group('user'), m.group('userid')
					usercmd = user.replace(' ', '_')
				else:
					user, usercmd, userid = None, None, m.group('user')
				unread = m.group('unread')
				arg = {'type': 'dialog_list_user', 'userid': userid, 'user': user, 'usercmd': usercmd, 'unread': unread}
				target.send(arg)
				continue
			m = unread_chat.search(clear_prompt(remove_color(line)).strip())
			if m:
				if m.group('groupid'):
					group, groupid = m.group('group'), m.group('groupid')
					groupcmd = group.replace(' ', '_')
				else:
					group, groupcmd, groupid = None, None, m.group('group')
				unread = m.group('unread')
				arg = {'type': 'dialog_list_group', 'groupid': groupid, 'group': group, 'groupcmd': groupcmd, 'unread': unread}
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
				if m.group('groupid'):
					group, groupid = m.group('group'), m.group('groupid')
					groupcmd = group.replace(' ', '_')
				else:
					group, groupcmd, groupid = None, None, m.group('group')
				arg = {'type': 'chat_info', 'group': group,
				       'groupcmd': groupcmd, 'groupid': groupid}
				target.send(arg)
				continue
			m = chat_info_body.search(clear_prompt(remove_color(line)).strip())
			if m and len(arg) > 0:
				if m.group('userid'):
					user, userid = m.group('user'), m.group('userid')
					usercmd = user.replace(' ', '_')
				else:
					user, usercmd, userid = None, None, m.group('user')
				if m.group('iuserid'):
					iuser, iuserid = m.group('iuser'), m.group('iuserid')
					cmdiuser = iuser.replace(' ', '_')
				else:
					iuser, cmdiuser, iuserid = None, None, m.group('iuser')
				timestamp = datetime(int(m.group('yr')), int(m.group('mth')),
				                     int(m.group('day')), int(m.group('hr')),
				                     int(m.group('min')), int(m.group('sec')))
				arg = {
					'type': 'chat_info_member', 'group': group, 'groupid': groupid,
					'user': user, 'usercmd': usercmd, 'userid': userid,
					'iuser': iuser, 'cmdiuser': cmdiuser, 'iuserid': userid,
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
				arg = {'type': 'user_info', 'userid': m.group('peerid')}
				continue
			m = user_info_realname.search(clear_prompt(remove_color(line)).strip())
			if m and header_found:
				arg['user'] = m.group('realname')
				arg['usercmd'] = arg['user'].replace(' ', '_')
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
				user, userid, status = m.group('user'), m.group('userid'), m.group('status')
				if not userid:
					userid, user = user, None
				arg = {
					'type': 'user_status', 'userid': userid, 'user': user, 'status': status
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
					'type': 'contact_list', 'userid': m.group('userid'),
					'user': m.group('user'), 'usercmd': m.group('usercmd'),
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
			m = print_message_data.search(clear_prompt(remove_color(line)).strip()) # http://regex101.com/r/aZ1pU3/2
			if m:
				arg = {
					'type': 'message', 'msgid': m.group('msgid'),
					'timestamp': m.group('timestamp'),
					'message': m.group('message'), 'media': None
				}
				arg['peer'] = 'group' if (m.group('chatid')) else 'user'
				arg['group'], arg['groupid'] = m.group('chat'),m.group('chatid')
				arg['groupcmd'] = arg['group'].replace(' ', '_') if arg['group'] else None
				arg['user'], arg['userid'] =  m.group('user'),  m.group('userid')
				arg['usercmd'] = arg['user'].replace(' ', '_') if arg['user'] else None
				# if arg['peer'] == 'user':
				arg['ownmsg'] = True if m.group('dir') in  ['«««','<<<'] else False
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
			else:
				print("not accepted:>" + line)
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
				if m.group('groupid'):
					arg['group'], arg['groupid'] = m.group('group'), m.group('groupid')
					arg['groupcmd'] = arg['group'].replace(' ', '_')
				else:
					arg['group'], arg['groupcmd'], arg['groupid'] = None, None, m.group('group')
				if m.group('userid'):
					arg['user'], arg['userid'] = m.group('user'), m.group('userid')
					arg['usercmd'] = arg['user'].replace(' ', '_')
				else:
					arg['user'], arg['usercmd'], arg['userid'] = None, None, m.group('user')
				if arg['action'] == 'changed title to':
					arg['actionarg'] = m.group('arg')
				else:
					tmp = m.group('arg').split('#')
					if len(tmp) == 2:
						arg['actionarg'] = {'user': None, 'userid': tmp[1]}
					else:
						arg['actionarg'] = {'user': tmp[1], 'userid': tmp[2]}
				target.send(arg)
	except GeneratorExit:
		pass
