import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import AIDeskWindow
from core.memory import set_affection

DEBUG_AFFECTION = 0  # 改这里测试不同好感度：0=陌生人 30=朋友 60=知己 90=恋人

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei UI", 9))
    app.setQuitOnLastWindowClosed(False)

    set_affection(DEBUG_AFFECTION)
    window = AIDeskWindow()
    window.show()

    print("AI Desk running. Ctrl+Space to toggle. Right-click tray icon to exit.")
    sys.exit(app.exec_())