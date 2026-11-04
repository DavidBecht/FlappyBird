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

Schreibe deine Lösung in die Datei `student_solutions/level_12.py` (gibt es sie noch nicht, lege sie an) und starte sie mit ▶!

```python
from flappybird.game import start_level

LEVEL = 12

def solution():
    # Füge hier deine Lösung ein!


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
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
