# Song-Lyrics-formatter-for-Holyrics

Formateador de letras de canciones pensado para preparar textos que se van a
proyectar con Holyrics en iglesias, reuniones y presentaciones.

El objetivo es que las letras queden faciles de leer en pantalla, sin lineas
demasiado largas y respetando los comentarios `//` que Holyrics usa para
separar secciones.

## Versiones

- `Lyrics-formatter.py`: version GUI original con PyQt6.
- `Lyrics-formatter_v2.py`: version GUI mejorada para bloques de Holyrics.
- `lyrics_formatter_curses.py`: version de terminal con curses.

## Caracteristicas principales

- Carga archivos `.txt` o permite pegar letras manualmente.
- Divide automaticamente lineas largas.
- Mantiene comentarios de Holyrics que empiezan con `//`.
- Permite guardar el resultado como un nuevo archivo `.txt`.
- Muestra una vista previa con fondo negro y texto grande.

## Version GUI mejorada para Holyrics

La version recomendada para preparar letras con bloques de Holyrics es:

```bash
python3 Lyrics-formatter_v2.py
```

Esta version agrega una regla especial para los comentarios `//`.

Si una seccion empieza asi:

```text
//Verso I
Dicen que son pocas y me consta
Son pocas las que son como tu
Guerrera genuina y verdadera
```

el programa la convierte en partes:

```text
//Verso I (Parte 1)
Dicen que
son pocas
y me
consta

//Verso I (Parte 2)
Son pocas
las que
son como
tu

//Verso I (Parte 3)
Guerrera
genuina y
verdadera
```

### Reglas de la version 2

- Cada bloque bajo un comentario `//` tiene maximo 6 lineas de letra.
- Entre bloque y bloque deja una sola linea vacia, como separador para Holyrics.
- Si una frase original no cabe en el bloque actual, pasa completa al siguiente
  bloque aunque el bloque anterior quede con menos de 6 lineas.
- Esto evita cortes poco naturales como dejar media frase en una parte y la otra
  mitad en la siguiente.
- Los comentarios se renombran automaticamente como:

```text
//Verso I (Parte 1)
//Verso I (Parte 2)
//Verso I (Parte 3)
```

### Controles de la version 2

- `Max. caracteres`: controla el largo maximo aproximado de cada linea.
- `Max. palabras cortas`: permite juntar varias palabras cortas cuando caben bien.
- `Formatear`: genera la letra preparada para Holyrics.
- `Cargar`: abre un archivo `.txt`.
- `Guardar`: guarda el resultado formateado.
- `Limpiar`: limpia entrada y salida.

Por defecto, la version 2 usa:

- 10 caracteres maximos por linea.
- 3 palabras cortas maximas por linea.

Estos valores buscan que la letra no se reduzca demasiado al proyectarse.

## Version GUI original

Para ejecutar la version original:

```bash
python3 Lyrics-formatter.py
```

Esta version divide las lineas segun:

- maximo de caracteres,
- maximo de palabras,
- palabras largas.

Tambien conserva comentarios `//`, pero no crea partes de 6 lineas para
Holyrics.

## Version terminal

Para ejecutar la version de terminal:

```bash
python3 lyrics_formatter_curses.py
```

Abrir en una carpeta especifica:

```bash
python3 lyrics_formatter_curses.py /ruta/a/carpeta
```

### Controles

```text
Arriba / Abajo   mover seleccion
Enter            abrir carpeta / seleccionar archivo
Backspace        subir carpeta
c / C            bajar/subir caracteres
w / W            bajar/subir palabras
h                ayuda
q                salir
```

## Requisitos

En Debian, Ubuntu, MX Linux o derivados:

```bash
sudo apt install python3 python3-pyqt6
```

Para la version de terminal solo se necesita Python 3:

```bash
sudo apt install python3
```

En Termux:

```bash
pkg install python
```

## Estructura del proyecto

```text
.
├── Lyrics-formatter.py        # GUI original
├── Lyrics-formatter_v2.py     # GUI mejorada para bloques de Holyrics
├── lyrics_formatter_curses.py # Version CLI con curses
├── README.md
```

## Autor

Washington Indacochea Delgado

Proyecto pensado para uso practico en iglesias y musicos.

## Licencia

GPL 3

Libre uso y modificacion.
