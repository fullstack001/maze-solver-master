import generate
import solver
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QAction, QPixmap, QImage, QPainter
from PyQt6.QtCore import Qt
from generate import generate
from solver import solver
# from maze_solver.generate import generate  // origin
# from maze_solver.solver import solver      // origin
# from .menu import make_menu
from .image import create_image_from_maze
import numpy as np
from PIL import Image, ImageQt

class GUI:
    height = 800
    width = 800
    title = "Maze Solver"
    maze = np.zeros(shape=(20, 20), dtype=int)
    maze_for_image_update = np.zeros(shape=(20, 20), dtype=int)
    
    app = None
    window = None
    image_label = None
    setCentralWidget = None
    timer = None

    def __init__(self):
        return
        #do nothing

    def draw(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.setWindowTitle(self.title)
        self.window.setGeometry(0, 0, self.width, self.height)

        self.draw_menus()

        self.image_label = QLabel(self.window)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.window.setCentralWidget(self.image_label)

        # self.timer = QTimer(self.window)
        # self.timer.timeout.connect(self.draw_maze)
        # self.timer.start(100)
        
        self.window.show()
        self.app.exec()

    def draw_menus(self):
        # menu_bar = make_menu(self.root, [
        #     {
        #         "label": "Maze",
        #         "commands": [
        #             {
        #                 "label": "Generate Maze",
        #                 "callback": self.generate_maze_action
        #             },
        #             {
        #                 "label": "Solve Maze",
        #                 "callback": self.solve_maze_action
        #             }
        #         ]
        #     }
        # ])
        menubar = self.window.menuBar()
        maze_menu = menubar.addMenu("Maze")
        generate_maze_action = QAction("Generate Maze", self.window)
        generate_maze_action.triggered.connect(self.generate_maze_action)
        maze_menu.addAction(generate_maze_action)
        solve_maze_action = QAction("Solve Maze", self.window)
        solve_maze_action.triggered.connect(self.solve_maze_action)
        maze_menu.addAction(solve_maze_action)

    def pil_to_qimage(self, pil_image):
        q_image = ImageQt.ImageQt(pil_image)
        qt_image = QImage(q_image)

        # Create a QPainter and set the interpolation
        painter = QPainter()
        painter.begin(qt_image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)

        # Draw the image onto the QImage
        painter.drawImage(0, 0, q_image)

        painter.end()


        return qt_image

    def draw_maze(self):
        pil_image = Image.fromarray(create_image_from_maze(self.maze_for_image_update, 2))
        qt_image = self.pil_to_qimage(pil_image)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)
        self.app.processEvents()

    def generate_maze_action(self):
        self.maze = generate.generate_maze(15, 15)
        self.maze_for_image_update = self.maze.copy()
        self.draw_maze()

    def maze_repainter(self, maze):
        self.maze_for_image_update = maze
        self.draw_maze()

    def solve_maze_action(self):
        explorer = solver.solve_maze(self.maze, self.maze_repainter)
        self.maze_for_image_update = explorer.paint_paths()
        self.draw_maze()
        self.app.processEvents()