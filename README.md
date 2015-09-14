## Env
hello all.
This script can configure container's ip-address persistence.
To confirm before use:
>
1. pip install docker-py
2. yum install bridge-utils -y
>

##Demo

```
cd docker-static-ip
python duration.py
```

run a test container
```
[root@image docker-static-ip]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
centos6             base                4fbd1376f4f6        4 weeks ago         311.3 MB

[root@image docker-static-ip]# docker run -d --net=none 4fbd1376f4f6 tail -f /var/log/yum.log
[root@image docker-static-ip]# docker ps
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
71792e4003d8        centos6:base        "tail -f /var/log/yu   34 minutes ago      Up 26 minutes                           serene_albattani
[root@image docker-static-ip]# docker exec -i 71792e4003d8 ip a
15: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever

```

configure duration
```
[root@image docker-static-ip]# echo >> "71792e4003d8,docker0,172.17.42.30/16,172.17.42.1" >> containers.cfg
```

> formation: [container-id],[bridge-name],[ipaddress/netmask],[gateway]

check
```
[root@image docker-static-ip]# docker exec -i 71792e4003d8 ip a
15: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
16: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 0a:d9:1d:00:be:71 brd ff:ff:ff:ff:ff:ff
    inet 172.17.42.30/16 scope global eth0
    inet6 fe80::8d9:1dff:fe00:be71/64 scope link 
       valid_lft forever preferred_lft forever
```

restart container test
```
[root@image docker-static-ip]# docker stop 71792e4003d8
71792e4003d8
[root@image docker-static-ip]# docker start 71792e4003d8
71792e4003d8
[root@image docker-static-ip]# docker exec -i 71792e4003d8 ip a
18: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
19: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 8a:85:16:6d:fc:08 brd ff:ff:ff:ff:ff:ff
    inet 172.17.42.30/16 scope global eth0
    inet6 fe80::8885:16ff:fe6d:fc08/64 scope link 
       valid_lft forever preferred_lft forever
```

> OK,static ip is not change !
