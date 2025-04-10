from PyQt5.QtGui import QColor

def apply_styles(app, theme="light"):
    """Применение стилей к приложению в зависимости от выбранной темы."""
    if theme == "light":
        app.setStyleSheet("""
            /* Основные стили */
            QMainWindow {
                background-color: #f0f2f5;
            }
            
            /* Текст */
            QLabel {
                color: #333333;
                font-size: 14px;
            }
            
            QLabel#balance_label {
                background-color: #e3f2fd;
                color: #0d47a1;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #bbdefb;
            }
            
            /* Кнопки */
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #1976d2;
            }
            
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            
            /* Поля ввода */
            QLineEdit, QComboBox, QDateEdit {
                background-color: white;
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
                color: #212121;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #bdbdbd;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #bdbdbd;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            
            /* Таблица */
            QTableWidget {
                background-color: white;
                alternate-background-color: #f5f5f5;
                gridline-color: #e0e0e0;
                border: 1px solid #bdbdbd;
                font-size: 14px;
            }
            
            QHeaderView::section {
                background-color: #2196f3;
                color: white;
                padding: 6px;
                border: none;
                font-size: 14px;
            }
            
            /* Вкладки */
            QTabWidget::pane {
                border: 1px solid #bdbdbd;
                background: white;
                margin-top: -1px;
            }
            
            QTabBar::tab {
                background: #e3f2fd;
                color: #1565c0;
                padding: 8px 12px;
                border: 1px solid #bbdefb;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background: white;
                color: #0d47a1;
                font-weight: bold;
                border-bottom: 1px solid white;
            }
            
            QTabBar::tab:hover {
                background: #bbdefb;
            }
            
            /* Меню */
            QMenuBar {
                background-color: #e3f2fd;
                color: #0d47a1;
            }
            
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
            }
            
            QMenuBar::item:selected {
                background: #bbdefb;
            }
            
            QMenu {
                background-color: white;
                border: 1px solid #bdbdbd;
            }
            
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #0d47a1;
            }
        """)
    else:
        app.setStyleSheet("""
            /* Основные стили */
            QMainWindow {
                background-color: #2d2d2d;
            }
            
            /* Текст */
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
            
            QLabel#balance_label {
                background-color: #424242;
                color: #bb86fc;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #616161;
            }
            
            /* Кнопки */
            QPushButton {
                background-color: #6200ee;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #3700b3;
            }
            
            QPushButton:pressed {
                background-color: #1a0068;
            }
            
            /* Поля ввода */
            QLineEdit, QComboBox, QDateEdit {
                background-color: #424242;
                border: 1px solid #616161;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
                color: #e0e0e0;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #616161;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #616161;
                border-left-style: solid;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            
            /* Таблица */
            QTableWidget {
                background-color: #424242;
                alternate-background-color: #535353;
                gridline-color: #616161;
                border: 1px solid #616161;
                font-size: 14px;
                color: #e0e0e0;
            }
            
            QHeaderView::section {
                background-color: #6200ee;
                color: white;
                padding: 6px;
                border: none;
                font-size: 14px;
            }
            
            /* Вкладки */
            QTabWidget::pane {
                border: 1px solid #616161;
                background: #424242;
                margin-top: -1px;
            }
            
            QTabBar::tab {
                background: #535353;
                color: #bb86fc;
                padding: 8px 12px;
                border: 1px solid #616161;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background: #424242;
                color: #bb86fc;
                font-weight: bold;
                border-bottom: 1px solid #424242;
            }
            
            QTabBar::tab:hover {
                background: #616161;
            }
            
            /* Меню */
            QMenuBar {
                background-color: #424242;
                color: #bb86fc;
            }
            
            QMenuBar::item {
                padding: 5px 10px;
                background: transparent;
            }
            
            QMenuBar::item:selected {
                background: #616161;
            }
            
            QMenu {
                background-color: #424242;
                border: 1px solid #616161;
            }
            
            QMenu::item:selected {
                background-color: #535353;
                color: #bb86fc;
            }
        """)