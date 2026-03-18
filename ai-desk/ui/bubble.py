from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, pyqtProperty, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QLinearGradient, QBrush, QFont


class BubbleLabel(QLabel):
    """单条气泡"""
    def __init__(self, text, is_user, theme_start="#4facfe", theme_end="#00f2fe", parent=None):
        super().__init__(text, parent)
        self.is_user = is_user
        self.theme_start = theme_start
        self.theme_end = theme_end
        self.setWordWrap(True)
        self.setMaximumWidth(420)
        self.setFont(QFont("Microsoft YaHei UI", 10))
        self.setContentsMargins(14, 10, 14, 10)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.setStyleSheet(f"""
            color: {'white' if is_user else 'rgba(220, 220, 220, 230)'};
            line-height: 140%;
        """)
        if is_user:
            self.setStyleSheet("color: white;")
        else:
            self.setStyleSheet("color: rgba(220, 220, 220, 230);")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        if self.is_user:
            grad = QLinearGradient(0, 0, self.width(), 0)
            grad.setColorAt(0, QColor(self.theme_start))
            grad.setColorAt(1, QColor(self.theme_end))
            painter.fillPath(path, QBrush(grad))
        else:
            painter.fillPath(path, QColor(255, 255, 255, 18))
        super().paintEvent(event)


class TypingBubble(QWidget):
    """AI 正在输入中气泡，带三点动画"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._dot_count = 1
        self.label = QLabel("●", self)
        self.label.setFont(QFont("Segoe UI Variable Display", 11))
        self.label.setStyleSheet("color: rgba(200, 200, 200, 180); background: transparent;")
        self.label.setContentsMargins(14, 10, 14, 10)
        self.setFixedHeight(44)
        self.setMinimumWidth(70)
        self.setMaximumWidth(120)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(500)

    def _tick(self):
        self._dot_count = self._dot_count % 3 + 1
        self.label.setText("●" * self._dot_count)
        self.label.adjustSize()

    def resizeEvent(self, event):
        self.label.resize(self.size())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        painter.fillPath(path, QColor(255, 255, 255, 18))

    def stop(self):
        self._timer.stop()


class BubbleRow(QWidget):
    """包裹气泡，控制左右对齐"""
    def __init__(self, bubble, is_user, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)
        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()