#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import MySQLdb as mysql
import etcd
from raven import Client
import top.api
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y%m%d %H:%M:%S',
                    filename='/tmp/flushdb.log',
                    filemode='a')

etcd_server = os.getenv('ETCD')
app_name = os.getenv('APP_NAME')
configs = {
    'mysql_host': 'localhost',
    'mysql_port': 3306,
    'mysql_user': 'flushdb',
    'mysql_passwd': 'flushdb',
    'mysql_db': 'flushdb',
    'dayu_key': 'dayu_key',
    'dayu_secret': 'dayu_secret',
    'dayu_tpl_id': 'dayu_tpl_id',
    'dayu_sign_name': 'dayu_sign_name',
    'sentry': 'sentry',
    'rerun': 2
}
if etcd_server and app_name:
    client = etcd.Client(host=etcd_server.split(':')[0], port=int(etcd_server.split(':')[1]), allow_reconnect=True)
    for result in client.get(app_name).children:
        configs[result.key.split('/')[-1]] = result.value
        logging.info(result.key.split('/')[-1] + " = " + result.value)

mysql_host = configs['mysql_host']
mysql_port = int(configs['mysql_port'])
mysql_user = configs['mysql_user']
mysql_passwd = configs['mysql_passwd']
mysql_db = configs['mysql_db']
dayu_key = configs['dayu_key']
dayu_secret = configs['dayu_secret']
dayu_tpl_id = configs['dayu_tpl_id']
dayu_sign_name = configs['dayu_sign_name']
sentry = configs['sentry']
rerun = int(configs['rerun'])

sentry = Client(sentry)
conn = mysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, port=mysql_port)
conn.autocommit(1)
cur = conn.cursor(mysql.cursors.DictCursor)


def send_sms(phone, sign_name, param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(dayu_key, dayu_secret))
    req.extend = ""
    req.sms_type = "normal"
    req.sms_free_sign_name = sign_name
    req.sms_param = ""
    req.rec_num = phone
    req.sms_template_code = dayu_tpl_id
    try:
        resp = req.getResponse(timeout=20)
        logging.info(resp)
    except Exception, e:
        logging.error(e)


def do():
    new_user_list = "select member.mobile_phone mobile, member.id member_id, \
                         member.member_name name, audit.id audit_id, audit.updatetime updatetime \
                     from t_member_rental_audit audit left \
                         JOIN t_member member ON audit.member_id=member.id  \
                     where audit.updatetime BETWEEN (now() - interval 1 HOUR) And (now() - interval 30 SECOND) \
                         and audit.member_status='auditing' limit 10;"
    cur.execute(new_user_list)
    results = cur.fetchall()
    for r in results:
        send_sms(r['mobile'], dayu_sign_name, '')
        logging.info("{}".format(r))

    approve_new_user = "update t_member_rental_audit set MEMBER_STATUS='approve' where MEMBER_STATUS='auditing';"
    cur.execute(approve_new_user)
