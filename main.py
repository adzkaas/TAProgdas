import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from order import Item, Order
from payment import CashPayment, NonCashPayment
import re  # Untuk memudahkan pengecekan nomor telepon

class MainApp:
    def __init__(self, apk):
        self.apk = apk
        self.apk.title("Sistem Pemesanan Toko Reptil")

        # Membuat objek
        self.order = Order()
        self.payment = CashPayment()
        # frame utama
        self.bg_color = '#F5F5DC'
        self.font_style = ("Helvetica", 14)

        self.init_welcome_screen()

    def init_welcome_screen(self):
        label_welcome = tk.Label(self.apk, text="Selamat datang di toko Reptile Tembalang!", font=("Helvetica", 25, 'bold'), bg=self.bg_color)
        label_welcome.place(relx=0.5, rely=0.4, anchor="center")

        proceed_button = tk.Button(self.apk, text="Mulai Belanja", font=self.font_style, bg='#B6A28E', fg='white', command=self.start_shopping)
        proceed_button.place(relx=0.5, rely=0.5, anchor="center")

    def start_shopping(self):
        # Menghapus pesan sambutan dan melanjutkan ke tampilan utama
        for widget in self.apk.winfo_children():
            widget.destroy()

        # Memulai UI pemilihan barang
        self.init_ui()

    def init_ui(self):
        image = Image.open("Kadal.jpg")
        image = image.resize((450, 600))
        self.photo = ImageTk.PhotoImage(image)
        label_image = tk.Label(self.apk, image=self.photo)
        label_image.place(x=580, y=0) 
        label_image.lower()  # Menurunkan layer agar gambar tidak menutupi widget lain

        label1 = tk.Label(self.apk, text="Silahkan Scroll dan Klik yang Anda Suka", font=("Helvetica", 20, 'bold'), bg=self.bg_color)
        label1.place(x=20, y=50)

        label_subtotal = tk.Label(self.apk, text="Total Belanja", font=self.font_style, bg=self.bg_color)
        label_subtotal.place(x=20, y=460)

        self.subtotal_label = tk.Label(self.apk, text="Rp 0", font=self.font_style, bg=self.bg_color)
        self.subtotal_label.place(x=150, y=460)

        # Frame utama untuk item
        frame_items = tk.Frame(self.apk, bg=self.bg_color)
        frame_items.place(x=20, y=120, width=530, height=330)

        self.canvas = tk.Canvas(frame_items)
        self.scrollbar = tk.Scrollbar(frame_items, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        item_frame = tk.Frame(self.canvas, bg=self.bg_color)
        self.canvas.create_window((0, 0), window=item_frame, anchor="nw")
        
        self.scrollbar.pack(side="right", fill="y", padx=20)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Barang pilihan
        self.items = [
            Item("sulcata 500k", 500000, "B.jpg","Nama Ilmiah: Centrochelys sulcate.\nHabitat: gurun Sahara dan Sahel.\nUkuran: 5 cm"),
            Item("python 200k", 200000, "C.jpg","Nama Ilmiah: Python regius.\nHabitat: hutan hujan tropis.\nUkuran: 61 cm"),
            Item("iguana 150k", 150000, "iguana.jpg","Nama Ilmiah: Iguana iguana.\nHabitat: Amerika Tengah dan Selatan.\nUkuran: 127 cm " ),
            Item("panana 300k", 300000, "panana.jpg","Nama Ilmiah: Tiliqua gigas.\nHabitat: papua.\nUkuran: 24 cm"),
            Item("cst 500k", 500000, "cst.jpg","Nama Ilmiah: Chelydra serpentina.\nHabitat: Amerika Utara.\nUkuran: 49,4 cm"),
            Item("cekiber 30k", 30000, "cekiber.jpg","Nama Ilmiah: Draco Volans.\nHabitat: Asia Tenggara.\nUkuran: 22 cm."),
            Item("bearded dragon 350k", 350000, "bearded dragon.jpg","Nama Ilmiah: Pogona vitticeps.\nHabitat: Australia.\nUkuran: 40 cm"),
            Item("soa layar 150k", 150000, "A.jpg","Nama Ilmiah: Hydrosaurus amboinensis.\nHabitat: Maluku, Sulawesi.\nUkuran: 120 cm"),
            Item("aligator 200k", 200000, "aligator.jpg","Nama Ilmiah: Caiman crocodilus.\nHabitat: Amerika Selatan.\nUkuran: 40 cm " ),
        ]

        self.item_buttons = []
        self.create_item_buttons(item_frame)

        # Tombol Submit
        submit_button = tk.Button(self.apk, text="Submit", font=self.font_style, bg='#B6A28E', fg='white', command=self.submit_order)
        submit_button.place(x=300, y=510)

        # Tombol Cancel
        cancel_button = tk.Button(self.apk, text="Cancel", font=self.font_style, bg='#B6A28E', fg='white', command=self.cancel_order)
        cancel_button.place(x=400, y=510)

    def create_item_buttons(self, frame):
        # Membuat tombol untuk memilih barang
        row_limit = 3  # Maksimum 3 barang per baris
        for i, item in enumerate(self.items):  # Perulangan untuk membuat tombol
            img = Image.open(item.get_image())
            img = img.resize((130, 150))
            photo = ImageTk.PhotoImage(img)
        
            # Membuat tombol untuk memilih item
            button = tk.Button(frame, text=item.get_name(), image=photo, compound="top", bg='#DCE4C9', command=lambda i=i: self.add_item_to_order(i))
            button.photo = photo  # Menjaga referensi gambar
            button.grid(row=i // row_limit * 2, column=i % row_limit, padx=10, pady=5)

            # Deskripsi di bawah tombol, rata kiri
            desc_label = tk.Label(frame, text=item.get_description(), font=("Helvetica", 9), bg=self.bg_color, wraplength=130, anchor="w", justify="left")
            desc_label.grid(row=(i // row_limit * 2) + 1, column=i % row_limit, padx=10, pady=10, sticky="w")  # Menyusun deskripsi tepat di bawah tombol dan rata kiri

            self.item_buttons.append(button)

        # Update area canvas agar scrollable
        frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def add_item_to_order(self, index):
        # Menambah item yang dipilih ke keranjang
        item = self.items[index]
        self.order.add_item(item)  # Menggunakan stack untuk menambah item
        self.update_subtotal()

    def update_subtotal(self):
        # Mengupdate subtotal belanjaan
        subtotal = self.order.get_total()  # Menggunakan getter untuk mendapatkan total
        self.subtotal_label.config(text=f"Rp {subtotal:,.0f}")

    def submit_order(self):
        # Menyelesaikan pemesanan
        if not self.order.get_items():  # Pengkondisian untuk memeriksa keranjang kosong
            messagebox.showerror("Error", "Keranjang Belanja Kosong")
            return

        # Menampilkan jendela pembayaran setelah submit
        self.show_payment_window()

    def show_payment_window(self):
        # Jendela pembayaran
        payment_window = tk.Toplevel(self.apk)
        payment_window.title("Konfirmasi Pembayaran")
        payment_window.geometry("400x500")
        payment_window.configure(bg=self.bg_color)

        label = tk.Label(payment_window, text="Konfirmasi Pembayaran", font=("Helvetica", 16, 'bold'), bg=self.bg_color)
        label.pack(pady=10)

        # Input Nama Pembeli
        label_name = tk.Label(payment_window, text="Nama Pembeli:", font=self.font_style, bg=self.bg_color)
        label_name.pack(pady=5)
        self.entry_name = tk.Entry(payment_window, font=self.font_style, bg='#DCE4C9', fg='black')
        self.entry_name.pack(pady=5)

        # Input Nomor Telepon Pembeli
        label_phone = tk.Label(payment_window, text="Nomor Telepon:", font=self.font_style, bg=self.bg_color)
        label_phone.pack(pady=5)
        self.entry_phone = tk.Entry(payment_window, font=self.font_style, bg='#DCE4C9', fg='black')
        self.entry_phone.pack(pady=5)

        # Opsi Pembayaran
        label_payment = tk.Label(payment_window, text="Pilih Opsi Pembayaran", font=self.font_style, bg=self.bg_color)
        label_payment.pack(pady=10)

        payment_method_var = tk.StringVar(value="Cash")
        payment_cash_rb = tk.Radiobutton(payment_window, text="Tunai", variable=payment_method_var, value="Cash", font=self.font_style, bg=self.bg_color, command=lambda: self.toggle_bank_selection(payment_window, False))
        payment_cash_rb.pack(pady=10)

        payment_non_cash_rb = tk.Radiobutton(payment_window, text="Non Tunai", variable=payment_method_var, value="Non-Cash", font=self.font_style, bg=self.bg_color, command=lambda: self.toggle_bank_selection(payment_window, True))
        payment_non_cash_rb.pack(pady=10)

        # Dropdown Bank (hidden initially)
        self.bank_var = tk.StringVar(value="Bank BCA")
        self.bank_dropdown = tk.OptionMenu(payment_window, self.bank_var, "Bank BCA", "Bank Mandiri", "Bank BRI", "Bank BNI")
        self.bank_dropdown.pack(pady=10)
        self.bank_dropdown.pack_forget()

        # Tombol konfirmasi pembayaran (pindah ke bawah setelah dropdown bank)
        self.submit_payment_button = tk.Button(payment_window, text="Konfirmasi Pembayaran", font=self.font_style, bg='#B6A28E', fg='white', command=lambda: self.confirm_payment(payment_window, payment_method_var.get()))
        self.submit_payment_button.pack(pady=20, side="bottom")

    def toggle_bank_selection(self, window, show):
        # Menampilkan atau menyembunyikan dropdown bank
        if show:
            self.bank_dropdown.pack(pady=10)
            self.submit_payment_button.pack_forget()
            self.submit_payment_button.pack(pady=20, side="bottom")
        else:
            self.bank_dropdown.pack_forget()
            self.submit_payment_button.pack_forget()
            self.submit_payment_button.pack(pady=20, side="bottom")

    def confirm_payment(self, payment_window, payment_type):
        # Mengkonfirmasi pembayaran
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        bank = self.bank_var.get() if payment_type == "Non-Cash" else None

        # Validasi nama dan telepon
        if not name or not phone:  # Pengkondisian jika nama atau telepon kosong
            messagebox.showerror("Error", "Nama dan Nomor Telepon harus diisi!")
            return

        # Validasi nomor telepon (hanya angka dan 12 digit)
        if not phone.isdigit() or len(phone) != 12:
            messagebox.showerror("Error", "Nomor Telepon harus terdiri dari 12 digit angka!")
            return

        if payment_type == "Non-Cash" and not bank:
            messagebox.showerror("Error", "Pilih bank untuk pembayaran non tunai!")
            return

        payment_message = self.payment.choose_payment_method(payment_type)

        items_str = "\n".join([item.get_name() for item in self.order.get_items()])
        subtotal = self.order.get_total()

        order_message = f"Nama: {name}\nNomor Telepon: {phone}\n\nItems:\n{items_str}\n\nSubtotal: Rp {subtotal:,.0f}\n\n{payment_message}"

        if bank:
            order_message += f"\n\nBank: {bank}"

        messagebox.showinfo("Pesanan Diterima", order_message)

        # Menutup jendela pembayaran dan reset keranjang belanja
        payment_window.destroy()
        self.order.clear_cart()
        self.update_subtotal()

    def cancel_order(self):
        # Membatalkan pesanan
        self.order.clear_cart()
        self.update_subtotal()
        messagebox.showinfo("Pesanan Dibatalkan", "Pesanan Anda telah dibatalkan.")

if __name__ == "__main__":
    apk = tk.Tk()
    app = MainApp(apk)
    apk.geometry("900x600")
    apk.configure(bg='#F5F5DC')
    apk.resizable(False, False)
    apk.mainloop()
