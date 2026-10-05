"""
AlgoLens PyQt6 Desktop Application
==================================
Standalone desktop UI showcasing the algorithm engine, execution traces,
and pedagogical inspection via PyQt6.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QLabel, QLineEdit, QSlider, QTableWidget,
    QTableWidgetItem, QTextEdit, QListWidget, QSplitter, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

from algolens.algorithms.registry import AlgorithmRegistry
from algolens.algorithms.steps import ExecutionTrace, AlgorithmStep
from algolens.validation.validators import InputValidator
from algolens.data.datasets import DatasetGenerator
from .widgets import ArrayCanvas


DARK_STYLESHEET = """
QMainWindow {
    background-color: #0C1322;
}
QWidget {
    background-color: #0C1322;
    color: #DCE2F7;
    font-family: 'Helvetica Neue', Arial, sans-serif;
}
QComboBox, QLineEdit {
    background-color: #141B2B;
    border: 1px solid #232A3A;
    border-radius: 4px;
    padding: 6px 10px;
    color: #4CD7F6;
    font-size: 13px;
}
QComboBox::drop-down {
    border: none;
}
QPushButton {
    background-color: #1E293B;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 6px 14px;
    color: #F8FAFC;
    font-weight: bold;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #2E3545;
    border-color: #06B6D4;
}
QPushButton#btn_play {
    background-color: #06B6D4;
    color: #003640;
    border: none;
}
QPushButton#btn_play:hover {
    background-color: #4CD7F6;
}
QTableWidget, QListWidget, QTextEdit {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 6px;
    gridline-color: #1F2937;
    color: #DCE2F7;
}
QTableWidget::item {
    padding: 4px;
}
QHeaderView::section {
    background-color: #0F172A;
    color: #94A3B8;
    border: 1px solid #1F2937;
    padding: 4px;
    font-weight: bold;
}
"""


class AlgoLensMainWindow(QMainWindow):
    """Main window for Sorted desktop edition."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorted — Look Inside the Algorithm (Desktop Edition)")
        self.resize(1200, 800)
        self.setStyleSheet(DARK_STYLESHEET)

        self.current_trace: ExecutionTrace = None
        self.current_step_idx = 0
        self.is_playing = False

        # Timer for playback
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.step_forward)

        self.init_ui()
        self.load_default_algorithm()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # 1. Top Header Bar
        header_layout = QHBoxLayout()
        title_label = QLabel("⚡ Sorted Desktop")
        title_label.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #4CD7F6;")

        badge = QLabel("IDE v3.12 • Engine Native")
        badge.setStyleSheet("background-color: #191F2F; color: #FFB95F; padding: 4px 8px; border-radius: 4px; font-size: 11px;")

        header_layout.addWidget(title_label)
        header_layout.addWidget(badge)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # 2. Control Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        # Algorithm selection
        self.algo_combo = QComboBox()
        for algo in AlgorithmRegistry.get_all():
            self.algo_combo.addItem(f"{algo.name} ({algo.category})", algo.name)
        self.algo_combo.currentIndexChanged.connect(self.on_algorithm_changed)
        toolbar.addWidget(QLabel("Algorithm:"))
        toolbar.addWidget(self.algo_combo)

        # Dataset input
        toolbar.addWidget(QLabel("Array:"))
        self.data_input = QLineEdit("45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 93, 8")
        self.data_input.setMinimumWidth(220)
        toolbar.addWidget(self.data_input)

        btn_run = QPushButton("Load & Run")
        btn_run.clicked.connect(self.run_algorithm)
        toolbar.addWidget(btn_run)

        toolbar.addSpacing(15)

        # VCR Buttons
        self.btn_back = QPushButton("◀ Step Back")
        self.btn_back.clicked.connect(self.step_backward)
        toolbar.addWidget(self.btn_back)

        self.btn_play = QPushButton("▶ Play")
        self.btn_play.setObjectName("btn_play")
        self.btn_play.clicked.connect(self.toggle_play)
        toolbar.addWidget(self.btn_play)

        self.btn_next = QPushButton("Step Forward ▶")
        self.btn_next.clicked.connect(self.step_forward)
        toolbar.addWidget(self.btn_next)

        btn_reset = QPushButton("Reset")
        btn_reset.clicked.connect(self.reset_playback)
        toolbar.addWidget(btn_reset)

        main_layout.addLayout(toolbar)

        # 3. Main Splitter (Left: Canvas & Metrics, Right: Code & Watch)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Container
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Array Canvas
        self.canvas = ArrayCanvas()
        left_layout.addWidget(self.canvas, stretch=3)

        # Step explanation card
        self.explanation_box = QTextEdit()
        self.explanation_box.setReadOnly(True)
        self.explanation_box.setMaximumHeight(80)
        self.explanation_box.setStyleSheet("background-color: #111827; border: 1px solid #1F2937; color: #DCE2F7; padding: 6px; font-size: 13px;")
        left_layout.addWidget(self.explanation_box, stretch=1)

        # Timeline Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.on_slider_moved)
        left_layout.addWidget(self.slider)

        splitter.addWidget(left_widget)

        # Right Container (Code & Memory Watch)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Code Viewer
        right_layout.addWidget(QLabel("Algorithm Source Code:"))
        self.code_list = QListWidget()
        self.code_list.setFont(QFont("Monospace", 11))
        right_layout.addWidget(self.code_list, stretch=2)

        # Memory Watch
        right_layout.addWidget(QLabel("Variable Watch & Scope:"))
        self.vars_table = QTableWidget(0, 2)
        self.vars_table.setHorizontalHeaderLabels(["Variable", "Value"])
        self.vars_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(self.vars_table, stretch=1)

        splitter.addWidget(right_widget)
        splitter.setSizes([750, 450])

        main_layout.addWidget(splitter, stretch=1)

        # Status Bar
        self.status_label = QLabel("Ready.")
        self.status_label.setStyleSheet("color: #869397; font-size: 11px;")
        main_layout.addWidget(self.status_label)

    def load_default_algorithm(self):
        self.run_algorithm()

    def on_algorithm_changed(self):
        self.run_algorithm()

    def run_algorithm(self):
        algo_name = self.algo_combo.currentData()
        try:
            raw_text = self.data_input.text()
            data = InputValidator.parse_array_input(raw_text)
            algo = AlgorithmRegistry.get(algo_name)

            # Load source code into code view
            self.code_list.clear()
            for line in algo.source_code:
                self.code_list.addItem(line)

            # Extra kwargs (e.g. search target)
            kwargs = {}
            if algo.category == "Searching":
                kwargs['target'] = data[len(data) // 2] if data else 42

            self.current_trace = algo.execute(data, **kwargs)
            self.current_step_idx = 0
            self.slider.setMaximum(len(self.current_trace.steps) - 1)
            self.slider.setValue(0)
            self.show_step(0)
        except Exception as e:
            self.explanation_box.setText(f"Error: {str(e)}")

    def show_step(self, idx: int):
        if not self.current_trace or not self.current_trace.steps:
            return

        idx = max(0, min(idx, len(self.current_trace.steps) - 1))
        self.current_step_idx = idx
        step: AlgorithmStep = self.current_trace.steps[idx]

        self.canvas.update_step(step)
        self.explanation_box.setText(f"[{step.operation}] Line {step.code_line}: {step.explanation}")

        # Highlight code line
        if 1 <= step.code_line <= self.code_list.count():
            self.code_list.setCurrentRow(step.code_line - 1)

        # Update variable watch table
        vars_dict = dict(step.variables)
        for p_name, p_val in step.pointers.items():
            vars_dict[f"ptr_{p_name}"] = p_val
        if step.pivot:
            vars_dict["pivot"] = step.pivot.get('value')

        self.vars_table.setRowCount(len(vars_dict))
        for row_idx, (k, v) in enumerate(vars_dict.items()):
            self.vars_table.setItem(row_idx, 0, QTableWidgetItem(str(k)))
            self.vars_table.setItem(row_idx, 1, QTableWidgetItem(str(v)))

        # Update status
        self.status_label.setText(
            f"Step {step.step_number} / {self.current_trace.total_steps} | "
            f"Comparisons: {step.metrics.get('comparisons', 0)} | "
            f"Swaps: {step.metrics.get('swaps', 0)}"
        )

    def on_slider_moved(self, value):
        self.show_step(value)

    def step_forward(self):
        if self.current_trace and self.current_step_idx < len(self.current_trace.steps) - 1:
            self.slider.setValue(self.current_step_idx + 1)
        else:
            if self.is_playing:
                self.toggle_play()

    def step_backward(self):
        if self.current_trace and self.current_step_idx > 0:
            self.slider.setValue(self.current_step_idx - 1)

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.btn_play.setText("⏸ Pause")
            self.timer.start(400)
        else:
            self.btn_play.setText("▶ Play")
            self.timer.stop()

    def reset_playback(self):
        if self.is_playing:
            self.toggle_play()
        self.slider.setValue(0)


def main():
    app = QApplication(sys.argv)
    window = AlgoLensMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
