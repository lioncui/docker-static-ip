#!/usr/bin/python
# -*- coding:UTF-8 -*-

'''

__author__ = 'lioncui'
__date__ = '2015-6-16'

'''

import docker
import os
import time

try:
    connect = docker.Client(base_url='unix:///var/run/docker.sock',version='1.17',timeout=120)
    connect.version()
except:
    exit()

def Duration(id, br, addr, gw):
    try:
        container_info = connect.inspect_container(resource_id=id)
        pid = str(container_info['State']['Pid'])
    except:
        pid = 0

    if int(pid) != 0:
        if not os.path.exists('/var/run/netns'):
            os.makedirs('/var/run/netns')
        source_namespace = '/proc/'+pid+'/ns/net'
        destination_namespace = '/var/run/netns/'+pid
        if not os.path.exists(destination_namespace):
            link = 'ln -s %s %s' % (source_namespace,destination_namespace)
            os.system(link)
            os.system('ip link add tap%s type veth peer name veth%s 2>> /var/log/docker-static-ip.log' % (pid,pid) )
            os.system('brctl addif %s tap%s 2>> /var/log/docker-static-ip.log' % (br,pid) )
            os.system('ip link set tap%s up 2>> /var/log/docker-static-ip.log' % pid )
            os.system('ip link set veth%s netns %s 2>> /var/log/docker-static-ip.log' % (pid,pid) )
            os.system('ip netns exec %s ip link set dev veth%s name eth0 2>> /var/log/docker-static-ip.log' % (pid,pid) )
            os.system('ip netns exec %s ip link set eth0 up 2>> /var/log/docker-static-ip.log' % pid)
            os.system('ip netns exec %s ip addr add %s dev eth0 2>> /var/log/docker-static-ip.log' % (pid,addr) )
            os.system('ip netns exec %s ip route add default via %s 2>> /var/log/docker-static-ip.log' % (pid,gw) )

syspid = os.fork()

if syspid == 0:
    while True:
        file = open('./containers.cfg')
        if file:
            for i in file:
                i = i.strip('\n')
                cfg = i.split(',') 
                Duration(*cfg)
        file.close()
        time.sleep(10)
else:
    exit()
