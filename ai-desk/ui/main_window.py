import sys
import time
import pyperclip
import pyautogui
import keyboard  # pip install keyboard
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QFrame,
                             QSystemTrayIcon, QMenu, QAction, QScrollArea)
from ui.bubble import BubbleRow, BubbleLabel, TypingBubble
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QPoint, pyqtProperty, QRectF, QThread, pyqtSignal, QTimer
from core.mode_router import route


class AIWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, mode, text, history=None):
        super().__init__()
        self.mode = mode
        self.text = text
        self.history = history or []

    def run(self):
        try:
            result = route(self.mode, self.text, self.history)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
from PyQt5.QtGui import (QColor, QFont, QLinearGradient, QRadialGradient,
                         QBrush, QPainter, QPainterPath, QIcon, QPixmap)
from core.memory import load_profile, set_affection

# 全局快捷键监听线程
class HotkeyThread(QThread):
    triggered = pyqtSignal()

    def run(self):
        # 监听 Ctrl+Space
        keyboard.add_hotkey('ctrl+space', self.triggered.emit)
        keyboard.wait()

# 自定义滑动模式选择器
class ModeSwitcher(QWidget):
    def __init__(self, items, callback, parent=None):
        super().__init__(parent)
        self.items = items
        self.callback = callback
        self.current_index = 0
        self.setFixedSize(220, 38)
        self._slider_x = 2
        self.item_width = (self.width() - 4) / len(items)
        self.setFont(QFont("Segoe UI Variable Display", 10, QFont.Bold))

    @pyqtProperty(float)
    def slider_x(self): return self._slider_x
    @slider_x.setter
    def slider_x(self, pos):
        self._slider_x = pos
        self.update()

    def mousePressEvent(self, event):
        index = int(event.x() // self.item_width)
        if 0 <= index < len(self.items) and index != self.current_index:
            self.current_index = index
            self.anim = QPropertyAnimation(self, b"slider_x")
            self.anim.setDuration(350)
            self.anim.setEndValue(index * self.item_width + 2)
            self.anim.setEasingCurve(QEasingCurve.OutExpo)
            self.anim.start()
            self.callback(self.items[index])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 19, 19)
        painter.fillPath(path, QColor(255, 255, 255, 10))
        parent_window = self.window()
        _, start, end = parent_window.current_theme
        slider_path = QPainterPath()
        slider_rect = QRectF(self._slider_x, 3, self.item_width - 2, self.height() - 6)
        slider_path.addRoundedRect(slider_rect, 16, 16)
        grad = QLinearGradient(slider_rect.topLeft(), slider_rect.topRight())
        grad.setColorAt(0, QColor(start))
        grad.setColorAt(1, QColor(end))
        painter.fillPath(slider_path, grad)
        for i, text in enumerate(self.items):
            color = QColor(15, 15, 20) if i == self.current_index else QColor(200, 200, 200)
            painter.setPen(color)
            item_rect = QRect(int(i * self.item_width), 0, int(self.item_width), self.height())
            painter.drawText(item_rect, Qt.AlignCenter, text)

class AIDeskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.is_expanded = False
        self._drag_pos = None
        self.current_mode = "Chat"
        self.themes = {
            "SQL":   (QColor(255, 100, 0, 35), "#f6d365", "#fda085"),
            "Linux": (QColor(0, 255, 150, 45), "#00b09b", "#96c93d"),
        }
        self.current_theme = self._chat_theme()
        self.chat_history = []  # 多轮对话历史
        self.init_ui()
        self.init_tray()

        # 启动快捷键监听
        self.hotkey_worker = HotkeyThread(self)
        self.hotkey_worker.triggered.connect(self.toggle_window)
        self.hotkey_worker.start()

    def _chat_theme(self):
        """根据好感度在 Blue→Purple→Pink 之间插值。"""
        score = load_profile().get("affection_score", 0)
        t = score / 100.0
        if t <= 0.5:
            s = t * 2
            r = int(79  + (138 - 79)  * s)
            g = int(172 + (43  - 172) * s)
            b = int(254 + (226 - 254) * s)
            r2 = int(0   + (138 - 0)  * s)
            g2 = int(242 + (43  - 242) * s)
            b2 = int(254 + (226 - 254) * s)
        else:
            s = (t - 0.5) * 2
            r = int(138 + (255 - 138) * s)
            g = int(43  + (105 - 43)  * s)
            b = int(226 + (180 - 226) * s)
            r2 = int(138 + (255 - 138) * s)
            g2 = int(43  + (82  - 43)  * s)
            b2 = int(226 + (147 - 226) * s)
        glow_alpha = int(35 + t * 40)
        glow = QColor(r, g // 2, b, glow_alpha)
        start = f"#{r:02x}{g:02x}{b:02x}"
        end   = f"#{r2:02x}{g2:02x}{b2:02x}"
        return (glow, start, end)

    def set_debug_affection(self, score: int):
        """调试用：设置好感度并刷新 UI。"""
        set_affection(score)
        self._animate_theme_to(self._chat_theme())

    def _animate_theme_to(self, target_theme):
        """平滑过渡到目标主题色，60步 × 16ms ≈ 1秒。"""
        glow_from, start_from, end_from = self.current_theme
        glow_to, start_to, end_to = target_theme

        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        r1, g1, b1 = hex_to_rgb(start_from)
        r2, g2, b2 = hex_to_rgb(end_from)
        tr1, tg1, tb1 = hex_to_rgb(start_to)
        tr2, tg2, tb2 = hex_to_rgb(end_to)

        steps = 60
        self._anim_step = 0

        def tick():
            t = self._anim_step / steps
            # ease in-out cubic
            t = t * t * (3 - 2 * t)
            cr1 = int(r1 + (tr1 - r1) * t)
            cg1 = int(g1 + (tg1 - g1) * t)
            cb1 = int(b1 + (tb1 - b1) * t)
            cr2 = int(r2 + (tr2 - r2) * t)
            cg2 = int(g2 + (tg2 - g2) * t)
            cb2 = int(b2 + (tb2 - b2) * t)
            s = f"#{cr1:02x}{cg1:02x}{cb1:02x}"
            e = f"#{cr2:02x}{cg2:02x}{cb2:02x}"
            glow = QColor(cr1, cg1 // 2, cb1, int(35 + t * 40))
            self.current_theme = (glow, s, e)
            self.apply_styles()
            self.update()
            self._anim_step += 1
            if self._anim_step > steps:
                self._theme_timer.stop()
                self.current_theme = target_theme

        self._theme_timer = QTimer(self)
        self._theme_timer.timeout.connect(tick)
        self._theme_timer.start(16)

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(650, 450)

        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(10, 10, 630, 80)
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(20, 12, 20, 12)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask me anything...")
        self.input_field.setFont(QFont("Segoe UI Variable Display", 13))
        self.input_field.setStyleSheet("background: transparent; border: none; color: white;")

        self.mode_switcher = ModeSwitcher(["Chat", "SQL", "Linux"], self.change_mode, self.main_frame)

        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedSize(85, 38)
        self.send_btn.setFont(QFont("Segoe UI Variable Display", 10, QFont.Bold))
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.clicked.connect(self.on_send)

        top_layout.addWidget(self.input_field)
        top_layout.addWidget(self.mode_switcher)
        top_layout.addWidget(self.send_btn)
        layout.addLayout(top_layout)

        # 气泡滚动区
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.scroll_area.hide()

        self.bubble_container = QWidget()
        self.bubble_container.setStyleSheet("background: transparent;")
        self.bubble_layout = QVBoxLayout(self.bubble_container)
        self.bubble_layout.setAlignment(Qt.AlignTop)
        self.bubble_layout.setSpacing(4)
        self.bubble_layout.setContentsMargins(4, 4, 4, 4)
        self.scroll_area.setWidget(self.bubble_container)
        layout.addWidget(self.scroll_area)

        # SQL/Linux 结果区（保留）
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.hide()
        self.result_area.setFont(QFont("Cascadia Code", 11))
        layout.addWidget(self.result_area)

        self.paste_btn = QPushButton("Paste & Close")
        self.paste_btn.setFixedHeight(36)
        self.paste_btn.setFont(QFont("Segoe UI Variable Display", 10, QFont.Bold))
        self.paste_btn.setCursor(Qt.PointingHandCursor)
        self.paste_btn.hide()
        self.paste_btn.clicked.connect(self._on_paste_close)
        layout.addWidget(self.paste_btn)
        self.apply_styles()

        self._typing_bubble_row = None

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)

        # 创建一个简单的图标（为了演示，我们动态创建一个蓝色圆点图标）
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#4facfe"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(4, 4, 24, 24)
        painter.end()
        self.tray_icon.setIcon(QIcon(pixmap))

        # 托盘菜单
        tray_menu = QMenu()
        show_action = QAction("Show / Hide", self)
        show_action.triggered.connect(self.toggle_window)
        quit_action = QAction("Exit AI Desk", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger: # 单击或双击图标
            self.toggle_window()

    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            # 记录当前前台窗口，稍后粘贴回去
            import ctypes
            self._prev_hwnd = ctypes.windll.user32.GetForegroundWindow()
            self.showNormal()
            self.activateWindow()
            self.raise_()
            self.input_field.setFocus()

    def apply_styles(self):
        _, start, end = self.current_theme
        grad = f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start}, stop:1 {end})"
        self.send_btn.setStyleSheet(f"QPushButton {{ background: {grad}; color: #0f0f14; border-radius: 19px; border: none; }}")
        self.paste_btn.setStyleSheet(f"QPushButton {{ background: {grad}; color: #0f0f14; border-radius: 18px; border: none; }}")
        self.result_area.setStyleSheet("QTextEdit { background: rgba(0, 0, 0, 65); color: rgba(255, 255, 255, 220); border-radius: 15px; border: 1px solid rgba(255, 255, 255, 10); margin-top: 10px; padding: 10px; }")

    def change_mode(self, mode_name):
        self.current_mode = mode_name
        if mode_name == "Chat":
            self.current_theme = self._chat_theme()
        else:
            self.current_theme = self.themes[mode_name]
        self.apply_styles()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPos() - self._drag_pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        path = QPainterPath()
        r = self.main_frame.geometry()
        path.addRoundedRect(QRectF(r), 26, 26)
        painter.fillPath(path, QColor(10, 10, 12, 165))
        glow = self.current_theme[0]
        grad = QRadialGradient(QPoint(80, 20), 550)
        grad.setColorAt(0, glow)
        grad.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillPath(path, QBrush(grad))

    def on_send(self):
        text = self.input_field.text().strip()
        if not text:
            return
        mode = self.mode_switcher.items[self.mode_switcher.current_index]
        self.send_btn.setEnabled(False)
        self.send_btn.setText("...")
        self.paste_btn.hide()
        if not self.is_expanded:
            self._expand(True)

        # 追加用户消息到对话框
        self.input_field.clear()

        if mode == "Chat":
            self.result_area.hide()
            self.scroll_area.show()
            self._add_bubble(text, is_user=True)
            self._show_typing()
        else:
            self.scroll_area.hide()
            self.result_area.show()
            self.result_area.setPlainText("Thinking...")

        self.worker = AIWorker(mode, text, self.chat_history if mode == "Chat" else [])
        self.worker.finished.connect(self.on_result)
        self.worker.error.connect(self.on_error)
        self._last_user_text = text
        self._last_mode = mode
        self.worker.start()

    def _add_bubble(self, text, is_user):
        _, start, end = self.current_theme
        bubble = BubbleLabel(text, is_user, start, end)
        row = BubbleRow(bubble, is_user)
        self.bubble_layout.addWidget(row)
        self._scroll_to_bottom()
        return row

    def _show_typing(self):
        self._typing_bubble = TypingBubble()
        self._typing_bubble_row = BubbleRow(self._typing_bubble, is_user=False)
        self.bubble_layout.addWidget(self._typing_bubble_row)
        self._scroll_to_bottom()

    def _remove_typing(self):
        if self._typing_bubble_row:
            self._typing_bubble.stop()
            self.bubble_layout.removeWidget(self._typing_bubble_row)
            self._typing_bubble_row.deleteLater()
            self._typing_bubble_row = None

    def _scroll_to_bottom(self):
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def on_result(self, text):
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send")
        if self._last_mode == "Chat":
            self._remove_typing()
            self._add_bubble(text, is_user=False)
            self.chat_history.append({"role": "user", "content": self._last_user_text})
            self.chat_history.append({"role": "assistant", "content": text})
            # 检查好感度变化，触发颜色渐变
            new_theme = self._chat_theme()
            if new_theme[1] != self.current_theme[1]:
                self._animate_theme_to(new_theme)
        else:
            self.result_area.setPlainText(text)
            self.paste_btn.show()

    def _on_paste_close(self):
        self.paste_btn.hide()
        self._auto_paste(self.result_area.toPlainText())

    def _auto_paste(self, text):
        import ctypes
        pyperclip.copy(text)
        self.hide()
        if hasattr(self, '_prev_hwnd') and self._prev_hwnd:
            ctypes.windll.user32.SetForegroundWindow(self._prev_hwnd)
        time.sleep(0.15)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.05)
        pyautogui.press('enter')

    def on_error(self, msg):
        self._remove_typing()
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send")
        if self._last_mode == "Chat":
            self._add_bubble(f"Error: {msg}", is_user=False)
        else:
            self.result_area.setPlainText(f"Error: {msg}")

    def _expand(self, expand: bool):
        self.anim = QPropertyAnimation(self.main_frame, b"geometry")
        self.anim.setDuration(500)
        self.anim.setEasingCurve(QEasingCurve.OutExpo)
        if expand:
            self.anim.setEndValue(QRect(10, 10, 630, 430))
            self.is_expanded = True
        else:
            self.anim.setEndValue(QRect(10, 10, 630, 80))
            self.anim.finished.connect(self.scroll_area.hide)
            self.anim.finished.connect(self.result_area.hide)
            self.is_expanded = False
        self.anim.start()

if __name__ == "__main__":
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)

    # 允许隐藏窗口后依然运行
    app.setQuitOnLastWindowClosed(False)

    window = AIDeskWindow()
    # 初始不调用 window.show()，保持静默启动

    print("AI Desk running. Ctrl+Space to toggle. Right-click tray icon to exit.")
    sys.exit(app.exec_())