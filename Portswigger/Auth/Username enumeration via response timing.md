![](Pasted%20image%2020261009182241.png)
![](Pasted%20image%2020261009182536.png)![](Pasted%20image%2020261009182519.png)

**wiener** fiind un user real are timp de raspuns de 1716 milisecunde, in timp ce **paius**, ce nu este un user real, are timp de raspuns de 55 milisecunde.
Also, am folosit `X-Forwarded-For` pentru a da bypass la rate limit.

![](Pasted%20image%2020261009183011.png)
![](Pasted%20image%2020261009183029.png)![](Pasted%20image%2020261009183130.png)

In pitchfork-ul de mai sus se poate observa cum response-ul pentru user-ul `af` este semnificativ mai mare decat restul, astfel am aflat ca user-ul valid pe care il cautam este `af`.

Ramane sa procedam la fel si cu parola, stiind deja user-ul si schimband valoarea de la `X-Forwarded-For` din nou.

