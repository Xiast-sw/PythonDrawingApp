import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Uygulaması")

        # Canvas oluşturma
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.color = "black"
        self.pen_width = 3
        self.shape = "line"  # Varsayılan şekil
        self.start_x = None
        self.start_y = None

        # Renk Seçim Butonu
        color_button = tk.Button(root, text="Renk Seç", command=self.choose_color)
        color_button.pack()

        # Kalem Kalınlığı Seçim Butonları
        thickness_frame = tk.Frame(root)
        thickness_frame.pack()

        for thickness in [1, 3, 5, 7, 10]:
            button = tk.Button(thickness_frame, text=str(thickness), command=lambda t=thickness: self.change_thickness(t))
            button.pack(side=tk.LEFT)

        # Şekil Seçim Butonları
        shape_frame = tk.Frame(root)
        shape_frame.pack()

        tk.Button(shape_frame, text="Kare", command=self.select_square).pack(side=tk.LEFT)
        tk.Button(shape_frame, text="Daire", command=self.select_circle).pack(side=tk.LEFT)
        tk.Button(shape_frame, text="Üçgen", command=self.select_triangle).pack(side=tk.LEFT)
        tk.Button(shape_frame, text="Düz Çizgi", command=self.select_line).pack(side=tk.LEFT)
        tk.Button(shape_frame, text="Serbest Çizim", command=self.select_free_draw).pack(side=tk.LEFT)  # Serbest Çizim Butonu
        tk.Button(shape_frame, text="Silgi", command=self.select_eraser).pack(side=tk.LEFT)  # Silgi Butonu

        # Temizleme Butonu
        clear_button = tk.Button(root, text="Temizle", command=self.clear_canvas)
        clear_button.pack()

        # Fare ile Çizim için olayları bağlama
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color

    def change_thickness(self, new_thickness):
        self.pen_width = new_thickness

    def select_square(self):
        self.shape = "square"

    def select_circle(self):
        self.shape = "circle"

    def select_triangle(self):
        self.shape = "triangle"

    def select_line(self):
        self.shape = "line"

    def select_free_draw(self):
        self.shape = "free"  # Serbest çizim seçeneğini ayarlama

    def select_eraser(self):
        self.shape = "eraser"  # Silgi seçeneğini ayarlama

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def paint(self, event):
        if self.shape == "free":
            # Serbest çizim için
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.pen_width)
            self.start_x = event.x
            self.start_y = event.y
        elif self.shape == "eraser":
            # Silgi için beyaz ile çizim yap (kalınlık artırıldı)
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill="white", width=self.pen_width + 5)  # Silgi kalınlığını artırdık
            self.start_x = event.x
            self.start_y = event.y
        else:
            if self.start_x is None or self.start_y is None:
                return

            self.canvas.delete("temp")

            if self.shape == "line":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.pen_width, tags="temp")
            elif self.shape == "square":
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.pen_width, tags="temp")
            elif self.shape == "circle":
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.pen_width, tags="temp")
            elif self.shape == "triangle":
                self.canvas.create_polygon(self.start_x, self.start_y, event.x, event.y, self.start_x, event.y, outline=self.color, width=self.pen_width, tags="temp", fill='')  # İçini boş bırak

    def on_button_release(self, event):
        if self.shape != "free":  # Eğer serbest çizim değilse şekli tamamla
            if self.shape == "line":
                self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.pen_width)
            elif self.shape == "square":
                self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.pen_width)
            elif self.shape == "circle":
                self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=self.pen_width)
            elif self.shape == "triangle":
                self.canvas.create_polygon(self.start_x, self.start_y, event.x, event.y, self.start_x, event.y, outline=self.color, width=self.pen_width, fill='')  # İçini boş bırak

        self.start_x = None
        self.start_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
