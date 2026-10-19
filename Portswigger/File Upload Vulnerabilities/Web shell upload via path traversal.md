![](../../attachments/Pasted%20image%2020261019140621.png)![](../../attachments/Pasted%20image%2020261019140630.png)

Mai jos se poate observa cum am incercat abordarea de la laboratorul trectut (`Web shell upload via Content-Type restriction bypass`)

![](../../attachments/Pasted%20image%2020261019140847.png)
![](../../attachments/Pasted%20image%2020261019140858.png)

Si a returnat direct comanda folosita: `<?php echo file_get_contents('/home/carlos/secret'); ?>`

![](../../attachments/Pasted%20image%2020261019141318.png)

Am incercat simpla metoda de path traversal folosind `../`, dar nu a functionat. File-ul meu a fost uploadat tot in `avatars`.