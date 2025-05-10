"""
CSS styles for the retro MP3 player.
These can be applied to specific components as needed.
"""

# Dark theme base style
DARK_THEME = """
QMainWindow, QDialog {
    background-color: #1e1e1e;
    color: #f0f0f0;
}

QLabel {
    color: #f0f0f0;
}

QPushButton, QToolButton {
    background-color: #2d2d2d;
    color: #f0f0f0;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 5px;
}

QPushButton:hover, QToolButton:hover {
    background-color: #3a3a3a;
    border: 1px solid #4d4d4d;
}

QPushButton:pressed, QToolButton:pressed {
    background-color: #1a1a1a;
}

QSlider::groove:horizontal {
    border: 1px solid #3d3d3d;
    height: 8px;
    background: #2d2d2d;
    margin: 2px 0;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #5a5a5a;
    border: 1px solid #7a7a7a;
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #7a7a7a;
}

QListWidget {
    background-color: #2d2d2d;
    color: #f0f0f0;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #3d6d99;
    color: #ffffff;
}

QListWidget::item:hover {
    background-color: #2d5d89;
}

QScrollBar:vertical {
    border: 1px solid #3d3d3d;
    background: #2d2d2d;
    width: 12px;
    margin: 12px 0 12px 0;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #5a5a5a;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical {
    border: 1px solid #3d3d3d;
    background: #2d2d2d;
    height: 12px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
    border-radius: 6px;
}

QScrollBar::sub-line:vertical {
    border: 1px solid #3d3d3d;
    background: #2d2d2d;
    height: 12px;
    subcontrol-position: top;
    subcontrol-origin: margin;
    border-radius: 6px;
}

QTabWidget::pane {
    border: 1px solid #3d3d3d;
    background-color: #2d2d2d;
}

QTabBar::tab {
    background-color: #1e1e1e;
    color: #f0f0f0;
    border: 1px solid #3d3d3d;
    padding: 6px 10px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #2d2d2d;
    border-bottom-color: #2d2d2d;
}

QTabBar::tab:hover {
    background-color: #3a3a3a;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #2d2d2d;
    color: #f0f0f0;
    border: 1px solid #3d3d3d;
    border-radius: 4px;
    padding: 2px 5px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-color: #3d3d3d;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}
"""

# Light theme base style
LIGHT_THEME = """
QMainWindow, QDialog {
    background-color: #f5f5f5;
    color: #333333;
}

QLabel {
    color: #333333;
}

QPushButton, QToolButton {
    background-color: #e0e0e0;
    color: #333333;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 5px;
}

QPushButton:hover, QToolButton:hover {
    background-color: #d0d0d0;
    border: 1px solid #c0c0c0;
}

QPushButton:pressed, QToolButton:pressed {
    background-color: #c0c0c0;
}

QSlider::groove:horizontal {
    border: 1px solid #d0d0d0;
    height: 8px;
    background: #e0e0e0;
    margin: 2px 0;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #999999;
    border: 1px solid #777777;
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #777777;
}

QListWidget {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #3d6d99;
    color: #ffffff;
}

QListWidget::item:hover {
    background-color: #e8e8e8;
}

QScrollBar:vertical {
    border: 1px solid #d0d0d0;
    background: #f0f0f0;
    width: 12px;
    margin: 12px 0 12px 0;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: #c0c0c0;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical {
    border: 1px solid #d0d0d0;
    background: #e0e0e0;
    height: 12px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
    border-radius: 6px;
}

QScrollBar::sub-line:vertical {
    border: 1px solid #d0d0d0;
    background: #e0e0e0;
    height: 12px;
    subcontrol-position: top;
    subcontrol-origin: margin;
    border-radius: 6px;
}

QTabWidget::pane {
    border: 1px solid #d0d0d0;
    background-color: #f0f0f0;
}

QTabBar::tab {
    background-color: #e0e0e0;
    color: #333333;
    border: 1px solid #d0d0d0;
    padding: 6px 10px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #f0f0f0;
    border-bottom-color: #f0f0f0;
}

QTabBar::tab:hover {
    background-color: #d0d0d0;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 2px 5px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-color: #d0d0d0;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}
"""

# Retro computer/terminal green theme
RETRO_TERMINAL_THEME = """
QMainWindow, QDialog {
    background-color: #000000;
    color: #00ff00;
}

QLabel {
    color: #00ff00;
    font-family: "Courier New", monospace;
}

QPushButton, QToolButton {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 0px;
    padding: 5px;
    font-family: "Courier New", monospace;
}

QPushButton:hover, QToolButton:hover {
    background-color: #002200;
    border: 1px dashed #00ff00;
}

QPushButton:pressed, QToolButton:pressed {
    background-color: #003300;
}

QSlider::groove:horizontal {
    border: 1px solid #00ff00;
    height: 6px;
    background: #001100;
    margin: 2px 0;
}

QSlider::handle:horizontal {
    background: #00ff00;
    border: 1px solid #00ff00;
    width: 12px;
    height: 12px;
    margin: -4px 0;
}

QListWidget {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    font-family: "Courier New", monospace;
}

QListWidget::item:selected {
    background-color: #00aa00;
    color: #000000;
}

QListWidget::item:hover {
    background-color: #002200;
}

QScrollBar:vertical {
    border: 1px solid #00ff00;
    background: #001100;
    width: 12px;
    margin: 12px 0 12px 0;
}

QScrollBar::handle:vertical {
    background: #00aa00;
    min-height: 20px;
}

QTabWidget::pane {
    border: 1px solid #00ff00;
    background-color: #000000;
}

QTabBar::tab {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    padding: 6px 10px;
    font-family: "Courier New", monospace;
}

QTabBar::tab:selected {
    background-color: #002200;
}

QTabBar::tab:hover {
    background-color: #003300;
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #001100;
    color: #00ff00;
    border: 1px solid #00ff00;
    border-radius: 0px;
    padding: 2px 5px;
    font-family: "Courier New", monospace;
}

QStatusBar {
    background-color: #000000;
    color: #00ff00;
    border-top: 1px solid #00ff00;
    font-family: "Courier New", monospace;
}

QProgressBar {
    border: 1px solid #00ff00;
    background-color: #001100;
    text-align: center;
    font-family: "Courier New", monospace;
}

QProgressBar::chunk {
    background-color: #00aa00;
}
"""

# Vaporwave/retrowave theme
VAPORWAVE_THEME = """
QMainWindow, QDialog {
    background-color: #19051a;
    color: #ff80ff;
}

QLabel {
    color: #ff80ff;
    font-family: "Arial", sans-serif;
}

QPushButton, QToolButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #800080, stop:1 #0000aa);
    color: #00ffff;
    border: 2px solid #00ffff;
    border-radius: 4px;
    padding: 5px;
    font-family: "Arial", sans-serif;
    font-weight: bold;
}

QPushButton:hover, QToolButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #aa00aa, stop:1 #0000ff);
    border: 2px solid #ffff00;
}

QPushButton:pressed, QToolButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #cc00cc, stop:1 #0000cc);
}

QSlider::groove:horizontal {
    border: 1px solid #ff80ff;
    height: 8px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #400040, stop:1 #000080);
    margin: 2px 0;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #00ffff;
    border: 1px solid #ffffff;
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
}

QSlider::handle:horizontal:hover {
    background: #ffff00;
}

QListWidget {
    background-color: #280a28;
    alternate-background-color: #3c143c;
    color: #ff80ff;
    border: 2px solid #800080;
    border-radius: 4px;
    font-family: "Arial", sans-serif;
}

QListWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #800080, stop:1 #0000aa);
    color: #00ffff;
}

QListWidget::item:hover {
    background-color: #400040;
}

QScrollBar:vertical {
    border: 1px solid #800080;
    background: #280a28;
    width: 12px;
    margin: 12px 0 12px 0;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #800080, stop:1 #0000aa);
    min-height: 20px;
    border-radius: 6px;
}

QTabWidget::pane {
    border: 2px solid #800080;
    background-color: #19051a;
    border-radius: 4px;
}

QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #400040, stop:1 #000080);
    color: #ff80ff;
    border: 1px solid #800080;
    padding: 6px 10px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #800080, stop:1 #0000aa);
    color: #00ffff;
}

QTabBar::tab:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #600060, stop:1 #000090);
}

QLineEdit, QComboBox, QSpinBox {
    background-color: #280a28;
    color: #ff80ff;
    border: 2px solid #800080;
    border-radius: 4px;
    padding: 2px 5px;
}

QStatusBar {
    background-color: #19051a;
    color: #ff80ff;
    border-top: 1px solid #800080;
}

QProgressBar {
    border: 2px solid #800080;
    background-color: #280a28;
    text-align: center;
    color: #ff80ff;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #800080, stop:1 #0000aa);
}
"""
