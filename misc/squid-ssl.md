# Squid w ssl instalation instructions
## Instalation of squid w ssl support
use superuser for this step
´´´
wget -qO - https://packages.diladele.com/diladele_pub.asc | sudo apt-key add -

echo "deb https://squid52.diladele.com/ubuntu/ focal main">/etc/apt/sources.list.d/squid52.diladele.com.list

apt-get update && apt-get install -y squid-common squid-openssl squidclient libecap3 libecap3-dev

mkdir -p /etc/systemd/system/squid.service.d

rm /etc/systemd/system/squid.service.d/override.conf

echo "[Service]"         >> /etc/systemd/system/squid.service.d/override.conf

echo "LimitNOFILE=65535" >> /etc/systemd/system/squid.service.d/override.conf

systemctl daemon-reload

´´´
## Config OpenSSL to generate certificates
´´´
sudo vim /etc/ssl/openssl.cnf
´´´
Add or uncomment:

[ v3_ca ]

keyUsage = cRLSign, keyCertSign


## Create tmp folder to create self-signed certs
´´´
mkdir /tmp/ssl_cert

cd /tmp/ssl_cert

´´´
## Create certs
´´´

openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -extensions v3_ca -keyout squid-self-signed.key -out squid-self-signed.crt

´´´

Convert the cert into a trusted certificate in DER format.

openssl x509 -in squid-self-signed.crt -outform DER -out squid-self-signed.der


Convert the cert into a trusted certificate in PEM format.

openssl x509 -in squid-self-signed.crt -outform PEM -out squid-self-signed.pem


Generate the settings file for the Diffie-Hellman algorithm.

openssl dhparam -outform PEM -out squid-self-signed_dhparam.pem 2048


## Move certs to squid 

create a directory.

sudo mkdir /etc/squid/certs


copy certs to the directory.

sudo cp -rf /tmp/ssl_cert/* /etc/squid/certs/


add trusted ca into local.

sudo cp /etc/squid/certs/squid-self-signed.pem /usr/local/share/ca-certificates/squid-self-signed.crt


Update CA certificate cache.

sudo update-ca-certificates


change ownership so that squid can access the certificate.

sudo chown -R proxy:proxy /etc/squid

modify certificate permissions (for self-signed certificate).

sudo chmod 700 /etc/squid/certs/*



## Create ssl_db

create the directory.

sudo mkdir -p /var/lib/squid



create the SSL database to be used by squid.

sudo /usr/lib/squid/security_file_certgen -c -s /var/lib/squid/ssl_db -M 20MB



Changing database permission so squid can access it.

sudo chown -R proxy:proxy /var/lib/squid



## Configuring squid

sudo vim /etc/squid/squid.conf



Add the following directives to the beginning of the file or before the first http_access directive.

acl intermediate_fetching transaction_initiator certificate-fetching 

http_access allow intermediate_fetching


Uncomment http_access allow localnet


Add below after acl Safe_ports port 777 directive.

acl Safe_ports port 777  # multiling http                       

acl CONNECT method CONNECT



Replace the http_port directive with the following. We are enabling ssl_bump for port 3128 with dynamic certificate generation using our self-signed CA. Further, we are configuring certificate_cache of 20MB (in general can store ~5000 certificates).



http_port 3128 tcpkeepalive=60,30,3 ssl-bump generate-host-certificates=on dynamic_cert_mem_cache_size=20MB tls-cert=/etc/squid/certs/squid-self-signed.crt tls-key=/etc/squid/certs/squid-self-signed.key cipher=HIGH:MEDIUM:!LOW:!RC4:!SEED:!IDEA:!3DES:!MD5:!EXP:!PSK:!DSS options=NO_TLSv1,NO_SSLv3,SINGLE_DH_USE,SINGLE_ECDH_USE tls-dh=prime256v1:/etc/squid/certs/squid-self-signed_dhparam.pem



sslcrtd_program /usr/lib/squid/security_file_certgen -s /var/lib/squid/ssl_db -M 20MB

sslcrtd_children 5

ssl_bump server-first all

ssl_bump stare all

sslproxy_cert_error deny all



# Cache options docs:https://wiki.squid-cache.org/SquidFaq/SquidMemory



uncomment.

cache_dir ufs /usr/local/squid/var/cache/squid 100 16 256



and edit the following params w your preferences

maximum_object_size 6 GB

cache_mem 8192 MB

cache_dir ufs /usr/local/squid/var/cache/squid 32000 16 256 # 32GB as Cache



# Edit refresh patterns docs:http://www.squid-cache.org/Doc/config/refresh_pattern/


Google good refresh patterns. Play with ttl 

refresh_pattern -i .(gif|png|jpg|jpeg|ico)$ 10080 90% 43200 override-expire ignore-no-cache ignore-no-store ignore-private

refresh_pattern -i .(iso|avi|wav|mp3|mp4|mpeg|swf|flv|x-flv)$ 43200 90% 432000 override-expire ignore-no-cache ignore-no-store ignore-private

refresh_pattern -i .(deb|rpm|exe|zip|tar|tgz|ram|rar|bin|ppt|doc|tiff)$ 10080 90% 43200 override-expire ignore-no-cache ignore-no-store ignore-private

refresh_pattern -i .index.(html|htm)$ 0 40% 10080

refresh_pattern -i .(html|htm|css|js)$ 1440 40% 40320

refresh_pattern . 0 40% 40320

refresh_pattern -i .(jar|zip|whl|gz|bz)  1 20% 259200 ignore-reload ignore-no-store ignore-private override-expire



# Last Steps

sudo chown -R proxy:proxy /etc/squid
systemctl restart squid 
squid -k parse and check for erros
