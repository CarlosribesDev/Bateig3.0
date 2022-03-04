import time
from tkinter import END, Tk,Label,LabelFrame,Button,ttk,filedialog,Entry,StringVar
from Report import Report
from Excel import export_to_excel
from Db import get_operators,set_directory,get_directory

#region Utilidades
###################################################################################

#    UTILIDADES

###################################################################################
#Crea una nueva ventana
def open_window(root,w,h,title):
 
    root.title(title)
    try:
        root.iconbitmap("LogoBateig.ico")
    except:
        print('no encuentra icono')
    
    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

#Ventana con mensaje de error
def error(message):
    root3 = Tk()
    open_window(root3,600,200,"Error")
    Label(root3,text=message).place(x=300,y=100,anchor="center")
#Ventana con mesaje informativo
def message(message):
    root3 = Tk()
    open_window(root3,200,100,"Aviso")
    Label(root3,text=message).place(x=100,y=50,anchor="center")
#entrada con su etiqueta y su tipo de dato
def app_entry(label,entryType,frame,row,column,values):
    Label(frame,text=label).grid(row=row,column=column)
    entry = entryType
    if(type(entry) == ttk.Combobox):
        entry["values"] = values    
    entry.grid(row=row,column=column+1)

    return entry 


#elige el directorio seleccionado
def select_folder(path,name):
    #busca directorio
    folder_directory = filedialog.askdirectory()
    #si se ha escogido un directorio,se asigna y se actualiza la base de datos
    if(folder_directory != ""):
       
        path.set(folder_directory)     
        set_directory(folder_directory,name)
       

#endregion

#region APP Escritrio  
# ############################################################################################

# #       APLICACION ESCRITORIO

# ########################################################################################## 
#VENTANA PRINCIPAL
class App(ttk.Frame):

    #inicializa
    def __init__(self,main_window):
        super().__init__(main_window)
        open_window(main_window,700,250," ")

       
        ###CUADRO PRINCIPAL####

        #Crea panel de pestañas
        self.notebook = ttk.Notebook(self)

        ###PESTAÑAS###
        self.data = LabelFrame(self.notebook)
        self.directories = LabelFrame(self.notebook)

        self.notebook.add(self.data, text='Datos',padding = 20)
        self.notebook.add(self.directories, text="Directorios",padding = 20)
        self.notebook.pack(padx = 10,pady = 10)

        ###DATOS###
        
        for x in range(3):
            self.data.rowconfigure(x,pad=10)
            self.data.columnconfigure(x,pad=10)
            self.directories.rowconfigure(x,pad=10)
            self.directories.columnconfigure(x,pad=20)

        self.data.columnconfigure(1,pad=10)
        #nombre
        self.name = app_entry("Operario",ttk.Combobox(self.data,state = "normal"),self.data,0,0,get_operators())

        #archivos de texto con el corte diario    

        self.week_day = app_entry("Dia de la semana",ttk.Combobox(self.data,state = "readonly"),self.data,1,0,("Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"))
        width_1 = 3
        
        hours = ("6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23")
        min = ("00","10","20","30","40","50","60")

        #hora entrada
        self.start_hour = app_entry("Hora inicio turno",ttk.Combobox(self.data,state = "readonly",width = width_1 ),self.data,0,3,hours)
        #min entrada
        self.start_min = app_entry(":",ttk.Combobox(self.data,state = "readonly",width = width_1),self.data,0,5,min)
        #hora salida
        self.end_hour = app_entry("Hora fin turno",ttk.Combobox(self.data,state = "readonly",width = width_1),self.data,1,3,hours)
        #min salida
        self.end_min = app_entry(":",ttk.Combobox(self.data,state = "readonly",width = width_1),self.data,1,5,min)

        width_2 = 5
        #slab inicio
        self.first_slab = app_entry("Primera tabla",Entry(self.data,width = width_2),self.data,2,3,())
        #slab inicio
        self.last_slab = app_entry("Última tabla",Entry(self.data,width = width_2),self.data,2,5,())
        ###DIRECTORIOS###
 
        #archivos de texto
    
        self.folder_path_1 = StringVar()

        app_entry('Carpeta Unloading Robot',Entry(self.directories,textvariable = self.folder_path_1,state='readonly' ,width = 50),self.directories,0,0,(" "))

        #boton navagacion
        self.browse_button_1 = ttk.Button(self.directories, 
        text="buscar",command=lambda:select_folder(self.folder_path_1,'Unloading_txt'),width=8).grid(row=0,column=2,padx=(0,20))

        #archivos de corte
        
        self.folder_path_2 = StringVar()
        app_entry('Carpeta LogCutMoveEditor',Entry(self.directories,textvariable = self.folder_path_2,state="readonly" ,width = 50),self.directories,1,0,(" "))

        #boton navegacion
        self.browse_button_2 = ttk.Button(self.directories, text="buscar",command=lambda:select_folder(self.folder_path_2,'LogCutMove_xml'),width=8).grid(row=1,column=2,padx=(0,20))
       
        ####BOTONES#####

        # #Cuadro Botones
        frame3 = LabelFrame(self)
        frame3.pack(fill="both",expand="yes",padx=20,pady=5)

        frame3.columnconfigure(0, weight=20)
        frame3.columnconfigure(1, weight=20)
        frame3.columnconfigure(2, weight=20)
        frame3.rowconfigure(0, pad=20)

        #mostrar todo
        Button(frame3, text="Mostrar Cortes",command=lambda:self.show()).grid(row=0,column=0)
        
        #exportar a excel
        Button(frame3, text="Exportar Excel",command=lambda:self.export()).grid(row=0,column=1)
        self.pack()
        self.load_data()
            
       

    def new_report(self):

        if(self.last_slab.get() < self.first_slab.get()):
            error('El codigo de la primera tabla \n no puede ser mayor que el de la última')
            return False

        first_slab = f'SLAB{self.first_slab.get().zfill(14)}'
        last_slab = f'SLAB{self.last_slab.get().zfill(14)}'
        
        try:
            report = Report(self.name.get(),self.start_hour.get(),self.start_min.get(),self.end_hour.get(),self.end_min.get(),first_slab,last_slab)
            report.get_data(self.folder_path_1.get(),self.folder_path_2.get(),self.week_day.get())
            return report
        except Exception as e:
            error(e)
            return False
        except:
            error('error inesperado')
            return False

    def show(self):

        
        report = self.new_report()

        if(report != False):
        
            root2 = Tk()
            open_window(root2,700,450,"Cortes")
            
            row_num = 0
            column_num = 0
            #salto de linea 
            def line_break():

                nonlocal row_num
                nonlocal column_num

                row_num +=1
                if row_num % 20 == 0:
                    column_num +=1
                    row_num = 0
    
            #mostrar losas
            for measure in report.measures_list:
                            
                next_piece = '{} x {} x {} | piezas = {} | material = {} | m2 = {}'.format(measure.length,measure.width,measure.thick,measure.amount,measure.material,round(measure.m2,2))
                
                Label(root2,text=next_piece).grid(row=row_num,column=column_num)
                
                line_break()
   
            #mostrar datos
            Label(root2,text=str(report.total_pieces) + " Losas " + str(report.total_slabs) + " Tablas") .grid(row=row_num,column= column_num)
            line_break()

            Label(root2,text=str(report.total_m2) + " M2") .grid(row=row_num,column = column_num)    
            line_break()

            Label(root2,text="Tiempo medio por tabla " + str(report.avegare_minutes) + ":" + str(report.average_seconds)) .grid(row=row_num,column= column_num)
            line_break()

            Label(root2,text="Slab Inicio " + report.first_slab) .grid(row=row_num,column= column_num)
            line_break()

            Label(root2,text="Slab Fin " + report.last_slab) .grid(row=row_num,column= column_num)
            line_break()

            Label(root2,text="Fecha : " + report.date).grid(row=row_num,column= column_num)
 
    def export(self):
        report = self.new_report()

        if(report != False):

            try:
                export_to_excel(report)  
            except:
                error('El documento esta siendo usado')
            
    def load_data(self):
       
        try:
            self.folder_path_1.set(get_directory('Unloading_txt'))
            self.folder_path_2.set(get_directory('LogCutMove_xml'))
        except:
            error('data.json modificado')
           
        self.name.set("Carlos")
        self.week_day.set("Lunes")
        self.start_hour.set("6")
        self.end_hour.set("14")
        self.start_min.set("00")
        self.end_min.set("00")
        self.first_slab.insert(0,0)

        self.last_slab.insert(0,0)
        ######TEST#########
        #self.week_day.set("Martes")
        #self.first_slab.insert(0,47639)

        #self.last_slab.insert(0,47669)


#endregion
