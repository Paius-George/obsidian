![](../../attachments/Pasted%20image%2020261021134618.png)
![](../../attachments/Pasted%20image%2020261021134654.png)
![](../../attachments/Pasted%20image%2020261021135106.png)
![](../../attachments/Pasted%20image%2020261021135217.png)

Voi folosi: https://apis.guru/graphql-voyager/ si il voi encoda URL si folosi drept query pentru a vedea schema.

![](../../attachments/Pasted%20image%2020261021135403.png)
![](../../attachments/Pasted%20image%2020261021135431.png)![699](../../attachments/Pasted%20image%2020261021135813.png)

Nu a functionat, asadar am ajuns la urmatoarea solutie: `GET /api?query=%7B__schema%0A%7Btypes%7Bname%7D%7D%7D HTTP/2`

```
{
  __schema
  {
    types {
      name
    }
  }
}
```
![](../../attachments/Pasted%20image%2020261021140512.png)
![](../../attachments/Pasted%20image%2020261021140918.png)
![](../../attachments/Pasted%20image%2020261021140940.png)
![](../../attachments/Pasted%20image%2020261021140955.png)
![](../../attachments/Pasted%20image%2020261021141211.png)![](../../attachments/Pasted%20image%2020261021141226.png)