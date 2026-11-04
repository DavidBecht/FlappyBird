<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 1**
Schreibe ein Programm, dass der FlappyBird den Namen des Benutzers ausgibt. Der Text muss folgendermaßen formatiert werden:
```
Hi, <deinen Namen>!
```
Schreibe deine Lösung in die Datei `student_solutions/level_1.py` (gibt es sie noch nicht, lege sie an) und starte sie mit ▶!
```python
from flappybird.game import start_level

LEVEL = 1
def solution():
    # Füge hier deine Lösung ein!


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
```

:::hint
Mit der  Funktion [`print`](https://docs.python.org/3/library/functions.html#print) kann Text in der Konsole und im Spiel ausgegeben werden.
```py
hello_world_string = "Hello World"
print(hello_world_string)
print("Tschau")
```
>**Output:**
> ```
> Hello World
> Tschau
> ```

:::

![solution](assets/level_1_solution.png)

:::solution
```python
LEVEL = 1
def solution():
    # Füge hier deine Lösung ein!
    print("Hi, Lisa!")
```
:::