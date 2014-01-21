# -*- coding: utf-8 -*-
import re

unread_user = re.compile("^User\ useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\:\ (?P<unread>\d+)\ unread", re.U)
unread_chat = re.compile("^Chat\ chati?d?\#(?P<group>[^#]+)\#?(?P<gid>\d+)?\:\ (?P<unread>\d+)\ unread", re.U)
chat_info_header = re.compile("^Chat\ chati?d?\#(?P<group>[^#]+)\#?(?P<gid>\d+)?\ members\:", re.U)
chat_info_body = re.compile("^\t?\t?useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\ invited\ by\ useri?d?\#(?P<iuser>[^#]+)\#?(?P<iuid>\d+)?\ at \[(?P<yr>\d{4})\/(?P<mth>\d{2})\/(?P<day>\d{2})\ (?P<hr>\d{2})\:(?P<min>\d{2})\:(?P<sec>\d{2})\]", re.U|re.M|re.S)
user_status_data = re.compile('^\[\d{2}\:\d{2}\]\ \ \{user_status\}\ User\ useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\ is\ now\ (?P<status>online|offline)', re.U)
user_info_header = re.compile("^User\ useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\:", re.U)
user_info_peerid = re.compile("peer\ id\:\ (?P<peerid>\d+)", re.U)
user_info_realname = re.compile("real\ name\:\ (?P<realname>.+)", re.U)
user_info_phone = re.compile("phone\:\ (?P<phone>\d+)", re.U)
contact_list_data = re.compile("^User\ \#(?P<uid>\d+)\:\ user\#(?P<user>.+)\#\d+\ \((?P<cmduser>[^\ ]+)\ (?P<phone>\d+).+", re.U)
print_message_data = re.compile('^(?P<msgid>\d+)\ \[(?P<timestamp>.{5,6})\]\ \[?(?P<media>.+)?\]?\ ?(?P<geolink>https\:\/\/map\.google\.com\/\?=[\d\.\,])?\ \{print_message}\ (chati?d?\#(?P<chat>.+)\ )?useri?d?\#(?P<user>.+)\ (?P<dir>[<>«»]{3})\ (?P<message>.*)\{end_print_message\}', re.U|re.M|re.S)
service_message_data = re.compile("^(?P<msgid>\d+)\ \[(?P<timestamp>.+)\]\ \ ?\{service_message\}\ (chati?d?\#(?P<group>[^#]+)\#?(?P<gid>\d+)?\ )??useri?d?\#(?P<user>[^#]+)\#?(?P<uid>\d+)?\ (?P<action>changed\ title\ to|added\ user|deleted\ user)\ (?P<arg>.+)", re.U)
