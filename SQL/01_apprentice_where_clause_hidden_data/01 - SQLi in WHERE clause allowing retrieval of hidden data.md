
---
# Problema:

Aplicația conține o vulnerabilitate de tip SQL Injection în filtrul de categorii de produse. În mod normal, magazinul afișează doar produsele care au parametrul de lansare setat pe `released = 1`
```
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```
**Obiectiv:** Exploatarea parametrului vulnerabil pentru a determina aplicația să returneze toate produsele din baza de date, inclusiv cele nelansate (`released = 0`)

---

# Rezolvare:

![[Pasted image 20260922174928.png]]

Putem observa ca deja putem vedea anumite produse. Asadar, o sa incercam o categorie anume, eu am ales "Lifestyle".

![[Pasted image 20260922175056.png]]

Acum ca avem mai putine produse de care putem tine cont, o sa ne mutam in burp.
![[Pasted image 20260922175213.png]]

Vom schimba categoria in: ``'+OR+1=1--`` 
![[Pasted image 20260922175345.png]]

Acum se poate observa ca numele categoriei s-a schimbat in `` ' OR 1=1-- ``

---
# Cum functioneaza:

Ce se intampla in backend:
Interogarea initiala SELECT * FROM products WHERE category = 'Lifestyle' AND released = 1
Acum devine: SELECT * FROM products WHERE category = ' ' OR 1=1 --' AND released = 1

Ce am facut:
Primul apostrof - da impresia backend-ului ca parametrul categoriei este un sir vid ('').
OR - In loc ca ambele conditii sa fie obligatorii (cum facea AND), schimba logica conditionala si va afisa randul daca oricare din parti este adevarata.
1=1 - returneaza intotdeauna True.
Comentariul(--) - tot ce urmeaza dupa aceste doua liniute este complet ignorat.

---
