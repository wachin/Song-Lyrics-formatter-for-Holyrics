#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lyrics_formatter_curses.py

Versión CLI/TUI con curses del Formateador de Letras para Proyector.
Pensado para Termux en Android, Linux y otros sistemas con Python + curses.

Controles principales:
  ↑ / ↓        Mover selección
  Enter        Entrar a carpeta o seleccionar archivo .txt
  Backspace    Subir a la carpeta anterior
  c / C        Cambiar máximo de caracteres por línea
  w / W        Cambiar máximo de palabras cortas por línea
  h            Ayuda
  q            Salir

Al seleccionar un archivo .txt, el programa lo formatea y lo guarda como:
  nombre - fixed.txt

También puedes indicar una carpeta inicial:
  python3 lyrics_formatter_curses.py /sdcard/Download
"""

from __future__ import annotations

import curses
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple


DEFAULT_MAX_CHARS = 10
DEFAULT_MAX_WORDS = 3
MIN_CHARS = 10
MAX_CHARS = 30
MIN_WORDS = 1
MAX_WORDS = 5


class AppState:
    def __init__(self, start_dir: Path) -> None:
        self.current_dir = start_dir.expanduser().resolve()
        self.selected = 0
        self.scroll = 0
        self.max_chars = DEFAULT_MAX_CHARS
        self.max_words = DEFAULT_MAX_WORDS
        self.message = "Selecciona un archivo .txt"
        self.running = True


def format_line(line: str, max_chars: int, max_words: int) -> list[str]:
    """Divide una frase en líneas cortas para que se lea mejor al proyectarse."""
    words = line.strip().split()
    if not words:
        return [""]

    formatted_lines: list[str] = []
    current_words: list[str] = []
    current_len = 0
    connector_words = {"y", "e", "o", "u"}

    for index, word in enumerate(words):
        word_len = len(word)
        space = 1 if current_words else 0
        total = current_len + space + word_len
        has_next_word = index < len(words) - 1

        exceeds_chars = total > max_chars
        exceeds_words = len(current_words) >= max_words
        long_word_with_company = bool(current_words) and word_len > 7
        line_would_end_with_connector = (
            has_next_word
            and bool(current_words)
            and word.lower() in connector_words
            and total >= max_chars
        )

        if exceeds_chars or exceeds_words or long_word_with_company or line_would_end_with_connector:
            formatted_lines.append(" ".join(current_words))
            current_words = [word]
            current_len = word_len
        else:
            current_words.append(word)
            current_len = total

    if current_words:
        formatted_lines.append(" ".join(current_words))

    return formatted_lines


def add_section(result: list[str], comment: Optional[str], lyric_groups: list[list[str]]) -> None:
    """Agrega una sección en partes de máximo 6 líneas bajo cada comentario //."""
    if not lyric_groups:
        if comment:
            result.append(comment)
        return

    if not comment:
        for group in lyric_groups:
            result.extend(group)
        return

    clean_comment = comment
    for part in range(1, 1000):
        marker = f" (Parte {part})"
        if clean_comment.endswith(marker):
            clean_comment = clean_comment[:-len(marker)]
            break

    parts: list[list[str]] = []
    current_part: list[str] = []
    current_line_count = 0

    for group in lyric_groups:
        if not group:
            continue

        if len(group) > 6:
            if current_part:
                parts.append(current_part)
                current_part = []
                current_line_count = 0

            for start in range(0, len(group), 6):
                parts.append(group[start:start + 6])
            continue

        if current_part and current_line_count + len(group) > 6:
            parts.append(current_part)
            current_part = []
            current_line_count = 0

        current_part.extend(group)
        current_line_count += len(group)

    if current_part:
        parts.append(current_part)

    for index, part_lines in enumerate(parts, start=1):
        if index > 1:
            result.append("")

        result.append(f"{clean_comment} (Parte {index})")
        result.extend(part_lines)


def format_lyrics(text: str, max_chars: int = DEFAULT_MAX_CHARS, max_words: int = DEFAULT_MAX_WORDS) -> str:
    """
    Formatea letras con la misma lógica de la versión gráfica:
    - Divide frases en líneas cortas.
    - Mantiene juntas las frases originales cuando caben en el bloque.
    - Cada comentario // genera partes de máximo 6 líneas de letra.
    - Entre parte y parte deja una sola línea vacía para Holyrics.
    """
    lines = text.splitlines()
    result: list[str] = []
    current_comment: Optional[str] = None
    current_lyrics: list[list[str]] = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("//"):
            add_section(result, current_comment, current_lyrics)
            current_comment = stripped
            current_lyrics = []
            continue

        if not stripped:
            add_section(result, current_comment, current_lyrics)
            current_comment = None
            current_lyrics = []
            if result and result[-1] != "":
                result.append("")
            continue

        current_lyrics.append(format_line(stripped, max_chars, max_words))

    add_section(result, current_comment, current_lyrics)

    return "\n".join(result)


def safe_addstr(win: curses.window, y: int, x: int, text: str, attr: int = 0) -> None:
    """Escribe texto sin romper curses cuando la pantalla es pequeña."""
    height, width = win.getmaxyx()
    if y < 0 or y >= height or x < 0 or x >= width:
        return
    available = max(0, width - x - 1)
    if available <= 0:
        return
    try:
        win.addstr(y, x, text[:available], attr)
    except curses.error:
        pass


def list_entries(current_dir: Path) -> List[Tuple[str, Path, str]]:
    """
    Devuelve carpetas y archivos .txt.
    kind puede ser: 'parent', 'dir', 'txt'.
    """
    entries: list[tuple[str, Path, str]] = []

    if current_dir.parent != current_dir:
        entries.append(("[..] Subir", current_dir.parent, "parent"))

    dirs: list[tuple[str, Path, str]] = []
    txts: list[tuple[str, Path, str]] = []

    try:
        for item in current_dir.iterdir():
            try:
                if item.is_dir():
                    dirs.append((f"[D] {item.name}", item, "dir"))
                elif item.is_file() and item.suffix.lower() == ".txt":
                    txts.append((f"[TXT] {item.name}", item, "txt"))
            except OSError:
                continue
    except PermissionError:
        return entries + [("[Sin permiso para leer esta carpeta]", current_dir, "info")]
    except OSError as error:
        return entries + [(f"[Error: {error}]", current_dir, "info")]

    dirs.sort(key=lambda x: x[0].lower())
    txts.sort(key=lambda x: x[0].lower())
    return entries + dirs + txts


def default_output_name(input_file: Path) -> Path:
    suffix = input_file.suffix or ".txt"
    return input_file.with_name(f"{input_file.stem} - fixed{suffix}")


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Algunos .txt viejos pueden venir en latin-1. Esto evita que el programa falle.
        return path.read_text(encoding="latin-1")


def confirm_dialog(stdscr: curses.window, title: str, lines: list[str]) -> bool:
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    safe_addstr(stdscr, 1, 2, title, curses.A_BOLD)
    y = 3
    for line in lines:
        safe_addstr(stdscr, y, 2, line)
        y += 1
    safe_addstr(stdscr, height - 3, 2, "Enter = aceptar    Esc/q = cancelar", curses.A_REVERSE)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (10, 13, curses.KEY_ENTER):
            return True
        if key in (27, ord("q"), ord("Q")):
            return False


def show_message(stdscr: curses.window, title: str, lines: list[str]) -> None:
    stdscr.clear()
    height, _ = stdscr.getmaxyx()
    safe_addstr(stdscr, 1, 2, title, curses.A_BOLD)
    y = 3
    for line in lines:
        safe_addstr(stdscr, y, 2, line)
        y += 1
    safe_addstr(stdscr, height - 3, 2, "Presiona cualquier tecla para continuar", curses.A_REVERSE)
    stdscr.refresh()
    stdscr.getch()


def show_help(stdscr: curses.window) -> None:
    show_message(
        stdscr,
        "Ayuda - Formateador de Letras TUI",
        [
            "Este programa muestra carpetas y archivos .txt.",
            "Enter abre carpetas o selecciona un .txt.",
            "Al seleccionar un .txt se guarda una copia formateada.",
            "Nombre de salida: nombre - fixed.txt",
            "",
            "Controles:",
            "  Flechas arriba/abajo: mover selección",
            "  Enter: abrir carpeta o formatear archivo",
            "  Backspace: subir carpeta",
            "  c / C: bajar/subir máximo de caracteres",
            "  w / W: bajar/subir máximo de palabras cortas",
            "  h: ayuda",
            "  q: salir",
        ],
    )


def process_txt_file(stdscr: curses.window, path: Path, state: AppState) -> None:
    output_path = default_output_name(path)

    if not confirm_dialog(
        stdscr,
        "Formatear archivo",
        [
            f"Entrada: {path}",
            f"Salida:  {output_path}",
            "",
            f"Max. caracteres: {state.max_chars}",
            f"Max. palabras cortas: {state.max_words}",
            "",
            "Se conservara el archivo original.",
        ],
    ):
        state.message = "Operacion cancelada"
        return

    try:
        raw_text = read_utf8(path)
        formatted = format_lyrics(raw_text, state.max_chars, state.max_words)
        output_path.write_text(formatted, encoding="utf-8")
        show_message(
            stdscr,
            "Archivo guardado correctamente",
            [
                f"Se guardo:",
                str(output_path),
                "",
                "El archivo original no fue modificado.",
            ],
        )
        state.message = f"Guardado: {output_path.name}"
    except OSError as error:
        show_message(stdscr, "Error", [f"No se pudo procesar el archivo:", str(error)])
        state.message = f"Error: {error}"


def draw(stdscr: curses.window, state: AppState, entries: list[tuple[str, Path, str]]) -> None:
    stdscr.erase()
    height, width = stdscr.getmaxyx()

    title = "Formateador de Letras para Proyector - Selector .txt"
    safe_addstr(stdscr, 0, 2, title[: max(0, width - 4)], curses.A_BOLD)
    safe_addstr(stdscr, 1, 2, f"Carpeta: {state.current_dir}")
    safe_addstr(
        stdscr,
        2,
        2,
        f"Max chars: {state.max_chars}   Max palabras cortas: {state.max_words}   h=ayuda   q=salir",
    )
    safe_addstr(stdscr, 3, 0, "-" * max(1, width - 1))

    list_top = 4
    list_bottom = height - 3
    visible_rows = max(1, list_bottom - list_top)

    if state.selected < state.scroll:
        state.scroll = state.selected
    elif state.selected >= state.scroll + visible_rows:
        state.scroll = state.selected - visible_rows + 1

    visible = entries[state.scroll : state.scroll + visible_rows]
    for row, (name, _path, kind) in enumerate(visible, start=list_top):
        absolute_index = state.scroll + (row - list_top)
        attr = curses.A_REVERSE if absolute_index == state.selected else curses.A_NORMAL
        if kind == "txt":
            attr |= curses.A_BOLD
        safe_addstr(stdscr, row, 2, name, attr)

    safe_addstr(stdscr, height - 2, 0, "-" * max(1, width - 1))
    safe_addstr(stdscr, height - 1, 2, state.message, curses.A_REVERSE)
    stdscr.refresh()


def normalize_start_dir(argv: list[str]) -> Path:
    if len(argv) > 1:
        candidate = Path(argv[1]).expanduser()
        if candidate.is_file():
            return candidate.parent.resolve()
        if candidate.is_dir():
            return candidate.resolve()
        print(f"No existe la ruta: {candidate}", file=sys.stderr)
        raise SystemExit(1)

    # Termux suele tener archivos de usuario en /sdcard, pero usamos cwd por seguridad.
    return Path.cwd().resolve()


def run(stdscr: curses.window, start_dir: Path) -> None:
    curses.curs_set(0)
    stdscr.keypad(True)
    state = AppState(start_dir)

    while state.running:
        entries = list_entries(state.current_dir)
        if not entries:
            entries = [("[Carpeta vacia o sin archivos .txt]", state.current_dir, "info")]

        state.selected = max(0, min(state.selected, len(entries) - 1))
        draw(stdscr, state, entries)
        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            state.running = False
        elif key in (ord("h"), ord("H")):
            show_help(stdscr)
        elif key == curses.KEY_UP:
            state.selected = max(0, state.selected - 1)
        elif key == curses.KEY_DOWN:
            state.selected = min(len(entries) - 1, state.selected + 1)
        elif key == curses.KEY_NPAGE:
            state.selected = min(len(entries) - 1, state.selected + 10)
        elif key == curses.KEY_PPAGE:
            state.selected = max(0, state.selected - 10)
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if state.current_dir.parent != state.current_dir:
                state.current_dir = state.current_dir.parent
                state.selected = 0
                state.scroll = 0
                state.message = "Subiste una carpeta"
        elif key == ord("c"):
            state.max_chars = max(MIN_CHARS, state.max_chars - 1)
            state.message = f"Max. caracteres: {state.max_chars}"
        elif key == ord("C"):
            state.max_chars = min(MAX_CHARS, state.max_chars + 1)
            state.message = f"Max. caracteres: {state.max_chars}"
        elif key == ord("w"):
            state.max_words = max(MIN_WORDS, state.max_words - 1)
            state.message = f"Max. palabras cortas: {state.max_words}"
        elif key == ord("W"):
            state.max_words = min(MAX_WORDS, state.max_words + 1)
            state.message = f"Max. palabras cortas: {state.max_words}"
        elif key in (10, 13, curses.KEY_ENTER):
            name, path, kind = entries[state.selected]
            if kind in ("parent", "dir"):
                if path.is_dir():
                    state.current_dir = path.resolve()
                    state.selected = 0
                    state.scroll = 0
                    state.message = f"Carpeta: {path.name or path}"
            elif kind == "txt":
                process_txt_file(stdscr, path, state)
            else:
                state.message = name


def main() -> int:
    start_dir = normalize_start_dir(sys.argv)
    curses.wrapper(run, start_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
