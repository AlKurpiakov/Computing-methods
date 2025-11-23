
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt, QTimer
from ui.widgets.matrix_editor import MatrixEditorPanel
from ui.widgets.control_panel import ControlPanel
from ui.widgets.visualization_tabs import VisualizationTabs
import Computing
from HungarianAlgorithm import HungarianAlgorithm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Визуализация Венгерского алгоритма")
        self.resize(1200, 800)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный макет
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 24, 24, 24) # Большие отступы от краев окна
        main_layout.setSpacing(24) # Большой отступ между панелями
        
        # Левая панель (Ввод + Управление)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6) # Уменьшенный отступ между карточками
        
        self.matrix_editor = MatrixEditorPanel()
        self.control_panel = ControlPanel()
        
        left_layout.addWidget(self.matrix_editor, stretch=2) # Матрица
        left_layout.addWidget(self.control_panel, stretch=3) # Увеличенное место для панели управления (и лога)
        
        # Правая панель (Визуализация)
        self.visualization_tabs = VisualizationTabs()
        
        # Разделитель
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.visualization_tabs)
        splitter.setStretchFactor(0, 4) # Левая часть 40%
        splitter.setStretchFactor(1, 6) # Правая часть 60%
        splitter.setHandleWidth(0) # Скрываем ручку разделителя визуально (или делаем тонкой)
        
        main_layout.addWidget(splitter)

        # Подключение сигналов
        self.control_panel.btn_solution.clicked.connect(self.show_solution)
        self.control_panel.btn_start.clicked.connect(self.start_algorithm)
        self.control_panel.btn_next.clicked.connect(self.next_step)
        self.control_panel.btn_back.clicked.connect(self.prev_step)
        self.control_panel.btn_auto.clicked.connect(self.toggle_auto)
        
        # Таймер для автоматического режима
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.next_step)
        
        self.algorithm = None

    def start_algorithm(self):
        matrix = self.matrix_editor.get_matrix()
        mode = 'min' if self.matrix_editor.radio_min.isChecked() else 'max'
        
        self.algorithm = HungarianAlgorithm(matrix, mode)
        self.control_panel.log("<b>Алгоритм запущен.</b>", "#89B4FA")
        self.update_ui_from_state()

    def next_step(self):
        if self.algorithm:
            state = self.algorithm.next()
            if state:
                self.update_ui_from_state()
            else:
                if self.algorithm.is_finished():
                    self.control_panel.log("Алгоритм завершен.", "#A6E3A1")
                    self.auto_timer.stop()
                    self.control_panel.btn_auto.setText(" Авто")

    def prev_step(self):
        if self.algorithm:
            state = self.algorithm.prev()
            if state:
                self.update_ui_from_state()

    def toggle_auto(self):
        if self.auto_timer.isActive():
            self.auto_timer.stop()
            self.control_panel.btn_auto.setText(" Авто")
        else:
            # Скорость зависит от слайдера: 100 (быстро) -> 50ms, 1 (медленно) -> 2000ms
            speed_val = self.control_panel.speed_slider.value()
            interval = int(2000 - (speed_val * 19.5))
            self.auto_timer.start(max(50, interval))
            self.control_panel.btn_auto.setText(" Стоп")

    def update_ui_from_state(self):
        if not self.algorithm:
            return
            
        state = self.algorithm.get_current_state()
        if state:
            self.control_panel.log(state['description'])
            self.visualization_tabs.update_matrix_visualization(state)

    def show_solution(self):
        """
        Демонстрация использования существующего функционала из Computing.py
        """
        try:
            matrix = self.matrix_editor.get_matrix()
            comp = Computing.Computing(matrix)
            
            if self.matrix_editor.radio_min.isChecked():
                cost = comp.HungarianMinimum()
                mode = "Минимизация"
            else:
                cost = comp.HungarianMaximum()
                mode = "Максимизация"
                
            self.control_panel.log(f"Режим: {mode}")
            self.control_panel.log(f"Оптимальная стоимость (через Computing.py): {cost}", "#A6E3A1")
            
        except Exception as e:
            self.control_panel.log(f"Ошибка при вычислении: {e}", "#F38BA8")
