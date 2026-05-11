# Song-Lyrics-formatter-for-Holyrics

**Español:** si prefieres leer esta documentación en español, abre
[README_ES.md](README_ES.md).

Song lyrics formatter designed to prepare text files for projection with
Holyrics in churches, meetings, and presentations.

The program helps lyrics stay easy to read on screen: it splits long lines,
respects Holyrics `//` comments, and creates short blocks so projected text does
not become too small.

## Included Scripts

This repository includes two versions of the same formatter:

- `Lyrics_formatter.py`: graphical version built with PyQt6.
- `lyrics_formatter_curses.py`: terminal version built with curses.

Both versions use the same formatting logic.

## What The Formatter Does

- Reads lyrics from `.txt` files.
- Also allows manual text input in the GUI version.
- Splits long phrases into short lines.
- Keeps Holyrics comments that start with `//`.
- Automatically creates parts when a section goes over 6 lines.
- Leaves exactly one blank line between blocks, as a separator for Holyrics.
- Saves the result as a new `.txt` file.

## Holyrics Rule

Holyrics uses comments like this to separate sections:

```text
//Verse I
They say there are few and I know it
Few are like you
Genuine and true warrior
```

The formatter converts that section into parts:

```text
//Verse I (Parte 1)
They say
there are
few and
I know it

//Verse I (Parte 2)
Few are
like you

//Verse I (Parte 3)
Genuine
and true
warrior
```

Each part contains up to 6 lyric lines. If an original phrase does not fit in
the current block, it is moved complete to the next block, even if the previous
block ends with fewer than 6 lines. This avoids unnatural cuts inside the same
idea.

## GUI Version

The graphical version is the most comfortable option for visual editing:

```bash
python3 Lyrics_formatter.py
```

It can:

- load `.txt` files,
- drag and drop files,
- paste lyrics manually,
- preview the result with a black background,
- adjust maximum characters per line,
- adjust maximum short words per line,
- save the formatted result.

Requirement on Debian, Ubuntu, MX Linux, or derivatives:

```bash
sudo apt install python3 python3-pyqt6
```

## Terminal Version

The terminal version is useful for Termux, servers, lightweight systems, or
working without a graphical desktop:

```bash
python3 lyrics_formatter_curses.py
```

You can also open a specific folder:

```bash
python3 lyrics_formatter_curses.py /path/to/folder
```

When you select a `.txt` file, it saves a formatted copy using this name:

```text
name - fixed.txt
```

### Controls

```text
Up / Down      move selection
Enter          open folder / select file
Backspace      go to parent folder
c / C          decrease/increase characters
w / W          decrease/increase short words
h              help
q              quit
```

Requirement:

```bash
sudo apt install python3
```

On Termux:

```bash
pkg install python
```

## Default Values

Both versions start with these values:

- 10 maximum characters per line.
- 3 maximum short words per line.
- 6 maximum lyric lines per block under each `//` comment.

## Project Structure

```text
.
├── Lyrics_formatter.py        # GUI version with PyQt6
├── lyrics_formatter_curses.py # Terminal version with curses
├── README.md                  # English documentation
├── README_ES.md               # Spanish documentation
```

## Author

Washington Indacochea Delgado

Project designed for practical use in churches and by musicians.

## License

GPL 3

Free to use and modify.
