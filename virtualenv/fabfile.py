#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    mysql-connector-python
    tornado
    
'''
__author__ = 'Lihang'


'''
打包
tar -zcvf www.tar.gz --exclude=.git --exclude=.DS_Store ./*

'''


'''
Deployment toolkit.
'''

import os, re, logging, paramiko

from datetime import datetime
from fabric.api import *

paramiko.util.log_to_file('paramiko.log')

env.user = 'airclear'
env.sudo_user = 'airclear'
env.hosts = '192.168.2.36'
env.password = '000000'

_TAR_FILE = 'test.tar.gz'

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE

_REMOTE_BASE_DIR = '/home/airclear/apps/test'

_PROJECT_NAME = 'virtualenv'
_PROJECT_NAME_TMP = _PROJECT_NAME + "_tmp"

def _current_path():
    return os.path.abspath('.')

def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')

def build():
    '''
    Build dist package.
    '''
    parent_path = os.path.abspath('..')
    local('rm -rf ../%s' % _PROJECT_NAME_TMP)
    with lcd(parent_path):
        local('cp -r %s  %s' % (_PROJECT_NAME, _PROJECT_NAME_TMP))
    with lcd(parent_path + '/' + _PROJECT_NAME_TMP):
        #local("python ./html_handler.py")
        #local("rm -f  conf.py")
        #local("mv  conf_d.py conf.py")
        local('rm -f %s' % _TAR_FILE)
        local('tar -zcf '+ _TAR_FILE +' --exclude=.git --exclude=*.pyc --exclude=dist --exclude=.DS_Store ./*')

def deploy():
    parent_path = os.path.abspath('..')
    newdir = 'www-%s' % _now()
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put( parent_path + '/' + _PROJECT_NAME_TMP + '/' +_TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
    run('sudo supervisorctl stop test')
    run('sudo supervisorctl start test')
       
