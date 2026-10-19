![](../../attachments/Pasted%20image%2020261019140621.png)![](../../attachments/Pasted%20image%2020261019140630.png)

Mai jos se poate observa cum am incercat abordarea de la laboratorul trectut (`Web shell upload via Content-Type restriction bypass`)

![](../../attachments/Pasted%20image%2020261019140847.png)
![](../../attachments/Pasted%20image%2020261019140858.png)

Si a returnat direct comanda folosita: `<?php echo file_get_contents('/home/carlos/secret'); ?>`

![](../../attachments/Pasted%20image%2020261019141318.png)

Am incercat simpla metoda de path traversal folosind `../`, dar nu a functionat. File-ul meu a fost uploadat tot in `avatars`.

![](../../attachments/Pasted%20image%2020261019141445.png)
![](../../attachments/Pasted%20image%2020261019141459.png)

Am folosit encodare url pe tentativa mea de path traversal (`../`) si a functionat. File-ul este acum uploadat in `avatars/../`, ceea ce inseamna ca acum php-ul meu se afla in `files`.

![](../../attachments/Pasted%20image%2020261019141628.png)
![](../../attachments/Pasted%20image%2020261019141640.png)
![](../../attachments/Pasted%20image%2020261019141701.png)


# Metoda 2 (Intruder)

![](../../attachments/Pasted%20image%2020261019141943.png)

Pentru aceasta metoda, am ales sa folosesc intruder alaturi de o lista ce contine mai multe metode de path traversal: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Directory%20Traversal/Intruder/deep_traversal.txt

