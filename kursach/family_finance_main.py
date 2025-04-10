import sys
import csv
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout,
    QHBoxLayout, QAction, QFileDialog, QTabWidget, QComboBox, QMenuBar,
    QDialog, QDialogButtonBox, QDateEdit, QSplitter, QGridLayout, QHeaderView
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate
import sqlite3
from family_finance_styles import apply_styles
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FamilyFinanceManager:
    def __init__(self, db_file="finance_data.db"):
        self.db_file = db_file
        self.balance = 0
        self.init_db()
        self.load_balance()

    def init_db(self):
        """Инициализация базы данных."""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS balance (
                id INTEGER PRIMARY KEY,
                current_balance REAL NOT NULL
            )
        """)
        self.conn.commit()

    def load_balance(self):
        self.cursor.execute("SELECT current_balance FROM balance LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            self.balance = result[0]
        else:
            self.balance = 0
            self.cursor.execute("INSERT INTO balance (current_balance) VALUES (?)", (self.balance,))
            self.conn.commit()

    def save_balance(self):
        self.cursor.execute("UPDATE balance SET current_balance = ?", (self.balance,))
        self.conn.commit()

    def add_income(self, amount):
        """Добавление дохода."""
        if amount > 0:
            self.balance += amount
            self.cursor.execute(
                "INSERT INTO transactions (category, amount) VALUES (?, ?)",
                (None, amount)
            )
            self.save_balance()
            return True
        return False

    def add_expense(self, category, amount):
        """Добавление расхода."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.cursor.execute(
                "INSERT INTO transactions (category, amount) VALUES (?, ?)",
                (category, -amount)
            )
            self.save_balance()
            return True
        return False

    def get_transactions(self, date_filter=None, category_filter=None):
        """Получение всех транзакций с фильтрами."""
        query = "SELECT category, amount, timestamp FROM transactions WHERE 1=1"
        params = []
        if date_filter:
            query += " AND DATE(timestamp) = ?"
            params.append(date_filter)
        if category_filter:
            query += " AND category = ?"
            params.append(category_filter)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.finance_manager = FamilyFinanceManager()
        self.setWindowTitle("Менеджер семейных финансов")
        self.setGeometry(100, 100, 900, 700)

        # Создаем меню
        self.create_menu()

        # Главный виджет и макет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Настройка вкладок
        self.setup_tabs()

        # Применение стилей
        apply_styles(self, self.current_theme)

        # Обновление данных
        self.update_balance_label()
        self.update_transactions_table()

    def create_menu(self):
        """Создание меню приложения."""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        export_action = QAction("Экспорт в CSV", self)
        export_action.triggered.connect(self.export_to_csv)
        file_menu.addAction(export_action)
        
        theme_action = QAction("Переключить тему", self)
        theme_action.triggered.connect(self.toggle_theme)
        file_menu.addAction(theme_action)
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Помощь
        help_menu = menubar.addMenu("Помощь")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_tabs(self):
        """Настройка вкладок приложения."""
        self.tabs = QTabWidget()
        
        # Вкладка Главная
        self.home_tab = QWidget()
        self.setup_home_tab()
        
        # Вкладка Графики
        self.charts_tab = QWidget()
        self.setup_charts_tab()
        
        self.tabs.addTab(self.home_tab, "Главная")
        self.tabs.addTab(self.charts_tab, "Графики")
        
        self.main_layout.addWidget(self.tabs)

    def setup_home_tab(self):
        """Настройка содержимого вкладки Главная."""
        layout = QVBoxLayout()
        
        # Блок баланса
        self.setup_balance_block(layout)
        
        # Блок добавления операций
        self.setup_transaction_blocks(layout)
        
        # Блок фильтров
        self.setup_filter_block(layout)
        
        # Таблица транзакций
        self.setup_transactions_table(layout)
        
        self.home_tab.setLayout(layout)

    def setup_balance_block(self, layout):
        """Настройка блока с балансом."""
        self.balance_label = QLabel(f"Текущий баланс: {self.finance_manager.balance} ₽")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.balance_label.setObjectName("balance_label")
        layout.addWidget(self.balance_label)

    def setup_transaction_blocks(self, layout):
        """Настройка блоков для добавления доходов и расходов."""
        # Блок дохода
        income_layout = QHBoxLayout()
        income_layout.addWidget(QLabel("Доход:"))
        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("Введите сумму дохода")
        income_layout.addWidget(self.income_input)
        self.add_income_button = QPushButton("Добавить доход")
        self.add_income_button.clicked.connect(self.add_income)
        income_layout.addWidget(self.add_income_button)
        layout.addLayout(income_layout)

        # Блок расхода
        expense_layout = QFormLayout()
        self.expense_category_input = QComboBox()
        self.expense_category_input.addItems(["Продукты", "Транспорт", "ЖКХ", "Развлечения", "Одежда"])
        self.expense_category_input.setEditable(True)
        self.expense_amount_input = QLineEdit()
        self.expense_amount_input.setPlaceholderText("Введите сумму расхода")
        expense_layout.addRow("Категория расхода:", self.expense_category_input)
        expense_layout.addRow("Сумма расхода:", self.expense_amount_input)
        self.add_expense_button = QPushButton("Добавить расход")
        self.add_expense_button.clicked.connect(self.add_expense)
        expense_layout.addRow(self.add_expense_button)
        layout.addLayout(expense_layout)

    def setup_filter_block(self, layout):
        """Настройка блока фильтров."""
        filter_layout = QGridLayout()
        filter_layout.addWidget(QLabel("Дата:"), 0, 0)
        self.date_filter = QDateEdit()
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.setCalendarPopup(True)
        filter_layout.addWidget(self.date_filter, 0, 1)
        
        filter_layout.addWidget(QLabel("Категория:"), 1, 0)
        self.category_filter = QComboBox()
        self.category_filter.addItems(["Все категории", "Продукты", "Транспорт", "ЖКХ", "Развлечения", "Одежда"])
        filter_layout.addWidget(self.category_filter, 1, 1)
        
        self.filter_button = QPushButton("Применить фильтры")
        self.filter_button.clicked.connect(self.apply_filters)
        self.clear_filters_button = QPushButton("Сбросить фильтры")
        self.clear_filters_button.clicked.connect(self.clear_filters)
        filter_layout.addWidget(self.filter_button, 2, 0)
        filter_layout.addWidget(self.clear_filters_button, 2, 1)
        
        layout.addLayout(filter_layout)

    def setup_transactions_table(self, layout):
        """Настройка таблицы транзакций."""
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(3)
        self.transactions_table.setHorizontalHeaderLabels(["Категория", "Сумма", "Дата"])
        self.transactions_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.transactions_table.verticalHeader().setVisible(False)
        layout.addWidget(self.transactions_table)

    def setup_charts_tab(self):
        """Настройка вкладки с графиками."""
        layout = QVBoxLayout()
        
        # Контейнер для графиков
        self.chart_container = QWidget()
        self.chart_layout = QVBoxLayout()
        self.chart_container.setLayout(self.chart_layout)
        
        # Кнопки для управления графиками
        buttons_layout = QHBoxLayout()
        self.expense_chart_button = QPushButton("Расходы по категориям")
        self.expense_chart_button.clicked.connect(self.plot_expense_analysis)
        buttons_layout.addWidget(self.expense_chart_button)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.chart_container)
        
        self.charts_tab.setLayout(layout)
        self.plot_expense_analysis()

    def update_balance_label(self):
        """Обновление отображения баланса."""
        self.balance_label.setText(f"Текущий баланс: {self.finance_manager.balance} ₽")

    def update_transactions_table(self, date_filter=None, category_filter=None):
        """Обновление таблицы транзакций."""
        transactions = self.finance_manager.get_transactions(date_filter, category_filter)
        self.transactions_table.setRowCount(len(transactions))
        
        for row, transaction in enumerate(transactions):
            category, amount, timestamp = transaction
            
            # Категория
            category_item = QTableWidgetItem(category if category else "Доход")
            self.transactions_table.setItem(row, 0, category_item)
            
            # Сумма
            amount_item = QTableWidgetItem(f"{abs(amount):.2f} ₽")
            if amount < 0:
                amount_item.setForeground(QColor(255, 0, 0))  # Красный для расходов
            else:
                amount_item.setForeground(QColor(0, 128, 0))  # Зеленый для доходов
            self.transactions_table.setItem(row, 1, amount_item)
            
            # Дата
            self.transactions_table.setItem(row, 2, QTableWidgetItem(timestamp))

    def plot_expense_analysis(self):
        """Построение круговой диаграммы расходов."""
        # Очистка предыдущего графика
        for i in reversed(range(self.chart_layout.count())):
            self.chart_layout.itemAt(i).widget().setParent(None)
        
        # Получение данных
        expenses = {}
        transactions = self.finance_manager.get_transactions()
        for t in transactions:
            category, amount, _ = t
            if amount < 0:  # Только расходы
                expenses[category] = expenses.get(category, 0) + abs(amount)
        
        if not expenses:
            no_data_label = QLabel("Нет данных о расходах для построения графика")
            no_data_label.setAlignment(Qt.AlignCenter)
            self.chart_layout.addWidget(no_data_label)
            return
        
        # Создание графика
        fig = plt.figure(figsize=(8, 6))
        if self.current_theme == "dark":
            fig.patch.set_facecolor('#2d2d2d')
            plt.rcParams.update({
                'text.color': 'white',
                'axes.labelcolor': 'white',
                'axes.facecolor': '#2d2d2d',
                'axes.edgecolor': 'lightgray'
            })
        
        ax = fig.add_subplot(111)
        categories = list(expenses.keys())
        amounts = list(expenses.values())
        
        colors = plt.cm.Pastel1(range(len(categories)))
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90,
               colors=colors, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
        ax.set_title("Распределение расходов по категориям", 
                    color='white' if self.current_theme == "dark" else 'black')
        
        # Встраивание графика в интерфейс
        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)

    def add_income(self):
        """Обработка добавления дохода."""
        amount_text = self.income_input.text()
        try:
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Ошибка", "Сумма дохода должна быть положительной")
                return
            
            if self.finance_manager.add_income(amount):
                self.income_input.clear()
                self.update_balance_label()
                self.update_transactions_table()
                self.plot_expense_analysis()
                QMessageBox.information(self, "Успешно", "Доход успешно добавлен")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить доход")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму")

    def add_expense(self):
        """Обработка добавления расхода."""
        category = self.expense_category_input.currentText()
        amount_text = self.expense_amount_input.text()
        
        if not category:
            QMessageBox.warning(self, "Ошибка", "Укажите категорию расхода")
            return
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, "Ошибка", "Сумма расхода должна быть положительной")
                return
            
            if self.finance_manager.add_expense(category, amount):
                self.expense_amount_input.clear()
                self.update_balance_label()
                self.update_transactions_table()
                self.plot_expense_analysis()
                QMessageBox.information(self, "Успешно", "Расход успешно добавлен")
            else:
                QMessageBox.warning(self, "Ошибка", "Недостаточно средств или произошла ошибка")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректную сумму")

    def apply_filters(self):
        """Применение фильтров к таблице транзакций."""
        date_filter = None
        if self.date_filter.date() != QDate.currentDate():
            date_filter = self.date_filter.date().toString("yyyy-MM-dd")
        
        category_filter = None
        if self.category_filter.currentText() != "Все категории":
            category_filter = self.category_filter.currentText()
        
        self.update_transactions_table(date_filter, category_filter)

    def clear_filters(self):
        """Сброс фильтров."""
        self.date_filter.setDate(QDate.currentDate())
        self.category_filter.setCurrentText("Все категории")
        self.update_transactions_table()

    def toggle_theme(self):
        """Переключение между светлой и темной темой."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        apply_styles(self, self.current_theme)
        self.plot_expense_analysis()  # Перерисовка графика с новой темой

    def export_to_csv(self):
        """Экспорт данных в CSV файл."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", "", "CSV файлы (*.csv)")
        
        if not file_path:
            return
        
        try:
            transactions = self.finance_manager.get_transactions()
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Тип", "Категория", "Сумма", "Дата"])
                
                for t in transactions:
                    category, amount, date = t
                    trans_type = "Доход" if amount > 0 else "Расход"
                    writer.writerow([trans_type, category or "", abs(amount), date])
            
            QMessageBox.information(self, "Успешно", f"Данные экспортированы в:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные:\n{str(e)}")

    def show_about(self):
        """Отображение информации о программе."""
        QMessageBox.about(self, "О программе",
                         "Менеджер семейных финансов\n"
                         "Версия 1.0\n\n"
                         "Программа для учета доходов и расходов\n"
                         "с возможностью анализа финансовых данных.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())