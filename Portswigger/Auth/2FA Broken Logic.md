![](../../attachments/Pasted%20image%2020261011175840.png)

Dupa ce m-am conectat folosind credentialele cunoscute deja, am trimis in repeater 2 endpoint-uri pentru a le studia: /login respectiv /login2.

Mai jos se poate observa cum arata /login. Avem un cookie session care se creaza in momentul login-ului si un verify care verifica daca sesiunea este pentru user-ul respectiv

![](../../attachments/Pasted%20image%2020261011175924.png)

/login2:
![](../../attachments/Pasted%20image%2020261011180143.png)

Similar cu /login, dar se poate observa ca avem si un mfa-code, care nu are rate limit, deci poate fi bruteforce-uit. 
Combinand finding-urile de mai sus, putem trimite request-ul in intruder si putem face un bruteforce astfel:

![](../../attachments/Pasted%20image%2020261011180344.png)

![](../../attachments/Pasted%20image%2020261011175723.png)
