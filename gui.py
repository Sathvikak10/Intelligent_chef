import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QRadioButton, QButtonGroup)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from obj_det import ObjectDetector
from recipe_generator import RecipeGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window properties
        self.setWindowTitle("Recipe Generator")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Display Image section
        display_image_section = QVBoxLayout()

        self.image_label = QLabel("Display Image")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("QLabel { background-color: white; color: black; border: 1px solid black; min-height: 400px; }")

        browse_button = QPushButton("Browse Image")
        browse_button.setStyleSheet("QPushButton { background-color: white; color: black; border: 1px solid black; }")
        browse_button.clicked.connect(self.browse_image)

        generate_recipe_button = QPushButton("Generate Recipe")
        generate_recipe_button.setStyleSheet("QPushButton { background-color: white; color: black; border: 1px solid black; }")
        generate_recipe_button.clicked.connect(self.generate_recipe)

        # Control layout for browse and generate buttons
        control_layout = QHBoxLayout()
        control_layout.addWidget(browse_button)
        control_layout.addWidget(generate_recipe_button)

        display_image_section.addWidget(self.image_label)
        display_image_section.addLayout(control_layout)

        # Display Generated Recipe section
        display_recipe_section = QVBoxLayout()

        self.recipe_label = QLabel("Display Generated Recipe")
        self.recipe_label.setAlignment(Qt.AlignLeft)
        self.recipe_label.setFont(QFont('Arial', 12))
        self.recipe_label.setStyleSheet("QLabel { background-color: white; color: black; border: 1px solid black; font-size: 14px; min-height: 400px; }")

        copy_recipe_button = QPushButton("Copy Recipe")
        copy_recipe_button.setStyleSheet("QPushButton { background-color: white; color: black; border: 1px solid black; }")
        copy_recipe_button.clicked.connect(self.copy_recipe)

        display_recipe_section.addWidget(self.recipe_label)
        display_recipe_section.addWidget(copy_recipe_button)

        # Add sections to the main layout
        layout.addLayout(display_image_section)
        layout.addLayout(display_recipe_section)

        central_widget.setLayout(layout)

        self.obj_detector = ObjectDetector()
        self.recipe_gen = RecipeGenerator("insert an apikey")

    def browse_image(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if self.file_name:
            pixmap = QPixmap(self.file_name)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def generate_recipe(self):
        frame = cv2.imread(self.file_name)
        frame, results = self.obj_detector.obj_detection(frame)
        ingredients = self.obj_detector.crop_objects_by_name(results, frame)
        recipe = self.recipe_gen.generate_recipe(ingredients)
        self.recipe_label.setText(recipe)  # Display the generated recipe in the label
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

    def copy_recipe(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.recipe_label.text())
        print("Recipe copied to clipboard...")

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
