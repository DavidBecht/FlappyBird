# FlappyBird

Python lernen mit FlappyBird: In 14 Levels steuerst du den Vogel mit deinem eigenen Code,
von der ersten Ausgabe mit `print` bis zum Autopiloten, der selbstständig durch die Röhren fliegt.

## Einrichten

1. Python 3.12 installieren.
2. Den Projektordner in PyCharm öffnen und, falls PyCharm danach fragt, einen Python-Interpreter
   auswählen. Ordner als *Sources Root* markieren ist nicht nötig, das ist schon eingestellt.
3. `pygame-ce` installieren:
   ```
   pip install pygame-ce
   ```

## Ein Level lösen

Die Angaben stehen in `angaben/level_X.md`. Deine Lösung kommt in die Datei
`student_solutions/level_X.py`. Gibt es sie noch nicht, legst du sie an und übernimmst
die Vorlage aus der Angabe, zum Beispiel für Level 1:

```python
from flappybird.game import start_level

LEVEL = 1

def solution():
    # Füge hier deine Lösung ein!


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
```

`LEVEL` muss zur Nummer im Dateinamen passen. Sonst bricht das Spiel mit einem Hinweis ab.

## Starten

**PyCharm:** Die Datei `student_solutions/level_X.py` öffnen und auf ▶ klicken
(oder Rechtsklick auf die Datei → *Run*).

**Terminal:** im Projektordner

```
python -m student_solutions.level_1
```

Das Spiel zeigt am Ende an, ob das Level bestanden ist. Das Ergebnis steht auch in der Konsole.

In VS Code funktioniert *Run Python File* nicht, weil dabei der Projektordner fehlt
und Python `flappybird` nicht findet. Dort den Befehl oben im Terminal verwenden.

### Selbst spielen

Ohne Level: Springen mit Leertaste oder Mausklick, Beenden mit Esc.

```
python -m flappybird.main_keyboard
```

## Lösungen prüfen

Alle Musterlösungen aus den Angaben testen:

```
python tests/test_solutions.py
```

Die eigenen Dateien in `student_solutions/` prüfen. Das macht auch GitHub Actions bei jedem Push
und schreibt eine Zusammenfassung (geschafft, nicht geschafft, noch keine Datei):

```
python tests/test_solutions.py --student-files
```

Unter Windows vorher `$env:PYTHONIOENCODING = "utf-8"` setzen, sonst scheitert die Ausgabe an den Emojis.

## Aufbau

```
angaben/              Aufgaben der Levels 1–14 (Markdown, teils als PDF)
student_solutions/    deine Lösungen, eine Datei pro Level
flappybird/
  game.py             bird, game und start_level() für deine Lösungen
  globals.py          Bildschirmgröße, Schwerkraft, Geschwindigkeit …
  main_keyboard.py    selbst spielen
  src/levels/         Prüfung der einzelnen Levels
  src/assets/         Grafiken
tests/                automatische Prüfung der Lösungen
```

## Grafiken

Die Grafiken stammen aus einem Paket von Megacrash und stehen unter
Creative Commons Zero v1.0, siehe `flappybird/src/assets/readme.txt`.
