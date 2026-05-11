# Song-Lyrics-formatter-for-Holyrics

Formateador de letras de canciones pensado para preparar textos que se van a
proyectar con Holyrics en iglesias, reuniones y presentaciones.

El programa ayuda a que las letras queden faciles de leer en pantalla: divide
lineas largas, respeta los comentarios `//` de Holyrics y crea bloques cortos
para que el texto no se reduzca demasiado al proyectarse.

## Scripts incluidos

Este repositorio tiene dos versiones del mismo formateador:

- `Lyrics_formatter.py`: version con interfaz grafica, hecha con PyQt6.
- `lyrics_formatter_curses.py`: version para terminal, hecha con curses.

Ambas versiones usan la misma logica de formateo.

## Que hace el formateador

- Lee letras desde archivos `.txt`.
- Tambien permite pegar texto manualmente en la version GUI.
- Divide frases largas en lineas cortas.
- Mantiene los comentarios de Holyrics que empiezan con `//`.
- Crea partes automaticamente cuando una seccion supera 6 lineas.
- Deja una sola linea vacia entre bloques, como separador para Holyrics.
- Guarda el resultado como un nuevo archivo `.txt`.

## Regla para Holyrics

Holyrics usa comentarios como este para separar secciones:

```text
//Verso I
Dicen que son pocas y me consta
Son pocas las que son como tu
Guerrera genuina y verdadera
```

El formateador convierte esa seccion en partes:

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

Cada parte tiene maximo 6 lineas de letra. Si una frase original no cabe en el
bloque actual, pasa completa al siguiente bloque aunque el bloque anterior quede
con menos de 6 lineas. Esto evita cortes poco naturales de una misma idea.

## Version GUI

La version grafica es la mas comoda para trabajar visualmente:

```bash
python3 Lyrics_formatter.py
```

Permite:

- cargar archivos `.txt`,
- arrastrar y soltar archivos,
- pegar letras manualmente,
- ver el resultado en una vista previa con fondo negro,
- ajustar caracteres maximos por linea,
- ajustar palabras cortas maximas por linea,
- guardar el resultado formateado.

Requisito en Debian, Ubuntu, MX Linux o derivados:

```bash
sudo apt install python3 python3-pyqt6
```

## Version terminal

La version de terminal es util para Termux, servidores, equipos ligeros o cuando
se prefiere trabajar sin entorno grafico:

```bash
python3 lyrics_formatter_curses.py
```

Tambien puedes abrir una carpeta especifica:

```bash
python3 lyrics_formatter_curses.py /ruta/a/carpeta
```

Al seleccionar un archivo `.txt`, se guarda una copia formateada con este nombre:

```text
nombre - fixed.txt
```

### Controles

```text
Arriba / Abajo   mover seleccion
Enter            abrir carpeta / seleccionar archivo
Backspace        subir carpeta
c / C            bajar/subir caracteres
w / W            bajar/subir palabras cortas
h                ayuda
q                salir
```

Requisito:

```bash
sudo apt install python3
```

En Termux:

```bash
pkg install python
```

## Valores por defecto

Ambas versiones empiezan con estos valores:

- 10 caracteres maximos por linea.
- 3 palabras cortas maximas por linea.
- 6 lineas maximas por bloque bajo cada comentario `//`.

## Estructura del proyecto

```text
.
├── Lyrics_formatter.py        # Version GUI con PyQt6
├── lyrics_formatter_curses.py # Version terminal con curses
├── assets/icons/              # Icono de la aplicacion
├── README.md
```

## Autor

Washington Indacochea Delgado

Proyecto pensado para uso practico en iglesias y musicos.

## Licencia

GPL 3

Libre uso y modificacion.
