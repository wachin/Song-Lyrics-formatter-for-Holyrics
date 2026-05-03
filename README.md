# Song-Lyrics-formatter-for-Holyrics
Praise song lyrics formatter for projecting with Holyrics

🎤 Lyrics Formatter (PyQt6 + CLI curses)

Formateador de letras de canciones optimizado para proyectores (iglesias, presentaciones, etc.).

Este proyecto tiene dos versiones:

- 🖥️ GUI (PyQt6) → Interfaz gráfica fácil de usar
- 🧑‍💻 CLI (curses) → Interfaz en terminal, ideal para Termux / Linux ligero

---

✨ Características

- Divide automáticamente líneas largas
- Control por:
  - número máximo de caracteres
  - número máximo de palabras
- Mantiene:
  - líneas vacías
  - comentarios tipo "//"
- Optimizado para lectura en pantalla (proyector)

---

🖥️ Versión 1: Interfaz Gráfica (PyQt6)

📦 Requisitos

En Debian / MX Linux:

sudo apt install python3 python3-pyqt6

---

▶️ Ejecutar

python3 Lyrics-formatter.py

---

🧠 Cómo usar

1. Cargar archivo ".txt" o pegar texto
2. Ajustar:
   - Máx. caracteres
   - Máx. palabras
3. Presionar Formatear
4. Guardar resultado

---

🎯 Ideal para

- Usuarios que prefieren interfaz gráfica
- Edición visual de letras
- Preparar canciones rápidamente

---

🧑‍💻 Versión 2: Terminal (CLI con curses)

Perfecta para:

- 📱 Termux (Android)
- 💻 Sistemas ligeros
- ⚡ Usuarios avanzados

---

📦 Requisitos

En Debian / MX Linux:

sudo apt install python3

En Termux:

pkg install python

---

▶️ Ejecutar

python3 lyrics_formatter_curses.py

Abrir en una carpeta específica:

python3 lyrics_formatter_curses.py /ruta/a/carpeta

---

🎮 Controles

↑ / ↓      mover selección
Enter      abrir carpeta / seleccionar archivo
Backspace  subir carpeta
c / C      bajar/subir caracteres
w / W      bajar/subir palabras
h          ayuda
q          salir

---

⚙️ Funcionamiento

1. Navegas por carpetas
2. Seleccionas un archivo ".txt"
3. El programa lo formatea automáticamente
4. Se guarda como:

nombre - fixed.txt

---

🧪 Ejemplo

Entrada:

Este es mi deseo honrarte a ti con todo mi ser te adoro a ti

Salida:

Este es mi
deseo honrarte
a ti con todo
mi ser te
adoro a ti

---

🧠 Lógica del algoritmo

El formateo se basa en:

- Máximo de caracteres por línea
- Máximo de palabras por línea
- Evita juntar palabras largas
- Respeta saltos importantes

---

📁 Estructura del proyecto

.
├── Lyrics-formatter.py        # Versión GUI (PyQt6)
├── lyrics_formatter_curses.py # Versión CLI (curses)
├── README.md

---

🙌 Autor

Washington Indacochea Delgado

Proyecto pensado para uso práctico en iglesias y músicos.

---

📜 Licencia

GPL 3 
Libre uso y modificación 👍
