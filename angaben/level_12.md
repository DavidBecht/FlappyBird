<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 12: while-Schleife**

Schreibe ein Programm, das mithilfe einer **while-Schleife** die Zahlen von **1 bis 10** ausgibt – jede Zahl in einer eigenen Zeile.

Erwartete Ausgabe:
```
1
2
3
4
5
6
7
8
9
10
```

Füge deine Lösung in das File `student_code.py` ein!

```python
LEVEL = 12

def solution():
    # Füge hier deine Lösung ein!
```

:::hint
Eine **while-Schleife** wiederholt ihren Schleifenrumpf so lange, wie die Bedingung `True` ist.

```python
i = 1
while i <= 5:
    print(i)
    i += 1
```
> **Output:**
> ```
> 1
> 2
> 3
> 4
> 5
> ```

Vergiss nicht, die Zählvariable in jedem Durchlauf zu erhöhen (`i += 1`), damit die Schleife irgendwann endet!
:::

:::solution
```python
LEVEL = 12

def solution():
    # Füge hier deine Lösung ein!
    i = 1
    while i <= 10:
        print(i)
        i += 1
```
:::
