# co jest juz zrobione:
# wczytywanie obrazów
# możliwość robienia operacji na 1 lub 2 obrazach
# operacje dodawnie liczby do jednego obrazu, dodawanie 2 obrazow, odejmowanie 2 obrazow
# normalizacje brak normalizacji (obciecie), modul i obciecie

import tkinter.font as font

import tkinter as tk
import cv2
import numpy as np

from tkinter import simpledialog, messagebox
from tkinter.filedialog import askopenfilename

from PIL import ImageTk, Image

def normalizacja_obciecie(arr):
    rows = int(len(arr))
    col = int(len(arr[0]))
    for i in range(rows):
        for j in range(col):
            if arr[i, j] > 255:
                arr[i, j] = 255
            if arr[i, j] < 0:
                arr[i, j] = 0
    return np.uint8(arr)


def normalizacja_modul_z_obcieciem(arr):
    rows = int(len(arr))
    col = int(len(arr[0]))
    for i in range(rows):
        for j in range(col):
            if 0 > arr[i, j]:
                arr[i, j] = arr[i, j] * -1
            if arr[i, j] > 255:
                arr[i, j] = 255
    return np.uint8(arr)


def normalizacja_skalowanie(arr):
    arr = np.uint32(arr)
    rows = int(len(arr))
    col = int(len(arr[0]))
    min_value = arr.min()
    max_value = arr.max()
    for i in range(rows):
        for j in range(col):
            arr[i, j] = (arr[i, j] - min_value) * 255 / (max_value - min_value)
    return np.uint8(arr)


def normalizacja_piloksztaltna(arr):
    arr = np.uint32(arr)
    rows = int(len(arr))
    col = int(len(arr[0]))
    for i in range(rows):
        for j in range(col):
            arr[i, j] = arr[i, j] % 255
    return np.uint8(arr)


def call_normalization(img_temp, selected_normalization):
    if selected_normalization.get() == 'A':
        return normalizacja_obciecie(img_temp)
    elif selected_normalization.get() == 'B':
        return normalizacja_modul_z_obcieciem(img_temp)
    elif selected_normalization.get() == 'C':
        return normalizacja_skalowanie(img_temp)
    elif selected_normalization.get() == 'D':
        return normalizacja_piloksztaltna(img_temp)


class Picture:
    def __init__(self):
        self.__img = None  # obraz w tablicy (na tym przeprowadzamy operacje) typ pola <class 'numpy.ndarray'> coś jak lista tylko składa sie np z uint8
        self.__image = None  # obraz, (tylko do wyświetlania) typ pola -  <class 'PIL.ImageTk.PhotoImage'> idk
        self.canvas = None  # płótno na którym będzie wyświetlał się obraz
        self.canvas_img = None  # ustawienie obrazu na tym płótnie (na początku blank_image) (mało ważne) (nie wiem co robi ale musi być)

    def set_canvas(self, value):
        self.__canvas = value

    def set_canvas_img(self, value):
        self.__canvas_img = value

    def get_canvas(self):
        return self.__canvas

    def get_img(self):
        return self.__img

    def set_new_image(self, image_to_set):
        height = int(len(image_to_set))
        width = int(len(image_to_set[0]))
        if height != 256 or width != 256:
            image_to_set = cv2.resize(image_to_set, (256, 256), interpolation=cv2.INTER_AREA)
        self.__img = image_to_set
        self.__image = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(image_to_set, (450, 450),
                                                                           interpolation=cv2.INTER_AREA)))  # przypisanie do zmiennej globalnej obrazu
        self.__canvas.itemconfig(self.__canvas_img, image=self.__image)  # zmiana obrazu z blank_image na nowy

    def input_picture(self):
        filename = askopenfilename()  # otwarcie okienka do wyboru pliku
        self.__img = cv2.imread(cv2.samples.findFile(filename), 0)  # wczytanie do zmiennej obrazu o podanej nazwie
        self.set_new_image(self.__img)

    def operation_add_value(self, p1, selected_normalization):
        value = simpledialog.askstring(title="Wprowadź", prompt="Podaj liczbę całkowitą:")
        if p1.__img is not None:
            if value is not None:
                try:
                    value = int(value)
                    img_temp = np.copy(p1.__img)
                    img_temp = np.int16(img_temp)
                    img_temp = img_temp + np.int16(value)
                    img_temp = call_normalization(img_temp, selected_normalization)
                    self.set_new_image(img_temp)
                except Exception:
                    tk.messagebox.showerror(title="Błąd", message="Podałeś złą wartość")
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obraz")

    def operation_add_pictures(self, p1, p2, selected_normalization):
        if p1.__img is not None and p2.__img is not None:
            img_temp = np.copy(p1.__img)
            img_temp = np.int16(img_temp)
            img_temp = img_temp + p2.__img
            img_temp = call_normalization(img_temp, selected_normalization)
            self.set_new_image(img_temp)
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obrazy")

    def operation_multiply_pictures(self, p1, p2, selected_normalization):
        if p1.__img is not None and p2.__img is not None:
            img_temp = np.copy(p1.__img)
            img_temp = np.int32(img_temp)
            img_temp = img_temp * p2.__img
            img_temp = call_normalization(img_temp, selected_normalization)
            self.set_new_image(img_temp)
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obrazy")

    def operation_subtract_pictures(self, p1, p2, selected_normalization):
        if p1.__img is not None and p2.__img is not None:
            img_temp = np.copy(p1.__img)
            img_temp = np.int16(img_temp)
            img_temp = img_temp - p2.__img
            img_temp = call_normalization(img_temp, selected_normalization)
            self.set_new_image(img_temp)
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obrazy")

    def operation_multiply_value(self, p1, selected_normalization):
        value = simpledialog.askstring(title="Wprowadź", prompt="Podaj liczbę całkowtą:")
        if p1.__img is not None:
            if value is not None:
                try:
                    value = int(value)
                    if int(value) <= 0:
                        raise ValueError()
                    img_temp = np.copy(p1.__img)
                    img_temp = np.int16(img_temp)
                    img_temp = img_temp * np.int16(value)
                    img_temp = call_normalization(img_temp, selected_normalization)
                    self.set_new_image(img_temp)
                except ValueError:
                    tk.messagebox.showerror(title="Błąd", message="Podaj całkowitą liczbę większą od zera")
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obraz")

    def operation_natural_logarithm(self, p1, selected_normalization):
        if p1.__img is not None:
            img_temp = np.copy(p1.__img)
            img_temp = np.int16(img_temp)
            try:
                img_temp = np.log(img_temp)
                img_temp = call_normalization(img_temp, selected_normalization)
                self.set_new_image(img_temp)
            except RuntimeWarning:
                tk.messagebox.showerror(title="Błąd", message="Nie istnieje ln z 0 ")
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obraz")

    def operation_negation(self, p1, selected_normalization):
        if p1.__img is not None:
            img_temp = np.copy(p1.__img)
            img_temp = np.int16(img_temp)
            img_temp = np.int16(255) - img_temp
            img_temp = call_normalization(img_temp, selected_normalization)
            self.set_new_image(img_temp)
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obraz")

    def operation_linear_combination(self, p1, p2, selected_normalization):
        value = simpledialog.askstring(title="Input", prompt="Podaj wartość p z przedziału od 0 do 1:")
        if p1.__img is not None and p2.__img is not None:
            if value is not None:
                try:
                    value = value.replace(",", ".")
                    value = float(value)
                    if value < 0 or value > 1:
                        raise Exception
                    img_temp = np.copy(p1.__img)
                    img_temp = np.int16(img_temp)
                    img_temp = img_temp * value + np.int16(p2.__img) * (1 - value)
                    img_temp = call_normalization(img_temp, selected_normalization)
                    self.set_new_image(img_temp)
                except Exception:
                    tk.messagebox.showerror(title="Błąd", message="Podałeś złą wartość")
        else:
            tk.messagebox.showerror(title="Błąd", message="Wprowadz obraz")


def main():
    root = tk.Tk()  # stworzenie okienka
    root.title("Demonstrator operacji arytmetycznych")

    myFont = font.Font(size=14)

    p1 = Picture()
    p2 = Picture()
    p3 = Picture()

    frame1 = tk.Frame(master=root, width=200, height=100, bg="#ffdbcb")  # stworzenie bloku - do grupowania elementów
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)  # umieszczenie bloku w okienku
    frame2 = tk.Frame(master=root, width=200, height=100, bg="#95a0fa")
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    frame3 = tk.Frame(master=root, width=200, height=100, bg="#4f60af")
    frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    # FRAME 1
    blank_image = ImageTk.PhotoImage(
        image=Image.fromarray(np.ones((512, 512)) * 150))  # szare tło niewczytanego jeszcze obrazu

    btn_select_img_1 = tk.Button(frame1, command=p1.input_picture, text="Wybierz obraz 1", height=2,
                                 width=15)  # stworzenie przycisku
    btn_select_img_1['font'] = myFont
    btn_select_img_1.grid(row=0, column=1, padx=(10, 50))  # umieszczenie przycisku w frame1 u samej góry

    p1.set_canvas(tk.Canvas(frame1, width=450, height=450))
    p1.get_canvas().grid(row=0, column=0, pady=(20, 10), padx=(50, 10))
    p1.set_canvas_img(p1.get_canvas().create_image(0, 0, anchor=tk.NW, image=blank_image))

    btn_select_img_2 = tk.Button(frame1, command=p2.input_picture, text="Wybierz obraz 2", height=2, width=15)
    btn_select_img_2['font'] = myFont
    btn_select_img_2.grid(row=1, column=1, padx=(10, 50))

    p2.set_canvas(tk.Canvas(frame1, width=450, height=450))
    p2.get_canvas().grid(row=1, column=0, pady=(10, 20), padx=(50, 10))
    p2.set_canvas_img(p2.get_canvas().create_image(0, 0, anchor=tk.NW, image=blank_image))

    # FRAME 2
    l1 = tk.Label(frame2, text="Operacje na jednym obrazie: ", bg="#95a0fa")
    l1['font'] = myFont
    l1.grid(row=0, column=0, pady=(20, 0))

    btn_option_1 = tk.Button(frame2, command=lambda: p3.operation_add_value(p1, selected_normalization),
                             text="dodaj liczbę do obrazu", width=25, height=1)
    btn_option_1['font'] = myFont
    btn_option_1.grid(row=1, column=0, pady=(5, 5), padx=(70, 70))

    btn_option_2 = tk.Button(frame2, command=lambda: p3.operation_multiply_value(p1, selected_normalization),
                             text="pomnoż obraz przez liczbę", width=25, height=1)
    btn_option_2['font'] = myFont
    btn_option_2.grid(row=2, column=0, pady=(5, 5), padx=(70, 70))

    btn_option_3 = tk.Button(frame2, command=lambda: p3.operation_natural_logarithm(p1, selected_normalization),
                             text="logarytm naturalny obrazu", width=25, height=1)
    btn_option_3['font'] = myFont
    btn_option_3.grid(row=3, column=0, pady=(5, 5), padx=(70, 70))

    btn_option_4 = tk.Button(frame2, command=lambda: p3.operation_negation(p1, selected_normalization),
                             text="negacja obrazu obrazu", width=25, height=1)
    btn_option_4['font'] = myFont
    btn_option_4.grid(row=4, column=0, pady=(5, 5), padx=(70, 70))

    l2 = tk.Label(frame2, text="Operacje na dwóch obrazach: ", bg="#95a0fa")
    l2['font'] = myFont
    l2.grid(row=10, column=0, pady=(100, 0))

    btn_option_5 = tk.Button(frame2, command=lambda: p3.operation_linear_combination(p1, p2, selected_normalization),
                             text="kombinacja liniowa", width=25, height=1)
    btn_option_5['font'] = myFont
    btn_option_5.grid(row=11, column=0, pady=(5, 5), padx=(70, 70))

    btn_option_6 = tk.Button(frame2, command=lambda: p3.operation_add_pictures(p1, p2, selected_normalization),
                             text="dodaj dwa obrazy", width=25, height=1)
    btn_option_6['font'] = myFont
    btn_option_6.grid(row=12, column=0, pady=(5, 5), padx=(70, 70))

    btn_option_7 = tk.Button(frame2, command=lambda: p3.operation_subtract_pictures(p1, p2, selected_normalization),
                             text="odejmij dwa obrazy", width=25, height=1)
    btn_option_7['font'] = myFont
    btn_option_7.grid(row=13, column=0, pady=(5, 5), padx=(70, 70))

    btn_option_8 = tk.Button(frame2, command=lambda: p3.operation_multiply_pictures(p1, p2, selected_normalization),
                             text="pomnóż dwa obrazy", width=25, height=1)
    btn_option_8['font'] = myFont
    btn_option_8.grid(row=14, column=0, pady=(5, 5), padx=(70, 70))

    selected_normalization = tk.StringVar()
    selected_normalization.set('normalizacja A')

    l3 = tk.Label(frame2, text="Normalizacje: ", bg="#95a0fa")
    l3['font'] = myFont
    l3.grid(row=20, column=0, pady=(100, 0))
    radio_1 = tk.Radiobutton(frame2, text='obcięcie', variable=selected_normalization, value='A', cursor="hand2",
                             width=25, height=1, anchor='w')
    radio_1['font'] = myFont
    radio_1.grid(row=21, column=0, pady=(5, 5), padx=(70, 70))
    radio_2 = tk.Radiobutton(frame2, text='moduł z obcięciem', variable=selected_normalization, value='B',
                             cursor="hand2", width=25, height=1, anchor='w')
    radio_2['font'] = myFont
    radio_2.grid(row=22, column=0, pady=(5, 5), padx=(70, 70))
    radio_3 = tk.Radiobutton(frame2, text='skalowanie z dopasowaniem', variable=selected_normalization, value='C',
                             cursor="hand2", width=25, height=1, anchor='w')
    radio_3['font'] = myFont
    radio_3.grid(row=23, column=0, pady=(5, 5), padx=(70, 70))
    radio_4 = tk.Radiobutton(frame2, text='piłokształtna', variable=selected_normalization, value='D', cursor="hand2",
                             width=25, height=1, anchor='w')
    radio_4['font'] = myFont
    radio_4.grid(row=24, column=0, pady=(5, 5), padx=(70, 70))
    radio_1.invoke()

    # FRAME 3
    p3.set_canvas(tk.Canvas(frame3, width=450, height=450))
    p3.get_canvas().grid(row=0, column=0, pady=(200, 10), padx=(50, 50))
    p3.set_canvas_img(p3.get_canvas().create_image(0, 0, anchor=tk.NW, image=blank_image))

    btn_copy_to_img_1 = tk.Button(frame3, command=lambda: p1.set_new_image(p3.get_img()), text="Skopiuj do obrazu 1",
                                  width=25, height=1)
    btn_copy_to_img_1['font'] = myFont
    btn_copy_to_img_1.grid(row=1, column=0, pady=(5, 5))
    btn_copy_to_img_2 = tk.Button(frame3, command=lambda: p2.set_new_image(p3.get_img()), text="Skopiuj do obrazu 2",
                                  width=25, height=1)
    btn_copy_to_img_2['font'] = myFont
    btn_copy_to_img_2.grid(row=2, column=0, pady=(5, 5))

    root.mainloop()


if __name__ == '__main__':
    main()
