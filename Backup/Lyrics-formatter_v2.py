import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QPlainTextEdit, QLabel,
                             QSpinBox, QFileDialog, QSplitter, QStatusBar,
                             QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent

class CustomPlainTextEdit(QPlainTextEdit):
    """QPlainTextEdit que deja que la ventana principal gestione archivos soltados."""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setAcceptDrops(False)
        self.setPlaceholderText(placeholder)
        self.setFont(QFont("Segoe UI", 11))
        self.setStyleSheet("QPlainTextEdit { border: 2px dashed #aaa; padding: 8px; background: #f9f9f9; }")

class LyricsFormatterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formateador de Letras para Proyector")
        self.resize(1050, 650)
        self.setAcceptDrops(True)
        self.current_file = None
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # ── Barra de controles ──
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(QLabel("Máx. caracteres:"))
        self.spin_chars = QSpinBox()
        self.spin_chars.setRange(10, 30)
        self.spin_chars.setValue(10)
        ctrl_layout.addWidget(self.spin_chars)

        ctrl_layout.addWidget(QLabel("Máx. palabras cortas:"))
        self.spin_words = QSpinBox()
        self.spin_words.setRange(1, 5)
        self.spin_words.setValue(3)
        ctrl_layout.addWidget(self.spin_words)

        self.btn_format = QPushButton("🔹 Formatear")
        self.btn_format.setStyleSheet("background-color: #0078d7; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold;")
        self.btn_format.clicked.connect(self.format_text)

        self.btn_load = QPushButton("📂 Cargar")
        self.btn_load.clicked.connect(self.load_file)

        self.btn_save = QPushButton("💾 Guardar")
        self.btn_save.clicked.connect(self.save_file)

        self.btn_clear = QPushButton("🗑️ Limpiar")
        self.btn_clear.clicked.connect(self.clear_all)

        for btn in [self.btn_load, self.btn_format, self.btn_save, self.btn_clear]:
            ctrl_layout.addWidget(btn)
        ctrl_layout.addStretch()
        main_layout.addLayout(ctrl_layout)

        # ── Área dividida ──
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.input_edit = CustomPlainTextEdit("Arrastra un archivo .txt aquí o pega el texto original...")
        self.input_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        self.output_edit = QPlainTextEdit()
        self.output_edit.setAcceptDrops(False)
        self.output_edit.setReadOnly(True)
        self.output_edit.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.output_edit.setStyleSheet("QPlainTextEdit { background-color: #000; color: #fff; padding: 10px; }")
        self.output_edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        splitter.addWidget(self.input_edit)
        splitter.addWidget(self.output_edit)
        splitter.setSizes([500, 550])
        main_layout.addWidget(splitter)

        self.statusBar().showMessage("✅ Listo. Arrastra un archivo o usa los botones.")

    def format_line(self, line: str, max_chars: int, max_words: int) -> list[str]:
        words = line.strip().split()
        if not words:
            return [""]

        formatted_lines = []
        current_words = []
        current_len = 0
        connector_words = {"y", "e", "o", "u"}

        for index, word in enumerate(words):
            w_len = len(word)
            space = 1 if current_words else 0
            total = current_len + space + w_len
            has_next_word = index < len(words) - 1

            exceeds_chars = total > max_chars
            exceeds_words = len(current_words) >= max_words
            long_word_with_company = current_words and w_len > 7
            line_would_end_with_connector = (
                has_next_word
                and current_words
                and word.lower() in connector_words
                and total >= max_chars
            )

            if exceeds_chars or exceeds_words or long_word_with_company or line_would_end_with_connector:
                formatted_lines.append(" ".join(current_words))
                current_words = [word]
                current_len = w_len
            else:
                current_words.append(word)
                current_len = total

        if current_words:
            formatted_lines.append(" ".join(current_words))

        return formatted_lines

    def add_section(self, result: list[str], comment: str | None, lyric_groups: list[list[str]]):
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

        parts = []
        current_part = []
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
                result.append("")

            result.append(f"{clean_comment} (Parte {index})")
            result.extend(part_lines)

    def format_lyrics(self, text: str, max_chars: int, max_words: int) -> str:
        lines = text.splitlines()
        result = []
        current_comment = None
        current_lyrics = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("//"):
                self.add_section(result, current_comment, current_lyrics)
                current_comment = stripped
                current_lyrics = []
                continue

            if not stripped:
                self.add_section(result, current_comment, current_lyrics)
                current_comment = None
                current_lyrics = []
                if result and result[-1] != "":
                    result.append("")
                continue

            current_lyrics.append(self.format_line(stripped, max_chars, max_words))

        self.add_section(result, current_comment, current_lyrics)

        return "\n".join(result)

    def open_dropped_file(self, file_path):
        if not os.path.exists(file_path) or not file_path.lower().endswith('.txt'):
            QMessageBox.warning(self, "Archivo no válido", "Solo se pueden abrir archivos .txt.")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.input_edit.setPlainText(f.read())
            self.current_file = file_path
            self.output_edit.clear()
            self.statusBar().showMessage(f"📄 Cargado: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error al abrir", f"No se pudo abrir el archivo:\n{e}")
            self.statusBar().showMessage(f"❌ Error: {e}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            self.open_dropped_file(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def format_text(self):
        raw = self.input_edit.toPlainText()
        if not raw.strip():
            self.statusBar().showMessage("⚠️ No hay texto para formatear.")
            return
        formatted = self.format_lyrics(raw, self.spin_chars.value(), self.spin_words.value())
        self.output_edit.setPlainText(formatted)
        self.statusBar().showMessage("✅ Texto formateado correctamente.")

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Textos (*.txt)")
        if path:
            self.open_dropped_file(path)

    def save_file(self):
        text = self.output_edit.toPlainText()
        if not text.strip():
            self.statusBar().showMessage("⚠️ Nada que guardar.")
            return

        default_name = "letra_arreglada.txt"
        if self.current_file:
            folder = os.path.dirname(self.current_file)
            base_name = os.path.basename(self.current_file)
            name, ext = os.path.splitext(base_name)
            default_name = os.path.join(folder, f"{name} - fixed{ext or '.txt'}")

        path, _ = QFileDialog.getSaveFileName(self, "Guardar como", default_name, "Textos (*.txt)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.statusBar().showMessage(f"💾 Guardado: {path}")
            except Exception as e:
                self.statusBar().showMessage(f"❌ Error al guardar: {e}")

    def clear_all(self):
        self.input_edit.clear()
        self.output_edit.clear()
        self.current_file = None
        self.statusBar().showMessage("🗑️ Todo limpio.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = LyricsFormatterApp()
    window.show()
    sys.exit(app.exec())
