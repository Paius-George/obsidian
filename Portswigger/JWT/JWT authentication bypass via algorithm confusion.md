![](../../attachments/Pasted%20image%2020261013214501.png)

```
/jwks.json
/jwks.json
/auth/jwks
/api/jwks
/keys
/security/jwks
/public-keys
/.well-known
```

![](../../attachments/Pasted%20image%2020261013230221.png)
![](../../attachments/Pasted%20image%2020261013230242.png)

```
{"keys":[{"kty":"RSA","e":"AQAB","use":"sig","kid":"fa7e0d96-487b-4a1b-acac-3c8609f1599f","alg":"RS256","n":"9slWMJbnCVIjejjXpHscwPxIxoPuNrU6u16npEkfP4KuXoUF1vW1vhPx5c0C9chyD_ILRKEsTpGqHTlI1PM62975tSHrhj83wWX0aBU-xKew7TwLhZJzMYh_oclpV5hOEW3NwB9aT32BF7gaX-eSz6iPwal5SIVDcm8jnQl5_vGkPzLVFtMq6ubI1yZiPEVfRYS-axoeyi852Mnwz4tE73uB3NWy1QfqR0_GUikg3uMIXQ9B09Y0hyTOwTMaVTiK3x3Yy8dacJO5KIBulqm9XncbmDgNjWQ-X4yeuNgTBS1EPa54HC3GW1FGZsamvEacCSVvzGF5BgMEQl1zS87I5w"}]}
```

![](../../attachments/Pasted%20image%2020261013230455.png)

Parametrul "k" are valoarea parametrului "n".

![](../../attachments/Pasted%20image%2020261013230812.png)

In body am pus key-ul gasit pe jwks.json, apoi am luat PEM si am encodat ca base64

![](../../attachments/Pasted%20image%2020261013230907.png)
![](../../attachments/Pasted%20image%2020261013230957.png)

Am creat o noua cheie simetrica, iar in parametrul "k" am pus encodarea din base64

![](../../attachments/Pasted%20image%2020261013231058.png)
![](../../attachments/Pasted%20image%2020261013231851.png)
![](../../attachments/Pasted%20image%2020261013231912.png)
![](../../attachments/Pasted%20image%2020261013231931.png)
![](../../attachments/Pasted%20image%2020261013231947.png)