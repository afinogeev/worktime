from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSystemTrayIcon, QStyle, QAction, qApp, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import widget
import sys
import time
import coretime

## UI
class UiApp(QtWidgets.QWidget, widget.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('clock.ico')) 
        
         # Инициализируем QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)  
        #self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setIcon(QIcon('clock.ico'))
 
        '''
            Объявим и добавим действия для работы с иконкой системного трея
            show - показать окно
            hide - скрыть окно
            exit - выход из программы
        '''
        show_action = QAction("Развернуть", self)
        quit_action = QAction("Выход", self)
        hide_action = QAction("Скрыть", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.lineEditD.returnPressed.connect(self.setDays)
        self.lineEditH.returnPressed.connect(self.setHours)
        
        self.update()
        
    # Переопределение метода closeEvent, для перехвата события закрытия окна
    # Окно будет закрываться только в том случае, если нет галочки в чекбоксе
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
                "Рабочее время",
                "Приложение свернуто в трей",
                QSystemTrayIcon.Information,
                1000
        )

    def update(self):
        coretime.update()
        self.labelM.setText(str(coretime.month))
        self.lineEditD.setText(str(coretime.allDays))
        self.lineEditH.setText(coretime.floatToTime(coretime.allHours))
        self.labelDd.setText(str(coretime.doneDays))
        self.labelHd.setText(coretime.floatToTime(coretime.doneHours))
        self.labelTb.setText(coretime.floatToTime(coretime.todayBegin))
        self.labelAd.setText(coretime.floatToTime(coretime.getDoneAverage()))
        self.labelDl.setText(str(coretime.getLeftDays()))
        self.labelHl.setText(coretime.floatToTime(coretime.getLeftHours()))
        self.labelAl.setText(coretime.floatToTime(coretime.getLeftAverage()))
        self.progressBarA.setValue(coretime.getPercentAll())
        self.progressBarT.setValue(coretime.getPercentToday())
        self.labelTe.setText(coretime.floatToTime(coretime.todayGo))
        leftTime = coretime.todayGo-coretime.todayBegin-coretime.todayDuration
        self.labelTl.setText(coretime.floatToTime(leftTime))
        if(0<leftTime<0.02):
            self.tray_icon.showMessage(
                "Рабочее время",
                "Пора домой!",
                QSystemTrayIcon.Information,
                1000
            )
            
    def setDays(self):
        days = int(self.lineEditD.text())
        hours = days*8.75
        coretime.setAllDays(days)
        coretime.setAllHours(hours)
        self.lineEditH.setText(coretime.floatToTime(coretime.allHours))
        self.update()
    
    def setHours(self):        
        hours = coretime.timeToFloat(self.lineEditH.text())
        coretime.setAllHours(hours)
        self.update()
    
###
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = UiApp()
    window.show()
    timer = QTimer()
    timer.timeout.connect(window.update)
    timer.start(60000)
    app.exec_()
    sys.exit()

    
if __name__ == '__main__':  
    main()  
