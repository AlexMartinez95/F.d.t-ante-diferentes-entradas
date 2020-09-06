import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import control
import numpy as np

naranja_fuerte_codigo_de_colores='#EEA006'
naranja_claro_codigo_de_colores='#FCEAC7'
s=control.tf('s')

def ajusta_el_retardo_segun_el_input_de_la_ventana(t_orig,y_orig,retardo):
   
    m=np.array([0])
    t=np.concatenate([m,t_orig+retardo])
    y=np.concatenate([m,y_orig])
    return t,y

def ecuacion_mal_definida(tipo_de_error):
    
    if tipo_de_error==0:
        tk.messagebox.showinfo(message="Verifique la ecuación.", title="Error")

    t_error=np.array([0,1,2,3,4,5,6,7])
    y_error=np.zeros(8,)
    fig.add_subplot(111).plot(t_error, y_error)
    
    canvas.draw()  
    
def graficado(valor_ajustado_de_la_deslizadera_del_tiempo,tamaño_impulso,tamaño_escalon,tamaño_rampa,boton_pulsado,G0):
    
    fig.clf()

    retardo=eval(input_del_retardo_en_la_ventana.get())   

    if boton_pulsado=='Impulso': 
        t,y=control.impulse_response(G0*tamaño_impulso,T=(valor_ajustado_de_la_deslizadera_del_tiempo))
    if boton_pulsado=='Escalon':      
        t,y=control.step_response(G0*tamaño_escalon,T=(valor_ajustado_de_la_deslizadera_del_tiempo))
    if boton_pulsado=='Rampa':    
        t,y=control.step_response(G0*tamaño_rampa/s,T=(valor_ajustado_de_la_deslizadera_del_tiempo))
    if boton_pulsado=='Arbitraria':
        t,y,xout=control.forced_response(G0,T=(t_experimental),U=(u_experimental))
        
    t_a_dibujar,y_a_dibujar=ajusta_el_retardo_segun_el_input_de_la_ventana(t,y,retardo)
    
    fig.add_subplot(111).plot(t_a_dibujar, y_a_dibujar)
    canvas.draw()  

def recibir_datos_fichero():
    
    global t_experimental,u_experimental
    
    t_junto_con_u_misma_matriz=np.loadtxt('datos.txt')
    t_experimental=t_junto_con_u_misma_matriz[:,0]
    u_experimental=t_junto_con_u_misma_matriz[:,1]
    leer_datos_de_la_ventana()
   
def recibir_ut_escrita_manualmente():
 
    global t_experimental,u_experimental
    
    u_experimental=eval(input_del_usuario_Ut.get())
    t_experimental=eval(input_del_usuario_tiempo.get())
    t_experimental=np.array(t_experimental)
    u_experimental=np.array(u_experimental)
    tfin=t_experimental[-1]
    vector_tiempos=np.linspace(0,tfin,num=1000)
    u_experimental=np.interp(vector_tiempos,t_experimental,u_experimental)
    t_experimental=vector_tiempos.copy()
    
    leer_datos_de_la_ventana()

   
def leer_datos_de_la_ventana():
        
    boton_pulsado=variable_de_los_radio_button.get() 
    try:
        G0=eval(input_del_fdt_en_la_ventana.get())
    except SyntaxError:
        ecuacion_mal_definida(0)
    tamaño_impulso=eval(input_impulso_en_la_ventana.get())
    tamaño_rampa=eval(input_rampa_en_la_ventana.get())
    tamaño_escalon=eval(input_escalon_en_la_ventana.get())
    valor_ajustado_de_la_deslizadera_del_tiempo=np.linspace(0.0,deslizadera_tiempo_objeto.variable.get(), num=1000)

    graficado(valor_ajustado_de_la_deslizadera_del_tiempo,tamaño_impulso,tamaño_escalon,tamaño_rampa,boton_pulsado,G0)
    

class Deslizadera:

    def __init__(self,master,texto,valor_inicial,valor_maximo,valor_minimo):
        
        self.dini=valor_inicial
        self.dmin=valor_minimo
        self.dmax=valor_maximo
        self.master=master
        self.variable=tk.DoubleVar()
        self.variable.set(valor_inicial)
        self.deslizadera=tk.Scale(master,variable=self.variable,
                                  from_=self.dmin,to=self.dmax,orient=tk.HORIZONTAL,label=texto,resolution=0.001,
                                  length=400,bg=naranja_fuerte_codigo_de_colores,troughcolor='black')
        self.deslizadera.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        self.deslizadera.bind("<ButtonRelease-1>",self.update)
        
    def update(self,event):
        
       if self.dmax==self.dini: 
            leer_datos_de_la_ventana()
       else:     
            if self.variable.get()==0:
                
                self.dmax=self.dmax/2
                self.deslizadera.configure(to=self.dmax)
                
            if self.variable.get() >= (self.dmax-self.dmax/1000):
                
                self.dmax=self.dmax*2
                self.deslizadera.configure(to=self.dmax)
            
            if self.dmax < 10:
                
                self.deslizadera.configure(resolution=(self.dmax/1000))
            
            leer_datos_de_la_ventana()
         
ventana = tk.Tk()
ventana.wm_title("Comportamiento de una f.d.t ante diferentes entradas")
ventana.config(width=500, height=200,bg=naranja_claro_codigo_de_colores)     
frame_canvas=tk.Frame(ventana,bg=naranja_claro_codigo_de_colores)
frame_canvas.grid(row=3, column=0)
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_canvas)   
toolbar = NavigationToolbar2Tk(canvas,frame_canvas)
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
toolbar.update()
deslizadera_tiempo_objeto=Deslizadera(frame_canvas,"Tiempo de visualizacion",20,100,0.05)
frame_fdt_y_retardo=tk.Frame(ventana,bg=naranja_claro_codigo_de_colores)
frame_fdt_y_retardo.grid(row=0,column=0)
input_del_fdt_en_la_ventana = ttk.Entry(frame_fdt_y_retardo, width=30)
input_del_fdt_en_la_ventana.insert(0,"(1)/(1+2*s+3*s**2)")
input_del_fdt_en_la_ventana.grid(row=1,column=0)
label_fdt=tk.Label(frame_fdt_y_retardo,text="F.d.t",bg=naranja_claro_codigo_de_colores)
label_fdt.grid(row = 0, column =0)
input_del_retardo_en_la_ventana=ttk.Entry(frame_fdt_y_retardo,width=10)
input_del_retardo_en_la_ventana.grid(row=1,column=1)
input_del_retardo_en_la_ventana.insert(0,"0")
label_retardo=tk.Label(frame_fdt_y_retardo,text="Retardo",bg=naranja_claro_codigo_de_colores)
label_retardo.grid(row = 0, column =1)
boton_de_ok = tk.Button(frame_fdt_y_retardo, text="Ok",command=leer_datos_de_la_ventana,bg=naranja_fuerte_codigo_de_colores)
boton_de_ok.grid(row =1, column = 2, sticky=tk.E)
frame_de_Ut=tk.Frame(ventana,bg=naranja_claro_codigo_de_colores)
frame_de_Ut.grid(row=1,column=0)
boton_datos_fichero = tk.Button(frame_de_Ut, text="Cargar datos u(t) y t de un fichero",command=recibir_datos_fichero
                                ,bg=naranja_fuerte_codigo_de_colores)
boton_datos_fichero.grid(row=6, column=0)   
input_impulso_en_la_ventana = ttk.Entry(frame_de_Ut,width=10)
input_rampa_en_la_ventana= ttk.Entry(frame_de_Ut,width=10)
input_escalon_en_la_ventana = ttk.Entry(frame_de_Ut,width=10)   
input_impulso_en_la_ventana.insert(0,"1")
input_rampa_en_la_ventana.insert(0,"1")
input_escalon_en_la_ventana.insert(0,"1")
variable_de_los_radio_button = tk.StringVar()
variable_de_los_radio_button.set(0)      
radio_button_impulso= tk.Radiobutton(frame_de_Ut, text="Impulso", variable=variable_de_los_radio_button,value='Impulso'
                                     ,command=leer_datos_de_la_ventana,bg=naranja_claro_codigo_de_colores)
radio_button_escalon= tk.Radiobutton(frame_de_Ut, text="Escalon", variable=variable_de_los_radio_button,value='Escalon'
                                     ,command=leer_datos_de_la_ventana,bg=naranja_claro_codigo_de_colores)
radio_button_rampa=  tk.Radiobutton(frame_de_Ut, text="Rampa", variable=variable_de_los_radio_button,value='Rampa'
                                    ,command=leer_datos_de_la_ventana,bg=naranja_claro_codigo_de_colores)
radio_button_arbitraria=  tk.Radiobutton(frame_de_Ut, text="Arbitraria", variable=variable_de_los_radio_button,value='Arbitraria'
                                         ,command=leer_datos_de_la_ventana,bg=naranja_claro_codigo_de_colores)        
radio_button_arbitraria.grid(row = 0, column =0)        
radio_button_impulso.grid(row = 0, column =1)
input_impulso_en_la_ventana.grid(row = 1, column=1)      
radio_button_escalon.grid(row = 0, column =2)
input_escalon_en_la_ventana.grid(row = 1, column =2)
radio_button_rampa.grid(row = 0, column = 3)
input_rampa_en_la_ventana.grid(row = 1, column = 3)
input_del_usuario_tiempo = ttk.Entry(frame_de_Ut,width=10)
input_del_usuario_tiempo.grid(row=2,column=0)
input_del_usuario_tiempo_label=tk.Label(frame_de_Ut,text="t",bg=naranja_claro_codigo_de_colores)
input_del_usuario_tiempo_label.grid(row=1,column=0)  
input_del_usuario_Ut = ttk.Entry(frame_de_Ut,width=10)
input_del_usuario_Ut_label=tk.Label(frame_de_Ut,text="U(t)",bg=naranja_claro_codigo_de_colores)     
input_del_usuario_Ut.grid(row=4,column=0)
input_del_usuario_Ut_label.grid(row=3,column=0)
boton_datos_Ut_t_input_usuario = tk.Button(frame_de_Ut, text="Cargar datos u(t),t escritos",command=recibir_ut_escrita_manualmente
                                           ,bg=naranja_fuerte_codigo_de_colores)
boton_datos_Ut_t_input_usuario.grid(row=5, column=0)
ventana.mainloop()