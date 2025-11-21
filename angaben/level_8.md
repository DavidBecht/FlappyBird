<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 8: If Verzweigungen**

Schreibe ein Programm, das solange `Erst <Distanz> Pixel` ausgibt, solange FlappyBird weniger als 500 Pixel geflogen ist. Sobald er 500 Pixel oder mehr geflogen ist, soll `Juhu` ausgegeben werden.

Füge deine Lösung in das File `student_code.py` ein!

```python
from flappybird.game import bird
LEVEL = 8

def solution():
    # Füge hier deine Lösung ein!
```

### **If-Verzweigung**
:::hint
Eine `if`-Anweisung kann mehrere Formen haben. Eine einfache `if`-Anweisung ohne `else`-Teil sieht wie folgt aus. Dabei wird die Bedingung (condition) geprüft. Ist das Ergebnis dieser Prüfung `True`, werden die Anweisungen (statements) nach dem Doppelpunkt ausgeführt die entsprechend eingerückt sind (ein Tab). Ansonsten geschieht nichts.

```py
if condition:
    statement
else:
    statement
```

Beispiel:

```py
a = 5
b = 6

if (a + b > 10):
    print("The answer is greater than 10.")
else:
    print("The answer is less or equal than 10.")
```
:::


### **Lösung**
![level 8 solution](assets/level_8_solution.png)

:::solution

```python
from flappybird.game import bird

LEVEL = 8
def solution():
    if bird.distance < 500:
        print(f"Erst {bird.distance} Pixel")
    else:
        print("Juhu")
```
:::
