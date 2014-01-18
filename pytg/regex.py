# -*- coding: utf-8 -*-
import re

unread_user = re.compile("^User\ useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\:\ (?P<unread>\d+)\ unread", re.U)
unread_chat = re.compile("^Chat\ chati?d?\#(?P<group>[^#]+)\#?(?P<gid>\d+)?\:\ (?P<unread>\d+)\ unread", re.U)
chat_info_header = re.compile("^Chat\ chati?d?\#(?P<group>[^#]+)\#?(?P<gid>\d+)?\ members\:", re.U)
chat_info_body = re.compile("^\t?\t?useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\ invited\ by\ useri?d?\#(?P<iuser>[^#]+)\#?(?P<iuid>\d+)?\ at \[(?P<yr>\d{4})\/(?P<mth>\d{2})\/(?P<day>\d{2})\ (?P<hr>\d{2})\:(?P<min>\d{2})\:(?P<sec>\d{2})\]", re.U|re.M|re.S)
print_message = re.compile('^(?P<msgid>\d+)\ \[(?P<timestamp>.{5,6})\]\ \{print_message}\ (chati?d?\#(?P<chat>.+)\ )?useri?d?\#(?P<user>.+)\ (?P<dir>[<>«»]{3})\ (?P<message>.*)\{end_print_message\}', re.U|re.M|re.S)
user_status = re.compile('^\[\d{2}\:\d{2}\]\ \ \{user_status\}\ User\ useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\ is\ now\ (?P<status>online|offline)', re.U)
