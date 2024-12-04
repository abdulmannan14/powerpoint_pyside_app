import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QHBoxLayout, \
    QPushButton, QFrame, QGroupBox, QDateEdit, QCheckBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PowerPoint MVP")  # Set window title
        self.setStyleSheet("background-color: lightblue;")
        self.setGeometry(0, 10, 1430, 0)  # Set window size and position

        # Initialize UI components
        self.main_layout = QVBoxLayout()
        self.top_button_layout = QHBoxLayout()
        self.form_layout = QFormLayout()
        self.top_row_layout = QHBoxLayout()

        # Mapping screens

        self.screens = {
            "Test Setup #2:Telescope: Range, manual.": SetupScreen2(self),
            "Test Setup #3:Lift: Range, powered": SetupScreen3(self),
            "Test Setup #4:Deflection, vertical": SetupScreen4(self),
            "Test Setup #5:(Right Bracket) Deflection, horizontal": SetupScreen5(self),
            "Test Setup #6:(Right Bracket) Lift: Behavior, motion": SetupScreen6(self),
            "Test Setup #7:(Left Bracket) Deflection, horizontal": SetupScreen7(self),
            "Test Setup #8:(Left Bracket) Lift: Behavior, motion": SetupScreen8(self)
            # Add more mappings here
        }

        self.device_sn = QLineEdit()
        self.operator = QLineEdit()
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.device_sn.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc;")
        self.operator.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc;")
        self.date.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc;")

        # Set up the UI
        self.setup_top_button()
        self.setup_form_layout()
        self.setup_test_select_section()
        self.main_layout.setSpacing(0)  # Remove spacing between widgets

        # Set the layout for the window
        self.setLayout(self.main_layout)

    def setup_top_button(self):
        """Set up the 'Generate Report' button at the top-right corner."""
        self.top_button_layout.setAlignment(Qt.AlignRight)  # Align the button to the right
        generate_report_button = QPushButton("Generate Report")
        generate_report_button.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.top_button_layout.addWidget(generate_report_button)

        # Add the top button layout to the main layout
        self.main_layout.addLayout(self.top_button_layout)

    def setup_form_layout(self):
        """Set up the form layout with labels and input fields."""
        self.top_row_layout.addWidget(QLabel("Device SN:"))
        self.top_row_layout.addWidget(self.device_sn)
        self.top_row_layout.addWidget(QLabel("Operator:"))
        self.top_row_layout.addWidget(self.operator)
        self.top_row_layout.addWidget(QLabel("Date:"))
        self.top_row_layout.addWidget(self.date)

        # Add the top row layout to the form layout
        self.form_layout.addRow(self.top_row_layout)
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;")

        self.top_row_layout.addWidget(submit_button)

        # Add a horizontal line for separation
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        self.form_layout.addRow(horizontal_line)

        # Wrap the form layout inside a QWidget to apply a stylesheet
        form_widget = QWidget()
        form_widget.setLayout(self.form_layout)
        form_widget.setStyleSheet("background-color: lightblue;")  # Set background color for the form section

        # Add the form widget to the main layout
        self.main_layout.addWidget(form_widget)

    def setup_test_select_section(self):
        """Set up the test selection section with button-like rows and checkboxes."""
        test_select_group = QGroupBox("Select Test Setup")
        test_select_group.setStyleSheet("background-color: #1f5673; color: white; padding: 40px;")
        test_select_layout = QVBoxLayout()

        test_setups = [
            "Test Setup #2:Telescope: Range, manual.",
            "Test Setup #3:Lift: Range, powered",
            "Test Setup #4:Deflection, vertical",
            "Test Setup #5:(Right Bracket) Deflection, horizontal",
            "Test Setup #6:(Right Bracket) Lift: Behavior, motion",
            "Test Setup #7:(Left Bracket) Deflection, horizontal",
            "Test Setup #8:(Left Bracket) Lift: Behavior, motion"
        ]

        self.checkboxes = {}  # Store checkboxes for manipulation later

        # Create checkboxes and buttons for each test setup
        for setup in test_setups:
            button = QPushButton(setup)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #3b7e99; 
                    color: white; 
                    padding: 10px; 
                    margin-bottom: 5px; 
                    border-radius: 5px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #2a697e;
                }
                QPushButton:pressed {
                    background-color: #1e4d5f;
                }
                """
            )
            button.clicked.connect(lambda checked, text=setup: self.redirect_to_screen(text))
            test_select_layout.addWidget(button)

            # Set the layout for the test select group
        test_select_group.setLayout(test_select_layout)

        # Add the test select group to the main layout
        self.main_layout.addWidget(test_select_group)

    def redirect_to_screen(self, setup_text):
        """Handle redirection based on the setup selected."""
        if setup_text in self.screens:
            self.hide()  # Hide the main window
            self.screens[setup_text].show()
        else:
            print(f"No screen defined for: {setup_text}")


# ==============================================================
class SetupScreenInside(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent  # Reference to the main screen
        self.setGeometry(0, 10, 1430, 0)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add a Back button
        back_button = QPushButton("Back to Main Screen")
        back_button.setStyleSheet(
            "background-color: #f44336; color: white; padding: 10px; border-radius: 5px;"
        )
        back_button.clicked.connect(self.go_back)
        self.layout.addWidget(back_button)

    def go_back(self):
        """Go back to the main screen."""
        self.hide()
        self.parent.show()


class SetupScreen2(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #2")
        self.layout.addWidget(QLabel("Welcome to Test Setup #2!"))


class SetupScreen3(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #3")
        self.layout.addWidget(QLabel("Welcome to Test Setup #3!"))


class SetupScreen4(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #4")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


class SetupScreen5(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #4")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


class SetupScreen6(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #4")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


class SetupScreen7(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #4")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


class SetupScreen8(SetupScreenInside):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Setup #4")
        self.layout.addWidget(QLabel("Welcome to Test Setup #4!"))


# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
