from optparse import Values
import requests,tkinter as tk ,sqlite3
from tkinter import ttk


def agregar_producto():
    #if precio_producto.isdecimal()==True:
    
    producto=caja1.get()
    precio_producto=caja2.get()
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO articulos Values (?,?)",(producto,precio_producto))
    conn.commit()
    #print("llego aca")

def consultar_dolar():
    r = requests.get("https://api.recursospython.com/dollar")
    if r.status_code ==200:
        cotizacion=r.json()
        dollar= cotizacion["buy_price"]
    return dollar         

def precio_en_pesos(preciodol):
        precio_producto=int(preciodol)
        precio_en_peso=precio_producto*dolar()
        return precio_en_peso

def mostrar_info():
    cursor.execute("SELECT * FROM articulos")
    listas=cursor.fetchall()
    for product,preciodol in listas:
        a=[product,preciodol,precio_en_pesos(preciodol)]
        tabla.insert("",tk.END,values=(a))
        
    
    
dolar=consultar_dolar    
conn = sqlite3.connect("productos.db")
cursor = conn.cursor()

try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS articulos(
        producto TEXT,
        precio_dolar INT
        )""")
    conn.commit()
except sqlite3.OperationalError:
    print("la consulta no se ejecuto correctamente.")
else:print("consulta ejecutada correctamente")   

 


    
root=tk.Tk()
root.title("Gestor de productos")
root.geometry("800x600")

#ETIQUETAS

etiqueta1=tk.Label(text="Producto",bg="skyblue")
etiqueta1.place(x=30,y=30)

etiqueta2=tk.Label(text="Precio(UDS)",bg="skyblue")
etiqueta2.place(x=300,y=30)

#-------------CAJAS----------------
caja1=tk.Entry()
caja1.place(x=120,y=30,width=100)

caja2=tk.Entry()
caja2.place(x=420,y=30,width=100)


#--------------TABLA--------------
tabla=ttk.Treeview(columns=("producto","precio_usd","precio_peso"),show="headings")
tabla.heading("producto",text="Producto")
tabla.heading("precio_usd",text="Precio(USD)")
tabla.heading("precio_peso",text="Precio(Pesos)")
tabla.place(x=30,y=80,width=700,height=500)

#-------------BOTON----------------------
boton=ttk.Button(text="Agregar",command=agregar_producto)
boton.place(x=600,y=30)

#-----------
mostrar_info()
conn.commit()
conn.close()

root.mainloop()
