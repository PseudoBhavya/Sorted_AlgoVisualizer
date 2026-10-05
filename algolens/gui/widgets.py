"""
AlgoLens PyQt6 Visualizer Widgets
=================================
Custom QPainter widget rendering the dynamic array visualization in PyQt6.
Adheres to the Stitch color palette and dark aesthetic.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QRectF
from algolens.algorithms.steps import AlgorithmStep


class ArrayCanvas(QWidget):
    """Custom painted canvas rendering array bars, pointers, and swap curves."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.step: AlgorithmStep = None
        self.setMinimumHeight(280)
        self.setStyleSheet("background-color: #0F172A; border-radius: 8px;")

    def update_step(self, step: AlgorithmStep):
        """Update active step and trigger repaint."""
        self.step = step
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.fillRect(self.rect(), QColor("#0F172A"))

        if not self.step or not self.step.array_state:
            painter.setPen(QColor("#94A3B8"))
            painter.setFont(QFont("Monospace", 12))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Active Algorithm Step")
            return

        arr = self.step.array_state
        n = len(arr)
        if n == 0:
            return

        max_val = max([float(x) for x in arr] + [1.0])
        w = self.width()
        h = self.height()

        margin_x = 30
        margin_bottom = 60
        margin_top = 40
        usable_w = w - (2 * margin_x)
        usable_h = h - margin_bottom - margin_top

        slot_w = usable_w / n
        bar_w = max(slot_w * 0.75, 12.0)
        spacing = (slot_w - bar_w) / 2.0

        pivot_idx = self.step.pivot.get('index') if self.step.pivot else None
        swap_a = self.step.swap.get('index_a') if self.step.swap else None
        swap_b = self.step.swap.get('index_b') if self.step.swap else None
        active_indices = set(self.step.active_indices or [])
        sorted_indices = set(self.step.sorted_indices or [])
        pointers = self.step.pointers or {}

        # Draw Swap Arc if swap is active
        if swap_a is not None and swap_b is not None and swap_a != swap_b:
            x1 = margin_x + swap_a * slot_w + slot_w / 2.0
            x2 = margin_x + swap_b * slot_w + slot_w / 2.0
            mid_x = (x1 + x2) / 2.0
            arc_top = margin_top - 20

            path = QPainterPath()
            path.moveTo(x1, margin_top + 10)
            path.quadTo(mid_x, arc_top, x2, margin_top + 10)

            pen = QPen(QColor("#F43F5E"), 2, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawPath(path)

            # Draw "SWAP" pill
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#93000A")))
            pill_rect = QRectF(mid_x - 30, arc_top - 8, 60, 20)
            painter.drawRoundedRect(pill_rect, 10, 10)

            painter.setPen(QColor("#FFDAD6"))
            painter.setFont(QFont("Monospace", 9, QFont.Weight.Bold))
            painter.drawText(pill_rect, Qt.AlignmentFlag.AlignCenter, "⇄ SWAP")

        # Draw bars
        for i, val in enumerate(arr):
            x = margin_x + i * slot_w + spacing
            val_f = float(val)
            bar_h = max(20.0, (val_f / max_val) * usable_h)
            y = margin_top + usable_h - bar_h

            is_pivot = (i == pivot_idx)
            is_swapping = (i == swap_a or i == swap_b)
            is_active = (i in active_indices and not is_pivot and not is_swapping)
            is_sorted = (i in sorted_indices)

            # Determine bar color
            if is_pivot:
                fill_color = QColor("#F59E0B")
                border_color = QColor("#FFDDB8")
            elif is_swapping:
                fill_color = QColor("#F43F5E")
                border_color = QColor("#FFB4AB")
            elif is_active:
                fill_color = QColor("#06B6D4")
                border_color = QColor("#4CD7F6")
            elif is_sorted:
                fill_color = QColor("#10B981")
                border_color = QColor("#A7F3D0")
            else:
                fill_color = QColor("#232A3A")
                border_color = QColor("#374151")

            rect = QRectF(x, y, bar_w, bar_h)
            painter.setPen(QPen(border_color, 1.5))
            painter.setBrush(QBrush(fill_color))
            painter.drawRoundedRect(rect, 4, 4)

            # Value label
            painter.setPen(QColor("#FFFFFF" if (is_pivot or is_swapping or is_active) else "#BCC9CD"))
            painter.setFont(QFont("Monospace", 10, QFont.Weight.Bold))
            painter.drawText(QRectF(x - 5, y + 4, bar_w + 10, 18), Qt.AlignmentFlag.AlignHCenter, str(val))

            # Index label [i]
            idx_y = margin_top + usable_h + 8
            painter.setPen(QColor("#94A3B8"))
            painter.setFont(QFont("Monospace", 9))
            painter.drawText(QRectF(x - 10, idx_y, bar_w + 20, 16), Qt.AlignmentFlag.AlignHCenter, f"[{i}]")

            # Pointers label
            ptrs = [k for k, v in pointers.items() if v == i]
            if is_pivot and "pivot" not in ptrs:
                ptrs.append("pvt")
            if ptrs:
                ptr_text = " • ".join(ptrs)
                painter.setPen(QColor("#F59E0B" if is_pivot else ("#F43F5E" if is_swapping else "#06B6D4")))
                painter.setFont(QFont("Monospace", 8, QFont.Weight.Bold))
                painter.drawText(QRectF(x - 15, idx_y + 18, bar_w + 30, 16), Qt.AlignmentFlag.AlignHCenter, ptr_text)
