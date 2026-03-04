import sys
from PyQt5 import QtWidgets
from calculator_ui import Ui_MainWindow
from calculator_sounds import SoundManager


class CalculatorApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.sound_manager = SoundManager.get_instance()
        
        self.current_input = "0"
        self.previous_value = None
        self.operation = None
        self.new_input = True
        self.is_error = False
        
        self.connect_signals()
        
        self.update_display()
    
    def connect_signals(self):
        for btn_name in ['num_0', 'num_1', 'num_2', 'num_3', 'num_4', 
                         'num_5', 'num_6', 'num_7', 'num_8', 'num_9']:
            btn = getattr(self, btn_name)
            btn.clicked.connect(self.on_number_click)
        
        self.num_dot.clicked.connect(self.on_dot_click)
        
        self.op_add.clicked.connect(self.on_operation_click)
        self.op_sub.clicked.connect(self.on_operation_click)
        self.op_mul.clicked.connect(self.on_operation_click)
        self.op_div.clicked.connect(self.on_operation_click)
        
        self.btn_equals.clicked.connect(self.on_equals_click)
        
        self.ctrl_c.clicked.connect(self.on_clear_click)
        self.ctrl_ce.clicked.connect(self.on_clear_entry_click)
        self.ctrl_delete.clicked.connect(self.on_delete_click)
        self.ctrl_percent.clicked.connect(self.on_percent_click)
        self.ctrl_sign.clicked.connect(self.on_sign_click)
        self.ctrl_inverse.clicked.connect(self.on_inverse_click)
        self.ctrl_square.clicked.connect(self.on_square_click)
        self.ctrl_sqrt.clicked.connect(self.on_sqrt_click)
    
    def update_display(self):
        self.display_output.setText(self.current_input)
    
    def on_number_click(self):
        self.sound_manager.play_number()
        
        button = self.sender()
        digit = button.text()
        
        if self.is_error:
            self.is_error = False
            self.current_input = digit
            self.new_input = False
            self.update_display()
            return
        
        if self.new_input:
            self.current_input = digit
            self.new_input = False
        else:
            if self.current_input == "0":
                self.current_input = digit
            else:
                self.current_input += digit
        
        self.update_display()
    
    def on_dot_click(self):
        self.sound_manager.play_number()
        
        if self.is_error:
            self.is_error = False
            self.current_input = "0."
            self.new_input = False
            self.update_display()
            return
        
        if self.new_input:
            self.current_input = "0."
            self.new_input = False
        elif "." not in self.current_input:
            self.current_input += "."
        self.update_display()
    
    def on_operation_click(self):
        self.sound_manager.play_operator()
        
        if self.is_error:
            self.on_clear_click()
            return
        
        button = self.sender()
        op = button.text()
        
        if self.operation and not self.new_input:
            self.calculate()
        
        if self.is_error:
            return
        
        self.previous_value = float(self.current_input)
        self.operation = op
        self.new_input = True
    
    def on_equals_click(self):
        self.sound_manager.play_equals()
        
        if self.is_error:
            self.on_clear_click()
            return
        
        if self.operation:
            self.calculate()
            self.operation = None
            self.new_input = True
    
    def calculate(self):
        try:
            current = float(self.current_input)
            if self.operation == "+":
                result = self.previous_value + current
            elif self.operation == "-":
                result = self.previous_value - current
            elif self.operation == "*":
                result = self.previous_value * current
            elif self.operation == "/":
                if current == 0:
                    self.current_input = "Ошибка"
                    self.is_error = True
                    self.sound_manager.play_error()
                    self.update_display()
                    return
                result = self.previous_value / current
            else:
                return
            
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = str(result)
            
            self.previous_value = float(self.current_input)
            self.update_display()
        except (ValueError, OverflowError):
            self.current_input = "Ошибка"
            self.is_error = True
            self.sound_manager.play_error()
            self.update_display()
    
    def on_clear_click(self):
        self.sound_manager.play_control()
        
        self.current_input = "0"
        self.previous_value = None
        self.operation = None
        self.new_input = True
        self.is_error = False
        self.update_display()
    
    def on_clear_entry_click(self):
        self.sound_manager.play_control()
        
        if self.is_error:
            self.is_error = False
        self.current_input = "0"
        self.new_input = True
        self.update_display()
    
    def on_delete_click(self):
        self.sound_manager.play_control()
        
        if self.is_error:
            return
        
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        self.update_display()
    
    def on_percent_click(self):
        self.sound_manager.play_control()
        
        if self.is_error:
            return
        
        try:
            current = float(self.current_input)
            self.current_input = str(current / 100)
            self.update_display()
        except (ValueError, OverflowError):
            self.current_input = "Ошибка"
            self.is_error = True
            self.sound_manager.play_error()
            self.update_display()
    
    def on_sign_click(self):
        self.sound_manager.play_control()
        
        if self.is_error:
            return
        
        try:
            current = float(self.current_input)
            self.current_input = str(-current)
            self.update_display()
        except (ValueError, OverflowError):
            self.current_input = "Ошибка"
            self.is_error = True
            self.sound_manager.play_error()
            self.update_display()
    
    def on_inverse_click(self):
        self.sound_manager.play_control()
        
        if self.is_error:
            return
        
        try:
            current = float(self.current_input)
            if current == 0:
                self.current_input = "Ошибка"
                self.is_error = True
                self.sound_manager.play_error()
            else:
                self.current_input = str(1 / current)
            self.update_display()
        except (ValueError, OverflowError):
            self.current_input = "Ошибка"
            self.is_error = True
            self.sound_manager.play_error()
            self.update_display()
    
    def on_square_click(self):
        self.sound_manager.play_control()
        
        if self.is_error:
            return
        
        try:
            current = float(self.current_input)
            result = current ** 2
            if result == int(result):
                self.current_input = str(int(result))
            else:
                self.current_input = str(result)
            self.update_display()
        except (ValueError, OverflowError):
            self.current_input = "Ошибка"
            self.is_error = True
            self.sound_manager.play_error()
            self.update_display()
    
    def on_sqrt_click(self):
        self.sound_manager.play_control()
        
        if self.is_error:
            return
        
        try:
            current = float(self.current_input)
            if current < 0:
                self.current_input = "Ошибка"
                self.is_error = True
                self.sound_manager.play_error()
            else:
                result = current ** 0.5
                if result == int(result):
                    self.current_input = str(int(result))
                else:
                    self.current_input = str(result)
            self.update_display()
        except (ValueError, OverflowError):
            self.current_input = "Ошибка"
            self.is_error = True
            self.sound_manager.play_error()
            self.update_display()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())