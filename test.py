import tkinter
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Menu
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor


class ploting():
    def __init__(self, file_path, time_col):
        df = pd.read_csv(file_path)
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        df = df.dropna(subset=[time_col])
        df['time'] = df[time_col]
        df = df.set_index(time_col, drop=True)
        df = df.resample('1min').min()
        index = df['id'].notnull()
        df = df[index]
        df.to_csv(r'data.csv')
        self.df = df

    def run(self):
        print(self.df)
        self.df.to_csv('data2.csv')
        self.figure()

    def figure(self):
        ax1 = self.df['time']
        ay1 = self.df['device_val']
        ax1.plot(ax1, ay1, color='r')
        '''''
        ax2 = ax1.twinx() #twinx将ax1的X轴共用与ax2，这步很重要
        ax2.plot(ax1, 100, color='g')
        ax2.set_ylabel('KWh')
        '''''
        cursor = Cursor(ax1, useblit=True, color='red', linewidth=2)
        plt.show()

class Maintk():
    def __init__(self, file_path, time_col):
        root = tkinter.Tk()  # 创建tkinter的主窗口
        root.title('UNNC Iot Monitor')
        self.root = root
        self.file_path = file_path
        self.time_col = time_col

    def run(self):
        self.canvas()
        self.menu()
        self.root.mainloop()

    def menu(self):
        # Creating a Menu Bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Add file menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="export csv file")
        file_menu.add_command(label='import new project')
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Add about menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)


    def canvas(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)  # 添加子图:1行1列第1个
        ax.set_xlabel('time')
        ax.set_ylabel('temperature')
        ax.grid()
        # 在前面得到的子图上绘图
        Plot = ploting(self.file_path, self.time_col)
        ax.plot(Plot.df['time'], Plot.df['device_val'])
        #line, = ax.plot(Plot.df['time'], Plot.df['device_val'])
        #snap_cursor = SnappingCursor(ax, line)
        #fig.canvas.mpl_connect('motion_notify_event', snap_cursor.on_mouse_move)
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()  # 注意show方法已经过时了,这里改用draw
        canvas.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                                    fill=tkinter.BOTH,  # 填充方式
                                    expand=tkinter.YES)  # 随窗口大小调整而调整
        # matplotlib的导航工具栏显示上来(默认是不会显示它的)
        toolbar = NavigationToolbar2Tk(canvas, self.root)
        toolbar.update()
        canvas._tkcanvas.pack(side=tkinter.TOP,  # get_tk_widget()得到的就是_tkcanvas
                              fill=tkinter.BOTH,
                              expand=tkinter.YES)

    def _quit(self):
        """点击退出按钮时调用这个函数"""
        self.root.quit()  # 结束主循环
        self.root.destroy()  # 销毁窗口

class SnappingCursor:
    """
    A cross hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    def __init__(self, ax, line):
        self.ax = ax
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        self.x, self.y = line.get_data()
        self._last_index = None
        # text location in axes coords
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            index = min(np.searchsorted(self.x, x), len(self.x) - 1)
            if index == self._last_index:
                return  # still on the same data point. Nothing to do.
            self._last_index = index
            x = self.x[index]
            y = self.y[index]
            # update the line positions
            self.horizontal_line.set_ydata(y)
            self.vertical_line.set_xdata(x)
            self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))
            self.ax.figure.canvas.draw()


if __name__ == '__main__':
    file_path = 'BBBBBB.csv'
    time_col = 'create_time'
    Maintk(file_path, time_col).run()  # Get user input
    Maintk(file_path, time_col).root.update()


