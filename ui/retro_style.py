from PyQt5.QtWidgets import QProxyStyle, QStyle
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QRect

class RetroStyle(QProxyStyle):
    """Custom style for retro aesthetics."""
    
    def __init__(self, theme="retro_green"):
        super().__init__()
        self.theme = theme
    
    def drawControl(self, element, option, painter, widget=None):
        """Custom drawing for controls."""
        if element == QStyle.CE_PushButton:
            # Custom button drawing
            rect = option.rect
            text = option.text
            
            # Draw button background with retro effects
            if self.theme == "retro_green":
                # Terminal Green Theme
                if option.state & QStyle.State_MouseOver:
                    painter.fillRect(rect, QColor(0, 60, 0))
                    painter.setPen(QColor(0, 255, 0))
                elif option.state & QStyle.State_Sunken:
                    painter.fillRect(rect, QColor(0, 40, 0))
                    painter.setPen(QColor(0, 200, 0))
                else:
                    painter.fillRect(rect, QColor(0, 30, 0))
                    painter.setPen(QColor(0, 200, 0))
                
                # Draw border
                painter.drawRect(rect.adjusted(0, 0, -1, -1))
                
                # Draw text
                painter.drawText(rect, Qt.AlignCenter, text)
                return
                
            elif self.theme == "retro_blue":
                # 80s Blue Theme
                if option.state & QStyle.State_MouseOver:
                    painter.fillRect(rect, QColor(0, 0, 100))
                    painter.setPen(QColor(0, 200, 255))
                elif option.state & QStyle.State_Sunken:
                    painter.fillRect(rect, QColor(0, 0, 80))
                    painter.setPen(QColor(0, 180, 255))
                else:
                    painter.fillRect(rect, QColor(0, 0, 60))
                    painter.setPen(QColor(0, 180, 255))
                
                # Draw border
                painter.drawRect(rect.adjusted(0, 0, -1, -1))
                
                # Draw text
                painter.drawText(rect, Qt.AlignCenter, text)
                return
                
            elif self.theme == "retro_pink":
                # Vaporwave Pink Theme
                if option.state & QStyle.State_MouseOver:
                    painter.fillRect(rect, QColor(80, 0, 80))
                    painter.setPen(QColor(255, 100, 255))
                elif option.state & QStyle.State_Sunken:
                    painter.fillRect(rect, QColor(60, 0, 60))
                    painter.setPen(QColor(255, 80, 255))
                else:
                    painter.fillRect(rect, QColor(40, 0, 40))
                    painter.setPen(QColor(255, 80, 255))
                
                # Draw border
                painter.drawRect(rect.adjusted(0, 0, -1, -1))
                
                # Draw text
                painter.drawText(rect, Qt.AlignCenter, text)
                return
        
        # For other elements, use the base style
        super().drawControl(element, option, painter, widget)
    
    def drawPrimitive(self, element, option, painter, widget=None):
        """Custom drawing for primitive elements."""
        if element == QStyle.PE_FrameFocusRect:
            # Custom focus rectangle
            rect = option.rect
            
            if self.theme == "retro_green":
                # Green glowing focus
                painter.setPen(QColor(0, 255, 0, 180))
            elif self.theme == "retro_blue":
                # Blue glowing focus
                painter.setPen(QColor(0, 200, 255, 180))
            elif self.theme == "retro_pink":
                # Pink glowing focus
                painter.setPen(QColor(255, 100, 255, 180))
            else:
                painter.setPen(Qt.white)
                
            painter.drawRect(rect.adjusted(0, 0, -1, -1))
            return
            
        # For other primitives, use the base style
        super().drawPrimitive(element, option, painter, widget)
    
    def styleHint(self, hint, option=None, widget=None, returnData=None):
        """Provide custom style hints."""
        if hint == QStyle.SH_DialogButtonBox_ButtonsHaveIcons:
            # Don't use icons in dialog buttons
            return 0
        return super().styleHint(hint, option, widget, returnData)
        
    def pixelMetric(self, metric, option=None, widget=None):
        """Adjust pixel metrics for a retro look."""
        if metric == QStyle.PM_ButtonMargin:
            # Larger button margins for a chunky retro look
            return 6
        elif metric == QStyle.PM_ToolBarItemMargin:
            # Larger toolbar margins
            return 4
        return super().pixelMetric(metric, option, widget)
    
    def apply_retro_palette(self, app):
        """Apply a retro-themed color palette to the application."""
        palette = QPalette()
        
        if self.theme == "retro_green":
            # Terminal Green Theme
            palette.setColor(QPalette.Window, QColor(0, 0, 0))
            palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
            palette.setColor(QPalette.Base, QColor(0, 20, 0))
            palette.setColor(QPalette.AlternateBase, QColor(0, 30, 0))
            palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
            palette.setColor(QPalette.ToolTipText, QColor(0, 255, 0))
            palette.setColor(QPalette.Text, QColor(0, 255, 0))
            palette.setColor(QPalette.Button, QColor(0, 40, 0))
            palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
            palette.setColor(QPalette.Highlight, QColor(0, 120, 0))
            palette.setColor(QPalette.HighlightedText, QColor(0, 255, 0))
            
            # Set a retro font
            font = QFont("Courier New", 10)
            app.setFont(font)
            
        elif self.theme == "retro_blue":
            # 80s Blue Theme
            palette.setColor(QPalette.Window, QColor(0, 20, 60))
            palette.setColor(QPalette.WindowText, QColor(50, 200, 255))
            palette.setColor(QPalette.Base, QColor(0, 40, 80))
            palette.setColor(QPalette.AlternateBase, QColor(0, 30, 70))
            palette.setColor(QPalette.ToolTipBase, QColor(0, 20, 60))
            palette.setColor(QPalette.ToolTipText, QColor(50, 200, 255))
            palette.setColor(QPalette.Text, QColor(50, 200, 255))
            palette.setColor(QPalette.Button, QColor(0, 50, 100))
            palette.setColor(QPalette.ButtonText, QColor(50, 200, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
            palette.setColor(QPalette.Highlight, QColor(0, 100, 200))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            
            # Set a retro font
            font = QFont("Arial", 10)
            app.setFont(font)
            
        elif self.theme == "retro_pink":
            # Vaporwave Pink Theme
            palette.setColor(QPalette.Window, QColor(30, 0, 30))
            palette.setColor(QPalette.WindowText, QColor(255, 130, 255))
            palette.setColor(QPalette.Base, QColor(40, 0, 40))
            palette.setColor(QPalette.AlternateBase, QColor(60, 0, 60))
            palette.setColor(QPalette.ToolTipBase, QColor(30, 0, 30))
            palette.setColor(QPalette.ToolTipText, QColor(255, 130, 255))
            palette.setColor(QPalette.Text, QColor(255, 130, 255))
            palette.setColor(QPalette.Button, QColor(100, 0, 100))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
            palette.setColor(QPalette.Highlight, QColor(180, 0, 180))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            
            # Set a retro font
            font = QFont("Arial", 10, QFont.Bold)
            app.setFont(font)
        
        # Apply palette
        app.setPalette(palette)