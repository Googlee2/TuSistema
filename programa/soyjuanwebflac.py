import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, os
from datetime import date

# =============================
# CONFIG / COLORES CELESTE
# =============================
APP = "SoyJuanWebFlac"

BG     = "#eaf4f8"
PANEL  = "#cfe9f3"
BTN    = "#4aa3df"
BTN_TX = "#ffffff"
TXT    = "#1f2d3d"
ENTRY  = "#ffffff"

# =============================
# DB
# =============================
BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "datos.db")

con = sqlite3.connect(DB)
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS usuarios(
id INTEGER PRIMARY KEY,
user TEXT,
pass TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS clientes(
id INTEGER PRIMARY KEY,
empresa TEXT,
nombre TEXT,
celular TEXT,
fecha TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS pagos(
id INTEGER PRIMARY KEY,
cliente_id INTEGER,
concepto TEXT,
importe REAL,
vence TEXT)""")

con.commit()

cur.execute("SELECT COUNT(*) FROM usuarios")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO usuarios VALUES(NULL,'admin','1234')")
    con.commit()

# =============================
# LOGIN
# =============================
root = tk.Tk()
root.title(APP)
root.geometry("400x260")
root.configure(bg=BG)
root.resizable(False, False)

tk.Label(root, text="LOGIN", bg=BG, fg=TXT,
         font=("Segoe UI", 16, "bold")).pack(pady=20)

f = tk.Frame(root, bg=BG)
f.pack()

tk.Label(f, text="Usuario", bg=BG, fg=TXT).grid(row=0, column=0, pady=5)
tk.Label(f, text="Clave", bg=BG, fg=TXT).grid(row=1, column=0, pady=5)

e_user = tk.Entry(f, bg=ENTRY, fg=TXT)
e_pass = tk.Entry(f, bg=ENTRY, fg=TXT, show="*")

e_user.grid(row=0, column=1)
e_pass.grid(row=1, column=1)

def login():
    cur.execute("SELECT * FROM usuarios WHERE user=? AND pass=?",
                (e_user.get(), e_pass.get()))
    if cur.fetchone():
        root.destroy()
        app()
    else:
        messagebox.showerror("Error", "Login incorrecto")

tk.Button(root, text="ENTRAR", bg=BTN, fg=BTN_TX,
          font=("Segoe UI", 10, "bold"),
          command=login).pack(pady=15)

# =============================
# APP PRINCIPAL
# =============================
def app():
    win = tk.Tk()
    win.title(APP)
    win.geometry("1150x720")
    win.configure(bg=BG)

    # -------- CLIENTES --------
    fc = tk.LabelFrame(win, text="Clientes", bg=PANEL, fg=TXT,
                       font=("Segoe UI", 10, "bold"))
    fc.pack(fill="x", padx=15, pady=10)

    tk.Label(fc, text="Empresa", bg=PANEL, fg=TXT).grid(row=0, column=0)
    tk.Label(fc, text="Nombre", bg=PANEL, fg=TXT).grid(row=0, column=1)
    tk.Label(fc, text="Celular", bg=PANEL, fg=TXT).grid(row=0, column=2)

    e_emp = tk.Entry(fc, bg=ENTRY, fg=TXT, width=25)
    e_nom = tk.Entry(fc, bg=ENTRY, fg=TXT, width=25)
    e_cel = tk.Entry(fc, bg=ENTRY, fg=TXT, width=15)

    e_emp.grid(row=1, column=0, padx=5, pady=5)
    e_nom.grid(row=1, column=1, padx=5, pady=5)
    e_cel.grid(row=1, column=2, padx=5, pady=5)

    tabla_clientes = ttk.Treeview(
        fc,
        columns=("id","empresa","nombre","celular","fecha"),
        show="headings",
        height=6
    )
    for c in tabla_clientes["columns"]:
        tabla_clientes.heading(c, text=c.upper())
        tabla_clientes.column(c, anchor="center")

    tabla_clientes.grid(row=2, column=0, columnspan=6, pady=10, sticky="ew")

    def cargar_clientes():
        tabla_clientes.delete(*tabla_clientes.get_children())
        for r in cur.execute("SELECT * FROM clientes"):
            tabla_clientes.insert("", "end", values=r)

    def cliente_seleccionado():
        sel = tabla_clientes.selection()
        if not sel:
            return None
        return tabla_clientes.item(sel[0])["values"]

    def limpiar():
        e_emp.delete(0,"end")
        e_nom.delete(0,"end")
        e_cel.delete(0,"end")

    def agregar_cliente():
        if e_emp.get().strip() == "":
            return
        cur.execute("INSERT INTO clientes VALUES(NULL,?,?,?,?)",
                    (e_emp.get(), e_nom.get(), e_cel.get(),
                     date.today().isoformat()))
        con.commit()
        limpiar()
        cargar_clientes()

    def editar_cliente():
        datos = cliente_seleccionado()
        if not datos:
            messagebox.showwarning("Atención", "Seleccioná un cliente")
            return
        cur.execute("""UPDATE clientes
                       SET empresa=?, nombre=?, celular=?
                       WHERE id=?""",
                    (e_emp.get(), e_nom.get(), e_cel.get(), datos[0]))
        con.commit()
        limpiar()
        cargar_clientes()

    def borrar_cliente():
        datos = cliente_seleccionado()
        if not datos:
            messagebox.showwarning("Atención", "Seleccioná un cliente")
            return
        if not messagebox.askyesno(
            "Confirmar",
            "Se borrará el cliente y TODOS sus pagos.\n¿Continuar?"
        ):
            return
        cur.execute("DELETE FROM pagos WHERE cliente_id=?", (datos[0],))
        cur.execute("DELETE FROM clientes WHERE id=?", (datos[0],))
        con.commit()
        limpiar()
        cargar_clientes()
        tabla_pagos.delete(*tabla_pagos.get_children())

    def cargar_a_form(event=None):
        datos = cliente_seleccionado()
        if not datos:
            return
        limpiar()
        e_emp.insert(0, datos[1])
        e_nom.insert(0, datos[2])
        e_cel.insert(0, datos[3])

    tk.Button(fc, text="AGREGAR", bg=BTN, fg=BTN_TX,
              command=agregar_cliente).grid(row=1, column=3, padx=5)
    tk.Button(fc, text="EDITAR", bg="#f0ad4e", fg="white",
              command=editar_cliente).grid(row=1, column=4, padx=5)
    tk.Button(fc, text="BORRAR", bg="#d9534f", fg="white",
              command=borrar_cliente).grid(row=1, column=5, padx=5)

    tabla_clientes.bind("<<TreeviewSelect>>", cargar_a_form)

    # -------- PAGOS --------
    fp = tk.LabelFrame(win, text="Pagos", bg=PANEL, fg=TXT,
                       font=("Segoe UI", 10, "bold"))
    fp.pack(fill="both", expand=True, padx=15, pady=10)

    tk.Label(fp, text="Concepto", bg=PANEL, fg=TXT).grid(row=0, column=0)
    tk.Label(fp, text="Importe", bg=PANEL, fg=TXT).grid(row=0, column=1)
    tk.Label(fp, text="Vence", bg=PANEL, fg=TXT).grid(row=0, column=2)

    e_con = tk.Entry(fp, bg=ENTRY, fg=TXT, width=30)
    e_imp = tk.Entry(fp, bg=ENTRY, fg=TXT, width=10)
    e_ven = tk.Entry(fp, bg=ENTRY, fg=TXT, width=12)
    e_ven.insert(0, date.today().isoformat())

    e_con.grid(row=1, column=0, padx=5, pady=5)
    e_imp.grid(row=1, column=1, padx=5, pady=5)
    e_ven.grid(row=1, column=2, padx=5, pady=5)

    tabla_pagos = ttk.Treeview(
        fp,
        columns=("concepto","importe","vence"),
        show="headings",
        height=8
    )
    for c in tabla_pagos["columns"]:
        tabla_pagos.heading(c, text=c.upper())
        tabla_pagos.column(c, anchor="center")

    tabla_pagos.grid(row=2, column=0, columnspan=4, pady=10)

    def cliente_id():
        sel = tabla_clientes.selection()
        if not sel:
            return None
        return tabla_clientes.item(sel[0])["values"][0]

    def cargar_pagos(event=None):
        tabla_pagos.delete(*tabla_pagos.get_children())
        cid = cliente_id()
        if not cid:
            return
        for r in cur.execute(
            "SELECT concepto,importe,vence FROM pagos WHERE cliente_id=?",
            (cid,)
        ):
            tabla_pagos.insert("", "end", values=r)

    def agregar_pago():
        cid = cliente_id()
        if not cid:
            messagebox.showwarning("Atención", "Seleccioná un cliente")
            return
        try:
            importe = float(e_imp.get())
        except:
            messagebox.showerror("Error", "Importe inválido")
            return
        cur.execute("INSERT INTO pagos VALUES(NULL,?,?,?,?)",
                    (cid, e_con.get(), importe, e_ven.get()))
        con.commit()
        cargar_pagos()

    tk.Button(fp, text="AGREGAR PAGO",
              bg=BTN, fg=BTN_TX,
              command=agregar_pago).grid(row=1, column=3, padx=10)

    tabla_clientes.bind("<<TreeviewSelect>>", cargar_pagos)

    cargar_clientes()
    win.mainloop()

root.mainloop()
