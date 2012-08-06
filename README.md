nmapme
======

Twisted nmap service. Scan IP of client and give him output of nmap -sT client_ip


install
-------

```
#aptitude install python-twisted
#twistd -ny nmapme.py
```

Client usage
------------

```
$ curl localhost:80

Starting Nmap 5.21 ( http://nmap.org ) at 2012-08-06 11:39 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00030s latency).
Not shown: 995 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
631/tcp  open  ipp
3306/tcp open  mysql
5901/tcp open  vnc-1

Nmap done: 1 IP address (1 host up) scanned in 0.06 seconds
```
