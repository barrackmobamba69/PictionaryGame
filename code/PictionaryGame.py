# Name- Udayy Singh Pawar
# GCD student number- 3085192
# Module- HCI and GUI Programming
# BSCH - Stage 3
# Assignment02 - Pictionary Game


# Necessary imports
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDockWidget, QPushButton, QVBoxLayout, \
    QLabel, QMessageBox, QSlider, QMenu, QColorDialog, QToolBar
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap, QImage, QColor
import sys
import csv, random
from PyQt6.QtCore import Qt, QPoint


class PictionaryGame(QMainWindow):  # documentation https://doc.qt.io/qt-6/qwidget.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Pictionary Game - Assignment 02")

        # Set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # Center the window
        self.center()

        # Set the icon
        # Windows version
        self.setWindowIcon(QIcon("./icons/paint-brush.png"))  # documentation: https://doc.qt.io/qt-6/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # Image settings (default)
        self.image = QPixmap("./icons/canvas.png")  # documentation: https://doc.qt.io/qt-6/qpixmap.html
        self.image.fill(Qt.GlobalColor.white)  # documentation: https://doc.qt.io/qt-6/qpixmap.html#fill
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # Draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum

        # Reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documentation: https://doc.qt.io/qt-6/qpoint.html

        # Scores and turns
        self.turn = 1
        self.p1score = 0
        self.p2score = 0
        self.gameStarted = False

        # Set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu("File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu("Brush Size")  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu("Brush Colour")  # add the "Brush Colour" menu to the menu bar
        helpMenu = mainMenu.addMenu("Help")  # add help menu with options for about and help
        editMenu = fileMenu.addMenu("Edit")  # add an 'Edit' submenu in fileMenu
        mode = mainMenu.addMenu("Mode")  # user can select two modes; easy or hard

        # Easy mode
        easyAction = QAction(QIcon("./icons/easy5.png"), "Easy",self)
        mode.addAction(easyAction)  # connect the action to the function below
        easyAction.triggered.connect(self.easy)

        # Hard mode
        hardAction = QAction(QIcon("./icons/hard5.png"), "Hard", self)
        mode.addAction(hardAction)  # connect the action to the function below
        hardAction.triggered.connect(self.hard)

        # Connect color dialog to action
        colorAction = QAction("Color Dialog", self)
        colorAction.triggered.connect(self.colorDialogMenu)

        # Open menu item
        openAction = QAction(QIcon("./icons/open.png"), "Open", self)  # create an open action with a png as an icon, documentation: https://doc.qt.io/qt-6/qaction.html
        openAction.setShortcut("Ctrl+O")  # connect this open action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(openAction)  # add the open action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        openAction.triggered.connect(self.open)  # when the menu option is selected or the shortcut is used the open slot is triggered, documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # Save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save", self)  # create a save action with a png as an icon, documentation: https://doc.qt.io/qt-6/qaction.html
        saveAction.setShortcut("Ctrl+S")  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(saveAction)  # add the save action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        saveAction.triggered.connect(self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered, documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # Clear menu item
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # Exit menu item
        exitAction = QAction(QIcon("./icons/exit.png"), "Exit", self) # create a clear action with a png as an icon
        exitAction.setShortcut("Ctrl+Q") # connect this exit action to a keyboard shortcut
        fileMenu.addAction(exitAction) # add the exit action to the file menu
        exitAction.triggered.connect(self.close) # when the menu option is selected or the shortcut is used the exit slot is triggered

        # About menu item
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

        # Help menu item
        helpAction = QAction(QIcon("./icons/help.png"), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        # Brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # Brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+Shift+B")
        brushColorMenu.addAction(blackAction);
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+Shift+R")
        brushColorMenu.addAction(redAction);
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+Shift+G")
        brushColorMenu.addAction(greenAction);
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Shift+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        ################## EXTRA FEATURE ########################
        # Implementation of undo and redo functionalities
        # History for undo and redo
        self.history = []
        self.history_index = -1

        # Undo menu item
        undoAction = QAction(QIcon("./icons/undo.png"), "Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        editMenu.addAction(undoAction)
        undoAction.triggered.connect(self.undo)

        # Redo menu item
        redoAction = QAction(QIcon("./icons/redo.png"), "Redo", self)
        redoAction.setShortcut("Ctrl+Y")
        editMenu.addAction(redoAction)
        redoAction.triggered.connect(self.redo)

        ################## EXTRA FEATURE ########################
        # Eraser Implementation below
        # Eraser size
        self.eraserSize = 5  # Set an initial size for the eraser

        # Eraser action
        eraserAction = QAction(QIcon("./icons/eraser.png"), "Eraser", self)
        eraserAction.setShortcut("Ctrl+E")
        brushSizeMenu.addAction(eraserAction)
        eraserAction.triggered.connect(self.eraser)

        # Side Dock
        self.dockInfo = QDockWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        # Widget inside the Dock
        playerInfo = QWidget()
        self.vbdock = QVBoxLayout()
        playerInfo.setLayout(self.vbdock)
        playerInfo.setMaximumSize(100, self.height())

        # Add controls to custom widget
        self.currTurn = QLabel("Current Turn: -")
        self.vbdock.addWidget(self.currTurn)
        self.vbdock.addSpacing(20)
        self.vbdock.addWidget(QLabel("Scores:"))
        self.playerOnePoint = 0
        self.playerTwoPoint = 0
        self.lblP1score = QLabel("Player 1: " + str(self.playerOnePoint))
        self.lblP2score = QLabel("Player 2: " + str(self.playerTwoPoint))

        self.vbdock.addWidget(self.lblP1score)
        self.vbdock.addWidget(self.lblP2score)
        self.vbdock.addStretch(1)

        # start buttom for user to start game
        self.qbtn = QPushButton("Start")
        # Set background color
        color = QColor(100, 100, 100)
        self.qbtn.setStyleSheet(f"background-color: {color.name()};")

        self.qbtn.clicked.connect(self.selectMode)
        self.qbtn.clicked.connect(self.displaySecretWordPopup)
        self.qbtn.clicked.connect(self.clear)  # clear canvas to allow next player draw
        self.vbdock.addWidget(self.qbtn)

        # Button for the player to acknowledge a correct guess and earn points
        self.correct = QPushButton("Correct")
        self.correct.setStyleSheet("background: green; ")
        self.vbdock.addWidget(self.correct)
        self.correct.hide()

        self.correct.clicked.connect(self.updateScore)  # awards points on correct guess
        self.correct.clicked.connect(self.displaySecretWordPopup)  # allows next player see word
        self.correct.clicked.connect(self.clear)  # clear canvas to allow next player draw

        # Setting colour of dock to gray
        playerInfo.setAutoFillBackground(True)
        p = playerInfo.palette()
        p.setColor(playerInfo.backgroundRole(), Qt.GlobalColor.gray)
        playerInfo.setPalette(p)

        # Set widget for dock
        self.dockInfo.setWidget(playerInfo)

        self.getList("easy")
        self.setupEraserMenu()  # Set up the eraser menu
        self.currentWord = self.getWord()

        ################## EXTRA FEATURE ########################
        # ENHANCED COLOR SELECTION
        # Introduced a color wheel for expanded color options
        colorAction = QAction(QIcon("./icons/color-wheel.png"), "Color wheel", self)
        colorAction.setShortcut("Ctrl+Shift+W")
        brushColorMenu.addAction(colorAction)
        colorAction.triggered.connect(self.colorDialogMenu)

        # Integrate color wheel into toolbar
        self.toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.toolbar)

    # Event handlers
    # Center the main window on the screen
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
            self.update_history()  # Save the current state to history
            print(self.lastPoint)  # print the lastPoint for debugging purposes

    def mouseMoveEvent(self, event):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-6/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self, event):  # when the mouse is released, documentation: https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button, documentation: https://doc.qt.io/qt-6/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode

    # Paint event
    def paintEvent(self, event):
        canvasPainter = QPainter(self)  # create a new QPainter object, documentation: https://doc.qt.io/qt-6/qpainter.html
        canvasPainter.drawPixmap(QPoint(), self.image)  # draw the image , documentation: https://doc.qt.io/qt-6/qpainter.html#drawImage-1

    # Resize event
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # Undo menu item
    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index].copy()
            self.update()

    # Redo menu item
    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.image = self.history[self.history_index].copy()
            self.update()

    def update_history(self):
        # Limit the history size to 10 for demonstration purposes
        self.history = self.history[:self.history_index + 1] + [self.image.copy()]
        self.history_index = len(self.history) - 1

    def save(self):
        """ Saves the image to the specified file path with specified file format (PNG, JPG or JPEG) """
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    # Clears the canvas after the user's confirmation
    def clear(self):
        self.image.fill(Qt.GlobalColor.white)  # fill the image with white, documentation: https://doc.qt.io/qt-6/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    # Exits the application after the user's confirmation
    def exit(self):
        btnReply = QMessageBox.question(self, 'Exit Confirmation', "Exit the application?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if btnReply == QMessageBox.Yes:
            QApplication.quit()

    # Method to display user guide and about pages
    def about(self):
        aboutText = ("Pictionary Game Application\n\n"
                     "© 2023 Udayy Singh Pawar. All rights reserved\n"
                     "Created by Udayy Singh Pawar\n\n"
                     "Copyright 2023\n\n"
                     "Griffith College Dublin")

        QMessageBox.about(self, "About Pictionary Game Application", aboutText)

    # Method to display user guide and about Help menu
    def help(self):
        aboutText = (
            "Welcome to the Pictionary Game Application!\n\n"
            "Here are some key features and instructions:\n\n"
            "- To draw, click and drag the left mouse button on the canvas.\n"
            "- Use the 'File' menu to open, save, clear the canvas, and exit the application.\n"
            "- Adjust the brush size and color from the 'Brush Size' and 'Brush Colour' menus.\n"
            "- Undo and redo actions are available in the 'Edit' menu.\n"
            "- Start the game by clicking the 'Start' button and follow the on-screen instructions.\n"
            "- The 'Correct' button awards points to the current player when they guess the word.\n"
            "- Explore additional features such as the eraser, different brush sizes, and color wheel.\n"
            "- Choose game modes ('Easy' or 'Hard') from the 'Mode' menu.\n"
            "- For more information, check the documentation."
        )
        QMessageBox.information(self, "Help - Pictionary Game", aboutText)

    # The brush size is set to 3
    def threepx(self):
        self.brushSize = 3

    # The brush size is set to 5
    def fivepx(self):
        self.brushSize = 5

    # The brush size is set to 7
    def sevenpx(self):
        self.brushSize = 7

    # The brush size is set to 9
    def ninepx(self):
        self.brushSize = 9

    # The brush colour is set to black
    def black(self):
        self.brushColor = Qt.GlobalColor.black

    # The brush colour is set to red
    def red(self):
        self.brushColor = Qt.GlobalColor.red

    # The brush colour is set to green
    def green(self):
        self.brushColor = Qt.GlobalColor.green

    # The brush colour is set to yellow
    def yellow(self):
        self.brushColor = Qt.GlobalColor.yellow

    # Get a random word from the list read from file
    def getWord(self):
        randomWord = random.choice(self.wordList)
        print(randomWord)
        return randomWord

    # Read word list from file
    def getList(self, mode):
        with open(mode + 'mode.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                #print(row)
                self.wordList = row
                line_count += 1
            #print(f'Processed {line_count} lines.')

    # Open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file dialog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    # Eraser Implementation
    def eraser(self):
        # Set the brush color to white for erasing
        self.brushColor = Qt.GlobalColor.white
        # Set the brush size to the eraser size
        self.brushSize = self.eraserSize
        # Show the eraser size slider
        self.eraserSizeSlider.show()

    # The updateEraserSize method is responsible for updating the eraser size based on the value of the eraser size slider.
    def updateEraserSize(self):
        # Update eraser size based on the slider value
        self.eraserSize = self.eraserSizeSlider.value()
        # If in eraser mode, update the brush size accordingly
        if self.brushColor == Qt.GlobalColor.white:
            self.brushSize = self.eraserSize

    # When the eraser tool is selected, it sets the brush color to white (Qt.GlobalColor.white) and adjusts the brush size to the specified eraser size.
    def setupEraserMenu(self):
        eraserMenu = QMenu(self)

        # Eraser action
        eraserAction = QAction(QIcon("./icons/eraser.png"), "Eraser", self)
        eraserAction.setShortcut("Ctrl+E")
        eraserMenu.addAction(eraserAction)
        eraserAction.triggered.connect(self.showEraserSlider)

        # Eraser size slider
        self.eraserSizeSlider = QSlider(Qt.Orientation.Horizontal)
        self.eraserSizeSlider.setMinimum(1)
        self.eraserSizeSlider.setMaximum(20)
        self.eraserSizeSlider.setValue(self.eraserSize)
        self.eraserSizeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.eraserSizeSlider.setTickInterval(1)
        self.eraserSizeSlider.valueChanged.connect(self.updateEraserSize)

        # Add eraser size slider to layout
        self.vbdock.addWidget(self.eraserSizeSlider)

        return eraserMenu

    def showEraserSlider(self):
        # Show the eraser size slider
        self.eraserSizeSlider.show()

    # Method for displaying popup box to reveal secret word to the current player
    def displaySecretWordPopup(self):

        if self.gameStarted:  # Check if the game has started before revealing the secret word
            print("Game has already started!!")
            if self.turn == 1:  # Update the current player's turn
                self.turn = 2
            else:
                self.turn = 1

        # Create and customize a QMessageBox instance to display the secret word
        message = QMessageBox()
        message.setText("Player " + str(self.turn) + " See your word:")  # Inform the player whose turn it is
        message.setInformativeText("Dont let others see! Click on details. ")  # Remind the player to keep the word confidential
        message.setStandardButtons(QMessageBox.StandardButton.Ok)  # Provide an "Ok" button to acknowledge the revealed word
        message.setIcon(QMessageBox.Icon.Question)
        message.setDetailedText(self.getWord())  # Display the randomly selected secret word
        button = message.exec()  # Execute the message box and capture the user's action

        # Handle the user's response to the secret word disclosure
        if button == QMessageBox.StandardButton.Ok:
            print("Secret word revealed!")
            self.gameStarted = True  # Indicate that the game has started
            self.qbtn.setText("Next player")  # Update the button text
            self.qbtn.setStyleSheet("background: none ")
            self.currTurn.setText("Player " + str(self.turn) + " Turn")  # Update the current player display
            self.statusBar().showMessage("Player " + str(self.turn) + " Drawing Turn")  # Update the status bar message
            self.show()  # Update the GUI display
            self.correct.show()  # Display the 'Correct' button
        else:
            print("Secret word not revealed!")

    # Update player scores and their corresponding GUI labels
    def updateScore(self):
        if self.turn == 1:
            # Player-1 gains 2 points and Player-2 gains 1 point
            self.playerOnePoint += 2
            self.playerTwoPoint += 1
        else:
            # Player-1 gains 1 point and Player-2 gains 2 points
            self.playerOnePoint += 1
            self.playerTwoPoint += 2

        self.lblP1score.setText("Player 1: " + str(self.playerOnePoint))
        self.lblP2score.setText("Player 2: " + str(self.playerTwoPoint))
        self.lblP1score.update()
        self.lblP2score.update()

    # Retrieve a list of items for the easy mode
    def easy(self):
        self.getList("easy")

    # Retrieve a list of items for the hard mode
    def hard(self):
        self.getList("hard")

    # Prompt user to select game mode between 'Hard Mode' and 'Easy Mode'
    def selectMode(self):
        modeSelectionPopup = QMessageBox()
        modeSelectionPopup.setText("Select Game Mode: ")  # Asking user to select game mode
        modeSelectionPopup.setInformativeText("Choose 'Hard Mode' for more challenge or 'Easy Mode' for a simpler experience.")
        modeSelectionPopup.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        modeSelectionPopup.button(QMessageBox.StandardButton.Yes).setText("Hard Mode")
        modeSelectionPopup.button(QMessageBox.StandardButton.No).setText("Easy Mode")
        button = modeSelectionPopup.exec()
        if button == QMessageBox.StandardButton.Yes:
            self.hard()  # Call the 'hard()' method if 'Hard Mode' is selected
        else:
            self.easy()  # Call the 'easy()' method if 'Easy Mode' is selected

    # Create color dialog, get selected color, and set brush color if valid
    def colorDialogMenu(self):
        colorDialog = QColorDialog(self)  # Create an instance of QColorDialog
        selectedColor = colorDialog.getColor()

        # Set the brush color if the selected color is valid
        if selectedColor .isValid():
            self.brushColor = selectedColor

    # Display color dialog and set brush color accordingly
    def showColorDialog(self):
        # Show QColorDialog and get the selected color
        colorDialog = QColorDialog(self)
        selectedColor = colorDialog.getColor()
        if selectedColor .isValid():
            self.brushColor = selectedColor


# Main program execution starts here
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PictionaryGame()
    window.show()
    app.exec()  # Start the event loop running
