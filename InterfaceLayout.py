# -----------------------------------------------------------------------------
# ---------------- GRAPHICAL INTERFACE TO PROCESS RISK RESULTS ----------------
# -----------------------------------------------------------------------------
"""
-------------------------------------------------------------------------------
---------------------------- Author: Daniela Novoa ----------------------------
-------------------------------------------------------------------------------
"""
#%% ====== IMPORT LIBRARIES ===================================================
# ........ Tkinter Library ....................................................
import tkinter as tk
from tkinter import ttk, filedialog, Toplevel, messagebox
# ........ Graphics TKinter Library ...........................................
from PIL import Image, ImageTk
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# ........ Directory Library ..................................................
import os
import glob
import zipfile
import io
# ........ Data Processing Libraries ..........................................
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
# ........ Summary Tables Libraries ...........................................
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side
# ........ Geographic Data Libraries ..........................................
import geopandas as gpd
import contextily as ctx
from matplotlib.colors import Normalize
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import ListedColormap
from matplotlib import cm
import matplotlib.offsetbox as offsetbox
from matplotlib.patches import Rectangle
import re
# ........ File Dialog and Message Box ........................................
from tkinter import filedialog, messagebox as tk_messagebox
# ........ PDF Generation Libraries ...........................................
from reportlab.pdfgen import canvas
import PyPDF2
# ........ HDF5 Libraries .....................................................
import h5py
import json
# ........ Function library ...................................................
import FuntionsLibrary as wnfun_lib
# ........ Own libraries ......................................................
import Home as home_lib
import StochasticEvents as event_lib
import CalibrationStochasticEvents as calibration_lib
import DispersionStochasticEvents as dispersion_lib
import LossesANDDamage as pyd_lib
import Losses as perdidas_lib
import Damage as danos_lib
import MapsGenerator as map_lib
import Generator as gen_lib
import DataSheets as fch_lib
import Reports as rep_lib

#%% ====== WINDOW COLORS ======================================================
# Change here the colors used in METRISK for buttons, text, and background of the 
# navigation bar and content.
cnt_color = "#FFFFFF"                                                           # Background Content Color 
upcnt_color = "#274151"                                                         # Background Logo Color
navbar_color = "#37586B"                                                        # Background Navigation Bar Color
#%% ====== TAB >> HOME ========================================================
# In this section, the variables used to generate de "HOME" content are displayed,
# along with the process the page follows when the HOME TAB is selected and when another
# TAB is selected

"""----------------------------------------------------------------------------
                        1). Define HOME Variables
----------------------------------------------------------------------------"""

# ........ Global Variables ...................................................
Home_Variables = ["Tab","Label","Rectng"]
Home_Var = {}
for hm in Home_Variables:
    Home_Var[hm] = None
# ........ Label Variables ....................................................
label_HME = ["lbl_log_HME"]
HME_label = {}
for lbl in label_HME:
    HME_label[lbl] = None
# ........ Text Variables .....................................................
text_HME = ["txt_cnt_HME1","txt_cnt_HME2","txt_cnt_HME3","txt_cnt_HME4",
            "txt_gid_HME1","txt_gid_HME2","txt_gid_HME3"]
HME_text = {}
for txt in text_HME:
    HME_text[txt] = None
# ........ Rectangle Variables ................................................
rectg_HME = ["rec_gid_HME"]
HME_rectg = {}
for rec in rectg_HME:
    HME_rectg[rec] = None
    
"""----------------------------------------------------------------------------
           Functions for displaying OR hide content in other tabs
----------------------------------------------------------------------------"""
def Show_Home():
    
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Events()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_PyD()
    Select_UnDesglo_Events()
    Select_UnDesglo_PyD()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW HOME >>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    home_lib.Show_Home_Elements(HME_label,HME_text,HME_rectg,cnt_container,cnt_color,User_Guide)
    Select_Show_Home()
    
    """........................................................................
                                 TABS are created
    ........................................................................"""
    
    # -------------------------------------------------------------------------
    # 1). ........ EVENTS TAB: ................................................
    Event_Var["Tab"] = tk.Button(navigation_bar, text="Eventos estocásticos", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Events, padx=5)
    Event_Var["Tab"].place(relx=0.56, rely=0.14, anchor=tk.CENTER)
    Event_Var["Label"] = wnfun_lib.Label_Image('/StocasticEvents.png', 28, 28, navigation_bar,navbar_color,0.16,0.135)
    Event_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_Desglo_Events)
    # -------------------------------------------------------------------------
    # 2). ........ MAPS TAB: ..................................................
    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    if Maps_Var["Tab"] is None:
        Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
        Maps_Var["Tab"].place(relx=0.544, rely=0.341, anchor=tk.CENTER)
    if Maps_Var["Label"] is None: 
        Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.338)
    # -------------------------------------------------------------------------
    # 3). ........ GENERATOR TAB: .............................................
    
    for index in Generador_Variables:
        if Generador_Var[index] is not None:
            Generador_Var[index].place_forget()
            Generador_Var[index] = None
            
    if Generador_Var["Linea"] is None: 
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is None:
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.565, anchor=tk.CENTER)
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.562)
    # -------------------------------------------------------------------------
    # 3). ........ FICHA TAB: .................................................
    
    for index in Ficha_Variables:
        if Ficha_Var[index] is not None:
            Ficha_Var[index].place_forget()
            Ficha_Var[index] = None
            
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.665, anchor=tk.CENTER)
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.662)
    # -------------------------------------------------------------------------
    # 3). ........ REPORT TAB: ................................................
    
    for index in Report_Variables:
        if Report_Var[index] is not None:
            Report_Var[index].place_forget()
            Report_Var[index] = None
            
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.765, anchor=tk.CENTER)
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.762)
    # -------------------------------------------------------------------------

def Hide_Home():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE HOME <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    home_lib.Hide_Home_Elements(label_HME,text_HME,rectg_HME,HME_label,HME_text,HME_rectg)
    Unselect_Show_Home()
    
def Select_Show_Home():
    # .... Eliminar tab y label de Home .......................................
    if Home_Var["Tab"] is not None:
        Home_Var["Tab"].place_forget()
        Home_Var["Tab"] = None
    if Home_Var["Label"] is not None:
        Home_Var["Label"].place_forget()
        Home_Var["Label"] = None
        
    # .... Seleccionar Home ...................................................
    if Home_Var["Rectng"] is None:
        Home_Var["Rectng"] = wnfun_lib.Label_Image('/Select.png', 275, 120, 
                                    navigation_bar,cnt_color,0.535,0.0359) 
    if Home_Var["Tab"] is None:
        Home_Var["Tab"] = tk.Button(navigation_bar, text="Inicio             ", font=("Abadi MT", 14), bd=0, 
                                bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_Home, padx=20)
        Home_Var["Tab"].place(relx=0.48, rely=0.0389, anchor=tk.CENTER)
    
    if Home_Var["Label"] is None:
        Home_Var["Label"] = wnfun_lib.Label_Image('/HomeSelect.png', 25, 23, 
                                        navigation_bar,cnt_color,0.16,0.0359)
    
def Unselect_Show_Home():
    # .... Eliminar tab, label y Rectng de Home ...............................
    if Home_Var["Tab"] is not None:
        Home_Var["Tab"].place_forget()
        Home_Var["Tab"] = None
    if Home_Var["Label"] is not None:
        Home_Var["Label"].place_forget()
        Home_Var["Label"] = None
    if Home_Var["Rectng"] is not None:
        Home_Var["Rectng"].place_forget()
        Home_Var["Rectng"] = None
    # .... Deseleccionar Home .................................................
    if Home_Var["Tab"] is None:
        Home_Var["Tab"] = tk.Button(navigation_bar, text="Inicio             ", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Home, padx=20)
        Home_Var["Tab"].place(relx=0.48, rely=0.0389, anchor=tk.CENTER)
    if Home_Var["Label"]  is None:
        Home_Var["Label"] = wnfun_lib.Label_Image('/Home.png', 25, 25, 
                                    navigation_bar,navbar_color,0.16,0.0359)

def User_Guide():
    wnfun_lib.Exportar_ManualUsuario()
    
#%% ====== TAB >> EVENTOS ESTOCASTICOS ========================================
"""
-------------------------------------------------------------------------------
Define Event Variables
-------------------------------------------------------------------------------
"""
# ........ Global Variables ...................................................
Event_Variables = ["Tab","Label","Rectng","Desglo"]
Event_Var = {}
for ev in Event_Variables:
    Event_Var[ev] = None
Desglo_Variables = ["CLB","DSP"]
Desglo_Var = {}
for dsg in Desglo_Variables:
    Desglo_Var[dsg] = None
# ........ Title Variables ....................................................
title_EVNT = ["tlt_tlt_EVNT","tlt_clb_EVNT","tlt_dsp_EVNT"]
EVNT_title = {}
for tlt in title_EVNT:
    EVNT_title[tlt] = None
# ........ Text Variables .....................................................
text_EVNT = ["txt_cnt_EVNT1"]
EVNT_text = {}
for txt in text_EVNT:
    EVNT_text[txt] = None
# ........ Label Variables ....................................................
label_EVNT = ["lbl_cnt_EVNT","lbl_clb_EVNT","lbl_dsp_EVNT"]
EVNT_label = {}
for lbl in label_EVNT:
    EVNT_label[lbl] = None
# ........ Button Variables ...................................................
boton_EVNT = ["btn_clb_EVNT","btn_dsp_EVNT"]
EVNT_boton = {}
for btn in boton_EVNT:
    EVNT_boton[btn] = None

"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_Events():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    
    Hide_Home()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_PyD()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    Select_UnDesglo_Events()
    Select_UnDesglo_PyD()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW EVENTS >>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    event_lib.Show_Events_Elements(EVNT_title,EVNT_text,EVNT_label,EVNT_boton,cnt_container,cnt_color,upcnt_color,Show_Calibrate,Show_Dispersion)
    Select_Show_Events()
    
def Hide_Events():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE HOME <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    event_lib.Hide_Events_Elements(title_EVNT,EVNT_title,text_EVNT,EVNT_text,label_EVNT,EVNT_label,boton_EVNT,EVNT_boton)
    Unselect_Show_Events()

def Select_Show_Events():
    # .... Eliminar tab y label de Events .....................................
    if Event_Var["Tab"] is not None:
        Event_Var["Tab"].place_forget()
        Event_Var["Tab"] = None
    if Event_Var["Label"] is not None:
        Event_Var["Label"].place_forget()
        Event_Var["Label"] = None
    if Event_Var["Desglo"] is not None:
        Event_Var["Desglo"].place_forget()
        Event_Var["Desglo"] = None
    # .... Seleccionar Events .................................................
    if Event_Var["Rectng"] is None:
        Event_Var["Rectng"] = wnfun_lib.Label_Image('/Select.png', 275, 120, 
                                        navigation_bar,cnt_color,0.535,0.138)
    if Event_Var["Tab"] is None:
        Event_Var["Tab"] = tk.Button(navigation_bar, text="Eventos estocásticos", font=("Abadi MT", 14), bd=0, 
                                bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_Events, padx=5)
        Event_Var["Tab"].place(relx=0.56, rely=0.14, anchor=tk.CENTER)
    if Event_Var["Label"] is None: 
        Event_Var["Label"] = wnfun_lib.Label_Image('/StocasticEvents_Select.png', 
                                    28, 28, navigation_bar,cnt_color,0.16,0.135)
    Unselect_Show_Home()
    # .... Cambiar el color de desglo .........................................
    if Event_Var["Desglo"] is not None:
        Event_Var["Desglo"].place_forget()
        Event_Var["Desglo"] = None
    Event_Var["Desglo"] = wnfun_lib.Button_Image('/desgloSelect.png', 12, 10, navigation_bar,"white",0.92,0.14,Select_Desglo_Events)
    
    # --------------- Acomodar pestanas de abajo ------------------------------
    
    # Perdidas y danos TAB
    
    if PyD_Var["Tab"] is not None:
        PyD_Var["Tab"].place_forget()
        PyD_Var["Tab"] = None
        
    PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_PyD, padx=5)
    PyD_Var["Tab"].place(relx=0.524, rely=0.241, anchor=tk.CENTER)#0.2411

    if PyD_Var["Label"] is not None:
        PyD_Var["Label"].place_forget()
        PyD_Var["Label"] = None
        
    PyD_Var["Label"] = wnfun_lib.Label_Image('/Damage.png', 28, 28, navigation_bar,navbar_color,0.16,0.236)

    if PyD_Var["Desglo"] is not None:
        PyD_Var["Desglo"].place_forget()
        PyD_Var["Desglo"] = None
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_Desglo_PyD)
    
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"]  = None
    
    if Generador_Var["Linea"]  is None:
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    
    if Generador_Var["Visual"] is not None: 
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"]  = None
        
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)    
   
    
def Unselect_Show_Events():
    # .... Eliminar tab, label y Rectng de Events .............................
    for index in Event_Variables:
        if Event_Var[index] is not None:
            Event_Var[index].place_forget()
            Event_Var[index] = None
            
    # .... Deseleccionar Events ...............................................
    Event_Var["Tab"] = tk.Button(navigation_bar, text="Eventos estocásticos", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Events, padx=5)
    Event_Var["Tab"].place(relx=0.56, rely=0.14, anchor=tk.CENTER)
    Event_Var["Label"] = wnfun_lib.Label_Image('/StocasticEvents.png', 28, 28, navigation_bar,navbar_color,0.16,0.135)
    Event_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_Desglo_Events)
    
    
def Select_Desglo_Events():
    
    Select_UnDesglo_PyD()
    
    # Acomodar pestaña perdidas y daños cuando se desglosa eventos estocasticos
    for index in PyD_Variables:
        if PyD_Var[index] is not None:
            PyD_Var[index].place_forget()
            PyD_Var[index] = None

    PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                                  bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_PyD, padx=5)
    PyD_Var["Tab"].place(relx=0.524, rely=0.38, anchor=tk.CENTER)
    PyD_Var["Label"] = wnfun_lib.Label_Image('/Damage.png', 28, 28, navigation_bar,navbar_color,0.16,0.375)
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.38,Select_Desglo_PyD)
    
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos

    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    
    Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
    Maps_Var["Tab"].place(relx=0.544, rely=0.48, anchor=tk.CENTER)
    Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.477)
    
    # acomodar visualizacion de resultados
    
    for index in Generador_Variables:
        if Generador_Var[index] is not None:
            Generador_Var[index].place_forget()
            Generador_Var[index] = None
    
    if Generador_Var["Linea"] is None: 
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.564)
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.604, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is None:
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.704, anchor=tk.CENTER)
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.701)
    
    # acomodar ficha tecnica
    
    for index in Ficha_Variables:
        if Ficha_Var[index] is not None:
            Ficha_Var[index].place_forget()
            Ficha_Var[index] = None    
    
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.804, anchor=tk.CENTER)
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.801)
        
    # acomodar reportes finalizados
    
    for index in Report_Variables:
        if Report_Var[index] is not None:
            Report_Var[index].place_forget()
            Report_Var[index] = None
    
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.904, anchor=tk.CENTER)
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.901)
    
    event_lib.Select_Desglo_Events_Elements(Desglo_Var,navigation_bar,navbar_color,Show_Calibrate,Show_Dispersion)
    # Cambiar el icono por el de dejar de desglosar
    if Event_Var["Rectng"] is None:
        if Event_Var["Desglo"] is not None:
            Event_Var["Desglo"].place_forget()
            Event_Var["Desglo"] = None
        Event_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_UnDesglo_Events)
    else:
        if Event_Var["Desglo"] is not None:
            Event_Var["Desglo"].place_forget()
            Event_Var["Desglo"] = None
        Event_Var["Desglo"] = wnfun_lib.Button_Image('/mtlSelect.png', 12, 10, navigation_bar,"white",0.92,0.14,Select_UnDesglo_Events)
        
    
def Select_UnDesglo_Events():
    event_lib.Select_UnDesglo_Events_Elements(Desglo_Variables,Desglo_Var)
    if Event_Var["Rectng"] is None:
        if Event_Var["Desglo"] is not None:
            Event_Var["Desglo"].place_forget()
            Event_Var["Desglo"] = None
        Event_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_Desglo_Events)
    else:
        if Event_Var["Desglo"] is not None:
            Event_Var["Desglo"].place_forget()
            Event_Var["Desglo"] = None
        Event_Var["Desglo"] = wnfun_lib.Button_Image('/desgloSelect.png', 12, 10, navigation_bar,"white",0.92,0.14,Select_Desglo_Events)
    # Quitar la seleccion de calibrar si existe
    if Calibrar_Var["Rectng"] is not None:
        Calibrar_Var["Rectng"].place_forget()
        Calibrar_Var["Rectng"] = None
    # Quitar la seleccion de dispersion si existe
    if Dispersion_Var["Rectng"] is not None:
        Dispersion_Var["Rectng"].place_forget()
        Dispersion_Var["Rectng"] = None
        
    # Acomodar pestanas de abajo
    if PyD_Var["Tab"] is not None:
        PyD_Var["Tab"].place_forget()
        PyD_Var["Tab"] = None
        PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                            bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_PyD, padx=5)
        PyD_Var["Tab"].place(relx=0.524, rely=0.241, anchor=tk.CENTER)
    
    if PyD_Var["Label"] is not None:
        PyD_Var["Label"].place_forget()
        PyD_Var["Label"] = None
        PyD_Var["Label"] = wnfun_lib.Label_Image('/Damage.png', 28, 28, navigation_bar,navbar_color,0.16,0.236)
    
    if PyD_Var["Desglo"] is not None:
        PyD_Var["Desglo"].place_forget()
        PyD_Var["Desglo"] = None
        PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_Desglo_PyD)
    
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos

    if Maps_Var["Tab"] is not None:
        Maps_Var["Tab"].place_forget()
        Maps_Var["Tab"] = None
        Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
        Maps_Var["Tab"].place(relx=0.544, rely=0.341, anchor=tk.CENTER)
        
    if Maps_Var["Label"] is not None:
        Maps_Var["Label"].place_forget()
        Maps_Var["Label"] = None
        Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.338)
    
    # acomodar visualizacion de resultados
    
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"] = None
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    if Generador_Var["Visual"] is not None:
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"] = None
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is not None:
        Generador_Var["Tab"].place_forget()
        Generador_Var["Tab"] = None
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.565, anchor=tk.CENTER)
    if Generador_Var["Label"] is not None: 
        Generador_Var["Label"].place_forget()
        Generador_Var["Label"] = None
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.562)
    
    if Ficha_Var["Tab"] is not None:
        Ficha_Var["Tab"].place_forget()
        Ficha_Var["Tab"] = None
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.665, anchor=tk.CENTER)
        
    if Ficha_Var["Label"] is not None: 
        Ficha_Var["Label"].place_forget()
        Ficha_Var["Label"] = None
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.662)
    
    if Report_Var["Tab"] is not None:
        Report_Var["Tab"].place_forget()
        Report_Var["Tab"] = None
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.765, anchor=tk.CENTER)
    if Report_Var["Label"] is not None: 
        Report_Var["Label"].place_forget()
        Report_Var["Label"] = None
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.762)
    
#%% ====== TAB >> CALIBRAR EVENTOS ESTOCASTICOS ===============================
"""
-------------------------------------------------------------------------------
Define Calibrate Variables
-------------------------------------------------------------------------------
"""
Calibrar_Variables = ["Rectng"]
Calibrar_Var = {}
for var in Calibrar_Variables:
    Calibrar_Var[var] = None

    
title_CLB = ["tlt_tlt_CLB"]
CLB_title = {}
for tlt in title_CLB:
    CLB_title[tlt] = None
    
text_CLB = ["txt_cnt_CLB1","txt_cp_CLB","txt_gf1_CLB","txt_gf2_CLB","tlt_sct_CLB",
            "tlt_rstv2_CLB"]
CLB_text = {}
for txt in text_CLB:
    CLB_text[txt] = None
    
boton_CLB = ["btn_slc_CLB","btn_clb_CLB","btn_inf_CLB","btn_exp_CLB","btn_exp2_CLB","btn_cbm_CLB",
             "cmb_Mnz_CLB","btn_cck_CLB"]
CLB_boton = {}
for btn in boton_CLB:
    CLB_boton[btn] = None

boton_CLB2 = ["SiNo"]
CLB_boton2 = {}
for btn in boton_CLB2:
    CLB_boton2[btn] = None
    
canva_CLB = ["cnv_cp_CLB","cnv_mnz_CLB","cnv_txn_CLB"]
CLB_canva = {}
for cnv in canva_CLB:
    CLB_canva[cnv] = None

label_CLB = ["lbl_cnt_CLB","lbl_rst_CLB","lbl_rstv2_CLB","lbl_DsF_CLB"]
CLB_label = {}
for lbl in label_CLB:
    CLB_label[lbl] = None
    
rect_CLB = ["rec_cmb_MNZ"]
CLB_rect = {}
for rec in rect_CLB:
    CLB_rect[rec] = None
# ------ Variables globales ---------------------------------------------------
carpeta_seleccionada = None
resultado_label = None
"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_Calibrate():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_PyD()
    Hide_Dispersion()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    # -------------------------------------------------------------------------
    # Acomodar pestanas de abajo
    for index in PyD_Variables:
        if PyD_Var[index] is not None:
            PyD_Var[index].place_forget()
            PyD_Var[index] = None

    PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                                  bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_PyD, padx=5)
    PyD_Var["Tab"].place(relx=0.524, rely=0.38, anchor=tk.CENTER)
    PyD_Var["Label"] = wnfun_lib.Label_Image('/Damage.png', 28, 28, navigation_bar,navbar_color,0.16,0.375)
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.38,Select_Desglo_PyD)
    
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos

    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    
    Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
    Maps_Var["Tab"].place(relx=0.544, rely=0.48, anchor=tk.CENTER)
    Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.477)
    
    # acomodar visualizacion de resultados
    
    for index in Generador_Variables:
        if Generador_Var[index] is not None:
            Generador_Var[index].place_forget()
            Generador_Var[index] = None
    
    if Generador_Var["Linea"] is None: 
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.564)
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.604, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is None:
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.704, anchor=tk.CENTER)
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.701)
    
    # acomodar ficha tecnica
    
    for index in Ficha_Variables:
        if Ficha_Var[index] is not None:
            Ficha_Var[index].place_forget()
            Ficha_Var[index] = None    
    
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.804, anchor=tk.CENTER)
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.801)
        
    # acomodar reportes finalizados
    
    for index in Report_Variables:
        if Report_Var[index] is not None:
            Report_Var[index].place_forget()
            Report_Var[index] = None
    
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.904, anchor=tk.CENTER)
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.901)
    
    
    
    
    # -------------------------------------------------------------------------
    # Cuando se entra desde "Eventos estocasticos" >> "Calibracion"
    if Desglo_Var["CLB"] is None and Desglo_Var["DSP"] is None:
        event_lib.Select_Desglo_Events_Elements(Desglo_Var,navigation_bar,navbar_color,Show_Calibrate,Show_Dispersion)
        Event_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_UnDesglo_Events)
    # Cuando se entra desglosando el menu >> "Calibracion"
    Event_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_UnDesglo_Events)
    # Y si se oprime se debe eliminar el rectangulo que simula que se selecciono
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>> SHOW CALIBRATION >>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    calibration_lib.Show_Calibration_Elements(CLB_title,CLB_text,CLB_boton,cnt_container,upcnt_color,Select_Folder_CLB,Ventana_Info_CLB,Function_Calibrate,resultado_label)
    Select_Show_Calibrate()

def Hide_Calibrate():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<< HIDE CALIBRATION <<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    calibration_lib.Hide_Calibration_Elements(title_CLB,CLB_title,text_CLB,CLB_text,boton_CLB,CLB_boton,canva_CLB,CLB_canva,label_CLB,CLB_label,rect_CLB,CLB_rect)
    Unselect_Show_Calibrate()

def Select_Show_Calibrate():
    Calibrar_Var["Rectng"] = wnfun_lib.Label_Image('/Select_SubMenu.png', 300, 35, navigation_bar,navbar_color,0.5,0.22)
    if Desglo_Var["CLB"] is not None:
        Desglo_Var["CLB"].place_forget()
        Desglo_Var["CLB"] = None
        
    Desglo_Var["CLB"] = tk.Button(navigation_bar, text="Calibrar eventos", font=("Abadi MT", 14), bd=0, 
                                bg="#456883", fg="white", relief=tk.FLAT, command=Show_Calibrate, padx=1)
    Desglo_Var["CLB"].place(relx=0.5, rely=0.22, anchor=tk.CENTER)
    

def Unselect_Show_Calibrate():
    if Calibrar_Var["Rectng"] is not None:
        Calibrar_Var["Rectng"].place_forget()
        Calibrar_Var["Rectng"] = None
    if Desglo_Var["CLB"] is not None:
        Desglo_Var["CLB"].place_forget()
        Desglo_Var["CLB"] = None
    Desglo_Var["CLB"] = tk.Button(navigation_bar, text="Calibrar eventos", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=Show_Calibrate, padx=20)
    Desglo_Var["CLB"].place(relx=0.5, rely=0.22, anchor=tk.CENTER)
        
#%% ====== TAB >> DISPERSION EVENTOS ESTOCASTICOS =============================
"""
-------------------------------------------------------------------------------
Define Dispersion Variables
-------------------------------------------------------------------------------
"""
Dispersion_Variables = ["Rectng"]
Dispersion_Var = {}
for var in Dispersion_Variables:
    Dispersion_Var[var] = None
    
title_DSP = ["tlt_tlt_DSP"]
DSP_title = {}
for tlt in title_DSP:
    DSP_title[tlt] = None

text_DSP = ["txt_cnt_DSP1","txt_cp_DSP","tlt_sct_DSP",
            "txt_gf1_DSP","txt_gf2_DSP","tlt_rstv2_DSP"]
DSP_text = {}
for txt in text_DSP:
    DSP_text[txt] = None

boton_DSP = ["btn_slc_DSP","btn_inf_DSP","btn_clb_DSP","cmb_Mnz_DSP",
             "btn_cck_DSP","btn_exp_DSP","btn_exp2_DSP","btn_cbm_DSP"]
DSP_boton = {}
for btn in boton_DSP:
    DSP_boton[btn] = None

boton_DSP2 = ["SiNo"]
DSP_boton2 = {}
for btn in boton_DSP2:
    DSP_boton2[btn] = None

label_DSP = ["lbl_cnt_DSP","lbl_rst_DSP","lbl_rstv2_DSP","lbl_rstv3_DSP","lbl_DsF_DSP"]
DSP_label = {}
for lbl in label_DSP:
    DSP_label[lbl] = None

canva_DSP = ["cnv_cp_DSP","cnv_mnz_DSP","cnv_txn_DSP"]
DSP_canva = {}
for cnv in canva_DSP:
    DSP_canva[cnv] = None
    
rect_DSP = ["rec_cmb_DSP"]
DSP_rect = {}
for rec in rect_DSP:
    DSP_rect[rec] = None
    
# ------ Variables globales ---------------------------------------------------
carpeta_seleccionada_DSP = None
resultado_label_Dispersion = None
"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_Dispersion():
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_PyD()
    Hide_Calibrate()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    # -------------------------------------------------------------------------
    # Acomodar pestanas de abajo
    for index in PyD_Variables:
        if PyD_Var[index] is not None:
            PyD_Var[index].place_forget()
            PyD_Var[index] = None

    PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                                  bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_PyD, padx=5)
    PyD_Var["Tab"].place(relx=0.524, rely=0.38, anchor=tk.CENTER)
    PyD_Var["Label"] = wnfun_lib.Label_Image('/Damage.png', 28, 28, navigation_bar,navbar_color,0.16,0.375)
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.38,Select_Desglo_PyD)
    
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos

    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    
    Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
    Maps_Var["Tab"].place(relx=0.544, rely=0.48, anchor=tk.CENTER)
    Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.477)
    
    # acomodar visualizacion de resultados
    
    for index in Generador_Variables:
        if Generador_Var[index] is not None:
            Generador_Var[index].place_forget()
            Generador_Var[index] = None
    
    if Generador_Var["Linea"] is None: 
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.564)
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.604, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is None:
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.704, anchor=tk.CENTER)
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.701)
    
    # acomodar ficha tecnica
    
    for index in Ficha_Variables:
        if Ficha_Var[index] is not None:
            Ficha_Var[index].place_forget()
            Ficha_Var[index] = None    
    
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.804, anchor=tk.CENTER)
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.801)
        
    # acomodar reportes finalizados
    
    for index in Report_Variables:
        if Report_Var[index] is not None:
            Report_Var[index].place_forget()
            Report_Var[index] = None
    
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.904, anchor=tk.CENTER)
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.901)
    
    
    # -------------------------------------------------------------------------
    # Cuando se entra desde "Eventos estocasticos" >> "Dispersion"
    if Desglo_Var["CLB"] is None and Desglo_Var["DSP"] is None:
        event_lib.Select_Desglo_Events_Elements(Desglo_Var,navigation_bar,navbar_color,Show_Calibrate,Show_Dispersion)
        Event_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_UnDesglo_Events)
    # Cuando se entra desglosando el menu >> "Dispersion"
    Event_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.14,Select_UnDesglo_Events)
    # Y si se oprime se debe eliminar el rectangulo que simula que se selecciono
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>> SHOW DISPERSION >>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    dispersion_lib.Show_Dispersion_Elements(DSP_title,DSP_text,DSP_boton,cnt_container,upcnt_color,Select_Folder_DSP,Ventana_Info_DSP,Function_Dispersion,resultado_label_Dispersion)
    Select_Show_Dispersion()

def Hide_Dispersion():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<< HIDE DISPERSION <<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    dispersion_lib.Hide_Dispersion_Elements(title_DSP,DSP_title,text_DSP,DSP_text,boton_DSP,DSP_boton,canva_DSP,DSP_canva,label_DSP,DSP_label,rect_DSP,DSP_rect)
    Unselect_Show_Dispersion()

def Select_Show_Dispersion():
    Dispersion_Var["Rectng"] = wnfun_lib.Label_Image('/Select_SubMenu.png', 300, 35, navigation_bar,navbar_color,0.5,0.29)
    if Desglo_Var["DSP"] is not None:
        Desglo_Var["DSP"].place_forget()
        Desglo_Var["DSP"] = None
    Desglo_Var["DSP"] = tk.Button(navigation_bar, text="Dispersión de eventos", font=("Abadi MT", 14), bd=0, 
                                bg="#456883", fg="white", relief=tk.FLAT, command=Show_Dispersion, padx=1)
    Desglo_Var["DSP"].place(relx=0.59, rely=0.29, anchor=tk.CENTER)
    
def Unselect_Show_Dispersion():
    if Dispersion_Var["Rectng"] is not None:
        Dispersion_Var["Rectng"].place_forget()
        Dispersion_Var["Rectng"] = None
    if Desglo_Var["DSP"] is not None:
        Desglo_Var["DSP"].place_forget()
        Desglo_Var["DSP"] = None
    Desglo_Var["DSP"] = tk.Button(navigation_bar, text="Dispersión de eventos", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=Show_Dispersion, padx=20)
    Desglo_Var["DSP"].place(relx=0.59, rely=0.29, anchor=tk.CENTER)

#%% ====== TAB >> PERDIDAS Y DANOS ============================================
"""
-------------------------------------------------------------------------------
Define Event Variables
-------------------------------------------------------------------------------
"""
# ........ Global Variables ...................................................
PyD_Variables = ["Tab","Label","Rectng","Desglo"]
PyD_Var = {}
for ev in PyD_Variables:
    PyD_Var[ev] = None
    
Desglo_PyD_Variables = ["PRD","DNO"]
Desglo_PyD_Var = {}
for dsg in Desglo_PyD_Variables:
    Desglo_PyD_Var[dsg] = None
# ........ Title Variables ....................................................
title_PyD = ["tlt_tlt_PyD"]
PyD_title = {}
for tlt in title_PyD:
    PyD_title[tlt] = None
# ........ Text Variables .....................................................
text_PyD = ["txt_cnt_PyD1"]
PyD_text = {}
for txt in text_PyD:
    PyD_text[txt] = None
# ........ Button Variables ...................................................
boton_PyD = ["btn_prd_PyD","btn_dno_PyD"]
PyD_boton = {}
for btn in boton_PyD:
    PyD_boton[btn] = None
    
Perdidas_Variables = ["Rectng"]
Perdidas_Var = {}
for var in Perdidas_Variables:
    Perdidas_Var[var] = None

Danos_Variables = ["Rectng"]
Danos_Var = {}
for var in Danos_Variables:
    Danos_Var[var] = None

"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_PyD():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_Events()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    Select_UnDesglo_PyD()
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>> SHOW PyD >>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    pyd_lib.Show_PyD_Elements(PyD_title,PyD_text,PyD_boton,cnt_container,cnt_color,upcnt_color,Show_Perdidas,Show_Danos)
    Select_Show_PyD()

def Hide_PyD():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE HOME <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    pyd_lib.Hide_PyD_Elements(title_PyD,PyD_title,text_PyD,PyD_text,boton_PyD,PyD_boton)
    Unselect_Show_PyD()
    
def Select_Show_PyD():
    # .... Eliminar tab y label de Events .....................................
    if PyD_Var["Tab"] is not None:
        PyD_Var["Tab"].place_forget()
        PyD_Var["Tab"] = None
    if PyD_Var["Label"] is not None:
        PyD_Var["Label"].place_forget()
        PyD_Var["Label"] = None
    if PyD_Var["Desglo"] is not None:
        PyD_Var["Desglo"].place_forget()
        PyD_Var["Desglo"] = None
    # .... Seleccionar Events .................................................
    if PyD_Var["Rectng"] is None:
        PyD_Var["Rectng"] = wnfun_lib.Label_Image('/Select.png', 275, 120, 
                                    navigation_bar,cnt_color,0.535,0.241)
    if PyD_Var["Tab"] is None: 
        PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                                bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_PyD, padx=5)
        PyD_Var["Tab"].place(relx=0.524, rely=0.241, anchor=tk.CENTER)
    
    if PyD_Var["Label"] is None: 
        PyD_Var["Label"] = wnfun_lib.Label_Image('/DamageSelect.png', 28, 28, 
                                        navigation_bar,cnt_color,0.16,0.236)
    
    # ======================= Arreglar pestana de arriba ======================
    Unselect_Show_Events()

    # .... Cambiar el color de desglo .........................................
    if PyD_Var["Desglo"] is not None:
        PyD_Var["Desglo"].place_forget()
        PyD_Var["Desglo"] = None
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desgloSelect.png', 12, 10, navigation_bar,"white",0.92,0.241,Select_Desglo_PyD)

    # ======================= Arreglar pestana de abajo =======================
    
    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    if Maps_Var["Tab"] is None:
        Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
        Maps_Var["Tab"].place(relx=0.544, rely=0.341, anchor=tk.CENTER)
    if Maps_Var["Label"] is None: 
        Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.338)
    
    
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"]  = None
    
    if Generador_Var["Linea"]  is None:
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    
    if Generador_Var["Visual"] is not None: 
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"]  = None
        
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)    
        
def Unselect_Show_PyD():
    # .... Eliminar tab, label y Rectng de Events .............................
    for index in PyD_Variables:
        if PyD_Var[index] is not None:
            PyD_Var[index].place_forget()
            PyD_Var[index] = None
    # .... Deseleccionar Events ...............................................
    PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_PyD, padx=5)
    PyD_Var["Tab"].place(relx=0.524, rely=0.241, anchor=tk.CENTER)
    PyD_Var["Label"] = wnfun_lib.Label_Image('/Damage.png', 28, 28, navigation_bar,navbar_color,0.16,0.236)
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_Desglo_PyD)

def Select_Desglo_PyD():
    
    Select_UnDesglo_Events()
    
    pyd_lib.Select_Desglo_PyD_Elements(Desglo_PyD_Var,navigation_bar,navbar_color,Show_Perdidas,Show_Danos)
    
    # Cambiar el icono por el de dejar de desglosar
    if PyD_Var["Rectng"] is None:
        if PyD_Var["Desglo"] is not None:
            PyD_Var["Desglo"].place_forget()
            PyD_Var["Desglo"] = None
        PyD_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_UnDesglo_PyD)
    else:
        if PyD_Var["Desglo"] is not None:
            PyD_Var["Desglo"].place_forget()
            PyD_Var["Desglo"] = None
        PyD_Var["Desglo"] = wnfun_lib.Button_Image('/mtlSelect.png', 12, 10, navigation_bar,"white",0.92,0.241,Select_UnDesglo_PyD)
        if PyD_Var["Label"] is not None:
            PyD_Var["Label"].place_forget()
            PyD_Var["Label"] = None
        PyD_Var["Label"] = wnfun_lib.Label_Image('/DamageSelect.png', 28, 28, navigation_bar,cnt_color,0.16,0.236)
        if PyD_Var["Tab"] is not None:
            PyD_Var["Tab"].place_forget()
            PyD_Var["Tab"] = None
        PyD_Var["Tab"] = tk.Button(navigation_bar, text="Pérdidas y Daños", font=("Abadi MT", 14), bd=0, 
                                    bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_PyD, padx=5)
        PyD_Var["Tab"].place(relx=0.524, rely=0.241, anchor=tk.CENTER)
        
    # ======================= Acomodar pestaña de abajo =======================
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos
    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    
    Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
    Maps_Var["Tab"].place(relx=0.544, rely=0.48, anchor=tk.CENTER)
    Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.477)
    
    # acomodar visualizacion de resultados
    
    for index in Generador_Variables:
        if Generador_Var[index] is not None:
            Generador_Var[index].place_forget()
            Generador_Var[index] = None
    
    if Generador_Var["Linea"] is None: 
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.564)
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.604, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is None:
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.704, anchor=tk.CENTER)
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.701)
    
    # acomodar ficha tecnica
    
    for index in Ficha_Variables:
        if Ficha_Var[index] is not None:
            Ficha_Var[index].place_forget()
            Ficha_Var[index] = None    
    
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.804, anchor=tk.CENTER)
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.801)
        
    # acomodar reportes finalizados
    
    for index in Report_Variables:
        if Report_Var[index] is not None:
            Report_Var[index].place_forget()
            Report_Var[index] = None
    
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.904, anchor=tk.CENTER)
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.901)
    
def Select_UnDesglo_PyD():
    pyd_lib.Select_UnDesglo_PyD_Elements(Desglo_PyD_Variables,Desglo_PyD_Var)
    if PyD_Var["Rectng"] is None:
        if PyD_Var["Desglo"] is not None:
            PyD_Var["Desglo"].place_forget()
            PyD_Var["Desglo"] = None
        PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desglo.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_Desglo_PyD)
    else:
        if PyD_Var["Desglo"] is not None:
            PyD_Var["Desglo"].place_forget()
            PyD_Var["Desglo"] = None
        PyD_Var["Desglo"] = wnfun_lib.Button_Image('/desgloSelect.png', 12, 10, navigation_bar,"white",0.92,0.241,Select_Desglo_PyD)
    # Quitar la seleccion de Perdidas si existe
    if Perdidas_Var["Rectng"] is not None:
        Perdidas_Var["Rectng"].place_forget()
        Perdidas_Var["Rectng"] = None
    # Quitar la seleccion de Danos si existe
    if Danos_Var["Rectng"] is not None:
        Danos_Var["Rectng"].place_forget()
        Danos_Var["Rectng"] = None
        
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos
    if Maps_Var["Tab"] is not None:
        Maps_Var["Tab"].place_forget()
        Maps_Var["Tab"] = None
        Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
        Maps_Var["Tab"].place(relx=0.544, rely=0.341, anchor=tk.CENTER)
        
    if Maps_Var["Label"] is not None:
        Maps_Var["Label"].place_forget()
        Maps_Var["Label"] = None
        Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.338)
    
    # acomodar visualizacion de resultados
    
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"] = None
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    if Generador_Var["Visual"] is not None:
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"] = None
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is not None:
        Generador_Var["Tab"].place_forget()
        Generador_Var["Tab"] = None
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.565, anchor=tk.CENTER)
    if Generador_Var["Label"] is not None: 
        Generador_Var["Label"].place_forget()
        Generador_Var["Label"] = None
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.562)
    
    if Ficha_Var["Tab"] is not None:
        Ficha_Var["Tab"].place_forget()
        Ficha_Var["Tab"] = None
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.665, anchor=tk.CENTER)
        
    if Ficha_Var["Label"] is not None: 
        Ficha_Var["Label"].place_forget()
        Ficha_Var["Label"] = None
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.662)
    
    if Report_Var["Tab"] is not None:
        Report_Var["Tab"].place_forget()
        Report_Var["Tab"] = None
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.765, anchor=tk.CENTER)
    if Report_Var["Label"] is not None: 
        Report_Var["Label"].place_forget()
        Report_Var["Label"] = None
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.762)
    
def nada():
    print('nada')
#%% ====== TAB >> PERDIDAS BASADAS EN EVENTOS =================================
"""
-------------------------------------------------------------------------------
Define Losses Variables
-------------------------------------------------------------------------------
"""
Perdidas_Variables = ["Rectng"]
Perdidas_Var = {}
for var in Perdidas_Variables:
    Perdidas_Var[var] = None

title_PRD = ["tlt_tlt_PRD"]
PRD_title = {}
for tlt in title_PRD:
    PRD_title[tlt] = None
    
text_PRD = ["txt_cnt_PRD1","txt_cp_PRD","txt_gf1_PRD","tlt_sct_PRD","tlt_sct_PRD1","tlt_rstv2_PRD",
            "txt_vlx_PRD1","txt_vlx_PRD2","txt_vlx_PRD3","txt_vlx_PRD4","txt_vlx_PRD5",
            "txt_vlx_PRD6","txt_vlx_PRD7","txt_vlx_PRD8","txt_vlx_PRD9","txt_vlx_PRD10",
            "txt_vlx_PRD11","txt_vlx_PRD12","txt_vlx_PRD13","txt_vlx_PRD14","txt_vlx_PRD15",
            "txt_vlx_PRD16","txt_vlx_PRD17","txt_vlx_PRD18","txt_vlx_PRD19","txt_vlx_PRD20",
            "txt_vlx_PRD21","txt_vlx_PRD22","txt_vlx_PRD23","tlt_rstv2_CLB"]
PRD_text = {}
for txt in text_PRD:
    PRD_text[txt] = None

boton_PRD = ["btn_ing_PRD","btn_clb_PRD","btn_slc_PRD","btn_inf_PRD","btn_exp_PRD","btn_cbm2_PRD",
             "lbl_cnt_PRD","lbl_tbl_PRD","btn_cbm_PRD","lbl_tbl_txn_PRD","btn_siguiente","btn_atras","btn_rps_txn",
             "lbl_leyend","cmb_lat","cmb_lon","cmb_min_lon","cmb_max_lon","cmb_min_lat","cmb_max_lat","btn_ajs_PRD",
             "btn_rin_PRD","lbl_mdm_PRD","btn_scc_PRD","btn_PAEVLE_PRD","btn_PAECOP_PRD","btn_exp2_PRD"]
PRD_boton = {}
for btn in boton_PRD:
    PRD_boton[btn] = None
    
boton_PRD2 = ["SiNo"]
PRD_boton2 = {}
for btn in boton_PRD2:
    PRD_boton2[btn] = None

entry_PRD = ["ent_per_PRD"]
PRD_entry = {}
for ent in entry_PRD:
    PRD_entry[ent] = None

label_PRD = ["lbl_rst_PRD","lbl_DsF_PRD","lbl_rstv2_PRD","lbl_rstv3_PRD","lbl_rstv4_PRD"]
PRD_label = {}
for lbl in label_PRD:
    PRD_label[lbl] = None

rectg_PRD = ["rec_per_PRD"]
PRD_rectg = {}
for ent in rectg_PRD:
    PRD_rectg[ent] = None
    
canva_PRD = ["cnv_cv_PRD","cnv_grph_PRD"]
PRD_canva = {}
for cnv in canva_PRD:
    PRD_canva[cnv] = None
    
# ------ Variables para tabla PAE taxonomia -----------------------------------
# Si o si van a ser 8 para cada columna, se eliminan y vuelven y se crean si
# hay mas taxonomias.

description_list, taxo_list, valexCop_list, valexPrc_list, PaeCop_list, PaePrc_list, PaePrcM_list = [], [], [], [], [], [], []
for index in range(int(8)):
    description_list.append("Description_"+str(index+1))
    taxo_list.append("Taxonomia_"+str(index+1))
    valexCop_list.append("ValexCOP_"+str(index+1))
    valexPrc_list.append("ValexPRC_"+str(index+1))
    PaeCop_list.append("PaeCOP_"+str(index+1))
    PaePrc_list.append("PaePRC_"+str(index+1))
    PaePrcM_list.append("PaePRCM_"+str(index+1))

# Crear las variables para guardar cada descripcion
PRD_Description = {}
for val in description_list:
    PRD_Description[val] = None

# Crear las variables para guardar cada taxonomia
PRD_Taxonomia = {}
for val in taxo_list:
    PRD_Taxonomia[val] = None

# Crear las variables para guardar cada valor expuesto en COP
PRD_ValexCOP = {}
for val in valexCop_list:
    PRD_ValexCOP[val] = None

# Crear las variables para guardar cada valor expuesto en porcentaje
PRD_ValexPRC = {}
for val in valexPrc_list:
    PRD_ValexPRC[val] = None

# Crear las variables para guardar cada perdida anual esperada en COP
PRD_PaeCOP = {}
for val in PaeCop_list:
    PRD_PaeCOP[val] = None

# Crear las variables para guardar cada perdida anual esperada en %
PRD_PaePRC = {}
for val in PaePrc_list:
    PRD_PaePRC[val] = None

# Crear las variables para guardar cada perdida anual esperada en %.
PRD_PaePRCM = {}
for val in PaePrcM_list:
    PRD_PaePRCM[val] = None    

# ------ Variables globales ---------------------------------------------------
carpeta_seleccionada_PRD_mnz = None
resultado_label_PRD = None
"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_Perdidas():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_PyD()
    Hide_Dispersion()
    Hide_Calibrate()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    # ======================= Acomodar pestaña de abajo =======================
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos
    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    
    Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
    Maps_Var["Tab"].place(relx=0.544, rely=0.48, anchor=tk.CENTER)
    Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.477)
    
    # acomodar visualizacion de resultados
    
    for index in Generador_Variables:
        if Generador_Var[index] is not None:
            Generador_Var[index].place_forget()
            Generador_Var[index] = None
    
    if Generador_Var["Linea"] is None: 
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.564)
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.604, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is None:
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.704, anchor=tk.CENTER)
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.701)
    
    # acomodar ficha tecnica
    
    for index in Ficha_Variables:
        if Ficha_Var[index] is not None:
            Ficha_Var[index].place_forget()
            Ficha_Var[index] = None    
    
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.804, anchor=tk.CENTER)
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.801)
        
    # acomodar reportes finalizados
    
    for index in Report_Variables:
        if Report_Var[index] is not None:
            Report_Var[index].place_forget()
            Report_Var[index] = None
    
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.904, anchor=tk.CENTER)
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.901)
    
    
    # -------------------------------------------------------------------------
    # Cuando se entra desde "Pérdidas y Daños" >> "Pérdidas"
    if Desglo_PyD_Var["PRD"] is None and Desglo_PyD_Var["DNO"] is None:
        # Despliega el menu de esa navegacion
        pyd_lib.Select_Desglo_PyD_Elements(Desglo_PyD_Var,navigation_bar,navbar_color,Show_Perdidas,Show_Danos)    
        # Cambia el boton desglo para que sea el no desglosado
        if PyD_Var["Desglo"] is not None:
            PyD_Var["Desglo"].place_forget()
            PyD_Var["Desglo"] = None
        PyD_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_UnDesglo_PyD)
    # Cuando se entra desglosando el menu >> "Pérdidas"
    if PyD_Var["Desglo"] is not None:
        PyD_Var["Desglo"].place_forget()
        PyD_Var["Desglo"] = None
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_UnDesglo_PyD)
    # Y si se oprime se debe eliminar el rectangulo que simula que se selecciono
    # Select_Desglo_PyD()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW LOSSES >>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    perdidas_lib.Show_Perdidas_Elements(PRD_title,PRD_text,PRD_boton,PRD_entry,PRD_rectg,cnt_container,upcnt_color,Select_Folder_PRD,Ventana_Info_PRD,Function_Perdidas,resultado_label_PRD)
    Select_Show_Perdidas()

def Hide_Perdidas():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<< HIDE CALIBRATION <<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    perdidas_lib.Hide_Perdidas_Elements(title_PRD,PRD_title,text_PRD,PRD_text,boton_PRD,PRD_boton,entry_PRD,PRD_entry,rectg_PRD,PRD_rectg,canva_PRD,PRD_canva,label_PRD,PRD_label)
    Unselect_Show_Perdidas()

def Select_Show_Perdidas():
    Perdidas_Var["Rectng"] = wnfun_lib.Label_Image('/Select_SubMenu.png', 300, 35, navigation_bar,navbar_color,0.5,0.323)
    
    if Desglo_PyD_Var["PRD"] is not None:
        Desglo_PyD_Var["PRD"].place_forget()
        Desglo_PyD_Var["PRD"] = None
    
    Desglo_PyD_Var["PRD"] = tk.Button(navigation_bar, text="Pérdidas", font=("Abadi MT", 14), bd=0, 
                                bg="#456883", fg="white", relief=tk.FLAT, command=Show_Perdidas, padx=1)
    Desglo_PyD_Var["PRD"].place(relx=0.393, rely=0.323, anchor=tk.CENTER)
    
    
def Unselect_Show_Perdidas():
    if Perdidas_Var["Rectng"] is not None:
        Perdidas_Var["Rectng"].place_forget()
        Perdidas_Var["Rectng"] = None
        
    if Desglo_PyD_Var["PRD"] is not None:
        Desglo_PyD_Var["PRD"].place_forget()
        Desglo_PyD_Var["PRD"] = None
        
        Desglo_PyD_Var["PRD"] = tk.Button(navigation_bar, text="Pérdidas", font=("Abadi MT", 14), bd=0, 
                                    bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=Show_Perdidas, padx=20)
        Desglo_PyD_Var["PRD"].place(relx=0.393, rely=0.323, anchor=tk.CENTER)

#%% ====== TAB >> DANOS BASADAS EN EVENTOS ====================================
"""
-------------------------------------------------------------------------------
Define Losses Variables
-------------------------------------------------------------------------------
"""
Danos_Variables = ["Rectng"]
Danos_Var = {}
for var in Danos_Variables:
    Danos_Var[var] = None

title_DNO = ["tlt_tlt_DNO"]
DNO_title = {}
for tlt in title_DNO:
    DNO_title[tlt] = None
    
text_DNO = ["txt_cnt_DNO","tlt_sct_DNO","tlt_rstv2_DNO",
            "tlt_sct_DNO1","txt_tbl1_DNO","txt_tbl2_DNO",
            "txt_tbl3_DNO","txt_tbl4_DNO","txt_tbl5_DNO",
            "txt_tbl6_DNO","txt_tbl7_DNO","txt_tbl22_DNO",
            "txt_tbl33_DNO","txt_tbl44_DNO","txt_tbl55_DNO",
            "txt_tbl66_DNO","txt_tbl77_DNO"]
DNO_text = {}
for txt in text_DNO:
    DNO_text[txt] = None

boton_DNO = ["btn_slc_DNO","btn_inf_DNO","btn_clb_DNO",
             "lbl_rst_DNO","lbl_DsF_DNO","lbl_rstv2_DNO",
             "lbl_rstv3_DNO","lbl_rstv4_DNO","tbl_CP_DNO",
             "btn_hml_DNO","btn_clp_DNO","btn_inj_DNO",
             "btn_ftl_DNO","btn_cbm_DNO","btn_exp_DNO",
             "btn_diag_DNO","btn_atras","btn_siguiente",
             "lbl_lyd_DNO","tbl_txn_DNO","tbl_txn2_DNO",
             "tbl_txn3_DNO","btn_exp2_DNO","lbl_mdm_DNO",
             "cmb_lon","cmb_lat","cmb_min_lon","cmb_max_lon",
             "cmb_max_lat","cmb_min_lat","btn_ajs_DNO",
             "btn_rin_DNO","btn_scc_DNO"]
DNO_boton = {}
for btn in boton_DNO:
    DNO_boton[btn] = None

canva_DNO = ["cnv_mp_DNO","cnv_dgm_DNO","cnv_homeless_DNO"]
DNO_canva = {}
for btn in canva_DNO:
    DNO_canva[btn] = None
    
boton_DNO2 = ["SiNo"]
DNO_boton2 = {}
for btn in boton_DNO2:
    DNO_boton2[btn] = None

# ------ Variables tabla taxonomia --------------------------------------------
DNO_table = {}
table_DNO = None

DNO_tblTaxo = {}
tblTaxo_DNO = None
tblTaxo_Num = None

listas_divididas_df_expotax = None

# ------ Variables globales ---------------------------------------------------
carpeta_seleccionada_DNO = None
resultado_label_DNO = None

"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_Danos():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_PyD()
    Hide_Dispersion()
    Hide_Calibrate()
    Hide_Perdidas()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    # ======================= Acomodar pestaña de abajo =======================
    # Acomodar pestaña mapas geograficos cuando se desglosa eventos estocasticos
    for index in Maps_Variables:
        if Maps_Var[index] is not None:
            Maps_Var[index].place_forget()
            Maps_Var[index] = None
    
    Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
    Maps_Var["Tab"].place(relx=0.544, rely=0.48, anchor=tk.CENTER)
    Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation_usl.png', 32, 32, navigation_bar,navbar_color,0.16,0.477)
    
    # acomodar visualizacion de resultados
    
    for index in Generador_Variables:
        if Generador_Var[index] is not None:
            Generador_Var[index].place_forget()
            Generador_Var[index] = None
    
    if Generador_Var["Linea"] is None: 
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.564)
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.604, anchor=tk.CENTER)
        
    if Generador_Var["Tab"] is None:
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.704, anchor=tk.CENTER)
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.701)
    
    # acomodar ficha tecnica
    
    for index in Ficha_Variables:
        if Ficha_Var[index] is not None:
            Ficha_Var[index].place_forget()
            Ficha_Var[index] = None    
    
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.804, anchor=tk.CENTER)
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.801)
        
    # acomodar reportes finalizados
    
    for index in Report_Variables:
        if Report_Var[index] is not None:
            Report_Var[index].place_forget()
            Report_Var[index] = None
    
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.904, anchor=tk.CENTER)
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.901)

    # -------------------------------------------------------------------------
    # Cuando se entra desde "Pérdidas y Daños" >> "Pérdidas"
    if Desglo_PyD_Var["PRD"] is None and Desglo_PyD_Var["DNO"] is None:
        # Despliega el menu de esa navegacion
        pyd_lib.Select_Desglo_PyD_Elements(Desglo_PyD_Var,navigation_bar,navbar_color,Show_Perdidas,Show_Danos)    
        # Cambia el boton desglo para que sea el no desglosado
        if PyD_Var["Desglo"] is not None:
            PyD_Var["Desglo"].place_forget()
            PyD_Var["Desglo"] = None
        PyD_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_UnDesglo_PyD)
    # Cuando se entra desglosando el menu >> "Pérdidas"
    if PyD_Var["Desglo"] is not None:
        PyD_Var["Desglo"].place_forget()
        PyD_Var["Desglo"] = None
    PyD_Var["Desglo"] = wnfun_lib.Button_Image('/mtl.png', 12, 10, navigation_bar,navbar_color,0.92,0.241,Select_UnDesglo_PyD)
    # Y si se oprime se debe eliminar el rectangulo que simula que se selecciono
    # Select_Desglo_PyD()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW LOSSES >>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    danos_lib.Show_Dano_Elements(DNO_title,DNO_text,DNO_boton,cnt_container,upcnt_color,Select_Folder_DNO,Ventana_Info_DNO,Function_Danos,resultado_label_DNO)
    Select_Show_Danos()

def Hide_Danos():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<< HIDE CALIBRATION <<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    danos_lib.Hide_Danos_Elements(title_DNO,DNO_title,text_DNO,DNO_text,boton_DNO,DNO_boton,canva_DNO,DNO_canva)
    Unselect_Show_Danos()

def Select_Show_Danos():
    Danos_Var["Rectng"] = wnfun_lib.Label_Image('/Select_SubMenu.png', 300, 35, navigation_bar,navbar_color,0.5,0.393)
    
    if Desglo_PyD_Var["DNO"] is not None:
        Desglo_PyD_Var["DNO"].place_forget()
        Desglo_PyD_Var["DNO"] = None
    
    Desglo_PyD_Var["DNO"] = tk.Button(navigation_bar, text="Daños", font=("Abadi MT", 14), bd=0, 
                                bg="#456883", fg="white", relief=tk.FLAT, command=Show_Danos, padx=1)
    Desglo_PyD_Var["DNO"].place(relx=0.35, rely=0.393, anchor=tk.CENTER)
    
def Unselect_Show_Danos():
    if Danos_Var["Rectng"] is not None:
        Danos_Var["Rectng"].place_forget()
        Danos_Var["Rectng"] = None
        
    if Desglo_PyD_Var["DNO"] is not None:
        Desglo_PyD_Var["DNO"].place_forget()
        Desglo_PyD_Var["DNO"] = None
        
        Desglo_PyD_Var["DNO"] = tk.Button(navigation_bar, text="Daños", font=("Abadi MT", 14), bd=0, 
                                    bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=Show_Danos, padx=20)
        Desglo_PyD_Var["DNO"].place(relx=0.35, rely=0.393, anchor=tk.CENTER)
#%% ====== TAB >> MAPAS GEOGRAFICOS ===========================================
"""
-------------------------------------------------------------------------------
Define Geographic maps variables
-------------------------------------------------------------------------------
"""
Maps_Variables = ["Tab","Label","Rectng"]
Maps_Var = {}
for var in Maps_Variables:
    Maps_Var[var] = None

# ........ Title Variables ....................................................
title_MAP = ["tlt_tlt_MAP"]
MAP_title = {}
for tlt in title_MAP:
    MAP_title[tlt] = None
# ........ Text Variables .....................................................
text_MAP = ["txt_cnt_MAP"]
MAP_text = {}
for txt in text_MAP:
    MAP_text[txt] = None
# ........ Button Variables ...................................................
boton_MAP = ["btn_slc_MAP","btn_inf_MAP","btn_clb_MAP",
             "btn_exp_MAP","btn_exp2_MAP"]
MAP_boton = {}
for btn in boton_MAP:
    MAP_boton[btn] = None

resultado_label_MAP = None
"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_MapsTAB():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_PyD()
    Hide_Perdidas()
    Hide_Danos()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    Select_UnDesglo_PyD()
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW MAPS >>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    map_lib.Show_Maps_Elements(MAP_title,MAP_text,MAP_boton,cnt_container,upcnt_color,Select_Folder_MAP,Ventana_Info_MAP,Function_Maps,resultado_label_MAP)
    Select_Show_MAP()
    
def Hide_MAP():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE MAPS <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    map_lib.Hide_Maps_Elements(title_MAP,MAP_title,text_MAP,MAP_text,boton_MAP,MAP_boton)
    Unselect_Show_MAP()    

def Select_Show_MAP():
    # .... Eliminar tab y label de MAPS ........................,..............
    for var in Maps_Variables:
        if Maps_Var[var] is not None:
            Maps_Var[var].place_forget()
            Maps_Var[var] = None
    # .... Seleccionar MAPS .................................................
    if Maps_Var["Rectng"] is None:
        Maps_Var["Rectng"] = wnfun_lib.Label_Image('/Select.png', 275, 120, 
                                    navigation_bar,cnt_color,0.535,0.340)
    if Maps_Var["Tab"] is None: 
        Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                                bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_MapsTAB, padx=5)
        Maps_Var["Tab"].place(relx=0.544, rely=0.341, anchor=tk.CENTER)
    
    if Maps_Var["Label"] is None: 
        Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation.png', 32, 32, 
                                        navigation_bar,cnt_color,0.16,0.338)
    
    # ======================= Arreglar pestana de arriba ======================
    Unselect_Show_PyD()
    # ======================= Arreglar pestana de abajo =======================
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"]  = None
    
    if Generador_Var["Linea"]  is None:
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    
    if Generador_Var["Visual"] is not None: 
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"]  = None
        
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)    

def Unselect_Show_MAP():
    # .... Eliminar tab, label y Rectng de Events .............................
    for var in Maps_Variables:
        if Maps_Var[var] is not None:
            Maps_Var[var].place_forget()
            Maps_Var[var] = None
    # .... Deseleccionar Events ...............................................
    Maps_Var["Tab"] = tk.Button(navigation_bar, text="Mapas geográficos", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_MapsTAB, padx=5)
    Maps_Var["Tab"].place(relx=0.544, rely=0.341, anchor=tk.CENTER)
    Maps_Var["Label"] = wnfun_lib.Label_Image('/geographical-navigation.png', 32, 32, navigation_bar,navbar_color,0.16,0.338)

#%% ====== TAB >> GENERADOR ===================================================
"""
-------------------------------------------------------------------------------
Define Generator variables
-------------------------------------------------------------------------------
"""
Generador_Variables = ["Tab","Label","Rectng","Linea","Visual"]
Generador_Var = {}
for var in Generador_Variables:
    Generador_Var[var] = None

# ........ Title Variables ....................................................
title_GEN = ["tlt_tlt_GEN"]
GEN_title = {}
for tlt in title_GEN:
    GEN_title[tlt] = None
# ........ Text Variables .....................................................
text_GEN = ["txt_cnt_GEN"]
GEN_text = {}
for txt in text_GEN:
    GEN_text[txt] = None
# ........ Button Variables ...................................................
boton_GEN = ["btn_slc_GEN","btn_inf_GEN","btn_clb_GEN",
             "btn_exp_GEN","btn_exp2_GEN"]
GEN_boton = {}
for btn in boton_GEN:
    GEN_boton[btn] = None

resultado_label_GEN = None

"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_Generator():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_PyD()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_FCH()
    Hide_REP()
    Hide_CNT()
    Select_UnDesglo_PyD()
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW MAPS >>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    gen_lib.Show_GEN_Elements(GEN_title,GEN_text,GEN_boton,cnt_container,upcnt_color,Select_Folder_GEN,Ventana_Info_GEN,Function_Generador,resultado_label_GEN)
    Select_Show_GEN()
    
def Hide_GEN():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE MAPS <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    gen_lib.Hide_GEN_Elements(title_GEN,GEN_title,text_GEN,GEN_text,boton_GEN,GEN_boton)
    Unselect_Show_GEN()    

def Select_Show_GEN():
    # .... Eliminar tab y label de MAPS ........................,..............
    for var in Generador_Variables:
        if Generador_Var[var] is not None:
            Generador_Var[var].place_forget()
            Generador_Var[var] = None
    # .... Seleccionar MAPS .................................................
    if Generador_Var["Rectng"] is None:
        Generador_Var["Rectng"] = wnfun_lib.Label_Image('/Select.png', 275, 120, 
                                    navigation_bar,cnt_color,0.535,0.564)
    if Generador_Var["Tab"] is None: 
        Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                                bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_Generator, padx=5)
        Generador_Var["Tab"].place(relx=0.42, rely=0.565, anchor=tk.CENTER)
    
    if Generador_Var["Label"] is None: 
        Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator_Slc.png', 30, 30, 
                                        navigation_bar,cnt_color,0.16,0.562)

    # ======================= Arreglar pestana de arriba ======================
    
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"]  = None
    
    if Generador_Var["Linea"]  is None:
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    
    if Generador_Var["Visual"] is not None: 
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"]  = None
        
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)    
    
    # ======================= Arreglar pestana de abajo =======================
    
    for var in Ficha_Variables:
        if Ficha_Var[var] is not None:
            Ficha_Var[var].place_forget()
            Ficha_Var[var] = None
    
    if Ficha_Var["Tab"] is None:
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.665, anchor=tk.CENTER)

    
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.662)
    

def Unselect_Show_GEN():
    # .... Eliminar tab, label y Rectng de Events .............................
    for var in Generador_Variables:
        if Generador_Var[var] is not None:
            Generador_Var[var].place_forget()
            Generador_Var[var] = None
    # .... Deseleccionar Events ...............................................
    Generador_Var["Tab"] = tk.Button(navigation_bar, text="Generador", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Generator, padx=5)
    Generador_Var["Tab"].place(relx=0.42, rely=0.565, anchor=tk.CENTER)
    Generador_Var["Label"] = wnfun_lib.Label_Image('/Generator.png', 30, 30, navigation_bar,navbar_color,0.16,0.562)
#%% ====== TAB >> FICHAS ======================================================
"""
-------------------------------------------------------------------------------
Define Generator variables
-------------------------------------------------------------------------------
"""
Ficha_Variables = ["Tab","Label","Rectng"]
Ficha_Var = {}
for var in Ficha_Variables:
    Ficha_Var[var] = None

# ........ Title Variables ....................................................
title_FCH = ["tlt_tlt_FCH"]
FCH_title = {}
for tlt in title_FCH:
    FCH_title[tlt] = None
# ........ Text Variables .....................................................
text_FCH = ["txt_cnt_FCH"]
FCH_text = {}
for txt in text_FCH:
    FCH_text[txt] = None
# ........ Button Variables ...................................................
boton_FCH = ["btn_slc_FCH","btn_inf_FCH","btn_clb_FCH",
             "btn_exp_FCH","btn_exp2_FCH"]
FCH_boton = {}
for btn in boton_FCH:
    FCH_boton[btn] = None

resultado_label_FCH = None

"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_FCH():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_PyD()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_REP()
    Hide_CNT()
    Select_UnDesglo_PyD()
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW FCHS >>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    fch_lib.Show_FCH_Elements(FCH_title,FCH_text,FCH_boton,cnt_container,upcnt_color,Select_Folder_FCH,Ventana_Info_FCH,Function_Ficha,resultado_label_FCH)
    Select_Show_FCH()
    
def Hide_FCH():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE FCHS <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    fch_lib.Hide_FCH_Elements(title_FCH,FCH_title,text_FCH,FCH_text,boton_FCH,FCH_boton)
    Unselect_Show_FCH()    

def Select_Show_FCH():
    # .... Eliminar tab y label de MAPS ........................,..............
    for var in Ficha_Variables:
        if Ficha_Var[var] is not None:
            Ficha_Var[var].place_forget()
            Ficha_Var[var] = None
    # .... Seleccionar MAPS .................................................
    if Ficha_Var["Rectng"] is None:
        Ficha_Var["Rectng"] = wnfun_lib.Label_Image('/Select.png', 275, 120, 
                                    navigation_bar,cnt_color,0.535,0.664)
    if Ficha_Var["Tab"] is None: 
        Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                                bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_FCH, padx=5)
        Ficha_Var["Tab"].place(relx=0.46, rely=0.665, anchor=tk.CENTER)
    
    if Ficha_Var["Label"] is None: 
        Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha_Slc.png', 30, 30, 
                                        navigation_bar,cnt_color,0.16,0.662)
    
    # ======================= Arreglar pestana de arriba ======================
    Unselect_Show_GEN()
    
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"]  = None
    
    if Generador_Var["Linea"]  is None:
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    
    if Generador_Var["Visual"] is not None: 
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"]  = None
        
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER)  
    
    # ======================= Arreglar pestana de abajo =======================
    
    for var in Report_Variables:
        if Report_Var[var] is not None:
            Report_Var[var].place_forget()
            Report_Var[var] = None
            
    if Report_Var["Tab"] is None:
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.765, anchor=tk.CENTER)
    
    
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.762)
    
def Unselect_Show_FCH():
    # .... Eliminar tab, label y Rectng de Events .............................
    for var in Ficha_Variables:
        if Ficha_Var[var] is not None:
            Ficha_Var[var].place_forget()
            Ficha_Var[var] = None
    # .... Deseleccionar Events ...............................................
    Ficha_Var["Tab"] = tk.Button(navigation_bar, text="Ficha técnica", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_FCH, padx=5)
    Ficha_Var["Tab"].place(relx=0.46, rely=0.665, anchor=tk.CENTER)
    Ficha_Var["Label"] = wnfun_lib.Label_Image('/Ficha.png', 30, 30, navigation_bar,navbar_color,0.16,0.662)
#%% ====== TAB >> REPORTES ====================================================
"""
-------------------------------------------------------------------------------
Define Generator variables
-------------------------------------------------------------------------------
"""
Report_Variables = ["Tab","Label","Rectng"]
Report_Var = {}
for var in Report_Variables:
    Report_Var[var] = None

# ........ Title Variables ....................................................
title_REP = ["tlt_tlt_REP"]
REP_title = {}
for tlt in title_REP:
    REP_title[tlt] = None
# ........ Text Variables .....................................................
text_REP = ["txt_cnt_REP"]
REP_text = {}
for txt in text_REP:
    REP_text[txt] = None
# ........ Button Variables ...................................................
boton_REP = ["btn_slc_REP","btn_inf_REP","btn_clb_REP"]
REP_boton = {}
for btn in boton_REP:
    REP_boton[btn] = None

resultado_label_REP = None

"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_REP():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_PyD()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_CNT()
    Select_UnDesglo_PyD()
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW MAPS >>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    rep_lib.Show_REP_Elements(FCH_title,FCH_text,FCH_boton,cnt_container,upcnt_color)
    Select_Show_REP()
    
def Hide_REP():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE MAPS <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    # rep_lib.Hide_Maps_Elements(title_MAP,MAP_title,text_MAP,MAP_text,boton_MAP,MAP_boton)
    Unselect_Show_REP()    

def Select_Show_REP():
    # .... Eliminar tab y label de MAPS ........................,..............
    for var in Report_Variables:
        if Report_Var[var] is not None:
            Report_Var[var].place_forget()
            Report_Var[var] = None
    # .... Seleccionar MAPS .................................................
    if Report_Var["Rectng"] is None:
        Report_Var["Rectng"] = wnfun_lib.Label_Image('/Select.png', 275, 120, 
                                    navigation_bar,cnt_color,0.535,0.764)
    if Report_Var["Tab"] is None: 
        Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                                bg=cnt_color, fg=navbar_color, relief=tk.FLAT, command=Show_REP, padx=5)
        Report_Var["Tab"].place(relx=0.57, rely=0.765, anchor=tk.CENTER)
    
    if Report_Var["Label"] is None: 
        Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte_Slc.png', 30, 30, 
                                        navigation_bar,cnt_color,0.16,0.762)
    
    # ======================= Arreglar pestana de arriba ======================
    Unselect_Show_FCH()
    
    if Generador_Var["Linea"] is not None: 
        Generador_Var["Linea"].place_forget()
        Generador_Var["Linea"]  = None
    
    if Generador_Var["Linea"]  is None:
        Generador_Var["Linea"] = wnfun_lib.Label_Image('/Frame_Results.png', 
                                220, 2, navigation_bar,navbar_color,0.5,0.425)
    
    if Generador_Var["Visual"] is not None: 
        Generador_Var["Visual"].place_forget()
        Generador_Var["Visual"]  = None
        
    if Generador_Var["Visual"] is None:
        Generador_Var["Visual"] = tk.Button(navigation_bar, text="Visualización de resultados", font=("Abadi MT", 14), bd=0, 
                        bg=navbar_color, fg="white", relief=tk.FLAT, command=nada, padx=5)
        Generador_Var["Visual"].place(relx=0.5, rely=0.465, anchor=tk.CENTER) 
    

def Unselect_Show_REP():
    # .... Eliminar tab, label y Rectng de Events .............................
    for var in Report_Variables:
        if Report_Var[var] is not None:
            Report_Var[var].place_forget()
            Report_Var[var] = None
    # .... Deseleccionar Events ...............................................
    Report_Var["Tab"] = tk.Button(navigation_bar, text="Reportes finalizados", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_REP, padx=5)
    Report_Var["Tab"].place(relx=0.57, rely=0.765, anchor=tk.CENTER)
    Report_Var["Label"] = wnfun_lib.Label_Image('/Reporte.png', 30, 30, navigation_bar,navbar_color,0.16,0.762)
#%% ====== TAB >> NOSOTROS ====================================================
"""
-------------------------------------------------------------------------------
Define Generator variables
-------------------------------------------------------------------------------
"""
Nosotros_Variables = ["Tab","Label"]
Nosotros_Var = {}
for var in Nosotros_Variables:
    Nosotros_Var[var] = None

# ........ Title Variables ....................................................
title_NOS = ["tlt_tlt_GEN"]
NOS_title = {}
for tlt in title_NOS:
    NOS_title[tlt] = None
# ........ Text Variables .....................................................
text_NOS = ["txt_cnt_GEN"]
NOS_text = {}
for txt in text_NOS:
    NOS_text[txt] = None
# ........ Button Variables ...................................................
boton_NOS = ["btn_slc_GEN","btn_inf_GEN","btn_clb_GEN"]
boton_NOS = {}
for btn in boton_NOS:
    boton_NOS[btn] = None

resultado_label_NOS = None

"""
-------------------------------------------------------------------------------
Functions for displaying OR hide content in other tabs
-------------------------------------------------------------------------------
"""
def Show_CNT():
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    Hide_Home()
    Hide_Events()
    Hide_Calibrate()
    Hide_Dispersion()
    Hide_PyD()
    Hide_Perdidas()
    Hide_Danos()
    Hide_MAP()
    Hide_GEN()
    Hide_FCH()
    Hide_REP()
    Select_UnDesglo_PyD()
    Select_UnDesglo_Events()
    # -------------------------------------------------------------------------
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>> SHOW MAPS >>>>>>>>>>>>>>>>')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # map_lib.Show_Maps_Elements(MAP_title,MAP_text,MAP_boton,cnt_container,upcnt_color,nada,nada,nada,resultado_label_MAP)
    
def Hide_CNT():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<< HIDE MAPS <<<<<<<<<<<<<<<')
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    # map_lib.Hide_Maps_Elements(title_MAP,MAP_title,text_MAP,MAP_text,boton_MAP,MAP_boton)

#%% ====== ELEMENTS >> CALIBRAR EVENTOS ESTOCASTICOS ==========================
""" ---------------------------------------------------------------------------
                            Variables globales
--------------------------------------------------------------------------- """

CP_Name = None
datos_CP = None
datos_MNZ = None
Mnz_Predeter = None
opciones_mnz = None
codigo_mnz = None
simmnz_losses = None
simmnz_losses2 = None
newNsim_mnz = None
Nevents = None
Txn_Predeter = None
datos_TXN = None
opciones_txn = None
codigo_txn = None
simtxn_losses = None
simtxn_losses2 = None
newNsim_txn = None

""" ---------------------------------------------------------------------------
--------------------------------------------------------------------------- """

def Function_Calibrate(resultado_label):
    if carpeta_seleccionada is not None:
        global CP_Name,datos_CP,datos_MNZ,Mnz_Predeter,opciones_mnz,codigo_mnz,simmnz_losses,simmnz_losses2,newNsim_mnz,Nevents,Txn_Predeter,datos_TXN,opciones_txn,codigo_txn,simtxn_losses,simtxn_losses2,newNsim_txn
        CP_Name,datos_CP,datos_MNZ,Mnz_Predeter,opciones_mnz,codigo_mnz,simmnz_losses,simmnz_losses2,newNsim_mnz,Nevents,Txn_Predeter,datos_TXN,opciones_txn,codigo_txn,simtxn_losses,simtxn_losses2,newNsim_txn = calibration_lib.Function_Calibrate_Elements(carpeta_seleccionada)
        if CP_Name is None:
            tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
        else:
            # ---- Preparar escenario -----------------------------------------
            # ---- Eliminar titulos -------------------------------------------
            for tlt in title_CLB:
                if CLB_title[tlt] is not None:
                    CLB_title[tlt].place_forget()
                    CLB_title[tlt] = None
            # ---- Eliminar descripcion informativa:
            for txt in text_CLB:
                if CLB_text[txt] is not None:
                    CLB_text[txt].place_forget()
                    CLB_text[txt] = None
            # ---- Eliminar boton calibrar y seleccionar carpeta:
            for btn in boton_CLB:
                if CLB_boton[btn] is not None:
                    CLB_boton[btn].place_forget()
                    CLB_boton[btn] = None
            # ---- Eliminar los labels:
            for lbl in label_CLB:
                if CLB_label[lbl] is not None:
                    CLB_label[lbl].place_forget()
                    CLB_label[lbl] = None
            # ---- Eliminar los canvas:
            for cnv in canva_CLB:
                if CLB_canva[cnv] is not None:
                    CLB_canva[cnv] = None
            
            
            # ================= Volver a acomodar la interfaz =================
            # -------- Frame resultados ---------------------------------------
            if CLB_label["lbl_rst_CLB"] is None:
                CLB_label["lbl_rst_CLB"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
            # -------- Design frame -------------------------------------------
            if CLB_label["lbl_DsF_CLB"] is None:
                CLB_label["lbl_DsF_CLB"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
            
            # -------- Title Section ------------------------------------------
            if CLB_text["tlt_sct_CLB"] is None:
                CLB_text["tlt_sct_CLB"] = tk.Label(cnt_container, text="Calibración de eventos estocásticos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
                CLB_text["tlt_sct_CLB"].place(relx=0.23, rely=0.093, anchor=tk.CENTER)
            # -------- Frame Results Title ------------------------------------
            if CLB_label["lbl_rstv2_CLB"] is None:
                CLB_label["lbl_rstv2_CLB"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 1300, 36, cnt_container,"white",0.5,0.170)
            # -------- Results Title ------------------------------------------
            if CLB_text["tlt_rstv2_CLB"] is None:
                CLB_text["tlt_rstv2_CLB"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
                CLB_text["tlt_rstv2_CLB"].place(relx=0.5, rely=0.17, anchor=tk.CENTER)
            
            # -------- Select Folder ------------------------------------------
            if CLB_boton["btn_slc_CLB"] is None:
                CLB_boton["btn_slc_CLB"] = wnfun_lib.Button_Image('/Select_FolderV2.png', 230, 50, cnt_container,"#F2F2F2",0.73,0.096,Select_Folder_CLB)
            # -------- Information Button -------------------------------------
            if CLB_boton["btn_inf_CLB"] is None:
                CLB_boton["btn_inf_CLB"] = wnfun_lib.Button_Image('/Info.png', 22, 22, cnt_container,"#F2F2F2",0.82,0.084,Ventana_Info_CLB) 
            # ---- Calibrar:
            CLB_boton2["SiNo"] = ["SiNo"]
            if CLB_boton["btn_clb_CLB"] is None:
                CLB_boton["btn_clb_CLB"] = wnfun_lib.Button_Image_lambda('/Calibrate_Button.png', 144, 43, cnt_container,"#F2F2F2",0.90,0.097,Function_Calibrate,resultado_label)
            # =================================================================
            
            # -----------------------------------------------------------------
            # Se generan distintos resultados de acuerdo al caso (carpeta seleccionada)
            # -----------------------------------------------------------------
            
            # Cuando el caso es el 1: Resulatos por municipio, manzana y taxonomía
            if datos_TXN is not None and datos_MNZ is not None:
                
                # ................... GRAFICO DEL MUNICIPIO ...................
                # ---- Generar grafico centro poblado:
                if CLB_canva["cnv_cp_CLB"] is None:
                    CLB_canva["cnv_cp_CLB"] = wnfun_lib.canva_CLB(datos_CP,
                                                    cnt_container,0.27,0.635)
                # ---- Titulo del grafico:
                if CLB_text["txt_gf1_CLB"] is None:
                    if datos_CP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = "Pérdida anual promedio del municipio"
                        font_size = 14
                        
                    elif datos_CP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = "Daño estructural anual promedio el municipio"
                        font_size = 13
                        
                    CLB_text["txt_gf1_CLB"] = tk.Label(cnt_container, text=titulo_grafico, 
                            font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    CLB_text["txt_gf1_CLB"].place(relx=0.27, rely=0.31, anchor=tk.CENTER)
                # .............................................................
                
                # ................... GRAFICO DE TAXONOMIAS ...................
                if CLB_canva["cnv_txn_CLB"] is None:
                    text_title = 'Taxonomía: '+str(Txn_Predeter)
                    CLB_canva["cnv_txn_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_TXN,
                                             cnt_container,text_title,0.75,0.58)
                    CLB_canva["cnv_txn_CLB"].get_tk_widget().pack_forget()
                # .............................................................
                
                # .................. GRAFICO DE LAS MANZANAS ..................
                # ---- Generar grafico manzanas:
                if CLB_canva["cnv_mnz_CLB"] is None:
                    text_title = 'CodDANE:'+str(Mnz_Predeter[1::])
                    CLB_canva["cnv_mnz_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_MNZ,
                                            cnt_container,text_title,0.75,0.58)
                # ---- Titulo del grafico:
                if CLB_text["txt_gf2_CLB"] is None:
                    if datos_MNZ['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = "Pérdida anual promedio de la manzana"
                        font_size = 14
                    elif datos_MNZ['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = "Daño estructural anual promedio de la manzana" 
                        font_size = 13
                    CLB_text["txt_gf2_CLB"] = tk.Label(cnt_container, text=titulo_grafico, 
                            font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    CLB_text["txt_gf2_CLB"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
                
                # ---- Combo manzanas:
                if CLB_rect["rec_cmb_MNZ"] is None:
                    CLB_rect["rec_cmb_MNZ"] = wnfun_lib.Label_Image('/combo_mnz.png', 
                                            215, 38, cnt_container,"white",0.75,0.91)
                if CLB_boton["cmb_Mnz_CLB"] is None:
                    CLB_boton["cmb_Mnz_CLB"] = ttk.Combobox(CLB_rect["rec_cmb_MNZ"],
                                                            values=opciones_mnz)
                    CLB_boton["cmb_Mnz_CLB"].place(relx=0.78, rely=0.48, 
                                        anchor=tk.CENTER, width=63, height=20)
                if CLB_boton["btn_cck_CLB"] is None:  
                    imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
                    imagen = imagen.resize((28,28), Image.LANCZOS)
                    imagen = ImageTk.PhotoImage(imagen)
                    CLB_boton["btn_cck_CLB"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", 
                                        command=lambda:Change_Block(CLB_boton["cmb_Mnz_CLB"].get(),CLB_canva["cnv_mnz_CLB"]))
                    CLB_boton["btn_cck_CLB"].image = imagen
                    CLB_boton["btn_cck_CLB"].place(relx=0.86, rely=0.91, anchor=tk.CENTER)
                
                # .............................................................
                # ---- Exportar resultados:
                if CLB_boton["btn_exp_CLB"]  is None:
                    CLB_boton["btn_exp_CLB"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    210, 50, cnt_container,"white",0.10,0.94)
                if CLB_boton["btn_exp2_CLB"] is None:
                    CLB_boton["btn_exp2_CLB"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", 
                        fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Calibrar(CLB_canva["cnv_cp_CLB"], CLB_canva["cnv_mnz_CLB"], CLB_canva["cnv_txn_CLB"]))
                    CLB_boton["btn_exp2_CLB"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                # .............................................................
                
                # ---- Cambiar a resultados por taxonomia:
                if CLB_boton["btn_cbm_CLB"] is None:
                    CLB_boton["btn_cbm_CLB"] = wnfun_lib.Button_Image('/pap_taxo.png', 210, 55, cnt_container,"white",0.755,0.25,Change_To_Txn)
            
            # Cuando el caso es el 2: Resultados por municipio y taxonomía
            elif datos_MNZ is None and datos_TXN is not None:
                
                # ................... GRAFICO DEL MUNICIPIO ...................
                # ---- Generar grafico centro poblado:
                if CLB_canva["cnv_cp_CLB"] is None:
                    CLB_canva["cnv_cp_CLB"] = wnfun_lib.canva_CLB(datos_CP,
                                                    cnt_container,0.27,0.635)
                # ---- Titulo del grafico:
                if CLB_text["txt_gf1_CLB"] is None:
                    if datos_CP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = "Pérdida anual promedio del municipio"
                        font_size = 14
                    elif datos_CP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = "Daño estructural anual promedio el municipio"
                        font_size = 13
                    CLB_text["txt_gf1_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    CLB_text["txt_gf1_CLB"].place(relx=0.27, rely=0.31, anchor=tk.CENTER)
                # .............................................................
                
                # ................. GRAFICO DE LAS TAXONOMIAS .................
                # ---- Generar grafico taxonomias:
                if CLB_canva["cnv_txn_CLB"] is None:
                    text_title = 'Taxonomía: '+str(Txn_Predeter)
                    CLB_canva["cnv_txn_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_TXN,cnt_container,text_title,0.75,0.58)
                # ---- Titulo del grafico:
                if CLB_text["txt_gf2_CLB"] is None:
                    if datos_TXN['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = "Pérdida anual promedio de la taxonomía"
                        font_size = 14
                    elif datos_TXN['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = "Daño estructural anual promedio de la taxonomía" 
                        font_size = 13
                    CLB_text["txt_gf2_CLB"] = tk.Label(cnt_container, text=titulo_grafico, 
                            font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    CLB_text["txt_gf2_CLB"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
                # ---- Combo taxonomias:
                if CLB_rect["rec_cmb_MNZ"] is not None:
                    CLB_rect["rec_cmb_MNZ"].place_forget()
                    CLB_rect["rec_cmb_MNZ"] = None  
    
                if CLB_boton["cmb_Mnz_CLB"] is not None:
                    CLB_boton["cmb_Mnz_CLB"].place_forget()
                    CLB_boton["cmb_Mnz_CLB"] = None 
                
                if CLB_boton["btn_cck_CLB"] is not None:
                    CLB_boton["btn_cck_CLB"].place_forget()
                    CLB_boton["btn_cck_CLB"] = None 
                
                if CLB_rect["rec_cmb_MNZ"] is None:
                    CLB_rect["rec_cmb_MNZ"] = wnfun_lib.Label_Image('/combo_txn.png', 250, 38, cnt_container,"white",0.75,0.91)
                if CLB_boton["cmb_Mnz_CLB"] is None:
                    CLB_boton["cmb_Mnz_CLB"] = ttk.Combobox(CLB_rect["rec_cmb_MNZ"],values=opciones_txn)
                    CLB_boton["cmb_Mnz_CLB"].place(relx=0.72, rely=0.48, anchor=tk.CENTER, width=119, height=20)
                if CLB_boton["btn_cck_CLB"] is None:  
                    imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
                    imagen = imagen.resize((28,28), Image.LANCZOS)
                    imagen = ImageTk.PhotoImage(imagen)
                    CLB_boton["btn_cck_CLB"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Taxo(CLB_boton["cmb_Mnz_CLB"].get(),CLB_canva["cnv_txn_CLB"]))
                    CLB_boton["btn_cck_CLB"].image = imagen
                    CLB_boton["btn_cck_CLB"].place(relx=0.875, rely=0.91, anchor=tk.CENTER)
                
                # Grafico de manzanas no se exporta porque no existe
                CLB_canva["cnv_mnz_CLB"] = None
                
                # .............................................................
                # ---- Exportar resultados:
                if CLB_boton["btn_exp_CLB"] is None:
                    CLB_boton["btn_exp_CLB"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 210, 50, cnt_container,"white",0.10,0.94)
                if CLB_boton["btn_exp2_CLB"] is None:
                    CLB_boton["btn_exp2_CLB"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Calibrar(CLB_canva["cnv_cp_CLB"], CLB_canva["cnv_mnz_CLB"], CLB_canva["cnv_txn_CLB"]))
                    CLB_boton["btn_exp2_CLB"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                # .............................................................
            
            # Cuando el caso es el 3: Resultados por municipio y manzana
            elif datos_TXN is None and datos_MNZ is not None:
                
                # ................... GRAFICO DEL MUNICIPIO ...................
                # ---- Generar grafico centro poblado:
                if CLB_canva["cnv_cp_CLB"] is None:
                    CLB_canva["cnv_cp_CLB"] = wnfun_lib.canva_CLB(datos_CP,cnt_container,0.27,0.635)#0.687
                # ---- Titulo del grafico:
                if CLB_text["txt_gf1_CLB"] is None:
                    if datos_CP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = "Pérdida anual promedio del municipio"
                        font_size = 14
                    elif datos_CP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = "Daño estructural anual promedio el municipio"
                        font_size = 13
                    CLB_text["txt_gf1_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    CLB_text["txt_gf1_CLB"].place(relx=0.27, rely=0.31, anchor=tk.CENTER)
                # .............................................................
                
                # .................. GRAFICO DE LAS MANZANAS ..................
                # ---- Generar grafico manzanas:
                if CLB_canva["cnv_mnz_CLB"] is None:
                    text_title = 'CodDANE:'+str(Mnz_Predeter[1::])
                    CLB_canva["cnv_mnz_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_MNZ,cnt_container,text_title,0.75,0.58)#0.632
                # ---- Titulo del grafico:
                if CLB_text["txt_gf2_CLB"] is None:
                    if datos_MNZ['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = "Pérdida anual promedio de la manzana"
                        font_size = 14
                    elif datos_MNZ['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = "Daño estructural anual promedio de la manzana" 
                        font_size = 13
                    CLB_text["txt_gf2_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    CLB_text["txt_gf2_CLB"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
                
                # ---- Combo manzanas:
                if CLB_rect["rec_cmb_MNZ"] is not None:
                    CLB_rect["rec_cmb_MNZ"].place_forget()
                    CLB_rect["rec_cmb_MNZ"] = None  
                
                if CLB_boton["cmb_Mnz_CLB"] is not None:
                    CLB_boton["cmb_Mnz_CLB"].place_forget()
                    CLB_boton["cmb_Mnz_CLB"] = None 
                
                if CLB_boton["btn_cck_CLB"] is not None:
                    CLB_boton["btn_cck_CLB"].place_forget()
                    CLB_boton["btn_cck_CLB"] = None         
            
                if CLB_rect["rec_cmb_MNZ"] is None:
                    CLB_rect["rec_cmb_MNZ"] = wnfun_lib.Label_Image('/combo_mnz.png', 215, 38, cnt_container,"white",0.75,0.91)
                if CLB_boton["cmb_Mnz_CLB"] is None:
                    CLB_boton["cmb_Mnz_CLB"] = ttk.Combobox(CLB_rect["rec_cmb_MNZ"],values=opciones_mnz)
                    CLB_boton["cmb_Mnz_CLB"].place(relx=0.78, rely=0.48, anchor=tk.CENTER, width=63, height=20)
                if CLB_boton["btn_cck_CLB"] is None:  
                    imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
                    imagen = imagen.resize((28,28), Image.LANCZOS)
                    imagen = ImageTk.PhotoImage(imagen)
                    CLB_boton["btn_cck_CLB"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Block(CLB_boton["cmb_Mnz_CLB"].get(),CLB_canva["cnv_mnz_CLB"]))
                    CLB_boton["btn_cck_CLB"].image = imagen
                    CLB_boton["btn_cck_CLB"].place(relx=0.86, rely=0.91, anchor=tk.CENTER)
                    
                # Grafico de manzanas no se exporta porque no existe
                CLB_canva["cnv_txn_CLB"] = None
                
                # .............................................................
                # ---- Exportar resultados:
                if CLB_boton["btn_exp_CLB"] is None:
                    CLB_boton["btn_exp_CLB"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 210, 50, cnt_container,"white",0.10,0.94)
                if CLB_boton["btn_exp2_CLB"] is None:
                    CLB_boton["btn_exp2_CLB"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Calibrar(CLB_canva["cnv_cp_CLB"], CLB_canva["cnv_mnz_CLB"], CLB_canva["cnv_txn_CLB"]))
                    CLB_boton["btn_exp2_CLB"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                # .............................................................
               
            # Cuando el caso es el 4: Resultados del municipio
            elif datos_TXN is None and datos_MNZ is None:
                
                # ................... GRAFICO DEL MUNICIPIO ...................
                # ---- Generar grafico centro poblado:
                if CLB_canva["cnv_cp_CLB"] is None:
                    CLB_canva["cnv_cp_CLB"] = wnfun_lib.canva_CLB(datos_CP,cnt_container,0.5,0.635)#0.687
                # ---- Titulo del grafico:
                if CLB_text["txt_gf1_CLB"] is None:
                    if datos_CP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = "Pérdida anual promedio del municipio"
                        font_size = 14
                    elif datos_CP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = "Daño estructural anual promedio el municipio"
                        font_size = 13
                    CLB_text["txt_gf1_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    CLB_text["txt_gf1_CLB"].place(relx=0.5, rely=0.31, anchor=tk.CENTER)
                # .............................................................
                
                # Grafico de manzanas y taxonomias no se exportan porque no existen
                CLB_canva["cnv_txn_CLB"] = None
                CLB_canva["cnv_mnz_CLB"] = None
                
                # .............................................................
                # ---- Exportar resultados:
                if CLB_boton["btn_exp_CLB"] is None:
                    CLB_boton["btn_exp_CLB"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 210, 50, cnt_container,"white",0.10,0.94)
                if CLB_boton["btn_exp2_CLB"] is None:
                    CLB_boton["btn_exp2_CLB"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Calibrar(CLB_canva["cnv_cp_CLB"], CLB_canva["cnv_mnz_CLB"], CLB_canva["cnv_txn_CLB"]))
                    CLB_boton["btn_exp2_CLB"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                # .............................................................
               
    else:
        # Si no se encuentra la carpeta, la consola bota:
        tk.messagebox.showinfo(" ", "La carpeta no ha sido seleccionada")

#%% ====== ElEMENTS >> DISPERSION DE EVENTOS ESTOCASTICOS =====================
""" ---------------------------------------------------------------------------
                            Variables globales
--------------------------------------------------------------------------- """

CP_Name_DSP = None
datos_CP_DSP = None
datos_MNZ_DSP = None
datos_TXN_DSP = None
Mnz_Predeter_DSP = None
Txn_Predeter_DSP = None
opciones_mnz_DSP = None
opciones_txn_DSP = None
codigo_mnz_DSP = None
codigo_txn_DSP = None
simmnz_losses_DSP = None
simtxn_losses_DSP = None
newNsim_mnz_DSP = None
newNsim_txn_DSP = None
Nevents_DSP = None

""" ---------------------------------------------------------------------------
--------------------------------------------------------------------------- """

def Function_Dispersion(resultado_label_Dispersion):

    if carpeta_seleccionada_DSP is not None:

        global CP_Name_DSP,datos_CP_DSP,datos_MNZ_DSP,datos_TXN_DSP,Mnz_Predeter_DSP,Txn_Predeter_DSP,opciones_mnz_DSP,opciones_txn_DSP,codigo_mnz_DSP,codigo_txn_DSP,simmnz_losses_DSP,simtxn_losses_DSP,newNsim_mnz_DSP,newNsim_txn_DSP,Nevents_DSP
        CP_Name_DSP,datos_CP_DSP,datos_MNZ_DSP,datos_TXN_DSP,Mnz_Predeter_DSP,Txn_Predeter_DSP,opciones_mnz_DSP,opciones_txn_DSP,codigo_mnz_DSP,codigo_txn_DSP,simmnz_losses_DSP,simtxn_losses_DSP,newNsim_mnz_DSP,newNsim_txn_DSP,Nevents_DSP = dispersion_lib.Function_Dispersion_Elements(carpeta_seleccionada_DSP)
        if CP_Name_DSP is None:
            tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
        else:
            # ---- Preparar escenario -----------------------------------------
            # ---- Eliminar descripcion informativa:
                
            for tlt in title_DSP:
                if DSP_title[tlt] is not None:
                    DSP_title[tlt].place_forget()
                    DSP_title[tlt] = None
            
            for txt in text_DSP:
                if DSP_text[txt] is not None:
                    DSP_text[txt].place_forget()
                    DSP_text[txt] = None
            # ---- Eliminar boton calibrar y seleccionar carpeta:
            for btn in boton_DSP:
                if DSP_boton[btn] is not None:
                    DSP_boton[btn].place_forget()
                    DSP_boton[btn] = None
            # ---- Elimiar recuadro de nombre ---------------------------------    
            for lbl in label_DSP:
                if DSP_label[lbl] is not None:
                    DSP_label[lbl].place_forget()
                    DSP_label[lbl] = None
            # Eliminar cavas si existen ---------------------------------------
            for cnv in canva_DSP:
                if DSP_canva[cnv] is not None:
                    DSP_canva[cnv] = None
            
            # ================= Volver a acomodar la interfaz =================
            # -------- Frame resultados ---------------------------------------
            if DSP_label["lbl_rst_DSP"] is None:
                DSP_label["lbl_rst_DSP"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
            # -------- Design frame -------------------------------------------
            if DSP_label["lbl_DsF_DSP"] is None:
                DSP_label["lbl_DsF_DSP"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
            
            # -------- Title Section ------------------------------------------
            if DSP_text["tlt_sct_DSP"] is None:
                DSP_text["tlt_sct_DSP"] = tk.Label(cnt_container, text="Dispersión de eventos estocásticos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
                DSP_text["tlt_sct_DSP"].place(relx=0.23, rely=0.093, anchor=tk.CENTER)
            # -------- Frame Results Title ------------------------------------
            if DSP_label["lbl_rstv2_DSP"] is None:
                DSP_label["lbl_rstv2_DSP"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
            if DSP_label["lbl_rstv3_DSP"] is None:
                DSP_label["lbl_rstv3_DSP"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.224)
            # -------- Results Title ------------------------------------------
            if DSP_text["tlt_rstv2_DSP"] is None:
                DSP_text["tlt_rstv2_DSP"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name_DSP, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
                DSP_text["tlt_rstv2_DSP"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
             
            # -------- Select Folder ------------------------------------------
            if DSP_boton["btn_slc_DSP"]  is None:
                DSP_boton["btn_slc_DSP"]  = wnfun_lib.Button_Image('/Select_FolderV2.png', 230, 50, cnt_container,"#F2F2F2",0.73,0.096,Select_Folder_DSP)
            # -------- Information Button -------------------------------------
            if DSP_boton["btn_inf_DSP"] is None:
                DSP_boton["btn_inf_DSP"] = wnfun_lib.Button_Image('/Info.png', 22, 22, cnt_container,"#F2F2F2",0.82,0.084,Ventana_Info_DSP) 
            # ---- Calibrar:
            DSP_boton2["SiNo"] = ["SiNo"]
            if DSP_boton["btn_clb_DSP"] is None:
                DSP_boton["btn_clb_DSP"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 48, cnt_container,"#F2F2F2",0.90,0.097,Function_Dispersion,resultado_label_Dispersion)
            # =================================================================
                            
            # -----------------------------------------------------------------
            # Se generan distintos resultados de acuerdo al caso (carpeta seleccionada)
            # -----------------------------------------------------------------
            
            # Cuando el caso es el 1: Resulatos por municipio, manzana y taxonomía
            if datos_TXN_DSP is not None and datos_MNZ_DSP is not None:    
        
                # ....................... GRAFICO DEL MUNICIPIO .......................
                # ---- Generar grafico centro poblado:
                if DSP_canva["cnv_cp_DSP"] is None:
                    DSP_canva["cnv_cp_DSP"] = wnfun_lib.canva_DSP(datos_CP_DSP,cnt_container,0.27,0.635)
                # ---- Titulo del grafico:
                if DSP_text["txt_gf1_DSP"] is None:
                    
                    if datos_CP_DSP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = 'Dispersión de las pérdidas anuales promedio del municipio'
                        font_size = 13
                    elif datos_CP_DSP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = 'Dispersión de los daños estructurales anuales promedio del municipio'
                        font_size = 12
                    
                    DSP_text["txt_gf1_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    DSP_text["txt_gf1_DSP"].place(relx=0.27, rely=0.31, anchor=tk.CENTER)
                    
                
                
                # ................... GRAFICO DE TAXONOMIAS ...................
                if DSP_canva["cnv_txn_DSP"] is None:
                    text_title = 'Taxonomía: ' + str(Txn_Predeter_DSP)
                    DSP_canva["cnv_txn_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_TXN_DSP,cnt_container,text_title,0.75,0.58)
                    DSP_canva["cnv_txn_DSP"].get_tk_widget().pack_forget()
                # .............................................................
                    
                # .................. GRAFICO DE LAS MANZANAS ..................
                # ---- Generar grafico manzanas:
                if DSP_canva["cnv_mnz_DSP"] is None:
                    text_title = 'CodDANE:'+str(Mnz_Predeter_DSP[1::])
                    DSP_canva["cnv_mnz_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_MNZ_DSP,cnt_container,text_title,0.75,0.58)
                # ---- Titulo del grafico:
                if DSP_text["txt_gf2_DSP"] is None:
                    
                    if datos_MNZ_DSP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = 'Dispersión de las pérdidas anuales promedio de la manzana'
                        font_size = 13
                    elif datos_MNZ_DSP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = 'Dispersión de los daños estructurales anuales promedio de la manzana'
                        font_size = 12
                    
                    DSP_text["txt_gf2_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    DSP_text["txt_gf2_DSP"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
                    
                # ---- Combo manzanas:
                if DSP_rect["rec_cmb_DSP"] is None:
                    DSP_rect["rec_cmb_DSP"] = wnfun_lib.Label_Image('/combo_mnz.png', 215, 38, cnt_container,"white",0.75,0.91)
                if DSP_boton["cmb_Mnz_DSP"] is None:
                    DSP_boton["cmb_Mnz_DSP"] = ttk.Combobox(DSP_rect["rec_cmb_DSP"],values=opciones_mnz_DSP)
                    DSP_boton["cmb_Mnz_DSP"].place(relx=0.78, rely=0.48, anchor=tk.CENTER, width=63, height=20)
                if DSP_boton["btn_cck_DSP"] is None:  
                    imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
                    imagen = imagen.resize((28,28), Image.LANCZOS)
                    imagen = ImageTk.PhotoImage(imagen)
                    DSP_boton["btn_cck_DSP"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Block_DSP(DSP_boton["cmb_Mnz_DSP"].get(),DSP_canva["cnv_mnz_DSP"]))
                    DSP_boton["btn_cck_DSP"].image = imagen
                    DSP_boton["btn_cck_DSP"].place(relx=0.86, rely=0.91, anchor=tk.CENTER)
                    
                # .....................................................................
                # ---- Exportar resultados:
                if DSP_boton["btn_exp_DSP"] is None:
                    DSP_boton["btn_exp_DSP"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    210, 50, cnt_container,"white",0.10,0.94)
                if DSP_boton["btn_exp2_DSP"] is None:
                    DSP_boton["btn_exp2_DSP"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", 
                        fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Dispersion(DSP_canva["cnv_cp_DSP"], DSP_canva["cnv_mnz_DSP"], DSP_canva["cnv_txn_DSP"]))
                    DSP_boton["btn_exp2_DSP"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                    
                # ---- Cambiar a resultados por taxonomia:
                if DSP_boton["btn_cbm_DSP"] is None:
                    DSP_boton["btn_cbm_DSP"] = wnfun_lib.Button_Image('/pap_taxo.png', 210, 55, cnt_container,"white",0.755,0.25,Change_To_Txn_DSP)
            
            
            # Cuando el caso es el 2: Resultados por municipio y taxonomía
            elif datos_MNZ_DSP is None and datos_TXN_DSP is not None:
                
                # ....................... GRAFICO DEL MUNICIPIO .......................
                # ---- Generar grafico centro poblado:
                if DSP_canva["cnv_cp_DSP"] is None:
                    DSP_canva["cnv_cp_DSP"] = wnfun_lib.canva_DSP(datos_CP_DSP,cnt_container,0.27,0.635)
                # ---- Titulo del grafico:
                if DSP_text["txt_gf1_DSP"] is None:
                    
                    if datos_CP_DSP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = 'Dispersión de las pérdidas anuales promedio del municipio'
                        font_size = 13
                    elif datos_CP_DSP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = 'Dispersión de los daños estructurales anuales promedio del municipio'
                        font_size = 12
                    
                    DSP_text["txt_gf1_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    DSP_text["txt_gf1_DSP"].place(relx=0.27, rely=0.31, anchor=tk.CENTER)
                
                # ...................... GRAFICO DE LAS TAXONOMIAS ......................
                # .................. Generar el grafico de la taxonomia ................... 
                # ---- Generar grafico taxonomias:
                if DSP_canva["cnv_txn_DSP"] is None:
                    text_title = 'Taxonomía: '+ str(Txn_Predeter_DSP)
                    DSP_canva["cnv_txn_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_TXN_DSP,cnt_container,text_title,0.75,0.58)
                # ---- Titulo del grafico:
                if DSP_text["txt_gf2_DSP"] is None:
                    
                    if datos_CP_DSP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = 'Dispersión de las pérdidas anuales promedio de la taxonomía'
                        font_size = 13
                    elif datos_CP_DSP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = 'Dispersión de los daños estructurales anuales promedio de la taxonomía'
                        font_size = 12
                    
                    DSP_text["txt_gf2_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    DSP_text["txt_gf2_DSP"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
                    
                # ---- Combo taxonomias:
                if DSP_rect["rec_cmb_DSP"] is None:
                    DSP_rect["rec_cmb_DSP"] = wnfun_lib.Label_Image('/combo_txn.png', 250, 38, cnt_container,"white",0.75,0.91)
                if DSP_boton["cmb_Mnz_DSP"] is None:
                    DSP_boton["cmb_Mnz_DSP"] = ttk.Combobox(DSP_rect["rec_cmb_DSP"],values=opciones_txn_DSP)
                    DSP_boton["cmb_Mnz_DSP"].place(relx=0.72, rely=0.48, anchor=tk.CENTER, width=119, height=20)
                if DSP_boton["btn_cck_DSP"] is None:  
                    imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
                    imagen = imagen.resize((28,28), Image.LANCZOS)
                    imagen = ImageTk.PhotoImage(imagen)
                    DSP_boton["btn_cck_DSP"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Taxo_DSP(DSP_boton["cmb_Mnz_DSP"].get(),DSP_canva["cnv_txn_DSP"]))
                    DSP_boton["btn_cck_DSP"].image = imagen
                    DSP_boton["btn_cck_DSP"].place(relx=0.875, rely=0.91, anchor=tk.CENTER)
                
                DSP_canva["cnv_mnz_DSP"] = None
                
                # .....................................................................
                # ---- Exportar resultados:
                if DSP_boton["btn_exp_DSP"] is None:
                    DSP_boton["btn_exp_DSP"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    210, 50, cnt_container,"white",0.10,0.94)
                if DSP_boton["btn_exp2_DSP"] is None:
                    DSP_boton["btn_exp2_DSP"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", 
                        fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Dispersion(DSP_canva["cnv_cp_DSP"], DSP_canva["cnv_mnz_DSP"], DSP_canva["cnv_txn_DSP"]))
                    DSP_boton["btn_exp2_DSP"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
            
            # Cuando el caso es el 3: Resultados por municipio y manzana
            elif datos_TXN_DSP is None and datos_MNZ_DSP is not None:
                
                # ....................... GRAFICO DEL MUNICIPIO .......................
                # ---- Generar grafico centro poblado:
                if DSP_canva["cnv_cp_DSP"] is None:
                    DSP_canva["cnv_cp_DSP"] = wnfun_lib.canva_DSP(datos_CP_DSP,cnt_container,0.27,0.635)
                # ---- Titulo del grafico:
                if DSP_text["txt_gf1_DSP"] is None:
                    
                    if datos_CP_DSP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = 'Dispersión de las pérdidas anuales promedio del municipio'
                        font_size = 13
                    elif datos_CP_DSP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = 'Dispersión de los daños estructurales anuales promedio del municipio'
                        font_size = 12
                    
                    DSP_text["txt_gf1_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    DSP_text["txt_gf1_DSP"].place(relx=0.27, rely=0.31, anchor=tk.CENTER)
                    
                # ...................... GRAFICO DE LAS MANZANAS ......................
                # ---- Generar grafico manzanas:
                if DSP_canva["cnv_mnz_DSP"] is None:
                    text_title = 'CodDANE:'+str(Mnz_Predeter_DSP[1::])
                    DSP_canva["cnv_mnz_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_MNZ_DSP,cnt_container,text_title,0.75,0.58)
                # ---- Titulo del grafico:
                if DSP_text["txt_gf2_DSP"] is None:
                    
                    if datos_MNZ_DSP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = 'Dispersión de las pérdidas anuales promedio de la manzana'
                        font_size = 13
                        
                    elif datos_MNZ_DSP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = 'Dispersión de los daños estructurales anuales promedio de la manzana'
                        font_size = 12
                    
                    DSP_text["txt_gf2_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    DSP_text["txt_gf2_DSP"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
                # ---- Combo manzanas:
                if DSP_rect["rec_cmb_DSP"] is None:
                    DSP_rect["rec_cmb_DSP"] = wnfun_lib.Label_Image('/combo_mnz.png', 215, 38, cnt_container,"white",0.75,0.91)
                if DSP_boton["cmb_Mnz_DSP"] is None:
                    DSP_boton["cmb_Mnz_DSP"] = ttk.Combobox(DSP_rect["rec_cmb_DSP"],values=opciones_mnz_DSP)
                    DSP_boton["cmb_Mnz_DSP"].place(relx=0.78, rely=0.48, anchor=tk.CENTER, width=63, height=20)
                if DSP_boton["btn_cck_DSP"] is None:  
                    imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
                    imagen = imagen.resize((28,28), Image.LANCZOS)
                    imagen = ImageTk.PhotoImage(imagen)
                    DSP_boton["btn_cck_DSP"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Block_DSP(DSP_boton["cmb_Mnz_DSP"].get(),DSP_canva["cnv_mnz_DSP"]))
                    DSP_boton["btn_cck_DSP"].image = imagen
                    DSP_boton["btn_cck_DSP"].place(relx=0.86, rely=0.91, anchor=tk.CENTER)
                    
                DSP_canva["cnv_txn_DSP"]  = None
                
                # .....................................................................
                # ---- Exportar resultados:
                if DSP_boton["btn_exp_DSP"] is None:
                    DSP_boton["btn_exp_DSP"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    210, 50, cnt_container,"white",0.10,0.94)
                if DSP_boton["btn_exp2_DSP"] is None:
                    DSP_boton["btn_exp2_DSP"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", 
                        fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Dispersion(DSP_canva["cnv_cp_DSP"], DSP_canva["cnv_mnz_DSP"], DSP_canva["cnv_txn_DSP"]))
                    DSP_boton["btn_exp2_DSP"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                
            # Cuando el caso es el 4: Resultados del municipio
            elif datos_TXN_DSP is None and datos_MNZ_DSP is None:
                
                # ....................... GRAFICO DEL MUNICIPIO .......................
                # ---- Generar grafico centro poblado:
                if DSP_canva["cnv_cp_DSP"] is None:
                    DSP_canva["cnv_cp_DSP"] = wnfun_lib.canva_DSP(datos_CP_DSP,cnt_container,0.27,0.635)
                # ---- Titulo del grafico:
                if DSP_text["txt_gf1_DSP"] is None:
                    
                    if datos_CP_DSP['Event_Based'][0] == "event_based_risk":
                        titulo_grafico = 'Dispersión de las pérdidas anuales promedio del municipio'
                        font_size = 13
                    elif datos_CP_DSP['Event_Based'][0] == "event_based_damage":
                        titulo_grafico = 'Dispersión de los daños estructurales anuales promedio del municipio'
                        font_size = 12
                    
                    DSP_text["txt_gf1_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
                    DSP_text["txt_gf1_DSP"].place(relx=0.27, rely=0.31, anchor=tk.CENTER)
                
                DSP_canva["cnv_txn_DSP"]  = None
                DSP_canva["cnv_mnz_DSP"]  = None
                
                # .....................................................................
                # ---- Exportar resultados:
                if DSP_boton["btn_exp_DSP"] is None:
                    DSP_boton["btn_exp_DSP"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    210, 50, cnt_container,"white",0.10,0.94)
                if DSP_boton["btn_exp2_DSP"] is None:
                    DSP_boton["btn_exp2_DSP"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", 
                        fg="white", command=lambda:wnfun_lib.ExportarGraficos_Perdidas_Dispersion(DSP_canva["cnv_cp_DSP"], DSP_canva["cnv_mnz_DSP"], DSP_canva["cnv_txn_DSP"]))
                    DSP_boton["btn_exp2_DSP"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                
    else:
        # Si no se encuentra la carpeta, la consola bota:
        tk.messagebox.showinfo(" ", "La carpeta no ha sido seleccionada")

#%% ====== ElEMENTS >> PERDIDAS BASADAS POR EVENTOS ===========================
""" ---------------------------------------------------------------------------
                            Variables globales
--------------------------------------------------------------------------- """
df_EBR = None
valexpuesto = None
aggsts_loss = None
PE_mill = None
df_resultados = None
Pr50_Val = None
CP_Name = None
df_expotax = None
taxo_description = None
valorperiodo = None
COD_mun = None
Modelo_Expo2 = None
""" ---------------------------------------------------------------------------
--------------------------------------------------------------------------- """

Excedence_Curve = None
Table_Resu = None
Table_Resu_Txn = None
Figure_txn = None
""" ---------------------------------------------------------------------------
--------------------------------------------------------------------------- """

def Function_Perdidas(resultado_label_PRD):
    
    global valorperiodo
    valorperiodo = PRD_entry["ent_per_PRD"].get()                               # Obtener el periodo de analisis ingresado desde la plataforma
    if valorperiodo == '':
        valorperiodo = None                                                     # Cuando no hay nada, se convierte en una variable vacía
    else:
        valorperiodo = int(PRD_entry["ent_per_PRD"].get())                      # Cuando si se ingresó un periodo de análisis
    
    if Select_Folder_PRD is not None:
        
        
        global Excedence_Curve,Table_Resu,Table_Resu_Txn,Figure_txn
        
        global df_EBR, valexpuesto,aggsts_loss,PE_mill,PAE_mill,df_resultados,Pr50_Val,CP_Name,COD_mun,df_expotax,taxo_description, mapdata_mnz_PAE, mapdata_scc_PAE, manzana_shp, seccion_shp, area_shp, calculation_mode, Modelo_Expo2
        df_EBR, valexpuesto,aggsts_loss,PE_mill,PAE_mill,df_resultados,Pr50_Val,CP_Name,COD_mun,df_expotax,taxo_description, mapdata_mnz_PAE, mapdata_scc_PAE, manzana_shp, seccion_shp, area_shp, calculation_mode, Modelo_Expo2 = perdidas_lib.Function_Perdidas_Elements(carpeta_seleccionada_PRD)
        
        if calculation_mode == "Probabilistico":
        
            if df_EBR is None:
                tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
            else:
                
                # =================================================================
                #                        Preparar escenario 
                # =================================================================
                
                for tlt in title_PRD:
                    if PRD_title[tlt] is not None:
                        PRD_title[tlt].place_forget()
                        PRD_title[tlt] = None
                for txt in text_PRD:
                    if PRD_text[txt] is not None:
                        PRD_text[txt].place_forget()
                        PRD_text[txt] = None
                for btn in boton_PRD:
                    if PRD_boton[btn] is not None:
                        PRD_boton[btn].place_forget()
                        PRD_boton[btn] = None
                for lbl in entry_PRD:
                    if PRD_entry[lbl] is not None:
                        PRD_entry[lbl].place_forget()
                        PRD_entry[lbl] = None
                for rct in rectg_PRD:
                    if PRD_rectg[rct] is not None:
                        PRD_rectg[rct].place_forget()
                        PRD_rectg[rct] = None
                for cnv in canva_PRD:
                    if PRD_canva[cnv] is not None:
                        PRD_canva[cnv].get_tk_widget().destroy()
                        PRD_canva[cnv] = None
                
                # =================================================================
                #                     Volver a acomodar botones
                # =================================================================
                
                # -------- Frame resultados ---------------------------------------
                if PRD_label["lbl_rst_PRD"] is None:
                    PRD_label["lbl_rst_PRD"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
                # -------- Design frame -------------------------------------------
                if PRD_label["lbl_DsF_PRD"] is None:
                    PRD_label["lbl_DsF_PRD"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
                
                # -------- Title Section ------------------------------------------
                if PRD_text["tlt_sct_PRD"] is None:
                    PRD_text["tlt_sct_PRD"] = tk.Label(cnt_container, text="Resultados de Riesgo Basado en Eventos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
                    PRD_text["tlt_sct_PRD"].place(relx=0.25, rely=0.072, anchor=tk.CENTER)
                if PRD_text["tlt_sct_PRD1"] is None:
                    if calculation_mode == "Probabilistico":
                        PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos probabilísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
                        PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
                    else:
                        PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos determinísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
                        PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
                # -------- Frame Results Title ------------------------------------
                if PRD_label["lbl_rstv2_PRD"] is None:
                    PRD_label["lbl_rstv2_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
                if PRD_label["lbl_rstv3_PRD"] is None:
                    PRD_label["lbl_rstv3_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.250)
                if PRD_label["lbl_rstv4_PRD"] is None:
                    PRD_label["lbl_rstv4_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 38, 30, cnt_container,"white",0.025,0.22)
                # -------- Results Title ------------------------------------------
                if PRD_text["tlt_rstv2_PRD"] is None:
                    PRD_text["tlt_rstv2_CLB"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
                    PRD_text["tlt_rstv2_CLB"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
                
                # ---- Ingresar periodo de analisis:
                if PRD_boton["btn_ing_PRD"] is None:
                    PRD_boton["btn_ing_PRD"] = wnfun_lib.Label_Image('/Ingresar_Periodo.png', 240, 47, cnt_container,"#F2F2F2",0.72,0.108)
                # -------- Select Folder ------------------------------------------
                if PRD_boton["btn_slc_PRD"]  is None:
                    PRD_boton["btn_slc_PRD"]  = wnfun_lib.Button_Image('/Select_FolderV2.png', 175, 41, cnt_container,"#F2F2F2",0.74,0.068,Select_Folder_PRD)
                # -------- Information Button -------------------------------------
                if PRD_boton["btn_inf_PRD"] is None:
                    PRD_boton["btn_inf_PRD"] = wnfun_lib.Button_Image('/Info.png', 19, 19, cnt_container,"#F2F2F2",0.81,0.055,Ventana_Info_PRD) 
                # ---- Ingresar numero
                if PRD_rectg["rec_per_PRD"] is None:
                    PRD_rectg["rec_per_PRD"] = tk.Canvas(cnt_container, bg="#F2F2F2", bd=0, highlightthickness=0)
                    PRD_rectg["rec_per_PRD"].place(relx=0.825, rely=0.1, anchor=tk.CENTER, width=55, height=28)
                    x2, y2 = 54, 27
                    x1, y1 = 10,10
                    radio_esquinas = 5
                    color = "#D0CECE"
                    wnfun_lib.rec_redond(PRD_rectg["rec_per_PRD"], x1, y1, x2, y2, radio_esquinas, color)
                if PRD_entry["ent_per_PRD"] is None:
                    PRD_entry["ent_per_PRD"] = tk.Entry(PRD_rectg["rec_per_PRD"], bg = "#D0CECE", bd=0, highlightthickness=0)
                    PRD_entry["ent_per_PRD"].place(relx=0.55, rely=0.63, anchor=tk.CENTER, width=30, height=15)
                # ---- Calibrar:
                PRD_boton2["SiNo"] = ["SiNo"]
                if PRD_boton["btn_clb_PRD"] is None:
                    PRD_boton["btn_clb_PRD"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 48, cnt_container,"#F2F2F2",0.92,0.097,Function_Perdidas,resultado_label_PRD)
    
    
                # =================================================================
                #                     Acomodar primera pagina
                # =================================================================            
    
                # ...................... CURVA DE EXCEDENCIA ......................
                PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_crv_EBR(df_EBR, valexpuesto, valorperiodo,cnt_container,0.27,0.60)
                # ---- Titulo del grafico:
                PRD_text["txt_gf1_PRD"] = tk.Label(cnt_container, text="Curva de excedencia - Pérdida anual esperada", font=("Abadi MT", 15, "bold"), bg="white", fg="#3B3838")
                PRD_text["txt_gf1_PRD"].place(relx=0.3, rely=0.31, anchor=tk.CENTER)
                
                # ---- Tabla resumen PAE:
                if PRD_boton["lbl_tbl_PRD"] is None:
                    PRD_boton["lbl_tbl_PRD"] = wnfun_lib.Label_Image('/Tabla_PAE.png', 520, 420, cnt_container,"white",0.73,0.57)
                # # ---- Colocar resultados en la tabla de resumen PAE:
                # # Valor expuesto:
                texto_ValorExpuesto = np.around(df_resultados.Col2[0]*1e6,2)     
                PRD_text["txt_vlx_PRD1"] = tk.Label(cnt_container, text=str(texto_ValorExpuesto), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD1"].place(relx=0.87, rely=0.308, anchor=tk.CENTER)
                # Perdida anual esperada en COP
                texto_PAE_Cop = np.around(df_resultados.Col2[1],2)             
                PRD_text["txt_vlx_PRD2"] = tk.Label(cnt_container, text=str(texto_PAE_Cop), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD2"].place(relx=0.87, rely=0.355, anchor=tk.CENTER)
                # Perdida anual esperada en porcentaje por mil
                texto_PAE_Prc = np.around(df_resultados.Col2[2],3)            
                PRD_text["txt_vlx_PRD3"] = tk.Label(cnt_container, text=str(texto_PAE_Prc), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD3"].place(relx=0.87, rely=0.405, anchor=tk.CENTER)
                # Periodo de retorno [31]
                PRD_text["txt_vlx_PRD4"] = tk.Label(cnt_container, text='31', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD4"].place(relx=0.57, rely=0.635, anchor=tk.CENTER)
                texto_PE50_31 = np.around(Pr50_Val[0],1)                            # Probabilidad de excedencia en 50 años [31]
                PRD_text["txt_vlx_PRD5"] = tk.Label(cnt_container, text=str(texto_PE50_31), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD5"].place(relx=0.702, rely=0.635, anchor=tk.CENTER)
                texto_PE_COP_31 = np.around(PE_mill[0],1)                           # Perdida esperada en COP [31]
                PRD_text["txt_vlx_PRD6"] = tk.Label(cnt_container, text=str(texto_PE_COP_31), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD6"].place(relx=0.83, rely=0.635, anchor=tk.CENTER)
                texto_PE_31 = np.around((PE_mill[0]/(df_resultados.Col2[0]*1e6))*100,1) # Perdida esperada en % [31]
                PRD_text["txt_vlx_PRD7"] = tk.Label(cnt_container, text=str(texto_PE_31), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD7"].place(relx=0.917, rely=0.635, anchor=tk.CENTER)
                # Periodo de retorno [225]
                PRD_text["txt_vlx_PRD8"] = tk.Label(cnt_container, text='225', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD8"].place(relx=0.57, rely=0.684, anchor=tk.CENTER)
                texto_PE50_225 = np.around(Pr50_Val[1],1)                           # Probabilidad de excedencia en 50 años [225]
                PRD_text["txt_vlx_PRD9"] = tk.Label(cnt_container, text=str(texto_PE50_225), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD9"].place(relx=0.702, rely=0.684, anchor=tk.CENTER)
                texto_PE_COP_225 = np.around(PE_mill[1],1)                          # Perdida esperada en COP [225]
                PRD_text["txt_vlx_PRD10"] = tk.Label(cnt_container, text=str(texto_PE_COP_225), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD10"].place(relx=0.83, rely=0.684, anchor=tk.CENTER)
                texto_PE_225 = np.around((PE_mill[1]/(df_resultados.Col2[0]*1e6))*100,1)  # Perdida esperada en % [225]
                PRD_text["txt_vlx_PRD11"] = tk.Label(cnt_container, text=str(texto_PE_225), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD11"].place(relx=0.917, rely=0.684, anchor=tk.CENTER)
                # Periodo de retorno [475]
                PRD_text["txt_vlx_PRD12"] = tk.Label(cnt_container, text='475', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD12"].place(relx=0.57, rely=0.733, anchor=tk.CENTER)
                texto_PE50_475 = np.around(Pr50_Val[2],1)                           # Probabilidad de excedencia en 50 años [475]
                PRD_text["txt_vlx_PRD13"] = tk.Label(cnt_container, text=str(texto_PE50_475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD13"].place(relx=0.702, rely=0.733, anchor=tk.CENTER)
                texto_PE_COP_475 = np.around(PE_mill[2],1)                          # Perdida esperada en COP [475]
                PRD_text["txt_vlx_PRD14"] = tk.Label(cnt_container, text=str(texto_PE_COP_475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD14"].place(relx=0.83, rely=0.733, anchor=tk.CENTER)
                texto_PE_475 = np.around((PE_mill[2]/(df_resultados.Col2[0]*1e6))*100,1) # Perdida esperada en % [475]
                PRD_text["txt_vlx_PRD15"] = tk.Label(cnt_container, text=str(texto_PE_475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD15"].place(relx=0.917, rely=0.733, anchor=tk.CENTER)
                # Periodo de retorno [975]
                PRD_text["txt_vlx_PRD16"] = tk.Label(cnt_container, text='975', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD16"].place(relx=0.57, rely=0.782, anchor=tk.CENTER)
                texto_PE50_975 = np.around(Pr50_Val[3],1)                           # Probabilidad de excedencia en 50 años [975]
                PRD_text["txt_vlx_PRD17"] = tk.Label(cnt_container, text=str(texto_PE50_975), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD17"].place(relx=0.702, rely=0.782, anchor=tk.CENTER)
                texto_PE_COP_975 = np.around(PE_mill[3],1)                          # Perdida esperada en COP [975]
                PRD_text["txt_vlx_PRD18"] = tk.Label(cnt_container, text=str(texto_PE_COP_975), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD18"].place(relx=0.83, rely=0.782, anchor=tk.CENTER)
                texto_PE_975 = np.around((PE_mill[3]/(df_resultados.Col2[0]*1e6))*100,1) # Perdida esperada en % [975]
                PRD_text["txt_vlx_PRD19"] = tk.Label(cnt_container, text=str(texto_PE_975), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD19"].place(relx=0.917, rely=0.782, anchor=tk.CENTER)
                # Periodo de retorno [1475]
                PRD_text["txt_vlx_PRD20"] = tk.Label(cnt_container, text='1475', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD20"].place(relx=0.57, rely=0.831, anchor=tk.CENTER)
                texto_PE50_1475 = np.around(Pr50_Val[4],1)                          # Probabilidad de excedencia en 50 años [1475]
                PRD_text["txt_vlx_PRD21"] = tk.Label(cnt_container, text=str(texto_PE50_1475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD21"].place(relx=0.702, rely=0.831, anchor=tk.CENTER)
                texto_PE_COP_1475 = np.around(PE_mill[4],1)                         # Perdida esperada en COP [1475]
                PRD_text["txt_vlx_PRD22"] = tk.Label(cnt_container, text=str(texto_PE_COP_1475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD22"].place(relx=0.83, rely=0.831, anchor=tk.CENTER)
                texto_PE_1475 = np.around((PE_mill[4]/(df_resultados.Col2[0]*1e6))*100,1)
                PRD_text["txt_vlx_PRD23"] = tk.Label(cnt_container, text=str(texto_PE_1475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
                PRD_text["txt_vlx_PRD23"].place(relx=0.917, rely=0.831, anchor=tk.CENTER)
                
                # ---- Cambiar a resultados por taxonomia:
                PRD_boton["btn_cbm_PRD"] = wnfun_lib.Button_Image('/GoTo_PAETxn.png', 250, 50, cnt_container,"white",0.84,0.94,Change_To_PAETxn)
                
                # .....................................................................
                # ---- Exportar resultados:
                if PRD_boton["btn_exp_PRD"] is None:
                    PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    210, 50, cnt_container,"white",0.10,0.94)
                    
                # .................................................................
                #            GENERAR TODOS LOS RESULTADOS PARA EXPORTAR 
                #               Todos los resultados menos los mapas
                # .................................................................
                # Tabla de resumen del muncipio PAE
                Table_Resu = wnfun_lib.Gen_Tabla_Resume_PRD(texto_ValorExpuesto,PAE_mill,PE_mill)
                # Tabla de resumen por taxonomia PAE
                Table_Resu_Txn = wnfun_lib.Gen_Tabla_taxonomia_PRD(df_expotax)
                # Diagrama PAE por taxonomia
                Figure_txn = wnfun_lib.Diagrama_Taxonomia_PRD(df_expotax)
                # Curva de excedencia 
                Excedence_Curve = PRD_canva["cnv_cv_PRD"]        
                # .................................................................
                
                if PRD_boton["btn_exp2_PRD"] is None:
                    PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarResultados_Event_Based_Risk(Excedence_Curve,Table_Resu,Table_Resu_Txn,Figure_txn))
                    PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                    
        if calculation_mode == "Deterministico":
            
            if df_EBR is None:
                tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
            else:
                
                # =================================================================
                #                        Preparar escenario 
                # =================================================================
                
                for tlt in title_PRD:
                    if PRD_title[tlt] is not None:
                        PRD_title[tlt].place_forget()
                        PRD_title[tlt] = None
                for txt in text_PRD:
                    if PRD_text[txt] is not None:
                        PRD_text[txt].place_forget()
                        PRD_text[txt] = None
                for btn in boton_PRD:
                    if PRD_boton[btn] is not None:
                        PRD_boton[btn].place_forget()
                        PRD_boton[btn] = None
                for lbl in entry_PRD:
                    if PRD_entry[lbl] is not None:
                        PRD_entry[lbl].place_forget()
                        PRD_entry[lbl] = None
                for rct in rectg_PRD:
                    if PRD_rectg[rct] is not None:
                        PRD_rectg[rct].place_forget()
                        PRD_rectg[rct] = None
                for cnv in canva_PRD:
                    if PRD_canva[cnv] is not None:
                        PRD_canva[cnv].get_tk_widget().destroy()
                        PRD_canva[cnv] = None
                    
                # =================================================================
                #                     Volver a acomodar botones
                # =================================================================
                
                # -------- Frame resultados ---------------------------------------
                if PRD_label["lbl_rst_PRD"] is None:
                    PRD_label["lbl_rst_PRD"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
                # -------- Design frame -------------------------------------------
                if PRD_label["lbl_DsF_PRD"] is None:
                    PRD_label["lbl_DsF_PRD"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
                
                # -------- Title Section ------------------------------------------
                if PRD_text["tlt_sct_PRD"] is None:
                    PRD_text["tlt_sct_PRD"] = tk.Label(cnt_container, text="Resultados de Riesgo Basado en Eventos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
                    PRD_text["tlt_sct_PRD"].place(relx=0.25, rely=0.072, anchor=tk.CENTER)
                if PRD_text["tlt_sct_PRD1"] is None:
                    if calculation_mode == "Probabilistico":
                        PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos probabilísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
                        PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
                    else:
                        PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos determinísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
                        PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
                # -------- Frame Results Title ------------------------------------
                if PRD_label["lbl_rstv2_PRD"] is None:
                    PRD_label["lbl_rstv2_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
                if PRD_label["lbl_rstv3_PRD"] is None:
                    PRD_label["lbl_rstv3_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.250)
                if PRD_label["lbl_rstv4_PRD"] is None:
                    PRD_label["lbl_rstv4_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 38, 30, cnt_container,"white",0.025,0.22)
                # -------- Results Title ------------------------------------------
                if PRD_text["tlt_rstv2_PRD"] is None:
                    PRD_text["tlt_rstv2_CLB"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
                    PRD_text["tlt_rstv2_CLB"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
                
                # ---- Ingresar periodo de analisis:
                if PRD_boton["btn_ing_PRD"] is None:
                    PRD_boton["btn_ing_PRD"] = wnfun_lib.Label_Image('/Ingresar_Periodo.png', 240, 47, cnt_container,"#F2F2F2",0.72,0.108)
                # -------- Select Folder ------------------------------------------
                if PRD_boton["btn_slc_PRD"]  is None:
                    PRD_boton["btn_slc_PRD"]  = wnfun_lib.Button_Image('/Select_FolderV2.png', 175, 41, cnt_container,"#F2F2F2",0.74,0.068,Select_Folder_PRD)
                # -------- Information Button -------------------------------------
                if PRD_boton["btn_inf_PRD"] is None:
                    PRD_boton["btn_inf_PRD"] = wnfun_lib.Button_Image('/Info.png', 19, 19, cnt_container,"#F2F2F2",0.81,0.055,Ventana_Info_PRD) 
                # ---- Ingresar numero
                if PRD_rectg["rec_per_PRD"] is None:
                    PRD_rectg["rec_per_PRD"] = tk.Canvas(cnt_container, bg="#F2F2F2", bd=0, highlightthickness=0)
                    PRD_rectg["rec_per_PRD"].place(relx=0.825, rely=0.1, anchor=tk.CENTER, width=55, height=28)
                    x2, y2 = 54, 27
                    x1, y1 = 10,10
                    radio_esquinas = 5
                    color = "#D0CECE"
                    wnfun_lib.rec_redond(PRD_rectg["rec_per_PRD"], x1, y1, x2, y2, radio_esquinas, color)
                if PRD_entry["ent_per_PRD"] is None:
                    PRD_entry["ent_per_PRD"] = tk.Entry(PRD_rectg["rec_per_PRD"], bg = "#D0CECE", bd=0, highlightthickness=0)
                    PRD_entry["ent_per_PRD"].place(relx=0.55, rely=0.63, anchor=tk.CENTER, width=30, height=15)
                # ---- Calibrar:
                PRD_boton2["SiNo"] = ["SiNo"]
                if PRD_boton["btn_clb_PRD"] is None:
                    PRD_boton["btn_clb_PRD"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 48, cnt_container,"#F2F2F2",0.92,0.097,Function_Perdidas,resultado_label_PRD)
                    
                # =============================================================
                #                     Acomodar primera pagina
                # =============================================================
                
                # ---- Tabla PE municipio:
                if PRD_boton["lbl_tbl_PRD"] is None:
                    PRD_boton["lbl_tbl_PRD"] = wnfun_lib.Label_Image('/Tabla_PE_CP.png', 520, 420, cnt_container,"white",0.73,0.57)

    else:
        # Si no se encuentra la carpeta, la consola bota:
        tk.messagebox.showinfo(" ", "El archivo no fue seleccionado correctamente")
#%% ====== ElEMENTS >> DANOS BASADOS EN EVENTOS ===============================

""" ---------------------------------------------------------------------------
                            Variables globales
--------------------------------------------------------------------------- """
Num_build = None
aggrisk_resu = None
df_expotax_DNO = None
taxonomias = None
aggrisk_mnz_DNO = None
mapdata_fatalities = None
mapdata_injured = None
mapdata_homeless = None
mapdata_collapsed = None
manzana_shp_DNO = None
seccion_shp_DNO = None
area_shp_DNO = None
calculation_mode_DNO = None
Modelo_Expo2_DNO = None
CP_Name_DNO = None
COD_mun_DNO = None
tipo_calculo = None
mapdata_fatalities_scc = None
mapdata_homeless_scc = None
mapdata_injured_scc = None
mapdata_collapsed_scc = None
""" ---------------------------------------------------------------------------
--------------------------------------------------------------------------- """

def Function_Danos(resultado_label_DNO):
    
    if Select_Folder_DNO is not None:
                
        global Num_build,aggrisk_resu,df_expotax_DNO,taxonomias,aggrisk_mnz_DNO,mapdata_fatalities,mapdata_injured,mapdata_homeless,mapdata_collapsed,manzana_shp_DNO,seccion_shp_DNO,area_shp_DNO, calculation_mode_DNO, Modelo_Expo2_DNO, CP_Name_DNO, COD_mun_DNO, mapdata_fatalities_scc, mapdata_homeless_scc, mapdata_injured_scc, mapdata_collapsed_scc
        Num_build,aggrisk_resu,df_expotax_DNO,taxonomias,aggrisk_mnz_DNO,mapdata_fatalities,mapdata_injured,mapdata_homeless,mapdata_collapsed,manzana_shp_DNO,seccion_shp_DNO,area_shp_DNO, calculation_mode_DNO, Modelo_Expo2_DNO, CP_Name_DNO, COD_mun_DNO, mapdata_fatalities_scc, mapdata_homeless_scc, mapdata_injured_scc, mapdata_collapsed_scc = danos_lib.Function_Danos_Elements(carpeta_seleccionada_DNO)
        
        if calculation_mode_DNO == "Probabilistico":
        
            if Num_build is None:
                tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
            else:
                
                # =================================================================
                #                        Preparar escenario 
                # =================================================================
                
                for tlt in title_DNO:
                    if DNO_title[tlt] is not None:
                        DNO_title[tlt].place_forget()
                        DNO_title[tlt] = None
                        
                for txt in text_DNO:
                    if DNO_text[txt] is not None:
                        DNO_text[txt].place_forget()
                        DNO_text[txt] = None
                        
                for btn in boton_DNO:
                    if DNO_boton[btn] is not None:
                        DNO_boton[btn].place_forget()
                        DNO_boton[btn] = None
                        
                for cnv in canva_DNO:
                    if DNO_canva[cnv] is not None:
                        DNO_canva[cnv].get_tk_widget().destroy()
                        DNO_canva[cnv] = None
                
                # =================================================================
                #                     Volver a acomodar botones
                # =================================================================
                
                # -------- Frame resultados ---------------------------------------
                if DNO_boton["lbl_rst_DNO"] is None:
                    DNO_boton["lbl_rst_DNO"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
                # -------- Design frame -------------------------------------------
                if DNO_boton["lbl_DsF_DNO"] is None:
                    DNO_boton["lbl_DsF_DNO"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
                
                # -------- Title Section ------------------------------------------
                if DNO_text["tlt_sct_DNO"] is None:
                    DNO_text["tlt_sct_DNO"] = tk.Label(cnt_container, text="Resultados de Daño Basado en Eventos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
                    DNO_text["tlt_sct_DNO"].place(relx=0.243, rely=0.072, anchor=tk.CENTER)
                if DNO_text["tlt_sct_DNO1"] is None:
                    if calculation_mode_DNO == "Probabilistico":
                        DNO_text["tlt_sct_DNO1"] = tk.Label(cnt_container, text="Eventos probabilísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
                        DNO_text["tlt_sct_DNO1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
                    else:
                        DNO_text["tlt_sct_DNO1"] = tk.Label(cnt_container, text="Eventos determinísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
                        DNO_text["tlt_sct_DNO1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
                # -------- Frame Results Title ------------------------------------
                if DNO_boton["lbl_rstv2_DNO"] is None:
                    DNO_boton["lbl_rstv2_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
                if DNO_boton["lbl_rstv3_DNO"] is None:
                    DNO_boton["lbl_rstv3_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.304)
                if DNO_boton["lbl_rstv4_DNO"] is None:
                    DNO_boton["lbl_rstv4_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 38, 58, cnt_container,"white",0.025,0.24)
                # -------- Results Title ------------------------------------------
                if DNO_text["tlt_rstv2_DNO"] is None:
                    DNO_text["tlt_rstv2_DNO"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name_DNO, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
                    DNO_text["tlt_rstv2_DNO"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
                
                # -------- Select Folder ------------------------------------------
                if DNO_boton["btn_slc_DNO"]  is None:
                    DNO_boton["btn_slc_DNO"]  = wnfun_lib.Button_Image('/Select_FolderV2.png', 175, 41, cnt_container,"#F2F2F2",0.74,0.094,Select_Folder_DNO)
                # -------- Information Button -------------------------------------
                if DNO_boton["btn_inf_DNO"] is None:
                    DNO_boton["btn_inf_DNO"] = wnfun_lib.Button_Image('/Info.png', 19, 19, cnt_container,"#F2F2F2",0.81,0.087,Ventana_Info_DNO) 
                
                # ---- Calibrar:
                DNO_boton2["SiNo"] = ["SiNo"]
                if DNO_boton["btn_clb_DNO"] is None:
                    DNO_boton["btn_clb_DNO"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 48, cnt_container,"#F2F2F2",0.90,0.097,Function_Danos,resultado_label_DNO)
                    
                # =============================================================
                #                     Acomodar primera pagina
                # =============================================================            
                
                # ------------ Llenar tabla resumen municipio -----------------
                
                if DNO_boton["tbl_CP_DNO"]  is None:
                    DNO_boton["tbl_CP_DNO"]  = wnfun_lib.Label_Image('/Tabla_Dano_CP.png', 583, 450, cnt_container,"white",0.35,0.57)
                
                if DNO_text["txt_tbl1_DNO"] is None:
                    DNO_text["txt_tbl1_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(Num_build,0), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl1_DNO"].place(relx=0.835, rely=0.046, anchor=tk.CENTER)
                    
                if DNO_text["txt_tbl2_DNO"] is None:
                    DNO_text["txt_tbl2_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[0],0), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl2_DNO"].place(relx=0.58, rely=0.384, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl22_DNO"] is None:
                    DNO_text["txt_tbl22_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[0]/np.sum(aggrisk_resu)*100,2), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl22_DNO"].place(relx=0.865, rely=0.384, anchor=tk.CENTER)
                    
                if DNO_text["txt_tbl3_DNO"] is None:
                    DNO_text["txt_tbl3_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[1],0), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl3_DNO"].place(relx=0.575, rely=0.49, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl33_DNO"] is None:
                    DNO_text["txt_tbl33_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[1]/np.sum(aggrisk_resu)*100,2), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl33_DNO"].place(relx=0.865, rely=0.49, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl4_DNO"] is None:
                    DNO_text["txt_tbl4_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[2],0), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl4_DNO"].place(relx=0.575, rely=0.60, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl44_DNO"] is None:
                    DNO_text["txt_tbl44_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[2]/np.sum(aggrisk_resu)*100,2), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl44_DNO"].place(relx=0.865, rely=0.60, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl5_DNO"] is None:
                    DNO_text["txt_tbl5_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[3],0), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl5_DNO"].place(relx=0.575, rely=0.71, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl55_DNO"] is None:
                    DNO_text["txt_tbl55_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[3]/np.sum(aggrisk_resu)*100,2), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl55_DNO"].place(relx=0.865, rely=0.71, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl6_DNO"] is None:
                    DNO_text["txt_tbl6_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[4],0), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl6_DNO"].place(relx=0.575, rely=0.83, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl66_DNO"] is None:
                    DNO_text["txt_tbl66_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(aggrisk_resu[4]/np.sum(aggrisk_resu)*100,2), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl66_DNO"].place(relx=0.865, rely=0.83, anchor=tk.CENTER)
                
                if DNO_text["txt_tbl7_DNO"] is None:
                    DNO_text["txt_tbl7_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= np.around(np.sum(aggrisk_resu),0), font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl7_DNO"].place(relx=0.575, rely=0.94, anchor=tk.CENTER)
                    
                if DNO_text["txt_tbl77_DNO"] is None:
                    DNO_text["txt_tbl77_DNO"] = tk.Label(DNO_boton["tbl_CP_DNO"], text= 100, font=("Abadi MT", 15), bg="#C6CFD4", fg="#000000")
                    DNO_text["txt_tbl77_DNO"].place(relx=0.865, rely=0.94, anchor=tk.CENTER)
                
                # -------------------------------------------------------------    
                # Botones para mostrar demás resultados 
                # -------------------------------------------------------------
                global tipo_calculo
                # -------- Salida Geográfica: Ocupantes en ed. colapsados -----
                if DNO_boton["btn_hml_DNO"]  is None:
                    
                    # Seleccionar tipo de calculo
                    #   1 para salida geografica por manzana
                    #   2 para salida grafica por seccion
                    
                    tipo_calculo = 1  
                    variable = 'aac_mnz_urb_colapso_hab'
                    
                    DNO_boton["btn_hml_DNO"]  = wnfun_lib.Button_Image_lambda3('/Salida_Geo_Ocupantes.png',
                                274, 90, cnt_container,"white",0.75,0.36,Salida_Geografica_DNO,tipo_calculo,mapdata_homeless,variable)
                
                # -------- Salida Geográfica: Edificios colapsados ------------
                if DNO_boton["btn_clp_DNO"]  is None:
                    tipo_calculo = 1 
                    variable = 'aac_mnz_colapso_no_edis'
                    DNO_boton["btn_clp_DNO"]  = wnfun_lib.Button_Image_lambda3('/Salida_Geo_Colapso.png',
                                274, 90, cnt_container,"white",0.75,0.50,Salida_Geografica_DNO,tipo_calculo,mapdata_collapsed,variable)
                
                # -------- Salida Geográfica: Distribución de heridos ---------
                if DNO_boton["btn_inj_DNO"]  is None:
                    tipo_calculo = 1 
                    variable = 'aad_mnz_heridos_hab'
                    DNO_boton["btn_inj_DNO"]  = wnfun_lib.Button_Image_lambda3('/Salida_Geo_Heridos.png',
                                274, 90, cnt_container,"white",0.75,0.64,Salida_Geografica_DNO,tipo_calculo,mapdata_injured,variable)
                
                # -------- Salida Geográfica: Distribución de fallecidos ------
                if DNO_boton["btn_ftl_DNO"]  is None:
                    tipo_calculo = 1 
                    variable = 'aad_mnz_fallecidos_hab'
                    DNO_boton["btn_ftl_DNO"]  = wnfun_lib.Button_Image_lambda3('/Salida_Geo_Fallecidos.png',
                                274, 90, cnt_container,"white",0.75,0.79,Salida_Geografica_DNO,tipo_calculo,mapdata_fatalities,variable)
                    
                # ---- Cambiar a resultados por taxonomia ---------------------
                DNO_boton["btn_cbm_DNO"] = wnfun_lib.Button_Image('/GoTo_EdTax_DNO.png', 272, 45, 
                                                cnt_container,"white",0.82,0.94,GoTo_Danos_Txn)
                
                # .............................................................
                # ---- Exportar resultados:
                if DNO_boton["btn_exp_DNO"] is None:
                    DNO_boton["btn_exp_DNO"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    210, 50, cnt_container,"white",0.10,0.94)
                    
                # .............................................................
                #          GENERAR TODOS LOS RESULTADOS PARA EXPORTAR 
                #             Todos los resultados menos los mapas
                # .............................................................
                Table_DNO_CP = wnfun_lib.Gen_Tabla_Resume_DNO(Num_build,aggrisk_resu)
                Table_DNO_Txn = wnfun_lib.Gen_Tabla_taxonomia_DNO(df_expotax_DNO)
                Figura_DNO_Txn = wnfun_lib.Figura_taxonomias_DNO_Export(taxonomias,aggrisk_mnz_DNO)
                # .............................................................

                if DNO_boton["btn_exp2_DNO"] is None:
                    DNO_boton["btn_exp2_DNO"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", 
                     command=lambda:wnfun_lib.ExportarResultados_Event_Based_Damage(Table_DNO_CP,Table_DNO_Txn,Figura_DNO_Txn))
                    DNO_boton["btn_exp2_DNO"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
                
                
    else:
        # Si no se encuentra la carpeta, la consola bota:
        tk.messagebox.showinfo(" ", "El archivo no fue seleccionado correctamente")
#%% ====== ELEMENTS >> MAPAS GEOGRAFICOS ======================================
def Function_Maps(resultado_label_MAP):
    if Select_Folder_MAP is not None:
        # Solo se genera el boton "exportar resultados" una vez todos los datos
        # hayan sido procesados
        global manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,calculation_mode_MAP,Modelo_Expo_MAP,CP_Name_MAP,COD_mun_MAP,mapdata_AreaCons_MAP,Txn_Rep_MAP,mapdata_Limits_MAP,mapdata_Pisos_MAP,title_npiso_MAP,valores_unidos_MAP,mapdata_allmnzmll_MAP,mapdata_allmnzcop_MAP,mapdata_fallmnz_MAP,mapdata_injuredmnz_MAP,mapdata_homelessmnz_MAP,mapdata_colapsedmnz_MAP,mapdata_allsccmll_MAP,mapdata_allscccop_MAP,mapdata_fallscc_MAP,mapdata_injuredscc_MAP,mapdata_homelessscc_MAP,mapdata_colapsedsecc_MAP,mapdata_danosmnz_MAP,mapdata_perdidasmnz_MAP
        manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,calculation_mode_MAP,Modelo_Expo_MAP,CP_Name_MAP,COD_mun_MAP,mapdata_AreaCons_MAP,Txn_Rep_MAP,mapdata_Limits_MAP,mapdata_Pisos_MAP,title_npiso_MAP,valores_unidos_MAP,mapdata_allmnzmll_MAP,mapdata_allmnzcop_MAP,mapdata_fallmnz_MAP,mapdata_injuredmnz_MAP,mapdata_homelessmnz_MAP,mapdata_colapsedmnz_MAP,mapdata_allsccmll_MAP,mapdata_allscccop_MAP,mapdata_fallscc_MAP,mapdata_injuredscc_MAP,mapdata_homelessscc_MAP,mapdata_colapsedsecc_MAP,mapdata_danosmnz_MAP,mapdata_perdidasmnz_MAP = map_lib.Function_MAPS_Elements(carpeta_seleccionada_MAP)
        
        # =================== Organizar input para exportar ===================
        if calculation_mode_MAP == "Probabilistico":
            if mapdata_AreaCons_MAP is None:
                tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
            else:
                
                Separa_x = 1
                Separa_y = 1 
                User_min_lon = -0.04
                User_max_lon = 0.02 
                User_min_lat = -0.02
                User_max_lat = 0.02
                
                # --------- Figura area construida por manzana censal ---------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'area_cons'
                # Generar figura
                Fig_Area_Cons = [0]*2
                Fig_Area_Cons[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_AreaCons_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_Area_Cons[1] = "Figura_area_construida.jpg"
                
                # -------- Figura area construida por numero de pisos ---------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                Fig_Area_Cons_Pisos, Lab_Area_Cons_Pisos = [], []
                for index in range(len(valores_unidos_MAP)):
                    variable = 'area_cons2'
                    # Generar figura
                    Fig_Area_Cons_Pisos.append(wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_Pisos_MAP[index],Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP[index],aggregate_by))
                    Lab_Area_Cons_Pisos.append("Figura_area_construida_piso"+valores_unidos_MAP[index]+".jpg")
                
                # ---------- Figura perdida anual promedio al millar ----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aal_mnz_mllr'
                # Generar figura
                Fig_PAP_mll = [0]*2
                Fig_PAP_mll[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_allmnzmll_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_PAP_mll[1] = "Figura_aal_mnz_mll.jpg"
                
                # ------------ Figura perdida anual promedio en COP -----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aal_mnz_cop'
                # Generar figura
                Fig_PAP_cop_mnz = [0]*2
                Fig_PAP_cop_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_allmnzcop_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_PAP_cop_mnz[1] = "Figura_aal_mnz_cop.jpg"
                
                # ------------ Figura fallecidos por cada 100k hab ------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aad_mnz_fallecidos_100m_hab'
                # Generar figura
                Fig_ftl_100_mnz = [0]*2
                Fig_ftl_100_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_fallmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_ftl_100_mnz[1] = "Figura_aad_mnz_fallecidos_100m_hab.jpg"
                
                # --------------- Figura fallecidos por manzana ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aad_mnz_fallecidos_hab'
                # Generar figura
                Fig_fatalities_mnz = [0]*2
                Fig_fatalities_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_fallmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_fatalities_mnz[1] = "Figura_aad_mnz_fallecidos_hab.jpg"
                
                # ------------ Figura heridos por cada 100k hab ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aai_mnz_heridos_100m_hab'
                # Generar figura
                Fig_inj_100_mnz = [0]*2
                Fig_inj_100_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_injuredmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_inj_100_mnz[1] = "Figura_aai_mnz_heridos_100m_hab.jpg"
                
                # --------------- Figura heridos por manzana ------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aai_mnz_heridos_hab'
                # Generar figura
                Fig_injured_mnz = [0]*2
                Fig_injured_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_injuredmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_injured_mnz[1] = "Figura_aai_mnz_heridos_hab.jpg"
    
                # --------------- Figura ocupantes por manzana ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aac_mnz_colapso_hab'
                # Generar figura
                Fig_homeless_mnz = [0]*2
                Fig_homeless_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_homelessmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_homeless_mnz[1] = "Figura_aac_mnz_colapso_hab.jpg"
                
                # --------------- Figura edificios por manzana ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aac_mnz_colapso_no_edis'
                # Generar figura
                Fig_colapsed_mnz = [0]*2
                Fig_colapsed_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_colapsedmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_colapsed_mnz[1] = "Figura_aac_mnz_colapso_no_edis.jpg"
                
                # ---------- Figura perdida anual promedio al millar ----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aal_secc_urb_mllr'
                # Generar figura
                Fig_PAP_mll_scc = [0]*2
                Fig_PAP_mll_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_allsccmll_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_PAP_mll_scc[1] = "Figura_aal_secc_urb_mll.jpg"
                
                # ------------ Figura perdida anual promedio en COP -----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aal_secc_urb_cop'
                # Generar figura
                Fig_PAP_cop_scc = [0]*2
                Fig_PAP_cop_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_allscccop_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_PAP_cop_scc[1] = "Figura_aal_secc_urb_cop.jpg"
                
                # ------------ Figura fallecidos por cada 100k hab ------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aad_secc_urb_fallecidos_100m_hab'
                # Generar figura
                Fig_ftl_100_scc = [0]*2
                Fig_ftl_100_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_fallscc_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_ftl_100_scc[1] = "Figura_aad_secc_urb_fallecidos_100m_hab.jpg"
                
                # --------------- Figura fallecidos por seccion ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aad_secc_urb_fallecidos_hab'
                # Generar figura
                Fig_fatalities_scc = [0]*2
                Fig_fatalities_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_fallscc_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_fatalities_scc[1] = "Figura_aad_secc_urb_fallecidos_hab.jpg"
                
                # ------------ Figura heridos por cada 100k hab ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aai_secc_urb_heridos_100m_hab'
                # Generar figura
                Fig_inj_100_scc = [0]*2
                Fig_inj_100_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_injuredscc_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_inj_100_scc[1] = "Figura_aai_secc_urb_heridos_100m_hab.jpg"
                
                # --------------- Figura heridos por seccion ------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aai_secc_urb_heridos_hab'
                # Generar figura
                Fig_injured_scc = [0]*2
                Fig_injured_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_injuredscc_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_injured_scc[1] = "Figura_aai_secc_urb_heridos_hab.jpg"
                
                # --------------- Figura ocupantes por seccion ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aac_secc_urb_colapso_hab'
                # Generar figura
                Fig_homeless_scc = [0]*2
                Fig_homeless_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_homelessscc_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_homeless_scc[1] = "Figura_aac_secc_urb_colapso_hab.jpg"
                
                # --------------- Figura edificios por seccion ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aac_secc_urb_colapso_no_edis'
                # Generar figura
                Fig_colapsed_scc = [0]*2
                Fig_colapsed_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_colapsedsecc_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_colapsed_scc[1] = "Figura_aac_secc_urb_colapso_no_edis.jpg"
                
                # --------------- Figura Danos dmg3 y dmg4 --------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'dmg3'
                # Generar figura
                Fig_dmg3 = [0]*2
                Fig_dmg3[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_danosmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_dmg3[1] = "Figura_ed_mnz_danosevero.jpg"
                
                variable = 'dmg4'
                # Generar figura
                Fig_dmg4 = [0]*2
                Fig_dmg4[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_danosmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_dmg4[1] = "Figura_ed_mnz_colapsadas.jpg"
                
                # -------------------- Figura Perdidas PAE --------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'pae_mnz_cop'
                # Generar figura
                Fig_paecop = [0]*2
                Fig_paecop[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_perdidasmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_paecop[1] = "Figura_pae_mnz_cop.jpg"
                
                variable = 'pae_mnz_prc'
                # Generar figura
                Fig_paeprc = [0]*2
                Fig_paeprc[0] = wnfun_lib.GeneradorMapas(COD_mun_MAP,CP_Name_MAP,manzana_shp_MAP,seccion_shp_MAP,area_shp_MAP,mapdata_perdidasmnz_MAP,Modelo_Expo_MAP,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_MAP,title_npiso_MAP,aggregate_by)
                Fig_paeprc[1] = "Figura_pae_mnz_‰.jpg"
                
                # .............................................................
                # ---- Exportar resultados:
                if MAP_boton["btn_exp_MAP"] is None:
                    MAP_boton["btn_exp_MAP"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    273, 65, cnt_container,"white",0.78,0.67)
                    
                if MAP_boton["btn_exp2_MAP"] is None:
                    MAP_boton["btn_exp2_MAP"] = tk.Button(MAP_boton["btn_exp_MAP"], text="Exportar resultados", font=("Abadi MT", 16), bd=0, bg="#B97F73", fg="white", 
                     command=lambda:wnfun_lib.ExportarResultados_MapasGeograficos(Fig_Area_Cons,Fig_Area_Cons_Pisos,Lab_Area_Cons_Pisos,Fig_PAP_mll,Fig_PAP_cop_mnz,Fig_ftl_100_mnz,Fig_fatalities_mnz,
                     Fig_inj_100_mnz,Fig_injured_mnz,Fig_homeless_mnz,Fig_colapsed_mnz,Fig_PAP_mll_scc,Fig_PAP_cop_scc,Fig_ftl_100_scc,Fig_fatalities_scc,Fig_inj_100_scc,Fig_injured_scc,Fig_homeless_scc,Fig_colapsed_scc,Fig_dmg3,Fig_dmg4,Fig_paecop,Fig_paeprc))
                    MAP_boton["btn_exp2_MAP"].place(relx=0.53, rely=0.42, anchor=tk.CENTER)
                

    else:
        # Si no se encuentra la carpeta, la consola bota:
        tk.messagebox.showinfo(" ", "El archivo no fue seleccionado correctamente")

#%% ====== ELEMENTS >> GENERADOR ==============================================
def Function_Generador(resultado_label_GEN):
    if Select_Folder_GEN is not None:
        # Solo se genera el boton "exportar resultados" una vez todos los datos
        # hayan sido procesados
        global df_EBR_GEN,valexpuesto_GEN,valorexp_GEN,PAE_mill_GEN,PE_mill_GEN,Num_build_table1,aggrisk_table1,df_expotax_table2,categorias_GEN,aggrisk_mnz_GEN,df_expotax_table3,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN, calculation_mode_GEN, Modelo_Expo_GEN, CP_Name_GEN, COD_mun_GEN, mapdata_AreaCons_GEN, Txn_Rep_GEN, mapdata_Limits_GEN, mapdata_Pisos_GEN, title_npiso_GEN, valores_unidos_GEN, mapdata_allmnzmll_GEN, mapdata_allmnzcop_GEN, mapdata_fallmnz_GEN, mapdata_injuredmnz_GEN, mapdata_homelessmnz_GEN, mapdata_colapsedmnz_GEN, mapdata_allsccmll_GEN, mapdata_allscccop_GEN, mapdata_fallscc_GEN, mapdata_injuredscc_GEN, mapdata_homelessscc_GEN, mapdata_colapsedsecc_GEN, mapdata_danosmnz_GEN, mapdata_perdidasmnz_GEN
        df_EBR_GEN,valexpuesto_GEN,valorexp_GEN,PAE_mill_GEN,PE_mill_GEN,Num_build_table1,aggrisk_table1,df_expotax_table2,categorias_GEN,aggrisk_mnz_GEN,df_expotax_table3,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN, calculation_mode_GEN, Modelo_Expo_GEN, CP_Name_GEN, COD_mun_GEN, mapdata_AreaCons_GEN, Txn_Rep_GEN, mapdata_Limits_GEN, mapdata_Pisos_GEN, title_npiso_GEN, valores_unidos_GEN, mapdata_allmnzmll_GEN, mapdata_allmnzcop_GEN, mapdata_fallmnz_GEN, mapdata_injuredmnz_GEN, mapdata_homelessmnz_GEN, mapdata_colapsedmnz_GEN, mapdata_allsccmll_GEN, mapdata_allscccop_GEN, mapdata_fallscc_GEN, mapdata_injuredscc_GEN, mapdata_homelessscc_GEN, mapdata_colapsedsecc_GEN, mapdata_danosmnz_GEN, mapdata_perdidasmnz_GEN = gen_lib.Function_GEN_Elements(carpeta_seleccionada_GEN)
        
        # =================== Organizar input para exportar ===================
        if calculation_mode_GEN == "Probabilistico":
            if mapdata_AreaCons_GEN is None:
                tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
            else:
                
                Separa_x = 1
                Separa_y = 1 
                User_min_lon = -0.04
                User_max_lon = 0.02 
                User_min_lat = -0.02
                User_max_lat = 0.02
                
                # --------- Figura area construida por manzana censal ---------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'area_cons'
                # Generar figura
                Fig_Area_Cons = [0]*2
                Fig_Area_Cons[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_AreaCons_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_Area_Cons[1] = "Figura_area_construida.jpg"
                
                # -------- Figura area construida por numero de pisos ---------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                Fig_Area_Cons_Pisos, Lab_Area_Cons_Pisos = [], []
                for index in range(len(valores_unidos_GEN)):
                    variable = 'area_cons2'
                    # Generar figura
                    Fig_Area_Cons_Pisos.append(wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_Pisos_GEN[index],Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN[index],aggregate_by))
                    Lab_Area_Cons_Pisos.append("Figura_area_construida_piso"+valores_unidos_GEN[index]+".jpg")
                
                # ---------- Figura perdida anual promedio al millar ----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aal_mnz_mllr'
                # Generar figura
                Fig_PAP_mll = [0]*2
                Fig_PAP_mll[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_allmnzmll_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_PAP_mll[1] = "Figura_aal_mnz_mll.jpg"
                
                # ------------ Figura perdida anual promedio en COP -----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aal_mnz_cop'
                # Generar figura
                Fig_PAP_cop_mnz = [0]*2
                Fig_PAP_cop_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_allmnzcop_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_PAP_cop_mnz[1] = "Figura_aal_mnz_cop.jpg"
                
                # ------------ Figura fallecidos por cada 100k hab ------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aad_mnz_fallecidos_100m_hab'
                # Generar figura
                Fig_ftl_100_mnz = [0]*2
                Fig_ftl_100_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_fallmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_ftl_100_mnz[1] = "Figura_aad_mnz_fallecidos_100m_hab.jpg"
                
                # --------------- Figura fallecidos por manzana ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aad_mnz_fallecidos_hab'
                # Generar figura
                Fig_fatalities_mnz = [0]*2
                Fig_fatalities_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_fallmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_fatalities_mnz[1] = "Figura_aad_mnz_fallecidos_hab.jpg"
                
                # ------------ Figura heridos por cada 100k hab ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aai_mnz_heridos_100m_hab'
                # Generar figura
                Fig_inj_100_mnz = [0]*2
                Fig_inj_100_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_injuredmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_inj_100_mnz[1] = "Figura_aai_mnz_heridos_100m_hab.jpg"
                
                # --------------- Figura heridos por manzana ------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aai_mnz_heridos_hab'
                # Generar figura
                Fig_injured_mnz = [0]*2
                Fig_injured_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_injuredmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_injured_mnz[1] = "Figura_aai_mnz_heridos_hab.jpg"
    
                # --------------- Figura ocupantes por manzana ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aac_mnz_colapso_hab'
                # Generar figura
                Fig_homeless_mnz = [0]*2
                Fig_homeless_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_homelessmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_homeless_mnz[1] = "Figura_aac_mnz_colapso_hab.jpg"
                
                # --------------- Figura edificios por manzana ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'aac_mnz_colapso_no_edis'
                # Generar figura
                Fig_colapsed_mnz = [0]*2
                Fig_colapsed_mnz[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_colapsedmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_colapsed_mnz[1] = "Figura_aac_mnz_colapso_no_edis.jpg"
                
                # ---------- Figura perdida anual promedio al millar ----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aal_secc_urb_mllr'
                # Generar figura
                Fig_PAP_mll_scc = [0]*2
                Fig_PAP_mll_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_allsccmll_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_PAP_mll_scc[1] = "Figura_aal_secc_urb_mll.jpg"
                
                # ------------ Figura perdida anual promedio en COP -----------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aal_secc_urb_cop'
                # Generar figura
                Fig_PAP_cop_scc = [0]*2
                Fig_PAP_cop_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_allscccop_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_PAP_cop_scc[1] = "Figura_aal_secc_urb_cop.jpg"
                
                # ------------ Figura fallecidos por cada 100k hab ------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aad_secc_urb_fallecidos_100m_hab'
                # Generar figura
                Fig_ftl_100_scc = [0]*2
                Fig_ftl_100_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_fallscc_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_ftl_100_scc[1] = "Figura_aad_secc_urb_fallecidos_100m_hab.jpg"
                
                # --------------- Figura fallecidos por seccion ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aad_secc_urb_fallecidos_hab'
                # Generar figura
                Fig_fatalities_scc = [0]*2
                Fig_fatalities_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_fallscc_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_fatalities_scc[1] = "Figura_aad_secc_urb_fallecidos_hab.jpg"
                
                # ------------ Figura heridos por cada 100k hab ---------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aai_secc_urb_heridos_100m_hab'
                # Generar figura
                Fig_inj_100_scc = [0]*2
                Fig_inj_100_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_injuredscc_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_inj_100_scc[1] = "Figura_aai_secc_urb_heridos_100m_hab.jpg"
                
                # --------------- Figura heridos por seccion ------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aai_secc_urb_heridos_hab'
                # Generar figura
                Fig_injured_scc = [0]*2
                Fig_injured_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_injuredscc_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_injured_scc[1] = "Figura_aai_secc_urb_heridos_hab.jpg"
                
                # --------------- Figura ocupantes por seccion ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aac_secc_urb_colapso_hab'
                # Generar figura
                Fig_homeless_scc = [0]*2
                Fig_homeless_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_homelessscc_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_homeless_scc[1] = "Figura_aac_secc_urb_colapso_hab.jpg"
                
                # --------------- Figura edificios por seccion ----------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "seccion"
                variable = 'aac_secc_urb_colapso_no_edis'
                # Generar figura
                Fig_colapsed_scc = [0]*2
                Fig_colapsed_scc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_colapsedsecc_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_colapsed_scc[1] = "Figura_aac_secc_urb_colapso_no_edis.jpg"
                
                # --------------- Figura Danos dmg3 y dmg4 --------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'dmg3'
                # Generar figura
                Fig_dmg3 = [0]*2
                Fig_dmg3[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_danosmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_dmg3[1] = "Figura_ed_mnz_danosevero.jpg"
                
                variable = 'dmg4'
                # Generar figura
                Fig_dmg4 = [0]*2
                Fig_dmg4[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_danosmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_dmg4[1] = "Figura_ed_mnz_colapsadas.jpg"
                
                # -------------------- Figura Perdidas PAE --------------------
                # -------------------------------------------------------------
                # Variables a utilizar
                aggregate_by = "manzana"
                variable = 'pae_mnz_cop'
                # Generar figura
                Fig_paecop = [0]*2
                Fig_paecop[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_perdidasmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_paecop[1] = "Figura_pae_mnz_cop.jpg"
                
                variable = 'pae_mnz_prc'
                # Generar figura
                Fig_paeprc = [0]*2
                Fig_paeprc[0] = wnfun_lib.GeneradorMapas(COD_mun_GEN,CP_Name_GEN,manzana_shp_GEN,seccion_shp_GEN,area_shp_GEN,mapdata_perdidasmnz_GEN,Modelo_Expo_GEN,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable,Txn_Rep_GEN,title_npiso_GEN,aggregate_by)
                Fig_paeprc[1] = "Figura_pae_mnz_‰.jpg"
                
                
                # -------------------------------------------------------------
                Table1_Danos = [0]*2
                Table1_Danos[0] = wnfun_lib.Gen_Tabla_Resume_DNO(Num_build_table1,aggrisk_table1)
                Table1_Danos[1] = "Edificaciones_DMG.xlsx"
                
                Table2_Danos = [0]*2
                Table2_Danos[0] = wnfun_lib.Gen_Tabla_taxonomia_DNO(df_expotax_table2)
                Table2_Danos[1] = "Taxonomias_DMG.xlsx"
                
                Figura1_Danos = [0]*2
                Figura1_Danos[0] = wnfun_lib.Figura_taxonomias_DNO_Export(categorias_GEN,aggrisk_mnz_GEN)
                Figura1_Danos[1] = "Danos_Taxonomias.jpg"
                
                Table1_Perdidas = [0]*2
                Table1_Perdidas[0] = wnfun_lib.Gen_Tabla_Resume_PRD(valorexp_GEN,PAE_mill_GEN,PE_mill_GEN)
                Table1_Perdidas[1] = "PAE_Municipio.xlsx"
                
                Table2_Perdidas = [0]*2
                Table2_Perdidas[0] = wnfun_lib.Gen_Tabla_taxonomia_PRD(df_expotax_table3)
                Table2_Perdidas[1] = "PAE_Taxonomias.xlsx"
                
                Figura1_Perdidas = [0]*2
                Figura1_Perdidas[0] = wnfun_lib.Diagrama_Taxonomia_PRD(df_expotax_table3)
                Figura1_Perdidas[1] = "Taxonomias_Diagrama.jpg"
                
                Figura2_Perdidas = [0]*2
                Figura2_Perdidas[0] = wnfun_lib.curva_excedencia(df_EBR_GEN, valexpuesto_GEN)
                Figura2_Perdidas[1] = "Curva_Excedencia.jpg"
                
                # .............................................................
                # ---- Exportar resultados:
                if GEN_boton["btn_exp_GEN"] is None:
                    GEN_boton["btn_exp_GEN"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                    273, 65, cnt_container,"white",0.78,0.67)
                    
                if GEN_boton["btn_exp2_GEN"] is None:
                    GEN_boton["btn_exp2_GEN"] = tk.Button(GEN_boton["btn_exp_GEN"], text="Exportar resultados", font=("Abadi MT", 16), bd=0, bg="#B97F73", fg="white", 
                     command=lambda:wnfun_lib.ExportarResultados_Generador(Fig_Area_Cons,Fig_Area_Cons_Pisos,Lab_Area_Cons_Pisos,Fig_PAP_mll,Fig_PAP_cop_mnz,Fig_ftl_100_mnz,Fig_fatalities_mnz,
                     Fig_inj_100_mnz,Fig_injured_mnz,Fig_homeless_mnz,Fig_colapsed_mnz,Fig_PAP_mll_scc,Fig_PAP_cop_scc,Fig_ftl_100_scc,Fig_fatalities_scc,Fig_inj_100_scc,Fig_injured_scc,Fig_homeless_scc,Fig_colapsed_scc,Fig_dmg3,Fig_dmg4,Fig_paecop,Fig_paeprc,Table1_Danos,Table2_Danos,Figura1_Danos,Table1_Perdidas,Table2_Perdidas,Figura1_Perdidas,Figura2_Perdidas))
                    GEN_boton["btn_exp2_GEN"].place(relx=0.53, rely=0.42, anchor=tk.CENTER)
                
    
    else:
        # Si no se encuentra la carpeta, la consola bota:
        tk.messagebox.showinfo(" ", "El archivo no fue seleccionado correctamente")
        
#%% ====== ELEMENTS >> FICHA TECNICA ==========================================
def Function_Ficha(resultado_label_FCH):
    if Select_Folder_FCH is not None:
        # Solo se genera el boton "exportar resultados" una vez todos los datos
        # hayan sido procesados
        global output_pdf_path,calculation_mode_FCH, CP_Name_FCH
        output_pdf_path,calculation_mode_FCH,CP_Name_FCH = fch_lib.Function_FCH_Elements(carpeta_seleccionada_FCH)
        
        # =================== Organizar input para exportar ===================
        if output_pdf_path is None:
            tk.messagebox.showinfo("ERROR", "Vuelva a intentarlo")
        else:
            
            # .............................................................
            # ---- Exportar resultados:
            if FCH_boton["btn_exp_FCH"] is None:
                FCH_boton["btn_exp_FCH"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                                273, 65, cnt_container,"white",0.78,0.67)

            if FCH_boton["btn_exp2_FCH"] is None:
                FCH_boton["btn_exp2_FCH"] = tk.Button(FCH_boton["btn_exp_FCH"], text="Exportar resultados", font=("Abadi MT", 16), bd=0, bg="#B97F73", fg="white", 
                 command=lambda:wnfun_lib.ExportarResultados_Ficha(output_pdf_path,CP_Name_FCH))
                FCH_boton["btn_exp2_FCH"].place(relx=0.53, rely=0.42, anchor=tk.CENTER)
                
    else:
        # Si no se encuentra la carpeta, la consola bota:
        tk.messagebox.showinfo(" ", "El archivo no fue seleccionado correctamente")
#%% ====== FUNCION >> DAÑOS TAXONOMIA =========================================

"""----------------------------------------------------------------------------

             PRIMERA FUNCION: ENTRAR A RESULTADOS POR TAXONOMIA
             
En esta primera función se muestran los resultados por taxonomia. Contiene:
    1. Tabla resultados por tipologia                                     [x]
    2. Boton siguiente y atras (habilitado si hay más de 6 tipologías)    [x]
    3. Boton representacion grafica de resultados por taxonomia           [x]
    4. Boton exportar resultados                                          [x]
    5. Boton regresar a resultados del municipio                          [x]

----------------------------------------------------------------------------"""

def GoTo_Danos_Txn():
    
    # .........................................................................
    #               PREPARAR ESCENARIO PARA NUEVOS RESULTADOS 
    #               Tabla resultados por taxonomia y diagrama
    # .........................................................................
    
    for tlt in title_DNO:
        if DNO_title[tlt] is not None:
            DNO_title[tlt].place_forget()
            DNO_title[tlt] = None
            
    for txt in text_DNO:
        if DNO_text[txt] is not None:
            DNO_text[txt].place_forget()
            DNO_text[txt] = None
            
    for btn in boton_DNO:
        if DNO_boton[btn] is not None:
            DNO_boton[btn].place_forget()
            DNO_boton[btn] = None
    
    
    # .........................................................................
    #                      VOLVER A ACOMODAR LOS BOTONES
    # .........................................................................
    
    # -------- Frame resultados -----------------------------------------------
    if DNO_boton["lbl_rst_DNO"] is None:
        DNO_boton["lbl_rst_DNO"] = wnfun_lib.Label_Image('/Frame_Results.png',
                                    1300, 300, cnt_container,"white",0.5,0.0)
    # -------- Design frame ---------------------------------------------------
    if DNO_boton["lbl_DsF_DNO"] is None:
        DNO_boton["lbl_DsF_DNO"] = wnfun_lib.Label_Image('/upper_container_v2.png',
                                1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
    
    # -------- Title Section --------------------------------------------------
    if DNO_text["tlt_sct_DNO"] is None:
        DNO_text["tlt_sct_DNO"] = tk.Label(cnt_container, text="Resultados de Daño Basado en Eventos",
                                           font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
        DNO_text["tlt_sct_DNO"].place(relx=0.243, rely=0.072, anchor=tk.CENTER)
    if DNO_text["tlt_sct_DNO1"] is None:
        if calculation_mode_DNO == "Probabilistico":
            DNO_text["tlt_sct_DNO1"] = tk.Label(cnt_container, text="Eventos probabilísticos", 
                                        font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            DNO_text["tlt_sct_DNO1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
        else:
            DNO_text["tlt_sct_DNO1"] = tk.Label(cnt_container, text="Eventos determinísticos", 
                                        font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            DNO_text["tlt_sct_DNO1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
    # -------- Frame Results Title --------------------------------------------
    if DNO_boton["lbl_rstv2_DNO"] is None:
        DNO_boton["lbl_rstv2_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 
                                        1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
    if DNO_boton["lbl_rstv3_DNO"] is None:
        DNO_boton["lbl_rstv3_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png',
                                            100, 36, cnt_container,"white",0.0,0.304)
    if DNO_boton["lbl_rstv4_DNO"] is None:
        DNO_boton["lbl_rstv4_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png',
                                            38, 58, cnt_container,"white",0.025,0.24)
    # -------- Results Title --------------------------------------------------
    if DNO_text["tlt_rstv2_DNO"] is None:
        DNO_text["tlt_rstv2_DNO"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name_DNO, 
                            font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
        DNO_text["tlt_rstv2_DNO"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
    
    # ---- Cambiar a diagrama de taxonomias -----------------------------------
    if DNO_boton["btn_diag_DNO"] is None:
        DNO_boton["btn_diag_DNO"] = wnfun_lib.Button_Image('/GoTo_DNO_Diag.png', 
                                160, 60, cnt_container,"white",0.5,0.252,GoTo_DNO_Diag)
    
    # ---- Cambiar a resultados del municipio ---------------------------------
    DNO_boton["btn_cbm_DNO"] = wnfun_lib.Button_Image('/GoTo_DNO_CP.png', 268, 45, 
                                    cnt_container,"white",0.82,0.94,GoTo_DNO_CP)
    
    # .............................................................
    # ---- Exportar resultados:
    if DNO_boton["btn_exp_DNO"] is None:
        DNO_boton["btn_exp_DNO"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    # .............................................................
    #          GENERAR TODOS LOS RESULTADOS PARA EXPORTAR 
    #             Todos los resultados menos los mapas
    # .............................................................
    Table_DNO_CP = wnfun_lib.Gen_Tabla_Resume_DNO(Num_build,aggrisk_resu)
    Table_DNO_Txn = wnfun_lib.Gen_Tabla_taxonomia_DNO(df_expotax_DNO)
    Figura_DNO_Txn = wnfun_lib.Figura_taxonomias_DNO_Export(taxonomias,aggrisk_mnz_DNO)
    # .............................................................

    if DNO_boton["btn_exp2_DNO"] is None:
        DNO_boton["btn_exp2_DNO"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", 
         command=lambda:wnfun_lib.ExportarResultados_Event_Based_Damage(Table_DNO_CP,Table_DNO_Txn,Figura_DNO_Txn))
        DNO_boton["btn_exp2_DNO"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
    
    # .........................................................................
    #                      GENERAR TABLA DE TAXONOMIAS
    # .........................................................................
    
    # ---------------------- Llenar tabla por taxonomias ----------------------
    global pos_x, pos_y
    
    pos_x = 0.50
    pos_y = 0.59
    
    if DNO_boton["tbl_CP_DNO"]  is None:
        DNO_boton["tbl_CP_DNO"]  = wnfun_lib.Label_Image('/Tabla_Dano_Txn.png', 
                                    991, 450, cnt_container,"white",pos_x,pos_y)
    
    # Primero hay que dividir las tipologias para mostrar en diferentes pestanas. 
    # Si el numero de taxonomias es menor o igual a 6, no es necesario, pero si 
    # es mayor, se debe dividir la cantidad de taxonomias entre 6 y repartirlas 
    # en las pestanas.
    
    global table_DNO,listas_divididas_df_expotax
    # Se crea la lista de variables necesarias para llenar los espacios de la 
    
    table_DNO = []
    if len(df_expotax_DNO) <= 6:
        
        # tabla por taxonomias
        for index in range(len(df_expotax_DNO)):
            VarName_TC = "tbl_TC" + str(index+1)
            table_DNO.append(VarName_TC)
            VarName_DS1 = "tbl_DS1_" + str(index+1)
            table_DNO.append(VarName_DS1)
            VarName_DS1_prc = "tbl_DS1_prc" + str(index+1)
            table_DNO.append(VarName_DS1_prc)
            VarName_DS2 = "tbl_DS2_" + str(index+1)
            table_DNO.append(VarName_DS2)
            VarName_DS2_prc = "tbl_DS2_prc" + str(index+1)
            table_DNO.append(VarName_DS2_prc)
            VarName_DS3 = "tbl_DS3_" + str(index+1)
            table_DNO.append(VarName_DS3)
            VarName_DS3_prc = "tbl_DS3_prc" + str(index+1)
            table_DNO.append(VarName_DS3_prc)
            VarName_DS4 = "tbl_DS4_" + str(index+1)
            table_DNO.append(VarName_DS4)
            VarName_DS4_prc = "tbl_DS4_prc" + str(index+1)
            table_DNO.append(VarName_DS4_prc)
            VarName_DS5 = "tbl_DS5_" + str(index+1)
            table_DNO.append(VarName_DS5)
            VarName_DS5_prc = "tbl_DS5_prc" + str(index+1)
            table_DNO.append(VarName_DS5_prc)
        
        for tbl in table_DNO:
            DNO_table[tbl] = None
        
        # Crear botones siguiente y atras pero inhabilitados
        DNO_boton["btn_atras"] = wnfun_lib.Label_Image('/PAE_Atras.png', 
                                50, 40, cnt_container,"white",pos_x+0.334,pos_y-0.333)
        DNO_boton["btn_siguiente"] = wnfun_lib.Label_Image('/PAE_Siguiente_Inh.png', 
                                50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333)
        
        danos_lib.Gen_Elements_Tax_6(df_expotax_DNO,DNO_table,DNO_boton) 
        
    else:
        
        def obtener_numero_de_unidades_DNO(df_expotax):
            longitud_df = len(df_expotax)
            unidades = math.ceil(longitud_df / 6)
            return unidades
        
        numero_de_unidades_expotax = obtener_numero_de_unidades_DNO(df_expotax_DNO)
        listas_divididas_df_expotax = [df_expotax_DNO[i*6 : (i+1)*6] for i in range(numero_de_unidades_expotax)]
        
        # aqui ya se obtiene la lista en cada parte. ahora se necesita crear un boton
        # que permita ir a la otra lista de los siguientes 6 valores. Entonces se debe
        # hacer el proceso normal para la primera lista y despues crear el boton de siguiente.
        # Ese boton de siguiente muestra la otra parte de la lista (como hay mas partes esa si o si va)
        # ahora se viene un condicional, si listas_divididas tiene una longitud mayor a 2 entonces
        # se debe crear un for con esos botones para que cada accion haga que cambie de lista
        # en ese bucle debe ingresar la lista que se va a usar y un contador. cuando el contador
        # sea igual al numero de unidades "numero_de_unidades" entonces para.
        
        # ---- Se genera la primera lista:
        # Para esta lista se necesitan los 6 primeros valores de df_expotax.
        df_expotax_1 = listas_divididas_df_expotax[0]              # obtiene entonces el primer dataframe de valores
        # Con esos valores se crean la primera tabla
        
        for index in range(len(df_expotax_1)):
            VarName_TC = "tbl_TC" + str(index+1)
            table_DNO.append(VarName_TC)
            VarName_DS1 = "tbl_DS1_" + str(index+1)
            table_DNO.append(VarName_DS1)
            VarName_DS1_prc = "tbl_DS1_prc" + str(index+1)
            table_DNO.append(VarName_DS1_prc)
            VarName_DS2 = "tbl_DS2_" + str(index+1)
            table_DNO.append(VarName_DS2)
            VarName_DS2_prc = "tbl_DS2_prc" + str(index+1)
            table_DNO.append(VarName_DS2_prc)
            VarName_DS3 = "tbl_DS3_" + str(index+1)
            table_DNO.append(VarName_DS3)
            VarName_DS3_prc = "tbl_DS3_prc" + str(index+1)
            table_DNO.append(VarName_DS3_prc)
            VarName_DS4 = "tbl_DS4_" + str(index+1)
            table_DNO.append(VarName_DS4)
            VarName_DS4_prc = "tbl_DS4_prc" + str(index+1)
            table_DNO.append(VarName_DS4_prc)
            VarName_DS5 = "tbl_DS5_" + str(index+1)
            table_DNO.append(VarName_DS5)
            VarName_DS5_prc = "tbl_DS5_prc" + str(index+1)
            table_DNO.append(VarName_DS5_prc)
        
        for tbl in table_DNO:
            DNO_table[tbl] = None
        
        # Creo un contador 
        Contador_Valores = 1
        
        Contador_Valores_lambda = danos_lib.Gen_Elements_Tax(df_expotax_1,DNO_table,DNO_boton,Contador_Valores)
        
        # Aca entonces se crea el boton que direccione a la siguiente parte de la tabla:
        DNO_boton["btn_atras"] = wnfun_lib.Label_Image('/PAE_Atras.png', 
                                50, 40, cnt_container,"white",pos_x+0.334,pos_y-0.333)
        DNO_boton["btn_siguiente"] = wnfun_lib.Button_Image_lambda('/PAE_Siguiente.png', 
                            50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333,ChangeTo_DNOTxn_Next,Contador_Valores_lambda)
        
"""----------------------------------------------------------------------------

             SEGUNDA FUNCION: MOSTRAR MÁS RESULTADOS DE TAXONOMIA
             
En esta segunda función se muestran los resultados por taxonomia del siguiente
conjunto de datos. Contiene:
    1. Tabla resultados por tipologia                                     [x]
    2. Boton siguiente y atras (habilitado si hay más de 6 tipologías y  
       para regresar a los resultados anteriores)                         [x]
    3. Boton representacion grafica de resultados por taxonomia           [x]
    4. Boton exportar resultados                                          [x]
    5. Boton regresar a resultados del municipio                          [x]

----------------------------------------------------------------------------"""
        
def ChangeTo_DNOTxn_Next(Contador_Valores):
    
    # Aqui entra si o si. la cosa es si hay mas listas divididas para mostrar
    
    # Eliminar el contenido de la tabla anterior
    
    for tbl in table_DNO:
        if DNO_table[tbl] is not None:
            DNO_table[tbl].place_forget()
            DNO_table[tbl] = None
    
    # Elimina boton atras y siguiente
    if DNO_boton["btn_atras"] is not None:
        DNO_boton["btn_atras"].place_forget()
        DNO_boton["btn_atras"] = None
    if DNO_boton["btn_siguiente"] is not None:
        DNO_boton["btn_siguiente"].place_forget()
        DNO_boton["btn_siguiente"] = None
    
    # Generar la nueva tabla:
    # si o si deberia entrar aqui porque eso quiere decir que las taxonomias
    # superaron los 6 valores.
    # el Contador_Valores debe estar en 1 la primera vez que entre aca.
    df_expotax_1 = listas_divididas_df_expotax[Contador_Valores]              # obtiene entonces los otros dataframes de valores
    df_expotax_1 = df_expotax_1.reset_index(drop=True)
    
    
    for index in range(len(df_expotax_1)):
        VarName_TC = "tbl_TC" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_TC)
        VarName_DS1 = "tbl_DS1_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS1)
        VarName_DS1_prc = "tbl_DS1_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS1_prc)
        VarName_DS2 = "tbl_DS2_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS2)
        VarName_DS2_prc = "tbl_DS2_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS2_prc)
        VarName_DS3 = "tbl_DS3_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS3)
        VarName_DS3_prc = "tbl_DS3_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS3_prc)
        VarName_DS4 = "tbl_DS4_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS4)
        VarName_DS4_prc = "tbl_DS4_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS4_prc)
        VarName_DS5 = "tbl_DS5_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS5)
        VarName_DS5_prc = "tbl_DS5_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS5_prc)
    
    for tbl in table_DNO:
        DNO_table[tbl] = None
    
    Contador_Valores_lambda = danos_lib.Gen_Elements_Tax(df_expotax_1,DNO_table,DNO_boton,Contador_Valores)
    
    # Aca entonces se crea el boton que direccione a la siguiente parte de la tabla si existe:
    # Entra entonces un condicional
    
    # Cuando hay mas valores en la lista
    if len(listas_divididas_df_expotax) > Contador_Valores_lambda+1: # Si la longitud de la lista es mayor al contador + 1 se crea un boton nuevo
        # El contados aumenta una unidad para entrar a la otra lista
        Contador_Valores = Contador_Valores_lambda+1
        # En el boton siguiente se redirecciona a esta misma funcion
        DNO_boton["btn_siguiente"] = wnfun_lib.Button_Image_lambda('/PAE_Siguiente.png', 
                            50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333,ChangeTo_DNOTxn_Next,Contador_Valores)
        # el boton de ir hacia atras debe si o si estar creado. Si llega hasta acá 
        # hay que saber que si o si hubo datos antes
        
    # Si no pasa eso entonces se borra el boton de siguiente o se deja inhabilitado        
    else:
        DNO_boton["btn_siguiente"] = wnfun_lib.Label_Image('/PAE_Siguiente_Inh.png', 
                                50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333)

    # Para crear el boton de atras al contador se le resta una unidad.
    Contador_Valores = Contador_Valores_lambda-1
    # Si el contador de valores nuevo es 0, entra a otra definicion, si no lo es
    # retorna a esta definicion
    if Contador_Valores == 0:
        DNO_boton["btn_atras"] = wnfun_lib.Button_Image_lambda('/PAE_Atras_Slc.png', 
            50, 40, cnt_container,"white",pos_x+0.334,pos_y-0.333,ChangeTo_DNOTxn_Cero,Contador_Valores)
    else:
        DNO_boton["btn_atras"] = wnfun_lib.Button_Image_lambda('/PAE_Atras_Slc.png', 
            50, 40, cnt_container,"white",pos_x+0.334,pos_y-0.333,ChangeTo_DNOTxn_Next,Contador_Valores)

"""----------------------------------------------------------------------------

             TERCERA FUNCION: VOLVER A LOS RESULTADOS ANTERIORES
             
En esta tercera función se muestran los resultados por taxonomia de los resul-
tados anteriores del conjunto de datos. Contiene:
    1. Tabla resultados por tipologia                                     [x]
    2. Boton siguiente y atras (habilitado si hay más de 6 tipologías y  
       para regresar a los resultados anteriores)                         [x]
    3. Boton representacion grafica de resultados por taxonomia           [x]
    4. Boton exportar resultados                                          [x]
    5. Boton regresar a resultados del municipio                          [x]

----------------------------------------------------------------------------"""

def ChangeTo_DNOTxn_Cero(Contador_Valores):
    
    # Aqui entra si o si. la cosa es si hay mas listas divididas para mostrar
    
    # Eliminar el contenido de la tabla anterior
    
    for tbl in table_DNO:
        if DNO_table[tbl] is not None:
            DNO_table[tbl].place_forget()
            DNO_table[tbl] = None
    
    # Elimina boton atras y siguiente
    if DNO_boton["btn_atras"] is not None:
        DNO_boton["btn_atras"].place_forget()
        DNO_boton["btn_atras"] = None
    if DNO_boton["btn_siguiente"] is not None:
        DNO_boton["btn_siguiente"].place_forget()
        DNO_boton["btn_siguiente"] = None
        
    # Generar la nueva tabla:
    # si o si deberia entrar aqui porque eso quiere decir que las taxonomias
    # superaron los 6 valores.
    # el Contador_Valores debe estar en 1 la primera vez que entre aca.
    df_expotax_1 = listas_divididas_df_expotax[Contador_Valores]              # obtiene entonces los otros dataframes de valores
    df_expotax_1 = df_expotax_1.reset_index(drop=True)
    
    
    for index in range(len(df_expotax_1)):
        VarName_TC = "tbl_TC" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_TC)
        VarName_DS1 = "tbl_DS1_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS1)
        VarName_DS1_prc = "tbl_DS1_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS1_prc)
        VarName_DS2 = "tbl_DS2_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS2)
        VarName_DS2_prc = "tbl_DS2_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS2_prc)
        VarName_DS3 = "tbl_DS3_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS3)
        VarName_DS3_prc = "tbl_DS3_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS3_prc)
        VarName_DS4 = "tbl_DS4_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS4)
        VarName_DS4_prc = "tbl_DS4_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS4_prc)
        VarName_DS5 = "tbl_DS5_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS5)
        VarName_DS5_prc = "tbl_DS5_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS5_prc)
    
    for tbl in table_DNO:
        DNO_table[tbl] = None
    
    Contador_Valores_lambda = danos_lib.Gen_Elements_Tax(df_expotax_1,DNO_table,DNO_boton,Contador_Valores)
    
    # Aca entonces se crea el boton que direccione a la siguiente parte de la tabla si existe:
    # Entra entonces un condicional
    
    # Cuando hay mas valores en la lista
    if len(listas_divididas_df_expotax) > Contador_Valores_lambda+1: # Si la longitud de la lista es mayor al contador + 1 se crea un boton nuevo
        # El contados aumenta una unidad para entrar a la otra lista
        Contador_Valores = Contador_Valores_lambda+1
        # En el boton siguiente se redirecciona a esta misma funcion
        DNO_boton["btn_siguiente"] = wnfun_lib.Button_Image_lambda('/PAE_Siguiente.png', 
                            50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333,ChangeTo_DNOTxn_Next,Contador_Valores)
        # el boton de ir hacia atras debe si o si estar creado. Si llega hasta acá 
        # hay que saber que si o si hubo datos antes
        
    # Si no pasa eso entonces se borra el boton de siguiente o se deja inhabilitado        
    else:
        DNO_boton["btn_siguiente"] = wnfun_lib.Label_Image('/PAE_Siguiente_Inh.png', 
                                50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333)
        
    DNO_boton["btn_atras"] = wnfun_lib.Label_Image('/PAE_Atras.png', 
                             50, 40, cnt_container,"white",pos_x+0.334,pos_y-0.333)

"""----------------------------------------------------------------------------

        CUARTA FUNCION: MOSTRAR REPRESENTACION GRAFICA DE RESULTADOS
             
En esta cuarta función se muestran los resultados por taxonomia representada
con un diagrama de barras. Contiene:
    1. Diagrama de barras porcentaje de edificaciones en estado de daño   [x]
    2. Tabla de taxonomías                                                [x]
    3. Boton resultados tabla por taxonomía                               [x]
    4. Boton exportar resultados                                          [x]
    5. Boton regresar a resultados del municipio                          [x]

----------------------------------------------------------------------------"""

def GoTo_DNO_Diag():
    
    # .........................................................................
    #               PREPARAR ESCENARIO PARA INSERTAR DIAGRAMA
    #   Muestra el diagrama de porcentaje de edificaciones en estado de daño
    # .........................................................................
    
    # ------- Eliminar tabla y contenido de la tabla --------------------------
    # Elimina contenido de la tabla
    for tbl in table_DNO:
        if DNO_table[tbl] is not None:
            DNO_table[tbl].place_forget()
            DNO_table[tbl] = None
    # Elimina la tabla
    if DNO_boton["tbl_CP_DNO"] is not None:
        DNO_boton["tbl_CP_DNO"].place_forget()
        DNO_boton["tbl_CP_DNO"] = None
    # Elimina boton atras y siguiente
    if DNO_boton["btn_atras"] is not None:
        DNO_boton["btn_atras"].place_forget()
        DNO_boton["btn_atras"] = None
    if DNO_boton["btn_siguiente"] is not None:
        DNO_boton["btn_siguiente"].place_forget()
        DNO_boton["btn_siguiente"] = None
    # Elimina exportar elementos
    if DNO_boton["btn_exp_DNO"] is not None:
        DNO_boton["btn_exp_DNO"].place_forget()
        DNO_boton["btn_exp_DNO"] = None
    if DNO_boton["btn_exp2_DNO"] is not None:
        DNO_boton["btn_exp2_DNO"].place_forget()
        DNO_boton["btn_exp2_DNO"] = None
    # Elimina regresar a tabla por taxonomia
    if DNO_boton["btn_diag_DNO"] is not None:
        DNO_boton["btn_diag_DNO"].place_forget()
        DNO_boton["btn_diag_DNO"] = None
    # Elimina regresar a resultados municipio
    if DNO_boton["btn_cbm_DNO"] is not None:
        DNO_boton["btn_cbm_DNO"].place_forget()
        DNO_boton["btn_cbm_DNO"] = None
    
    # ------- Insertar diagrama -----------------------------------------------
    if DNO_canva["cnv_dgm_DNO"] is None:
        DNO_canva["cnv_dgm_DNO"] = wnfun_lib.Figura_taxonomias_DNO(taxonomias,
                                       aggrisk_mnz_DNO,cnt_container,0.39,0.62)
    # ------- Insertar tabla de convenciones ----------------------------------
    if DNO_boton["lbl_lyd_DNO"] is None:
        DNO_boton["lbl_lyd_DNO"] = wnfun_lib.Label_Image('/Leyenda_DNO.png', 
                                505, 65, cnt_container,"white",0.42,0.255)
    # ------- Insertar tabla de taxonomias -----------------------------------
    global tblTaxo_DNO,tblTaxo_Num
    if len(taxonomias) <= 16:
        if DNO_boton["tbl_txn_DNO"] is None:
            DNO_boton["tbl_txn_DNO"] = wnfun_lib.Label_Image('/Tabla_Diag_Taxo.png', 
                                    320, 272, cnt_container,"white",0.83,0.55)
        # Generar variables para insertar en tabla
        tblTaxo_DNO, tblTaxo_Num = [], []
        for index in range(len(taxonomias)):
            tblTaxo_DNO.append("tbl_taxo"+str(index+1))
            tblTaxo_Num.append("tbl_Num"+str(index+1))
        for tbl in tblTaxo_DNO:
            DNO_tblTaxo[tbl] = None
        
        # Empezar a colocar variables
        suma = 0
        for index, txn in enumerate(taxonomias):
            if index%2 == 0: # Cuando el indice es par muestra taxonomia en indice impar
                DNO_tblTaxo[tblTaxo_DNO[index]] = tk.Label(DNO_boton["tbl_txn_DNO"], text=str(txn), 
                                    font=("Abadi MT", 8), bg="#E7E6E6", fg="#000000")
                DNO_tblTaxo[tblTaxo_DNO[index]].place(relx=0.31, rely=0.168+suma, anchor=tk.CENTER)
                
                DNO_tblTaxo[tblTaxo_Num[index]] = tk.Label(DNO_boton["tbl_txn_DNO"], text=str(index+1), 
                                    font=("Abadi MT", 9,"bold"), bg="#274151", fg="white")
                DNO_tblTaxo[tblTaxo_Num[index]].place(relx=0.058, rely=0.168+suma, anchor=tk.CENTER)
                
            else:
                DNO_tblTaxo[tblTaxo_DNO[index]] = tk.Label(DNO_boton["tbl_txn_DNO"], text=str(txn), 
                                    font=("Abadi MT", 8), bg="#E7E6E6", fg="#000000")
                DNO_tblTaxo[tblTaxo_DNO[index]].place(relx=0.81, rely=0.114+suma, anchor=tk.CENTER)
                
                DNO_tblTaxo[tblTaxo_Num[index]] = tk.Label(DNO_boton["tbl_txn_DNO"], text=str(index+1), 
                                    font=("Abadi MT", 9,"bold"), bg="#274151", fg="white")
                DNO_tblTaxo[tblTaxo_Num[index]].place(relx=0.558, rely=0.114+suma, anchor=tk.CENTER)
                
            suma = suma + 0.054
        
    elif len(taxonomias) > 16 and len(taxonomias) <= 24:
        if DNO_boton["tbl_txn2_DNO"] is None:
            DNO_boton["tbl_txn2_DNO"] = wnfun_lib.Label_Image('/Tabla_Diag_Taxo2.png', 
                                    320, 410, cnt_container,"white",0.83,0.55)
        
        # Generar variables para insertar en tabla
        tblTaxo_DNO, tblTaxo_Num = [], []
        for index in range(len(taxonomias)):
            tblTaxo_DNO.append("tbl_taxo"+str(index+1))
            tblTaxo_Num.append("tbl_Num"+str(index+1))
        for tbl in tblTaxo_DNO:
            DNO_tblTaxo[tbl] = None
        
        # Empezar a colocar variables
        suma = 0
        print(taxonomias)
        for index, txn in enumerate(taxonomias):
            if index%2 == 0: # Cuando el indice es par muestra taxonomia en indice impar
                DNO_tblTaxo[tblTaxo_DNO[index]] = tk.Label(DNO_boton["tbl_txn2_DNO"], text=str(txn), 
                                    font=("Abadi MT", 8), bg="#E7E6E6", fg="#000000")
                DNO_tblTaxo[tblTaxo_DNO[index]].place(relx=0.31, rely=0.120+suma, anchor=tk.CENTER)
                
                DNO_tblTaxo[tblTaxo_Num[index]] = tk.Label(DNO_boton["tbl_txn2_DNO"], text=str(index+1), 
                                    font=("Abadi MT", 9,"bold"), bg="#274151", fg="white")
                DNO_tblTaxo[tblTaxo_Num[index]].place(relx=0.058, rely=0.120+suma, anchor=tk.CENTER)
            else:
                DNO_tblTaxo[tblTaxo_DNO[index]] = tk.Label(DNO_boton["tbl_txn2_DNO"], text=str(txn), 
                                    font=("Abadi MT", 8), bg="#E7E6E6", fg="#000000")
                DNO_tblTaxo[tblTaxo_DNO[index]].place(relx=0.81, rely=0.0825+suma, anchor=tk.CENTER)
                
                DNO_tblTaxo[tblTaxo_Num[index]] = tk.Label(DNO_boton["tbl_txn2_DNO"], text=str(index+1), 
                                    font=("Abadi MT", 9,"bold"), bg="#274151", fg="white")
                DNO_tblTaxo[tblTaxo_Num[index]].place(relx=0.558, rely=0.0825+suma, anchor=tk.CENTER)
                
            suma = suma + 0.0375

    elif len(taxonomias) > 24:
        if DNO_boton["tbl_txn3_DNO"] is None:
            DNO_boton["tbl_txn3_DNO"] = wnfun_lib.Label_Image('/Tabla_Diag_Taxo3.png', 
                                    320, 537, cnt_container,"white",0.83,0.60)
        
        # Generar variables para insertar en tabla
        tblTaxo_DNO, tblTaxo_Num = [], []
        for index in range(len(taxonomias)):
            tblTaxo_DNO.append("tbl_taxo"+str(index+1))
            tblTaxo_Num.append("tbl_Num"+str(index+1))
        for tbl in tblTaxo_DNO:
            DNO_tblTaxo[tbl] = None
        
        # Empezar a colocar variables
        suma = 0
        print(taxonomias)
        for index, txn in enumerate(taxonomias):
            if index%2 == 0: # Cuando el indice es par muestra taxonomia en indice impar
                DNO_tblTaxo[tblTaxo_DNO[index]] = tk.Label(DNO_boton["tbl_txn3_DNO"], text=str(txn), 
                                    font=("Abadi MT", 8), bg="#E7E6E6", fg="#000000")
                DNO_tblTaxo[tblTaxo_DNO[index]].place(relx=0.31, rely=0.091+suma, anchor=tk.CENTER)
                
                DNO_tblTaxo[tblTaxo_Num[index]] = tk.Label(DNO_boton["tbl_txn3_DNO"], text=str(index+1), 
                                    font=("Abadi MT", 9,"bold"), bg="#274151", fg="white")
                DNO_tblTaxo[tblTaxo_Num[index]].place(relx=0.058, rely=0.091+suma, anchor=tk.CENTER)
            else:
                DNO_tblTaxo[tblTaxo_DNO[index]] = tk.Label(DNO_boton["tbl_txn3_DNO"], text=str(txn), 
                                    font=("Abadi MT", 8), bg="#E7E6E6", fg="#000000")
                DNO_tblTaxo[tblTaxo_DNO[index]].place(relx=0.81, rely=0.0623+suma, anchor=tk.CENTER)
                
                DNO_tblTaxo[tblTaxo_Num[index]] = tk.Label(DNO_boton["tbl_txn3_DNO"], text=str(index+1), 
                                    font=("Abadi MT", 9,"bold"), bg="#274151", fg="white")
                DNO_tblTaxo[tblTaxo_Num[index]].place(relx=0.558, rely=0.0623+suma, anchor=tk.CENTER)
                
            suma = suma + 0.0287
        
    # ------- Boton volver a tabla de taxonomias ------------------------------
    if DNO_boton["btn_diag_DNO"] is None:
        DNO_boton["btn_diag_DNO"] = wnfun_lib.Button_Image('/GoTo_DNO_tabla.png', 
                                150, 60, cnt_container,"white",0.13,0.260,ChangeTo_DNOTxn_Inicio)
    
    # ---- Cambiar a resultados del municipio ---------------------------------
    DNO_boton["btn_cbm_DNO"] = wnfun_lib.Button_Image('/GoTo_DNO_CP.png', 268, 45, 
                                    cnt_container,"white",0.82,0.94,GoTo_DNO_CP)
    
    ## .............................................................
    # ---- Exportar resultados:
    if DNO_boton["btn_exp_DNO"] is None:
        DNO_boton["btn_exp_DNO"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    # .............................................................
    #          GENERAR TODOS LOS RESULTADOS PARA EXPORTAR 
    #             Todos los resultados menos los mapas
    # .............................................................
    Table_DNO_CP = wnfun_lib.Gen_Tabla_Resume_DNO(Num_build,aggrisk_resu)
    Table_DNO_Txn = wnfun_lib.Gen_Tabla_taxonomia_DNO(df_expotax_DNO)
    Figura_DNO_Txn = wnfun_lib.Figura_taxonomias_DNO_Export(taxonomias,aggrisk_mnz_DNO)
    # .............................................................

    if DNO_boton["btn_exp2_DNO"] is None:
        DNO_boton["btn_exp2_DNO"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", 
         command=lambda:wnfun_lib.ExportarResultados_Event_Based_Damage(Table_DNO_CP,Table_DNO_Txn,Figura_DNO_Txn))
        DNO_boton["btn_exp2_DNO"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)

"""----------------------------------------------------------------------------

          QUINTA FUNCION: VOLVER A RESULTADOS TABLA POR TAXONOMIA
             
En esta quinta función se muestran los resultados por taxonomia. Contiene:
    1. Tabla resultados por tipologia                                     [x]
    2. Boton siguiente y atras (habilitado si hay más de 6 tipologías)    [x]
    3. Boton representacion grafica de resultados por taxonomia           [x]
    4. Boton exportar resultados                                          [x]
    5. Boton regresar a resultados del municipio                          [x]

----------------------------------------------------------------------------"""

def ChangeTo_DNOTxn_Inicio():
    
    Contador_Valores = 0
    # Eliminar el contenido de la tabla anterior
    
    for tbl in table_DNO:
        if DNO_table[tbl] is not None:
            DNO_table[tbl].place_forget()
            DNO_table[tbl] = None
    
    for tbl in tblTaxo_DNO:
        if DNO_tblTaxo[tbl] is not None:
            DNO_tblTaxo[tbl].place_forget()
            DNO_tblTaxo[tbl] = None
    
    if DNO_boton["btn_diag_DNO"] is not None:
        DNO_boton["btn_diag_DNO"].place_forget()
        DNO_boton["btn_diag_DNO"] = None
    
    if DNO_canva["cnv_dgm_DNO"] is not None:
        DNO_canva["cnv_dgm_DNO"].get_tk_widget().destroy()
        DNO_canva["cnv_dgm_DNO"] = None
    
    if DNO_boton["lbl_lyd_DNO"] is not None:
        DNO_boton["lbl_lyd_DNO"].place_forget()
        DNO_boton["lbl_lyd_DNO"] = None
    
    if DNO_boton["tbl_txn_DNO"] is not None:
        DNO_boton["tbl_txn_DNO"].place_forget()
        DNO_boton["tbl_txn_DNO"] = None
    
    if DNO_boton["btn_atras"] is not None:
        DNO_boton["btn_atras"].place_forget()
        DNO_boton["btn_atras"] = None
    if DNO_boton["btn_siguiente"] is not None:
        DNO_boton["btn_siguiente"].place_forget()
        DNO_boton["btn_siguiente"] = None
    
    # Generar la nueva tabla:
        
    if DNO_boton["tbl_CP_DNO"]  is None:
        DNO_boton["tbl_CP_DNO"]  = wnfun_lib.Label_Image('/Tabla_Dano_Txn.png', 
                                 991, 450, cnt_container,"white",pos_x,pos_y)
        
    # si o si deberia entrar aqui porque eso quiere decir que las taxonomias
    # superaron los 6 valores.
    # el Contador_Valores debe estar en 1 la primera vez que entre aca.
    df_expotax_1 = listas_divididas_df_expotax[Contador_Valores]              # obtiene entonces los otros dataframes de valores
    df_expotax_1 = df_expotax_1.reset_index(drop=True)
    
    
    for index in range(len(df_expotax_1)):
        VarName_TC = "tbl_TC" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_TC)
        VarName_DS1 = "tbl_DS1_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS1)
        VarName_DS1_prc = "tbl_DS1_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS1_prc)
        VarName_DS2 = "tbl_DS2_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS2)
        VarName_DS2_prc = "tbl_DS2_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS2_prc)
        VarName_DS3 = "tbl_DS3_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS3)
        VarName_DS3_prc = "tbl_DS3_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS3_prc)
        VarName_DS4 = "tbl_DS4_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS4)
        VarName_DS4_prc = "tbl_DS4_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS4_prc)
        VarName_DS5 = "tbl_DS5_" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS5)
        VarName_DS5_prc = "tbl_DS5_prc" + str(index+1)+str(Contador_Valores)
        table_DNO.append(VarName_DS5_prc)
    
    for tbl in table_DNO:
        DNO_table[tbl] = None
    
    Contador_Valores_lambda = danos_lib.Gen_Elements_Tax(df_expotax_1,DNO_table,DNO_boton,Contador_Valores)
    
    # Aca entonces se crea el boton que direccione a la siguiente parte de la tabla si existe:
    # Entra entonces un condicional
    
    # Cuando hay mas valores en la lista
    if len(listas_divididas_df_expotax) > Contador_Valores_lambda+1: # Si la longitud de la lista es mayor al contador + 1 se crea un boton nuevo
        # El contados aumenta una unidad para entrar a la otra lista
        Contador_Valores = Contador_Valores_lambda+1
        # En el boton siguiente se redirecciona a esta misma funcion
        DNO_boton["btn_siguiente"] = wnfun_lib.Button_Image_lambda('/PAE_Siguiente.png', 
                            50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333,ChangeTo_DNOTxn_Next,Contador_Valores)
        # el boton de ir hacia atras debe si o si estar creado. Si llega hasta acá 
        # hay que saber que si o si hubo datos antes
        
    # Si no pasa eso entonces se borra el boton de siguiente o se deja inhabilitado        
    else:
        DNO_boton["btn_siguiente"] = wnfun_lib.Label_Image('/PAE_Siguiente_Inh.png', 
                                50, 40, cnt_container,"white",pos_x+0.379,pos_y-0.333)
        
    DNO_boton["btn_atras"] = wnfun_lib.Label_Image('/PAE_Atras.png', 
                             50, 40, cnt_container,"white",pos_x+0.334,pos_y-0.333)
    
    # ---- Cambiar a diagrama de taxonomias -----------------------------------
    if DNO_boton["btn_diag_DNO"] is None:
        DNO_boton["btn_diag_DNO"] = wnfun_lib.Button_Image('/GoTo_DNO_Diag.png', 
                                160, 60, cnt_container,"white",0.5,0.252,GoTo_DNO_Diag)

def GoTo_DNO_CP():
    
    if table_DNO is not None:
        for tbl in table_DNO:
            if DNO_table[tbl] is not None:
                DNO_table[tbl].place_forget()
                DNO_table[tbl] = None
    
    if tblTaxo_DNO is not None:
        for tbl in tblTaxo_DNO:
            if DNO_tblTaxo[tbl] is not None:
                DNO_tblTaxo[tbl].place_forget()
                DNO_tblTaxo[tbl] = None
            
    Function_Danos(resultado_label_DNO)
#%% ====== FUNCION >> SALIDA GEOGRAFICA OCUPANTES COLAPSOS ====================

def Salida_Geografica_DNO(tipo_calculo,map_data,variable):

    
    # =========================================================================
    #  1. Preparar escenario 
    # =========================================================================
    
    for tlt in title_DNO:
        if DNO_title[tlt] is not None:
            DNO_title[tlt].place_forget()
            DNO_title[tlt] = None
            
    for txt in text_DNO:
        if DNO_text[txt] is not None:
            DNO_text[txt].place_forget()
            DNO_text[txt] = None
            
    for btn in boton_DNO:
        if DNO_boton[btn] is not None:
            DNO_boton[btn].place_forget()
            DNO_boton[btn] = None
            
    for cnv in canva_DNO:
        if DNO_canva[cnv] is not None:
            DNO_canva[cnv].get_tk_widget().destroy()
            DNO_canva[cnv] = None
    
    if table_DNO is not None:
        for tbl in table_DNO:
            if DNO_table[tbl] is not None:
                DNO_table[tbl].place_forget()
                DNO_table[tbl] = None
    
    if tblTaxo_DNO is not None:
        for tbl in tblTaxo_DNO:
            if DNO_tblTaxo[tbl] is not None:
                DNO_tblTaxo[tbl].place_forget()
                DNO_tblTaxo[tbl] = None
    
    # =========================================================================
    #  2. Preparar escenario 
    # =========================================================================
    
    # -------- Frame resultados -----------------------------------------------
    if DNO_boton["lbl_rst_DNO"] is None:
        DNO_boton["lbl_rst_DNO"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
    # -------- Design frame ---------------------------------------------------
    if DNO_boton["lbl_DsF_DNO"] is None:
        DNO_boton["lbl_DsF_DNO"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
    
    # -------- Title Section --------------------------------------------------
    if DNO_text["tlt_sct_DNO"] is None:
        DNO_text["tlt_sct_DNO"] = tk.Label(cnt_container, text="Resultados de Daño Basado en Eventos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
        DNO_text["tlt_sct_DNO"].place(relx=0.243, rely=0.072, anchor=tk.CENTER)
    if DNO_text["tlt_sct_DNO1"] is None:
        if calculation_mode_DNO == "Probabilistico":
            DNO_text["tlt_sct_DNO1"] = tk.Label(cnt_container, text="Eventos probabilísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            DNO_text["tlt_sct_DNO1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
        else:
            DNO_text["tlt_sct_DNO1"] = tk.Label(cnt_container, text="Eventos determinísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            DNO_text["tlt_sct_DNO1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
    # -------- Frame Results Title --------------------------------------------
    if DNO_boton["lbl_rstv2_DNO"] is None:
        DNO_boton["lbl_rstv2_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
    if DNO_boton["lbl_rstv3_DNO"] is None:
        DNO_boton["lbl_rstv3_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.304)
    if DNO_boton["lbl_rstv4_DNO"] is None:
        DNO_boton["lbl_rstv4_DNO"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 38, 58, cnt_container,"white",0.025,0.24)
    # -------- Results Title --------------------------------------------------
    if DNO_text["tlt_rstv2_DNO"] is None:
        DNO_text["tlt_rstv2_DNO"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name_DNO, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
        DNO_text["tlt_rstv2_DNO"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
        
    # =========================================================================
    #  3. Colocar el mapa con configuracion predeterminada
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # -------- Poner en la pagina el mapa -------------------------------------
    # -------------------------------------------------------------------------
    
    if DNO_canva["cnv_homeless_DNO"] is None:
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................
        Separa_x = 1
        Separa_y = 1 
        
        User_min_lon = -0.04
        User_max_lon = 0.02 
        
        User_min_lat = -0.02
        User_max_lat = 0.02
        # .....................................................................
        
        if tipo_calculo == 1:
            DNO_canva["cnv_homeless_DNO"] = wnfun_lib.canva_DNO_ocupantes_mnz(COD_mun_DNO,CP_Name_DNO,manzana_shp_DNO,seccion_shp_DNO,area_shp_DNO,map_data,Modelo_Expo2_DNO,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable)
        else:
            DNO_canva["cnv_homeless_DNO"] = wnfun_lib.canva_DNO_ocupantes_scc(COD_mun_DNO,CP_Name_DNO,seccion_shp_DNO,area_shp_DNO,map_data,Modelo_Expo2_DNO,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable)
            
            
    # -------------------------------------------------------------------------
    # -------- Poner modificacion del mapa ------------------------------------
    # -------------------------------------------------------------------------
    
    if DNO_boton['lbl_mdm_DNO'] is None:
        DNO_boton['lbl_mdm_DNO'] = wnfun_lib.Label_Image('/Modificar_Mapa.png', 
                                        250, 330, cnt_container,"white",0.106,0.57)
        
    opciones_PRD = [-4,-3,-2,-1,0,1,2,3,4]
    opciones2_PRD = [0,1,2,3,4,5]
    
    # 1. Selección de kilometros de separacion latitudinal 
    if DNO_boton["cmb_lon"] is None:
        DNO_boton["cmb_lon"] = ttk.Combobox(DNO_boton['lbl_mdm_DNO'],
                                                values=opciones2_PRD)
        DNO_boton["cmb_lon"].place(relx=0.816, rely=0.20, 
                            anchor=tk.CENTER, width=40, height=20)
    # 2. Selección de kilometros de separacion longitudinal 
    if DNO_boton["cmb_lat"] is None:
        DNO_boton["cmb_lat"] = ttk.Combobox(DNO_boton['lbl_mdm_DNO'],
                                                values=opciones2_PRD)
        DNO_boton["cmb_lat"].place(relx=0.77, rely=0.285, 
                            anchor=tk.CENTER, width=40, height=20)
    # 3. Selección de kilometros de limite oeste 
    if DNO_boton["cmb_min_lon"] is None:
        DNO_boton["cmb_min_lon"] = ttk.Combobox(DNO_boton['lbl_mdm_DNO'],
                                                values=opciones_PRD)
        DNO_boton["cmb_min_lon"].place(relx=0.62, rely=0.375, 
                            anchor=tk.CENTER, width=40, height=20)
    # 4. Selección de kilometros de limite este 
    if DNO_boton["cmb_max_lon"] is None:
        DNO_boton["cmb_max_lon"] = ttk.Combobox(DNO_boton['lbl_mdm_DNO'],
                                                values=opciones_PRD)
        DNO_boton["cmb_max_lon"].place(relx=0.59, rely=0.465, 
                            anchor=tk.CENTER, width=40, height=20)
    # 5. Selección de kilometros de limite norte 
    if DNO_boton["cmb_max_lat"] is None:
        DNO_boton["cmb_max_lat"] = ttk.Combobox(DNO_boton['lbl_mdm_DNO'],
                                                values=opciones_PRD)
        DNO_boton["cmb_max_lat"].place(relx=0.607, rely=0.545, 
                            anchor=tk.CENTER, width=40, height=20)
    # 6. Selección de kilometros de limite sur 
    if DNO_boton["cmb_min_lat"] is None:
        DNO_boton["cmb_min_lat"] = ttk.Combobox(DNO_boton['lbl_mdm_DNO'],
                                                values=opciones_PRD)
        DNO_boton["cmb_min_lat"].place(relx=0.572, rely=0.64, 
                            anchor=tk.CENTER, width=40, height=20)        
    
    # -------------------------------------------------------------------------
    # -------- Agregar ajustes al mapa ----------------------------------------
    # -------------------------------------------------------------------------
    
    if DNO_boton["btn_ajs_DNO"] is None:
        DNO_boton["btn_ajs_DNO"] = wnfun_lib.Button_Image_lambda3('/Aplicar_Ajustes.png', 
                144, 40, cnt_container,"white",0.106,0.70,ConfigMap_DNO,tipo_calculo,map_data,variable)
        
    # -------------------------------------------------------------------------
    # -------- Reiniciar los ajustes ------------------------------------------
    # -------------------------------------------------------------------------

    if DNO_boton["btn_rin_DNO"] is None:
        DNO_boton["btn_rin_DNO"] = wnfun_lib.Button_Image_lambda3('/Reiniciar_Ajustes.png', 
                157, 42, cnt_container,"white",0.106,0.748,ResetConfigMap_DNO,tipo_calculo,map_data,variable)
    
    # -------------------------------------------------------------------------
    # ---- Cambiar a resultados del municipio ---------------------------------
    # -------------------------------------------------------------------------

    DNO_boton["btn_cbm_DNO"] = wnfun_lib.Button_Image('/GoTo_DNO_CP.png', 268, 45, 
                                    cnt_container,"white",0.82,0.94,GoTo_DNO_CP)
        
    # -------------------------------------------------------------------------
    # -------- Resultados por seccion/manzana ---------------------------------
    # -------------------------------------------------------------------------

    # La primera vez que entra se debe mostrar resultados por seccion
    
    if tipo_calculo == 1:
        if DNO_boton["btn_scc_DNO"] is None:
            tipo_calculo = 2
            if variable.startswith("aac") and variable.endswith("hab"):
                variable2 = 'aac_secc_urb_colapso_hab'
                map_data2 = mapdata_homeless_scc
            elif variable.startswith("aac") and variable.endswith("edis"):
                variable2 = 'aac_secc_urb_colapso_no_edis'
                map_data2 = mapdata_collapsed_scc
            elif variable.startswith("aad") and variable.endswith("heridos_hab"):
                variable2 = 'aad_secc_urb_heridos_hab'
                map_data2 = mapdata_injured_scc
            elif variable.startswith("aad") and variable.endswith("fallecidos_hab"):
                variable2 = 'aad_secc_urb_fallecidos_hab'
                map_data2 = mapdata_fatalities_scc
            
            DNO_boton["btn_scc_DNO"] = wnfun_lib.Button_Image_lambda3('/Visualizar_Seccion_PRD.png', 
                    170, 60, cnt_container,"white",0.12,0.28,Salida_Geografica_DNO,tipo_calculo,map_data2,variable2)
    else:
        if DNO_boton["btn_scc_DNO"] is None:
            tipo_calculo = 1
            if variable.startswith("aac") and variable.endswith("hab"):
                variable2 = 'aac_mnz_urb_colapso_hab'
                map_data2 = mapdata_homeless
            elif variable.startswith("aac") and variable.endswith("edis"):
                variable2 = 'aac_mnz_colapso_no_edis'
                map_data2 = mapdata_collapsed
            elif variable.startswith("aad") and variable.endswith("heridos_hab"):
                variable2 = 'aad_mnz_heridos_hab'
                map_data2 = mapdata_injured
            elif variable.startswith("aad") and variable.endswith("fallecidos_hab"):
                variable2 = 'aad_mnz_fallecidos_hab'
                map_data2 = mapdata_fatalities
            
            DNO_boton["btn_scc_DNO"] = wnfun_lib.Button_Image_lambda3('/Visualizar_mnz_PRD.png', 
                    170, 60, cnt_container,"white",0.12,0.28,Salida_Geografica_DNO,tipo_calculo,map_data2,variable2)
    
    # .........................................................................
    # ---- Exportar resultados:
    if DNO_boton['btn_exp_DNO'] is not None:
        DNO_boton['btn_exp_DNO'].place_forget()
        DNO_boton['btn_exp_DNO']  = None
    if DNO_boton['btn_exp2_DNO'] is not None:
        DNO_boton['btn_exp2_DNO'].place_forget()
        DNO_boton['btn_exp2_DNO']  = None
    
    if DNO_boton["btn_exp_DNO"] is None:
        DNO_boton["btn_exp_DNO"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if DNO_boton["btn_exp2_DNO"] is None:
        DNO_boton["btn_exp2_DNO"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", 
        command=lambda:wnfun_lib.ExportarMapa_Event_Based_Damage(DNO_canva["cnv_homeless_DNO"],"Figura"+str(variable)+".jpg"))
        DNO_boton["btn_exp2_DNO"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
    # .........................................................................
    
#%% ====== FUNCION >> AGREGAR/RESETEAR CONFIGURACION DEL MAPA DANOS MNZ =======

def ConfigMap_DNO(tipo_calculo,map_data,variable):
    
    for cnv in canva_DNO:
        if DNO_canva[cnv] is not None:
            DNO_canva[cnv].get_tk_widget().destroy()
            DNO_canva[cnv] = None
            
    # --------- Verificar separacion horizontal -------------------------------
    if DNO_boton["cmb_lon"].get() == '':
        cmb_lon = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación horizontal/longitud")
    else:
        cmb_lon = int(DNO_boton["cmb_lon"].get())
    # --------- Verificar separacion vertical ---------------------------------    
    if DNO_boton["cmb_lat"].get() == '':
        cmb_lat = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación vertical/latitud")
    else:
        cmb_lat = int(DNO_boton["cmb_lat"].get())
    # --------- Verificar limite oeste ----------------------------------------
    if DNO_boton["cmb_min_lon"].get() == '':
        cmb_min_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al oeste del mapa")
    else:
        cmb_min_lon = int(DNO_boton["cmb_min_lon"].get())
    # --------- Verificar limite este -----------------------------------------    
    if DNO_boton["cmb_max_lon"].get() == '':
        cmb_max_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al este del mapa")
    else:
        cmb_max_lon = int(DNO_boton["cmb_max_lon"].get())
    # --------- Verificar limite norte ----------------------------------------    
    if DNO_boton["cmb_max_lat"].get() == '':
        cmb_max_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al norte del mapa")
    else:
        cmb_max_lat = int(DNO_boton["cmb_max_lat"].get())
    # --------- Verificar limite sur ------------------------------------------    
    if DNO_boton["cmb_min_lat"].get() == '':
        cmb_min_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al sur del mapa")
    else:
        cmb_min_lat = int(DNO_boton["cmb_min_lat"].get())
    
    if cmb_lon is not None and cmb_lat is not None and cmb_min_lon is not None and cmb_max_lon is not None and cmb_min_lat is not None and cmb_max_lat is not None:
        # Entra aca cuando el usuario hace uso del modificador de mapa 
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................        
        User_min_lon_defecto = -0.04
        User_max_lon_defecto = 0.02 
        
        User_min_lat_defecto = -0.02
        User_max_lat_defecto = 0.02
        # .....................................................................
        
        
        Separa_x = cmb_lon
        Separa_y = cmb_lat
        
        User_min_lon = User_min_lon_defecto-1*(cmb_min_lon/100)
        User_max_lon = User_max_lon_defecto+(cmb_max_lon/100)
        User_min_lat = User_min_lat_defecto-1*(cmb_min_lat/100)
        User_max_lat = User_max_lat_defecto+(cmb_max_lat/100)
        
        if tipo_calculo == 1:
            DNO_canva["cnv_homeless_DNO"] = wnfun_lib.canva_DNO_ocupantes_mnz(COD_mun_DNO,CP_Name_DNO,manzana_shp_DNO,seccion_shp_DNO,area_shp_DNO,map_data,Modelo_Expo2_DNO,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable)
        else:
            DNO_canva["cnv_homeless_DNO"] = wnfun_lib.canva_DNO_ocupantes_scc(COD_mun_DNO,CP_Name_DNO,seccion_shp_DNO,area_shp_DNO,map_data,Modelo_Expo2_DNO,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat,variable)
            
    else:
        tk.messagebox.showinfo("ERROR", "Ingresa todos los parámetros para modificar el mapa")
    
    # .........................................................................
    # ---- Exportar resultados:
    if DNO_boton['btn_exp_DNO'] is not None:
        DNO_boton['btn_exp_DNO'].place_forget()
        DNO_boton['btn_exp_DNO']  = None
    if DNO_boton['btn_exp2_DNO'] is not None:
        DNO_boton['btn_exp2_DNO'].place_forget()
        DNO_boton['btn_exp2_DNO']  = None
    
    if DNO_boton["btn_exp_DNO"] is None:
        DNO_boton["btn_exp_DNO"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if DNO_boton["btn_exp2_DNO"] is None:
        DNO_boton["btn_exp2_DNO"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", 
        command=lambda:wnfun_lib.ExportarMapa_Event_Based_Damage(DNO_canva["cnv_homeless_DNO"],"Figura"+str(variable)+".jpg"))
        DNO_boton["btn_exp2_DNO"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
    # .........................................................................

def ResetConfigMap_DNO(tipo_calculo,map_data):
    Salida_Geografica_DNO(tipo_calculo,map_data)
    
#%% ====== FUNCION >> CAMBIAR A PAE POR TAXONOMIA =============================
lista_combinada = None
listas_divididas_taxo_description = None
listas_divididas_df_expotax = None
Contador_Valores = None
def Change_To_PAETxn():
    
    # =================================================================
    #                        Preparar escenario 
    # =================================================================
    
    for tlt in title_PRD:
        if PRD_title[tlt] is not None:
            PRD_title[tlt].place_forget()
            PRD_title[tlt] = None
    for txt in text_PRD:
        if PRD_text[txt] is not None:
            PRD_text[txt].place_forget()
            PRD_text[txt] = None
    for btn in boton_PRD:
        if PRD_boton[btn] is not None:
            PRD_boton[btn].place_forget()
            PRD_boton[btn] = None
    for lbl in entry_PRD:
        if PRD_entry[lbl] is not None:
            PRD_entry[lbl].place_forget()
            PRD_entry[lbl] = None
    for rct in rectg_PRD:
        if PRD_rectg[rct] is not None:
            PRD_rectg[rct].place_forget()
            PRD_rectg[rct] = None
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
    
    # =================================================================
    #                     Volver a acomodar botones
    # =================================================================
    
    # -------- Frame resultados ---------------------------------------
    if PRD_label["lbl_rst_PRD"] is None:
        PRD_label["lbl_rst_PRD"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
    # -------- Design frame -------------------------------------------
    if PRD_label["lbl_DsF_PRD"] is None:
        PRD_label["lbl_DsF_PRD"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
    
    # -------- Title Section ------------------------------------------
    if PRD_text["tlt_sct_PRD"] is None:
        PRD_text["tlt_sct_PRD"] = tk.Label(cnt_container, text="Resultados de Riesgo Basado en Eventos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
        PRD_text["tlt_sct_PRD"].place(relx=0.25, rely=0.072, anchor=tk.CENTER)
    if PRD_text["tlt_sct_PRD1"] is None:
        if calculation_mode == "Probabilistico":
            PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos probabilísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
        else:
            PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos determinísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
    # -------- Frame Results Title ------------------------------------
    if PRD_label["lbl_rstv2_PRD"] is None:
        PRD_label["lbl_rstv2_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
    if PRD_label["lbl_rstv3_PRD"] is None:
        PRD_label["lbl_rstv3_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.250)
    if PRD_label["lbl_rstv4_PRD"] is None:
        PRD_label["lbl_rstv4_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 38, 30, cnt_container,"white",0.025,0.22)
    # -------- Results Title ------------------------------------------
    if PRD_text["tlt_rstv2_PRD"] is None:
        PRD_text["tlt_rstv2_CLB"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
        PRD_text["tlt_rstv2_CLB"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
    
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarResultados_Event_Based_Risk(Excedence_Curve,Table_Resu,Table_Resu_Txn,Figure_txn))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
    
    # ---- Tabla resumen PAE taxonomias:
    if PRD_boton["lbl_tbl_txn_PRD"] is None:
        PRD_boton["lbl_tbl_txn_PRD"] = wnfun_lib.Label_Image('/Tabla_PAE_Txn.png', 920, 490, cnt_container,"white",0.55,0.59)
    
    # ---- boton para cambiar a la representacion grafica
    PRD_boton["btn_rps_txn"] = wnfun_lib.Button_Image('/GoTo_GrapTxn.png', 200, 70, cnt_container,"white",0.09,0.6,Change_Representation)
    
    # ---- Devolver a PAE del municipio:
    PRD_boton["btn_cbm_PRD"] = wnfun_lib.Button_Image('/GoTo_PAECp.png', 250, 50, cnt_container,"white",0.63,0.97,Change_To_PAE)
    
    # ---- Ir a mapas:
    PRD_boton["btn_cbm2_PRD"] = wnfun_lib.Button_Image('/GoTo_MapPAE.png', 260, 50, cnt_container,"white",0.835,0.97,Change_To_MapPAE)


    # ---- Colocar descripcion de tipologia constructiva:
        
    # Primero hay que dividir las tipologias para mostrar en diferentes pestanas. si el numero de 
    # taxonomias es menor o igual a 8 no es necesario, pero si es mayor se debe dividir la cantidad de 
    # taxonomias entre 8 y repartirlas en las pestanas.
    
    global lista_combinada, listas_divididas_taxo_description,listas_divididas_df_expotax,Contador_Valores
    if len(df_expotax) <= 8:
        
        # Crear botones siguiente y atras pero inhabilitados
        PRD_boton["btn_atras"] = wnfun_lib.Label_Image('/PAE_Atras.png', 50, 40, cnt_container,"white",0.859,0.23)
        PRD_boton["btn_siguiente"] = wnfun_lib.Label_Image('/PAE_Siguiente_Inh.png', 50, 40, cnt_container,"white",0.904,0.23)
        
        lista_combinada = perdidas_lib.PaeTaxo_8menos(df_expotax,taxo_description,cnt_container,description_list,PRD_Description,taxo_list,PRD_Taxonomia,valexCop_list,PRD_ValexCOP,valexPrc_list,PRD_ValexPRC,PaeCop_list,PRD_PaeCOP,PaePrc_list,PRD_PaePRC,PaePrcM_list,PRD_PaePRCM,PRD_boton,Change_To_PAE)
        
    else:
        def obtener_numero_de_unidades(df_expotax):
            longitud_df = len(df_expotax)
            unidades = math.ceil(longitud_df / 8)
            return unidades
        
        numero_de_unidades_expotax = obtener_numero_de_unidades(df_expotax)
        listas_divididas_df_expotax = [df_expotax[i*8 : (i+1)*8] for i in range(numero_de_unidades_expotax)]
        
        # listas_divididas_df_expotax genera listas divididas cada 8 valores. obtiene entonces un dataframe por
        # cada vez que se completen los 8 valores.
        numero_de_unidades_taxo = obtener_numero_de_unidades(taxo_description)
        listas_divididas_taxo_description = [taxo_description[i*8 : (i+1)*8] for i in range(numero_de_unidades_taxo)]
        
        # listas_divididas_taxo_description genera listas divididas cada 8 valores. obtiene entonces una lista
        # cada vez que se completen los 8 valores de la lista de descripcion de taxonomias.
                
        # aqui ya se obtiene la lista en cada parte. ahora se necesita crear un boton
        # que permita ir a la otra lista de los siguientes 8 valores. Entonces se debe
        # hacer el proceso normal para la primera lista y despues crear el boton de siguiente.
        # Ese boton de siguiente muestra la otra parte de la lista (como hay mas partes esa si o si va)
        # ahora se viene un condicional, si listas_divididas tiene una longitud mayor a 2 entonces
        # se debe crear un for con esos botones para que cada accion haga que cambie de lista
        # en ese bucle debe ingresar la lista que se va a usar y un contador. cuando el contador
        # sea igual al numero de unidades "numero_de_unidades" entonces para.
        
        # ---- Se genera la primera lista:
        # Para esta lista se necesitan los 8 primeros valores de df_expotax y de taxo_description.
        df_expotax_1 = listas_divididas_df_expotax[0]              # obtiene entonces el primer dataframe de valores
        taxo_description_2 = listas_divididas_taxo_description[0]  # obtiene entonces el primer conjunto de descripciones
        # Con esos valores se crean la primera tabla
        lista_combinada = perdidas_lib.PaeTaxo_8menos(df_expotax_1,taxo_description_2,cnt_container,description_list,PRD_Description,taxo_list,PRD_Taxonomia,valexCop_list,PRD_ValexCOP,valexPrc_list,PRD_ValexPRC,PaeCop_list,PRD_PaeCOP,PaePrc_list,PRD_PaePRC,PaePrcM_list,PRD_PaePRCM,PRD_boton,Change_To_PAE)
        # Aca entonces se crea el boton que direccione a la siguiente parte de la tabla:
        PRD_boton["btn_atras"] = wnfun_lib.Label_Image('/PAE_Atras.png', 50, 40, cnt_container,"white",0.805,0.23)
        PRD_boton["btn_siguiente"] = wnfun_lib.Button_Image('/PAE_Siguiente.png', 50, 40, cnt_container,"white",0.85,0.23,Change_To_PAETxn_Next)
        # Creo un contador 
        Contador_Valores = 1
        
        
def Change_To_PAETxn_Next():
    # Eliminar el contenido de la tabla anterior
    global lista_combinada,Contador_Valores
    for val in lista_combinada:
        if PRD_Description[val] is not None:
            PRD_Description[val].place_forget()
            PRD_Description[val] = None
            
    for val in taxo_list:
        if PRD_Taxonomia[val] is not None:
            PRD_Taxonomia[val].place_forget()
            PRD_Taxonomia[val] = None
    
    for val in valexCop_list:
        if PRD_ValexCOP[val] is not None:
            PRD_ValexCOP[val].place_forget()
            PRD_ValexCOP[val] = None
   
    for val in valexPrc_list:
        if PRD_ValexPRC[val] is not None:
            PRD_ValexPRC[val].place_forget()
            PRD_ValexPRC[val] = None
    
    for val in PaeCop_list:
        if PRD_PaeCOP[val] is not None:
            PRD_PaeCOP[val].place_forget()
            PRD_PaeCOP[val] = None
    
    for val in PaePrc_list:
        if PRD_PaePRC[val] is not None:
            PRD_PaePRC[val].place_forget()
            PRD_PaePRC[val] = None
    
    for val in PaePrcM_list:
        if PRD_PaePRCM[val] is not None:
            PRD_PaePRCM[val].place_forget()
            PRD_PaePRCM[val] = None
    # Generar la nueva tabla:
    # si o si deberia entrar aqui porque eso quiere decir que las taxonomias
    # superaron los 8 valores.
    # el Contador_Valores debe estar en 1 la primera vez que entre aca.
    df_expotax_1 = listas_divididas_df_expotax[Contador_Valores]              # obtiene entonces los otros dataframes de valores
    taxo_description_2 = listas_divididas_taxo_description[Contador_Valores]  # obtiene entonces los otros conjuntos de descripciones
    lista_combinada = perdidas_lib.PaeTaxo_8menos(df_expotax_1,taxo_description_2,cnt_container,description_list,PRD_Description,taxo_list,PRD_Taxonomia,valexCop_list,PRD_ValexCOP,valexPrc_list,PRD_ValexPRC,PaeCop_list,PRD_PaeCOP,PaePrc_list,PRD_PaePRC,PaePrcM_list,PRD_PaePRCM,PRD_boton,Change_To_PAE)
    # Aca entonces se crea el boton que direccione a la siguiente parte de la tabla si existe:
    # Entra entonces un condicional
    if len(listas_divididas_df_expotax) > Contador_Valores+1: # Si la longitud de la lista es mayor al contador + 1 se crea un boton nuevo
        # Creamos mejor otra funcion para evitar errores.    
        PRD_boton["btn_siguiente"] = wnfun_lib.Button_Image('/PAE_Siguiente.png', 60, 40, cnt_container,"white",0.35,0.75,Change_To_PAETxn_Next2)
        Contador_Valores = Contador_Valores+1
    # si no pasa eso entonces se borra el boton de siguiente o se deja inhabilitado
        
def Change_To_PAETxn_Next2():
    # Eliminar el contenido de la tabla anterior
    global lista_combinada,Contador_Valores
    for val in lista_combinada:
        if PRD_Description[val] is not None:
            PRD_Description[val].place_forget()
            PRD_Description[val] = None
            
    for val in taxo_list:
        if PRD_Taxonomia[val] is not None:
            PRD_Taxonomia[val].place_forget()
            PRD_Taxonomia[val] = None
    
    for val in valexCop_list:
        if PRD_ValexCOP[val] is not None:
            PRD_ValexCOP[val].place_forget()
            PRD_ValexCOP[val] = None
   
    for val in valexPrc_list:
        if PRD_ValexPRC[val] is not None:
            PRD_ValexPRC[val].place_forget()
            PRD_ValexPRC[val] = None
    
    for val in PaeCop_list:
        if PRD_PaeCOP[val] is not None:
            PRD_PaeCOP[val].place_forget()
            PRD_PaeCOP[val] = None
    
    for val in PaePrc_list:
        if PRD_PaePRC[val] is not None:
            PRD_PaePRC[val].place_forget()
            PRD_PaePRC[val] = None
    
    for val in PaePrcM_list:
        if PRD_PaePRCM[val] is not None:
            PRD_PaePRCM[val].place_forget()
            PRD_PaePRCM[val] = None
    # Generar la nueva tabla:
    # solo entra aqui si hay mas de dos tablas por generar.
    
    df_expotax_1 = listas_divididas_df_expotax[Contador_Valores]              # obtiene entonces los otros dataframes de valores
    taxo_description_2 = listas_divididas_taxo_description[Contador_Valores]  # obtiene entonces los otros conjuntos de descripciones
    lista_combinada = perdidas_lib.PaeTaxo_8menos(df_expotax_1,taxo_description_2,cnt_container,description_list,PRD_Description,taxo_list,PRD_Taxonomia,valexCop_list,PRD_ValexCOP,valexPrc_list,PRD_ValexPRC,PaeCop_list,PRD_PaeCOP,PaePrc_list,PRD_PaePRC,PaePrcM_list,PRD_PaePRCM,PRD_boton,Change_To_PAE)
    # Aca entonces se crea el boton que direccione a la siguiente parte de la tabla si existe:
    # Entra entonces un condicional
    if len(listas_divididas_df_expotax) > Contador_Valores+1: # Si la longitud de la lista es mayor al contador + 1 se crea un boton nuevo
        # Creamos mejor otra funcion para evitar errores.    
        PRD_boton["btn_siguiente"] = wnfun_lib.Button_Image('/PAE_Siguiente.png', 60, 40, cnt_container,"white",0.35,0.75,Change_To_PAETxn_Next)    
        Contador_Valores = Contador_Valores+1
    # si no pasa eso entonces se borra el boton de siguiente o se deja inhabilitado
#%% ====== FUNCION >> CAMBIAR A REPRESENTACION GRAFICA ========================
def Change_Representation():
    
    # ---- Preparar escenario ---------------------------------------------
    # ---- Eliminar los datos de la tabla:
    for val in lista_combinada:
        if PRD_Description[val] is not None:
            PRD_Description[val].place_forget()
            PRD_Description[val] = None
            
    for val in taxo_list:
        if PRD_Taxonomia[val] is not None:
            PRD_Taxonomia[val].place_forget()
            PRD_Taxonomia[val] = None
    
    for val in valexCop_list:
        if PRD_ValexCOP[val] is not None:
            PRD_ValexCOP[val].place_forget()
            PRD_ValexCOP[val] = None
   
    for val in valexPrc_list:
        if PRD_ValexPRC[val] is not None:
            PRD_ValexPRC[val].place_forget()
            PRD_ValexPRC[val] = None
    
    for val in PaeCop_list:
        if PRD_PaeCOP[val] is not None:
            PRD_PaeCOP[val].place_forget()
            PRD_PaeCOP[val] = None
    
    for val in PaePrc_list:
        if PRD_PaePRC[val] is not None:
            PRD_PaePRC[val].place_forget()
            PRD_PaePRC[val] = None
    
    for val in PaePrcM_list:
        if PRD_PaePRCM[val] is not None:
            PRD_PaePRCM[val].place_forget()
            PRD_PaePRCM[val] = None
    
    # ---- Eliminar tabla PAE
    if PRD_boton["lbl_tbl_txn_PRD"] is not None:
        PRD_boton["lbl_tbl_txn_PRD"].place_forget()
        PRD_boton["lbl_tbl_txn_PRD"] = None
    if PRD_boton["lbl_cnt_PRD"]  is not None:
        PRD_boton["lbl_cnt_PRD"].place_forget()
        PRD_boton["lbl_cnt_PRD"] = None
    if PRD_text["txt_cp_PRD"] is not None:
        PRD_text["txt_cp_PRD"].place_forget()
        PRD_text["txt_cp_PRD"] = None
    if PRD_boton["btn_rps_txn"] is not None:
        PRD_boton["btn_rps_txn"].place_forget()
        PRD_boton["btn_rps_txn"] = None
    if PRD_boton["btn_siguiente"] is not None:
        PRD_boton["btn_siguiente"].place_forget()
        PRD_boton["btn_siguiente"] = None
    if PRD_boton["btn_atras"] is not None:
        PRD_boton["btn_atras"].place_forget()
        PRD_boton["btn_atras"] = None
    
    # ---- Generar grafico:
    PRD_canva["cnv_grph_PRD"] = wnfun_lib.canva_EBR_taxo(df_expotax,cnt_container,0.65,0.56)
    
    PRD_boton["lbl_leyend"] = wnfun_lib.Label_Image('/Leyenda_Losses_Txn.png', 330, 170, cnt_container,"white",0.20,0.5)
    
    # ---- Boton de regresar:
    PRD_boton["btn_rps_txn"] = wnfun_lib.Button_Image('/GoTo_PAETxn_2.png', 210, 70, cnt_container,"white",0.20,0.70,Change_To_PAETxn)

#%% ====== FUNCION >> CAMBIAR A PAE ===========================================

def Change_To_PAE():
    
    # ---- Preparar escenario ---------------------------------------------
    # ---- Eliminar los datos de la tabla:
    for val in lista_combinada:
        if PRD_Description[val] is not None:
            PRD_Description[val].place_forget()
            PRD_Description[val] = None
            
    for val in taxo_list:
        if PRD_Taxonomia[val] is not None:
            PRD_Taxonomia[val].place_forget()
            PRD_Taxonomia[val] = None
    
    for val in valexCop_list:
        if PRD_ValexCOP[val] is not None:
            PRD_ValexCOP[val].place_forget()
            PRD_ValexCOP[val] = None
   
    for val in valexPrc_list:
        if PRD_ValexPRC[val] is not None:
            PRD_ValexPRC[val].place_forget()
            PRD_ValexPRC[val] = None
    
    for val in PaeCop_list:
        if PRD_PaeCOP[val] is not None:
            PRD_PaeCOP[val].place_forget()
            PRD_PaeCOP[val] = None
    
    for val in PaePrc_list:
        if PRD_PaePRC[val] is not None:
            PRD_PaePRC[val].place_forget()
            PRD_PaePRC[val] = None
    
    for val in PaePrcM_list:
        if PRD_PaePRCM[val] is not None:
            PRD_PaePRCM[val].place_forget()
            PRD_PaePRCM[val] = None
    
    # ---- Eliminar tabla PAE
    if PRD_boton["lbl_tbl_txn_PRD"] is not None:
        PRD_boton["lbl_tbl_txn_PRD"].place_forget()
        PRD_boton["lbl_tbl_txn_PRD"] = None
    if PRD_boton["lbl_cnt_PRD"]  is not None:
        PRD_boton["lbl_cnt_PRD"].place_forget()
        PRD_boton["lbl_cnt_PRD"] = None
    if PRD_text["txt_cp_PRD"] is not None:
        PRD_text["txt_cp_PRD"].place_forget()
        PRD_text["txt_cp_PRD"] = None
    if PRD_boton["btn_rps_txn"] is not None:
        PRD_boton["btn_rps_txn"].place_forget()
        PRD_boton["btn_rps_txn"] = None
    if PRD_boton["btn_siguiente"] is not None:
        PRD_boton["btn_siguiente"].place_forget()
        PRD_boton["btn_siguiente"] = None
    if PRD_boton["btn_atras"] is not None:
        PRD_boton["btn_atras"].place_forget()
        PRD_boton["btn_atras"] = None
    
    # =================================================================
    #                        Preparar escenario 
    # =================================================================
    
    for tlt in title_PRD:
        if PRD_title[tlt] is not None:
            PRD_title[tlt].place_forget()
            PRD_title[tlt] = None
    for txt in text_PRD:
        if PRD_text[txt] is not None:
            PRD_text[txt].place_forget()
            PRD_text[txt] = None
    for btn in boton_PRD:
        if PRD_boton[btn] is not None:
            PRD_boton[btn].place_forget()
            PRD_boton[btn] = None
    for lbl in entry_PRD:
        if PRD_entry[lbl] is not None:
            PRD_entry[lbl].place_forget()
            PRD_entry[lbl] = None
    for rct in rectg_PRD:
        if PRD_rectg[rct] is not None:
            PRD_rectg[rct].place_forget()
            PRD_rectg[rct] = None
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
    
    # =================================================================
    #                     Volver a acomodar botones
    # =================================================================
    
    # -------- Frame resultados ---------------------------------------
    if PRD_label["lbl_rst_PRD"] is None:
        PRD_label["lbl_rst_PRD"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
    # -------- Design frame -------------------------------------------
    if PRD_label["lbl_DsF_PRD"] is None:
        PRD_label["lbl_DsF_PRD"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
    
    # -------- Title Section ------------------------------------------
    if PRD_text["tlt_sct_PRD"] is None:
        PRD_text["tlt_sct_PRD"] = tk.Label(cnt_container, text="Resultados de Riesgo Basado en Eventos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
        PRD_text["tlt_sct_PRD"].place(relx=0.25, rely=0.072, anchor=tk.CENTER)
    if PRD_text["tlt_sct_PRD1"] is None:
        if calculation_mode == "Probabilistico":
            PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos probabilísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
        else:
            PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos determinísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
    # -------- Frame Results Title ------------------------------------
    if PRD_label["lbl_rstv2_PRD"] is None:
        PRD_label["lbl_rstv2_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
    if PRD_label["lbl_rstv3_PRD"] is None:
        PRD_label["lbl_rstv3_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.250)
    if PRD_label["lbl_rstv4_PRD"] is None:
        PRD_label["lbl_rstv4_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 38, 30, cnt_container,"white",0.025,0.22)
    # -------- Results Title ------------------------------------------
    if PRD_text["tlt_rstv2_PRD"] is None:
        PRD_text["tlt_rstv2_CLB"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
        PRD_text["tlt_rstv2_CLB"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)
    
    # ---- Ingresar periodo de analisis:
    if PRD_boton["btn_ing_PRD"] is None:
        PRD_boton["btn_ing_PRD"] = wnfun_lib.Label_Image('/Ingresar_Periodo.png', 240, 47, cnt_container,"#F2F2F2",0.72,0.108)
    # -------- Select Folder ------------------------------------------
    if PRD_boton["btn_slc_PRD"]  is None:
        PRD_boton["btn_slc_PRD"]  = wnfun_lib.Button_Image('/Select_FolderV2.png', 175, 41, cnt_container,"#F2F2F2",0.74,0.068,Select_Folder_DSP)
    # -------- Information Button -------------------------------------
    if PRD_boton["btn_inf_PRD"] is None:
        PRD_boton["btn_inf_PRD"] = wnfun_lib.Button_Image('/Info.png', 19, 19, cnt_container,"#F2F2F2",0.81,0.055,Ventana_Info_DSP) 
    # ---- Ingresar numero
    if PRD_rectg["rec_per_PRD"] is None:
        PRD_rectg["rec_per_PRD"] = tk.Canvas(cnt_container, bg="#F2F2F2", bd=0, highlightthickness=0)
        PRD_rectg["rec_per_PRD"].place(relx=0.825, rely=0.1, anchor=tk.CENTER, width=55, height=28)
        x2, y2 = 54, 27
        x1, y1 = 10,10
        radio_esquinas = 5
        color = "#D0CECE"
        wnfun_lib.rec_redond(PRD_rectg["rec_per_PRD"], x1, y1, x2, y2, radio_esquinas, color)
    if PRD_entry["ent_per_PRD"] is None:
        PRD_entry["ent_per_PRD"] = tk.Entry(PRD_rectg["rec_per_PRD"], bg = "#D0CECE", bd=0, highlightthickness=0)
        PRD_entry["ent_per_PRD"].place(relx=0.55, rely=0.63, anchor=tk.CENTER, width=30, height=15)
    # ---- Calibrar:
    PRD_boton2["SiNo"] = ["SiNo"]
    if PRD_boton["btn_clb_PRD"] is None:
        PRD_boton["btn_clb_PRD"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 48, cnt_container,"#F2F2F2",0.92,0.097,Function_Dispersion,resultado_label_Dispersion)


    # =================================================================
    #                     Acomodar primera pagina
    # =================================================================            

    # ...................... CURVA DE EXCEDENCIA ......................
    PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_crv_EBR(df_EBR, valexpuesto, valorperiodo,cnt_container,0.27,0.60)
    # ---- Titulo del grafico:
    PRD_text["txt_gf1_PRD"] = tk.Label(cnt_container, text="Curva de excedencia - Pérdida anual esperada", font=("Abadi MT", 15, "bold"), bg="white", fg="#3B3838")
    PRD_text["txt_gf1_PRD"].place(relx=0.3, rely=0.31, anchor=tk.CENTER)
    
    # ---- Tabla resumen PAE:
    if PRD_boton["lbl_tbl_PRD"] is None:
        PRD_boton["lbl_tbl_PRD"] = wnfun_lib.Label_Image('/Tabla_PAE.png', 520, 420, cnt_container,"white",0.73,0.57)
    # # ---- Colocar resultados en la tabla de resumen PAE:
    # # Valor expuesto:
    texto_ValorExpuesto = np.around(df_resultados.Col2[0]*1e6,2)     
    PRD_text["txt_vlx_PRD1"] = tk.Label(cnt_container, text=str(texto_ValorExpuesto), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD1"].place(relx=0.87, rely=0.308, anchor=tk.CENTER)
    # Perdida anual esperada en COP
    texto_PAE_Cop = np.around(df_resultados.Col2[1],2)             
    PRD_text["txt_vlx_PRD2"] = tk.Label(cnt_container, text=str(texto_PAE_Cop), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD2"].place(relx=0.87, rely=0.355, anchor=tk.CENTER)
    # Perdida anual esperada en porcentaje por mil
    texto_PAE_Prc = np.around(df_resultados.Col2[2],3)            
    PRD_text["txt_vlx_PRD3"] = tk.Label(cnt_container, text=str(texto_PAE_Prc), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD3"].place(relx=0.87, rely=0.405, anchor=tk.CENTER)
    # Periodo de retorno [31]
    PRD_text["txt_vlx_PRD4"] = tk.Label(cnt_container, text='31', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD4"].place(relx=0.57, rely=0.635, anchor=tk.CENTER)
    texto_PE50_31 = np.around(Pr50_Val[0],1)                            # Probabilidad de excedencia en 50 años [31]
    PRD_text["txt_vlx_PRD5"] = tk.Label(cnt_container, text=str(texto_PE50_31), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD5"].place(relx=0.702, rely=0.635, anchor=tk.CENTER)
    texto_PE_COP_31 = np.around(PE_mill[0],1)                           # Perdida esperada en COP [31]
    PRD_text["txt_vlx_PRD6"] = tk.Label(cnt_container, text=str(texto_PE_COP_31), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD6"].place(relx=0.83, rely=0.635, anchor=tk.CENTER)
    texto_PE_31 = np.around((PE_mill[0]/(df_resultados.Col2[0]*1e6))*100,1) # Perdida esperada en % [31]
    PRD_text["txt_vlx_PRD7"] = tk.Label(cnt_container, text=str(texto_PE_31), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD7"].place(relx=0.917, rely=0.635, anchor=tk.CENTER)
    # Periodo de retorno [225]
    PRD_text["txt_vlx_PRD8"] = tk.Label(cnt_container, text='225', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD8"].place(relx=0.57, rely=0.684, anchor=tk.CENTER)
    texto_PE50_225 = np.around(Pr50_Val[1],1)                           # Probabilidad de excedencia en 50 años [225]
    PRD_text["txt_vlx_PRD9"] = tk.Label(cnt_container, text=str(texto_PE50_225), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD9"].place(relx=0.702, rely=0.684, anchor=tk.CENTER)
    texto_PE_COP_225 = np.around(PE_mill[1],1)                          # Perdida esperada en COP [225]
    PRD_text["txt_vlx_PRD10"] = tk.Label(cnt_container, text=str(texto_PE_COP_225), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD10"].place(relx=0.83, rely=0.684, anchor=tk.CENTER)
    texto_PE_225 = np.around((PE_mill[1]/(df_resultados.Col2[0]*1e6))*100,1)  # Perdida esperada en % [225]
    PRD_text["txt_vlx_PRD11"] = tk.Label(cnt_container, text=str(texto_PE_225), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD11"].place(relx=0.917, rely=0.684, anchor=tk.CENTER)
    # Periodo de retorno [475]
    PRD_text["txt_vlx_PRD12"] = tk.Label(cnt_container, text='475', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD12"].place(relx=0.57, rely=0.733, anchor=tk.CENTER)
    texto_PE50_475 = np.around(Pr50_Val[2],1)                           # Probabilidad de excedencia en 50 años [475]
    PRD_text["txt_vlx_PRD13"] = tk.Label(cnt_container, text=str(texto_PE50_475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD13"].place(relx=0.702, rely=0.733, anchor=tk.CENTER)
    texto_PE_COP_475 = np.around(PE_mill[2],1)                          # Perdida esperada en COP [475]
    PRD_text["txt_vlx_PRD14"] = tk.Label(cnt_container, text=str(texto_PE_COP_475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD14"].place(relx=0.83, rely=0.733, anchor=tk.CENTER)
    texto_PE_475 = np.around((PE_mill[2]/(df_resultados.Col2[0]*1e6))*100,1) # Perdida esperada en % [475]
    PRD_text["txt_vlx_PRD15"] = tk.Label(cnt_container, text=str(texto_PE_475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD15"].place(relx=0.917, rely=0.733, anchor=tk.CENTER)
    # Periodo de retorno [975]
    PRD_text["txt_vlx_PRD16"] = tk.Label(cnt_container, text='975', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD16"].place(relx=0.57, rely=0.782, anchor=tk.CENTER)
    texto_PE50_975 = np.around(Pr50_Val[3],1)                           # Probabilidad de excedencia en 50 años [975]
    PRD_text["txt_vlx_PRD17"] = tk.Label(cnt_container, text=str(texto_PE50_975), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD17"].place(relx=0.702, rely=0.782, anchor=tk.CENTER)
    texto_PE_COP_975 = np.around(PE_mill[3],1)                          # Perdida esperada en COP [975]
    PRD_text["txt_vlx_PRD18"] = tk.Label(cnt_container, text=str(texto_PE_COP_975), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD18"].place(relx=0.83, rely=0.782, anchor=tk.CENTER)
    texto_PE_975 = np.around((PE_mill[3]/(df_resultados.Col2[0]*1e6))*100,1) # Perdida esperada en % [975]
    PRD_text["txt_vlx_PRD19"] = tk.Label(cnt_container, text=str(texto_PE_975), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD19"].place(relx=0.917, rely=0.782, anchor=tk.CENTER)
    # Periodo de retorno [1475]
    PRD_text["txt_vlx_PRD20"] = tk.Label(cnt_container, text='1475', font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD20"].place(relx=0.57, rely=0.831, anchor=tk.CENTER)
    texto_PE50_1475 = np.around(Pr50_Val[4],1)                          # Probabilidad de excedencia en 50 años [1475]
    PRD_text["txt_vlx_PRD21"] = tk.Label(cnt_container, text=str(texto_PE50_1475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD21"].place(relx=0.702, rely=0.831, anchor=tk.CENTER)
    texto_PE_COP_1475 = np.around(PE_mill[4],1)                         # Perdida esperada en COP [1475]
    PRD_text["txt_vlx_PRD22"] = tk.Label(cnt_container, text=str(texto_PE_COP_1475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD22"].place(relx=0.83, rely=0.831, anchor=tk.CENTER)
    texto_PE_1475 = np.around((PE_mill[4]/(df_resultados.Col2[0]*1e6))*100,1)
    PRD_text["txt_vlx_PRD23"] = tk.Label(cnt_container, text=str(texto_PE_1475), font=("Abadi MT", 10), bg="#C6CFD4", fg="#3B3838")
    PRD_text["txt_vlx_PRD23"].place(relx=0.917, rely=0.831, anchor=tk.CENTER)
    
    # ---- Cambiar a resultados por taxonomia:
    PRD_boton["btn_cbm_PRD"] = wnfun_lib.Button_Image('/GoTo_PAETxn.png', 250, 50, cnt_container,"white",0.84,0.94,Change_To_PAETxn)
    
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_Resultados.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
    
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar resultados", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarResultados_Event_Based_Risk(Excedence_Curve,Table_Resu,Table_Resu_Txn,Figure_txn))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
#%% ====== FUNCION >> CAMBIAR A MAPA PAE ======================================
def Change_To_MapPAE():
    
    # ---- Preparar escenario -------------------------------------------------
    # ---- Eliminar los datos de la tabla:
    for val in lista_combinada:
        if PRD_Description[val] is not None:
            PRD_Description[val].place_forget()
            PRD_Description[val] = None
            
    for val in taxo_list:
        if PRD_Taxonomia[val] is not None:
            PRD_Taxonomia[val].place_forget()
            PRD_Taxonomia[val] = None
    
    for val in valexCop_list:
        if PRD_ValexCOP[val] is not None:
            PRD_ValexCOP[val].place_forget()
            PRD_ValexCOP[val] = None
   
    for val in valexPrc_list:
        if PRD_ValexPRC[val] is not None:
            PRD_ValexPRC[val].place_forget()
            PRD_ValexPRC[val] = None
    
    for val in PaeCop_list:
        if PRD_PaeCOP[val] is not None:
            PRD_PaeCOP[val].place_forget()
            PRD_PaeCOP[val] = None
    
    for val in PaePrc_list:
        if PRD_PaePRC[val] is not None:
            PRD_PaePRC[val].place_forget()
            PRD_PaePRC[val] = None
    
    for val in PaePrcM_list:
        if PRD_PaePRCM[val] is not None:
            PRD_PaePRCM[val].place_forget()
            PRD_PaePRCM[val] = None
    
    # ---- Eliminar tabla PAE
    if PRD_boton["lbl_tbl_txn_PRD"] is not None:
        PRD_boton["lbl_tbl_txn_PRD"].place_forget()
        PRD_boton["lbl_tbl_txn_PRD"] = None
    if PRD_boton["lbl_cnt_PRD"]  is not None:
        PRD_boton["lbl_cnt_PRD"].place_forget()
        PRD_boton["lbl_cnt_PRD"] = None
    if PRD_text["txt_cp_PRD"] is not None:
        PRD_text["txt_cp_PRD"].place_forget()
        PRD_text["txt_cp_PRD"] = None
    if PRD_boton["btn_rps_txn"] is not None:
        PRD_boton["btn_rps_txn"].place_forget()
        PRD_boton["btn_rps_txn"] = None
    if PRD_boton["btn_siguiente"] is not None:
        PRD_boton["btn_siguiente"].place_forget()
        PRD_boton["btn_siguiente"] = None
    if PRD_boton["btn_atras"] is not None:
        PRD_boton["btn_atras"].place_forget()
        PRD_boton["btn_atras"] = None
    
    # =========================================================================
    #                           Preparar escenario 
    # =========================================================================
    
    for tlt in title_PRD:
        if PRD_title[tlt] is not None:
            PRD_title[tlt].place_forget()
            PRD_title[tlt] = None
    for txt in text_PRD:
        if PRD_text[txt] is not None:
            PRD_text[txt].place_forget()
            PRD_text[txt] = None
    for btn in boton_PRD:
        if PRD_boton[btn] is not None:
            PRD_boton[btn].place_forget()
            PRD_boton[btn] = None
    for lbl in entry_PRD:
        if PRD_entry[lbl] is not None:
            PRD_entry[lbl].place_forget()
            PRD_entry[lbl] = None
    for rct in rectg_PRD:
        if PRD_rectg[rct] is not None:
            PRD_rectg[rct].place_forget()
            PRD_rectg[rct] = None
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
    
    # =========================================================================
    #                       Volver a acomodar botones
    # =========================================================================
    
    # -------- Frame resultados -----------------------------------------------
    if PRD_label["lbl_rst_PRD"] is None:
        PRD_label["lbl_rst_PRD"] = wnfun_lib.Label_Image('/Frame_Results.png', 1300, 300, cnt_container,"white",0.5,0.0)
    # -------- Design frame ---------------------------------------------------
    if PRD_label["lbl_DsF_PRD"] is None:
        PRD_label["lbl_DsF_PRD"] = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,"#F2F2F2",0.505,0.00)
    
    # -------- Title Section --------------------------------------------------
    if PRD_text["tlt_sct_PRD"] is None:
        PRD_text["tlt_sct_PRD"] = tk.Label(cnt_container, text="Resultados de Riesgo Basado en Eventos", font=("Abadi MT", 22, "bold"), bg="#F2F2F2", fg="#274151")
        PRD_text["tlt_sct_PRD"].place(relx=0.25, rely=0.072, anchor=tk.CENTER)
    if PRD_text["tlt_sct_PRD1"] is None:
        if calculation_mode == "Probabilistico":
            PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos probabilísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.118, anchor=tk.CENTER)
        else:
            PRD_text["tlt_sct_PRD1"] = tk.Label(cnt_container, text="Eventos determinísticos", font=("Abadi MT", 19, "bold"), bg="#F2F2F2", fg="#B97F73")
            PRD_text["tlt_sct_PRD1"].place(relx=0.137, rely=0.121, anchor=tk.CENTER)
    # -------- Frame Results Title --------------------------------------------
    if PRD_label["lbl_rstv2_PRD"] is None:
        PRD_label["lbl_rstv2_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2_DSP.png', 1400, 45, cnt_container,"#F2F2F2",0.579,0.17)
    if PRD_label["lbl_rstv3_PRD"] is None:
        PRD_label["lbl_rstv3_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 100, 36, cnt_container,"white",0.0,0.250)
    if PRD_label["lbl_rstv4_PRD"] is None:
        PRD_label["lbl_rstv4_PRD"] = wnfun_lib.Label_Image('/Frame_ResultsV2.png', 38, 30, cnt_container,"white",0.025,0.22)
    # -------- Results Title ------------------------------------------
    if PRD_text["tlt_rstv2_PRD"] is None:
        PRD_text["tlt_rstv2_CLB"] = tk.Label(cnt_container, text="Resultados Municipio: " + CP_Name, font=("Abadi MT", 18, "bold"), bg="#C6CFD4", fg="#595959")
        PRD_text["tlt_rstv2_CLB"].place(relx=0.5, rely=0.166, anchor=tk.CENTER)

    # -------- Poner en la pagina el mapa -------------------------------------    
    if PRD_canva["cnv_cv_PRD"] is None:
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................
        Separa_x = 1
        Separa_y = 1 
        
        User_min_lon = -0.04
        User_max_lon = 0.02 
        
        User_min_lat = -0.02
        User_max_lat = 0.02
        # .....................................................................
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAE(COD_mun,CP_Name,manzana_shp,seccion_shp,area_shp,mapdata_mnz_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    
    
    # -------- Poner modificacion del mapa ------------------------------------
    if PRD_boton['lbl_mdm_PRD'] is None:
        PRD_boton['lbl_mdm_PRD'] = wnfun_lib.Label_Image('/Modificar_Mapa.png', 
                                        250, 330, cnt_container,"white",0.106,0.57)
        
    opciones_PRD = [-4,-3,-2,-1,0,1,2,3,4]
    opciones2_PRD = [0,1,2,3,4,5]
    # -------- Selección de kilometros de separacion latitudinal --------------
    if PRD_boton["cmb_lon"] is None:
        PRD_boton["cmb_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lon"].place(relx=0.816, rely=0.20, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de separacion longitudinal -------------
    if PRD_boton["cmb_lat"] is None:
        PRD_boton["cmb_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lat"].place(relx=0.77, rely=0.285, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite oeste ------------------------
    if PRD_boton["cmb_min_lon"] is None:
        PRD_boton["cmb_min_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lon"].place(relx=0.62, rely=0.375, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite este -------------------------
    if PRD_boton["cmb_max_lon"] is None:
        PRD_boton["cmb_max_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lon"].place(relx=0.59, rely=0.465, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite norte ------------------------
    if PRD_boton["cmb_max_lat"] is None:
        PRD_boton["cmb_max_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lat"].place(relx=0.607, rely=0.545, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite sur --------------------------
    if PRD_boton["cmb_min_lat"] is None:
        PRD_boton["cmb_min_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lat"].place(relx=0.572, rely=0.64, 
                            anchor=tk.CENTER, width=40, height=20)        
    
    # -------- Agregar ajustes al mapa ----------------------------------------
    if PRD_boton["btn_ajs_PRD"] is None:
        PRD_boton["btn_ajs_PRD"] = wnfun_lib.Button_Image('/Aplicar_Ajustes.png', 
                144, 40, cnt_container,"white",0.106,0.70,Add_Config_Map)

    # -------- Reiniciar los ajustes ------------------------------------------
    if PRD_boton["btn_rin_PRD"] is None:
        PRD_boton["btn_rin_PRD"] = wnfun_lib.Button_Image('/Reiniciar_Ajustes.png', 
                157, 42, cnt_container,"white",0.106,0.748,Reset_Congig_Map)
    
    # -------- Resultados por seccion PAE_COP ---------------------------------
    if PRD_boton["btn_scc_PRD"] is None:
        PRD_boton["btn_scc_PRD"] = wnfun_lib.Button_Image('/Visualizar_Seccion_PRD.png', 
                170, 60, cnt_container,"white",0.12,0.28,Visual_Map_Secc)
    
    # -------- Resultados PAE sobre valor expuesto ----------------------------
    if PRD_boton["btn_PAEVLE_PRD"] is None:
        PRD_boton["btn_PAEVLE_PRD"] = wnfun_lib.Button_Image('/GoTo_PAE_ValExt.png', 
                113, 40, cnt_container,"white",0.15,0.85,Change_To_PAEValex)
        
    # -------- Resultados PAE COP deshabilitado -------------------------------
    if PRD_boton["btn_PAECOP_PRD"] is None:
        PRD_boton["btn_PAECOP_PRD"] = wnfun_lib.Label_Image('/Goto_PAE_COP_uns.png', 
                107, 38, cnt_container,"white",0.06,0.848)
    
    # ---- Devolver a PAE del municipio:
    PRD_boton["btn_cbm_PRD"] = wnfun_lib.Button_Image('/ReturnTo_PAETax.png', 250, 50, cnt_container,"white",0.84,0.975,Change_To_PAETxn)
    
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_mnz_cop.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)


'''============================================================================
                        ENLACES SECCION PAE POR MANZANA
============================================================================'''

#//////////////////////////////////////////////////////////////////////////////
#                      Configuracion del mapa PAE manzana
#//////////////////////////////////////////////////////////////////////////////

def Add_Config_Map():
    
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
            
    # --------- Verificar separacion horizontal -------------------------------
    if PRD_boton["cmb_lon"].get() == '':
        cmb_lon = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación horizontal/longitud")
    else:
        cmb_lon = int(PRD_boton["cmb_lon"].get())
    # --------- Verificar separacion vertical ---------------------------------    
    if PRD_boton["cmb_lat"].get() == '':
        cmb_lat = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación vertical/latitud")
    else:
        cmb_lat = int(PRD_boton["cmb_lat"].get())
    # --------- Verificar limite oeste ----------------------------------------
    if PRD_boton["cmb_min_lon"].get() == '':
        cmb_min_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al oeste del mapa")
    else:
        cmb_min_lon = int(PRD_boton["cmb_min_lon"].get())
    # --------- Verificar limite este -----------------------------------------    
    if PRD_boton["cmb_max_lon"].get() == '':
        cmb_max_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al este del mapa")
    else:
        cmb_max_lon = int(PRD_boton["cmb_max_lon"].get())
    # --------- Verificar limite norte ----------------------------------------    
    if PRD_boton["cmb_max_lat"].get() == '':
        cmb_max_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al norte del mapa")
    else:
        cmb_max_lat = int(PRD_boton["cmb_max_lat"].get())
    # --------- Verificar limite sur ------------------------------------------    
    if PRD_boton["cmb_min_lat"].get() == '':
        cmb_min_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al sur del mapa")
    else:
        cmb_min_lat = int(PRD_boton["cmb_min_lat"].get())
    
    if cmb_lon is not None and cmb_lat is not None and cmb_min_lon is not None and cmb_max_lon is not None and cmb_min_lat is not None and cmb_max_lat is not None:
        # Entra aca cuando el usuario hace uso del modificador de mapa 
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................        
        User_min_lon_defecto = -0.04
        User_max_lon_defecto = 0.02 
        
        User_min_lat_defecto = -0.02
        User_max_lat_defecto = 0.02
        # .....................................................................
        
        
        Separa_x = cmb_lon
        Separa_y = cmb_lat
        
        User_min_lon = User_min_lon_defecto-1*(cmb_min_lon/100)
        User_max_lon = User_max_lon_defecto+(cmb_max_lon/100)
        User_min_lat = User_min_lat_defecto-1*(cmb_min_lat/100)
        User_max_lat = User_max_lat_defecto+(cmb_max_lat/100)
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAE(COD_mun,CP_Name,manzana_shp,seccion_shp,area_shp,mapdata_mnz_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    else:
        tk.messagebox.showinfo("ERROR", "Ingresa todos los parámetros para modificar el mapa")
    
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton['btn_exp_PRD'] is not None:
        PRD_boton['btn_exp_PRD'].place_forget()
        PRD_boton['btn_exp_PRD']  = None
    if PRD_boton['btn_exp2_PRD'] is not None:
        PRD_boton['btn_exp2_PRD'].place_forget()
        PRD_boton['btn_exp2_PRD']  = None
    
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_mnz_cop.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)

#//////////////////////////////////////////////////////////////////////////////
#                           Reiniciar los ajustes
#//////////////////////////////////////////////////////////////////////////////

def Reset_Congig_Map():
    Change_To_MapPAE()

#//////////////////////////////////////////////////////////////////////////////
#                       Visualizar mapa PAE por sección
#//////////////////////////////////////////////////////////////////////////////

def Visual_Map_Secc():
    # esto es cop 
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
            
    # -------- Poner en la pagina el mapa -------------------------------------    
    if PRD_canva["cnv_cv_PRD"] is None:
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................
        Separa_x = 1
        Separa_y = 1 
        
        User_min_lon = -0.04
        User_max_lon = 0.02 
        
        User_min_lat = -0.02
        User_max_lat = 0.02
        # .....................................................................
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAE_secc(COD_mun,CP_Name,seccion_shp,area_shp,mapdata_scc_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    
    # -------- Poner modificacion del mapa ------------------------------------
    if PRD_boton['lbl_mdm_PRD'] is not None:
        PRD_boton['lbl_mdm_PRD'].place_forget()
        PRD_boton['lbl_mdm_PRD']  = None
    
    if PRD_boton['lbl_mdm_PRD'] is None:
        PRD_boton['lbl_mdm_PRD'] = wnfun_lib.Label_Image('/Modificar_Mapa.png', 
                                        250, 330, cnt_container,"white",0.106,0.57)
        
    opciones_PRD = [-4,-3,-2,-1,0,1,2,3,4]
    opciones2_PRD = [0,1,2,3,4,5]
    # -------- Selección de kilometros de separacion latitudinal --------------
    if PRD_boton['cmb_lon'] is not None:
        PRD_boton['cmb_lon'].place_forget()
        PRD_boton['cmb_lon']  = None
        
    if PRD_boton["cmb_lon"] is None:
        PRD_boton["cmb_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lon"].place(relx=0.816, rely=0.20, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de separacion longitudinal -------------
    if PRD_boton['cmb_lat'] is not None:
        PRD_boton['cmb_lat'].place_forget()
        PRD_boton['cmb_lat']  = None
    
    if PRD_boton["cmb_lat"] is None:
        PRD_boton["cmb_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lat"].place(relx=0.77, rely=0.285, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite oeste ------------------------
    if PRD_boton['cmb_min_lon'] is not None:
        PRD_boton['cmb_min_lon'].place_forget()
        PRD_boton['cmb_min_lon']  = None
        
    if PRD_boton["cmb_min_lon"] is None:
        PRD_boton["cmb_min_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lon"].place(relx=0.62, rely=0.375, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite este -------------------------
    if PRD_boton['cmb_max_lon'] is not None:
        PRD_boton['cmb_max_lon'].place_forget()
        PRD_boton['cmb_max_lon']  = None
    
    if PRD_boton["cmb_max_lon"] is None:
        PRD_boton["cmb_max_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lon"].place(relx=0.59, rely=0.465, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite norte ------------------------
    if PRD_boton['cmb_max_lat'] is not None:
        PRD_boton['cmb_max_lat'].place_forget()
        PRD_boton['cmb_max_lat']  = None
    
    if PRD_boton["cmb_max_lat"] is None:
        PRD_boton["cmb_max_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lat"].place(relx=0.607, rely=0.545, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite sur --------------------------
    if PRD_boton['cmb_min_lat'] is not None:
        PRD_boton['cmb_min_lat'].place_forget()
        PRD_boton['cmb_min_lat']  = None
    
    if PRD_boton["cmb_min_lat"] is None:
        PRD_boton["cmb_min_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lat"].place(relx=0.572, rely=0.64, 
                            anchor=tk.CENTER, width=40, height=20)        
    
    # -------- Agregar ajustes al mapa ----------------------------------------
    if PRD_boton['btn_ajs_PRD'] is not None:
        PRD_boton['btn_ajs_PRD'].place_forget()
        PRD_boton['btn_ajs_PRD']  = None
    
    if PRD_boton["btn_ajs_PRD"] is None:
        PRD_boton["btn_ajs_PRD"] = wnfun_lib.Button_Image('/Aplicar_Ajustes.png', 
                144, 40, cnt_container,"white",0.106,0.70,Add_Config_Map_secc)

    # -------- Reiniciar los ajustes ------------------------------------------
    if PRD_boton['btn_rin_PRD'] is not None:
        PRD_boton['btn_rin_PRD'].place_forget()
        PRD_boton['btn_rin_PRD']  = None
    
    if PRD_boton["btn_rin_PRD"] is None:
        PRD_boton["btn_rin_PRD"] = wnfun_lib.Button_Image('/Reiniciar_Ajustes.png', 
                157, 42, cnt_container,"white",0.106,0.748,Reset_Congig_Map_secc)
    
    # -------- Resultados por seccion PAE_COP ----------------------------------------
    if PRD_boton['btn_scc_PRD'] is not None:
        PRD_boton['btn_scc_PRD'].place_forget()
        PRD_boton['btn_scc_PRD']  = None
    
    if PRD_boton["btn_scc_PRD"] is None:
        PRD_boton["btn_scc_PRD"] = wnfun_lib.Button_Image('/Visualizar_mnz_PRD.png', 
                170, 60, cnt_container,"white",0.12,0.28, Change_To_MapPAE)
    
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton['btn_exp_PRD'] is not None:
        PRD_boton['btn_exp_PRD'].place_forget()
        PRD_boton['btn_exp_PRD']  = None
    if PRD_boton['btn_exp2_PRD'] is not None:
        PRD_boton['btn_exp2_PRD'].place_forget()
        PRD_boton['btn_exp2_PRD']  = None
    
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_scc_cop.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
        
    
def Add_Config_Map_secc():
    
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
            
    # --------- Verificar separacion horizontal -------------------------------
    if PRD_boton["cmb_lon"].get() == '':
        cmb_lon = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación horizontal/longitud")
    else:
        cmb_lon = int(PRD_boton["cmb_lon"].get())
    # --------- Verificar separacion vertical ---------------------------------    
    if PRD_boton["cmb_lat"].get() == '':
        cmb_lat = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación vertical/latitud")
    else:
        cmb_lat = int(PRD_boton["cmb_lat"].get())
    # --------- Verificar limite oeste ----------------------------------------
    if PRD_boton["cmb_min_lon"].get() == '':
        cmb_min_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al oeste del mapa")
    else:
        cmb_min_lon = int(PRD_boton["cmb_min_lon"].get())
    # --------- Verificar limite este -----------------------------------------    
    if PRD_boton["cmb_max_lon"].get() == '':
        cmb_max_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al este del mapa")
    else:
        cmb_max_lon = int(PRD_boton["cmb_max_lon"].get())
    # --------- Verificar limite norte ----------------------------------------    
    if PRD_boton["cmb_max_lat"].get() == '':
        cmb_max_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al norte del mapa")
    else:
        cmb_max_lat = int(PRD_boton["cmb_max_lat"].get())
    # --------- Verificar limite sur ------------------------------------------    
    if PRD_boton["cmb_min_lat"].get() == '':
        cmb_min_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al sur del mapa")
    else:
        cmb_min_lat = int(PRD_boton["cmb_min_lat"].get())
    
    if cmb_lon is not None and cmb_lat is not None and cmb_min_lon is not None and cmb_max_lon is not None and cmb_min_lat is not None and cmb_max_lat is not None:
        # Entra aca cuando el usuario hace uso del modificador de mapa 
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................        
        User_min_lon_defecto = -0.04
        User_max_lon_defecto = 0.02 
        
        User_min_lat_defecto = -0.02
        User_max_lat_defecto = 0.02
        # .....................................................................
        
        
        Separa_x = cmb_lon
        Separa_y = cmb_lat
        
        User_min_lon = User_min_lon_defecto-1*(cmb_min_lon/100)
        User_max_lon = User_max_lon_defecto+(cmb_max_lon/100)
        User_min_lat = User_min_lat_defecto-1*(cmb_min_lat/100)
        User_max_lat = User_max_lat_defecto+(cmb_max_lat/100)
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAE_secc(COD_mun,CP_Name,seccion_shp,area_shp,mapdata_scc_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    else:
        tk.messagebox.showinfo("ERROR", "Ingresa todos los parámetros para modificar el mapa")

    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton['btn_exp_PRD'] is not None:
        PRD_boton['btn_exp_PRD'].place_forget()
        PRD_boton['btn_exp_PRD']  = None
    if PRD_boton['btn_exp2_PRD'] is not None:
        PRD_boton['btn_exp2_PRD'].place_forget()
        PRD_boton['btn_exp2_PRD']  = None
    
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_scc_cop.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)    

def Reset_Congig_Map_secc():
    Visual_Map_Secc()
    
    
'''============================================================================
                       Cambiar a PAE/Valor_Expuesto
============================================================================'''

def Change_To_PAEValex():
    
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
            
    # -------- Poner en la pagina el mapa -------------------------------------    
    if PRD_canva["cnv_cv_PRD"] is None:
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................
        Separa_x = 1
        Separa_y = 1 
        
        User_min_lon = -0.04
        User_max_lon = 0.02 
        
        User_min_lat = -0.02
        User_max_lat = 0.02
        # .....................................................................
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAE_Valex(COD_mun,CP_Name,manzana_shp,seccion_shp,area_shp,mapdata_mnz_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    
    # -------- Poner modificacion del mapa ------------------------------------
    if PRD_boton['lbl_mdm_PRD'] is not None:
        PRD_boton['lbl_mdm_PRD'].place_forget()
        PRD_boton['lbl_mdm_PRD']  = None
    
    if PRD_boton['lbl_mdm_PRD'] is None:
        PRD_boton['lbl_mdm_PRD'] = wnfun_lib.Label_Image('/Modificar_Mapa.png', 
                                        250, 330, cnt_container,"white",0.106,0.57)
        
    opciones_PRD = [-4,-3,-2,-1,0,1,2,3,4]
    opciones2_PRD = [0,1,2,3,4,5]
    # -------- Selección de kilometros de separacion latitudinal --------------
    if PRD_boton['cmb_lon'] is not None:
        PRD_boton['cmb_lon'].place_forget()
        PRD_boton['cmb_lon']  = None
        
    if PRD_boton["cmb_lon"] is None:
        PRD_boton["cmb_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lon"].place(relx=0.816, rely=0.20, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de separacion longitudinal -------------
    if PRD_boton['cmb_lat'] is not None:
        PRD_boton['cmb_lat'].place_forget()
        PRD_boton['cmb_lat']  = None
    
    if PRD_boton["cmb_lat"] is None:
        PRD_boton["cmb_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lat"].place(relx=0.77, rely=0.285, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite oeste ------------------------
    if PRD_boton['cmb_min_lon'] is not None:
        PRD_boton['cmb_min_lon'].place_forget()
        PRD_boton['cmb_min_lon']  = None
        
    if PRD_boton["cmb_min_lon"] is None:
        PRD_boton["cmb_min_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lon"].place(relx=0.62, rely=0.375, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite este -------------------------
    if PRD_boton['cmb_max_lon'] is not None:
        PRD_boton['cmb_max_lon'].place_forget()
        PRD_boton['cmb_max_lon']  = None
    
    if PRD_boton["cmb_max_lon"] is None:
        PRD_boton["cmb_max_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lon"].place(relx=0.59, rely=0.465, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite norte ------------------------
    if PRD_boton['cmb_max_lat'] is not None:
        PRD_boton['cmb_max_lat'].place_forget()
        PRD_boton['cmb_max_lat']  = None
    
    if PRD_boton["cmb_max_lat"] is None:
        PRD_boton["cmb_max_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lat"].place(relx=0.607, rely=0.545, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite sur --------------------------
    if PRD_boton['cmb_min_lat'] is not None:
        PRD_boton['cmb_min_lat'].place_forget()
        PRD_boton['cmb_min_lat']  = None
    
    if PRD_boton["cmb_min_lat"] is None:
        PRD_boton["cmb_min_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lat"].place(relx=0.572, rely=0.64, 
                            anchor=tk.CENTER, width=40, height=20)        
        
        
    # -------- Agregar ajustes al mapa ----------------------------------------
    if PRD_boton['btn_ajs_PRD'] is not None:
        PRD_boton['btn_ajs_PRD'].place_forget()
        PRD_boton['btn_ajs_PRD']  = None
    
    if PRD_boton["btn_ajs_PRD"] is None:
        PRD_boton["btn_ajs_PRD"] = wnfun_lib.Button_Image('/Aplicar_Ajustes.png', 
                144, 40, cnt_container,"white",0.106,0.70,Add_Config_Map2)

    # -------- Reiniciar los ajustes ------------------------------------------
    if PRD_boton['btn_rin_PRD'] is not None:
        PRD_boton['btn_rin_PRD'].place_forget()
        PRD_boton['btn_rin_PRD']  = None
    
    if PRD_boton["btn_rin_PRD"] is None:
        PRD_boton["btn_rin_PRD"] = wnfun_lib.Button_Image('/Reiniciar_Ajustes.png', 
                157, 42, cnt_container,"white",0.106,0.748,Reset_Congig_Map2)
    
    # -------- Resultados por seccion PAE/valex -------------------------------
    if PRD_boton['btn_scc_PRD'] is not None:
        PRD_boton['btn_scc_PRD'].place_forget()
        PRD_boton['btn_scc_PRD']  = None
    
    if PRD_boton["btn_scc_PRD"] is None:
        PRD_boton["btn_scc_PRD"] = wnfun_lib.Button_Image('/Visualizar_Seccion_PRD.png', 
                170, 60, cnt_container,"white",0.12,0.28,Visual_Map_Secc2)
    
    # -------- Resultados PAE valex deshabilitado -----------------------------
    if PRD_boton['btn_PAEVLE_PRD'] is not None:
        PRD_boton['btn_PAEVLE_PRD'].place_forget()
        PRD_boton['btn_PAEVLE_PRD']  = None
    
    if PRD_boton["btn_PAEVLE_PRD"] is None:
        PRD_boton["btn_PAEVLE_PRD"] = wnfun_lib.Label_Image('/GoTo_PAE_ValExt_uns.png', 
                113, 40, cnt_container,"white",0.15,0.85)
        
    # -------- Resultados PAE COP ---------------------------------------------
    if PRD_boton['btn_PAECOP_PRD'] is not None:
        PRD_boton['btn_PAECOP_PRD'].place_forget()
        PRD_boton['btn_PAECOP_PRD']  = None
    
    if PRD_boton["btn_PAECOP_PRD"] is None:
        PRD_boton["btn_PAECOP_PRD"] = wnfun_lib.Button_Image('/Goto_PAE_COP.png', 
                107, 38, cnt_container,"white",0.06,0.848, Change_To_MapPAE)
    
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton['btn_exp_PRD'] is not None:
        PRD_boton['btn_exp_PRD'].place_forget()
        PRD_boton['btn_exp_PRD']  = None
    if PRD_boton['btn_exp2_PRD'] is not None:
        PRD_boton['btn_exp2_PRD'].place_forget()
        PRD_boton['btn_exp2_PRD']  = None
    
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_mnz_‰.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)

#//////////////////////////////////////////////////////////////////////////////
#              Configuracion de mapa PAE/Valex por manzana
#//////////////////////////////////////////////////////////////////////////////
    
def Add_Config_Map2():
    
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
            
    # --------- Verificar separacion horizontal -------------------------------
    if PRD_boton["cmb_lon"].get() == '':
        cmb_lon = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación horizontal/longitud")
    else:
        cmb_lon = int(PRD_boton["cmb_lon"].get())
    # --------- Verificar separacion vertical ---------------------------------    
    if PRD_boton["cmb_lat"].get() == '':
        cmb_lat = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación vertical/latitud")
    else:
        cmb_lat = int(PRD_boton["cmb_lat"].get())
    # --------- Verificar limite oeste ----------------------------------------
    if PRD_boton["cmb_min_lon"].get() == '':
        cmb_min_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al oeste del mapa")
    else:
        cmb_min_lon = int(PRD_boton["cmb_min_lon"].get())
    # --------- Verificar limite este -----------------------------------------    
    if PRD_boton["cmb_max_lon"].get() == '':
        cmb_max_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al este del mapa")
    else:
        cmb_max_lon = int(PRD_boton["cmb_max_lon"].get())
    # --------- Verificar limite norte ----------------------------------------    
    if PRD_boton["cmb_max_lat"].get() == '':
        cmb_max_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al norte del mapa")
    else:
        cmb_max_lat = int(PRD_boton["cmb_max_lat"].get())
    # --------- Verificar limite sur ------------------------------------------    
    if PRD_boton["cmb_min_lat"].get() == '':
        cmb_min_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al sur del mapa")
    else:
        cmb_min_lat = int(PRD_boton["cmb_min_lat"].get())
    
    if cmb_lon is not None and cmb_lat is not None and cmb_min_lon is not None and cmb_max_lon is not None and cmb_min_lat is not None and cmb_max_lat is not None:
        # Entra aca cuando el usuario hace uso del modificador de mapa 
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................        
        User_min_lon_defecto = -0.04
        User_max_lon_defecto = 0.02 
        
        User_min_lat_defecto = -0.02
        User_max_lat_defecto = 0.02
        # .....................................................................
        
        
        Separa_x = cmb_lon
        Separa_y = cmb_lat
        
        User_min_lon = User_min_lon_defecto-1*(cmb_min_lon/100)
        User_max_lon = User_max_lon_defecto+(cmb_max_lon/100)
        User_min_lat = User_min_lat_defecto-1*(cmb_min_lat/100)
        User_max_lat = User_max_lat_defecto+(cmb_max_lat/100)
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAE_Valex(COD_mun,CP_Name,manzana_shp,seccion_shp,area_shp,mapdata_mnz_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    else:
        tk.messagebox.showinfo("ERROR", "Ingresa todos los parámetros para modificar el mapa")
    
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton['btn_exp_PRD'] is not None:
        PRD_boton['btn_exp_PRD'].place_forget()
        PRD_boton['btn_exp_PRD']  = None
    if PRD_boton['btn_exp2_PRD'] is not None:
        PRD_boton['btn_exp2_PRD'].place_forget()
        PRD_boton['btn_exp2_PRD']  = None
    
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_mnz_‰.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
    
#//////////////////////////////////////////////////////////////////////////////
#                 Reiniciar los ajustes PAE/Valex por manzana
#//////////////////////////////////////////////////////////////////////////////

def Reset_Congig_Map2():
    Change_To_PAEValex()

#//////////////////////////////////////////////////////////////////////////////
#                    Visualizar mapa PAE/Valex por sección
#//////////////////////////////////////////////////////////////////////////////

def Visual_Map_Secc2():
    
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
            
    # -------- Poner en la pagina el mapa -------------------------------------    
    if PRD_canva["cnv_cv_PRD"] is None:
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................
        Separa_x = 1
        Separa_y = 1 
        
        User_min_lon = -0.04
        User_max_lon = 0.02 
        
        User_min_lat = -0.02
        User_max_lat = 0.02
        # .....................................................................
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAEValex_secc(COD_mun,CP_Name,seccion_shp,area_shp,mapdata_scc_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    
    # -------- Poner modificacion del mapa ------------------------------------
    if PRD_boton['lbl_mdm_PRD'] is not None:
        PRD_boton['lbl_mdm_PRD'].place_forget()
        PRD_boton['lbl_mdm_PRD']  = None
    
    if PRD_boton['lbl_mdm_PRD'] is None:
        PRD_boton['lbl_mdm_PRD'] = wnfun_lib.Label_Image('/Modificar_Mapa.png', 
                                        250, 330, cnt_container,"white",0.106,0.57)
        
    opciones_PRD = [-4,-3,-2,-1,0,1,2,3,4]
    opciones2_PRD = [0,1,2,3,4,5]
    # -------- Selección de kilometros de separacion latitudinal --------------
    if PRD_boton['cmb_lon'] is not None:
        PRD_boton['cmb_lon'].place_forget()
        PRD_boton['cmb_lon']  = None
        
    if PRD_boton["cmb_lon"] is None:
        PRD_boton["cmb_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lon"].place(relx=0.816, rely=0.20, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de separacion longitudinal -------------
    if PRD_boton['cmb_lat'] is not None:
        PRD_boton['cmb_lat'].place_forget()
        PRD_boton['cmb_lat']  = None
    
    if PRD_boton["cmb_lat"] is None:
        PRD_boton["cmb_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones2_PRD)
        PRD_boton["cmb_lat"].place(relx=0.77, rely=0.285, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite oeste ------------------------
    if PRD_boton['cmb_min_lon'] is not None:
        PRD_boton['cmb_min_lon'].place_forget()
        PRD_boton['cmb_min_lon']  = None
        
    if PRD_boton["cmb_min_lon"] is None:
        PRD_boton["cmb_min_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lon"].place(relx=0.62, rely=0.375, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite este -------------------------
    if PRD_boton['cmb_max_lon'] is not None:
        PRD_boton['cmb_max_lon'].place_forget()
        PRD_boton['cmb_max_lon']  = None
    
    if PRD_boton["cmb_max_lon"] is None:
        PRD_boton["cmb_max_lon"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lon"].place(relx=0.59, rely=0.465, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite norte ------------------------
    if PRD_boton['cmb_max_lat'] is not None:
        PRD_boton['cmb_max_lat'].place_forget()
        PRD_boton['cmb_max_lat']  = None
    
    if PRD_boton["cmb_max_lat"] is None:
        PRD_boton["cmb_max_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_max_lat"].place(relx=0.607, rely=0.545, 
                            anchor=tk.CENTER, width=40, height=20)
    # -------- Selección de kilometros de limite sur --------------------------
    if PRD_boton['cmb_min_lat'] is not None:
        PRD_boton['cmb_min_lat'].place_forget()
        PRD_boton['cmb_min_lat']  = None
    
    if PRD_boton["cmb_min_lat"] is None:
        PRD_boton["cmb_min_lat"] = ttk.Combobox(PRD_boton['lbl_mdm_PRD'],
                                                values=opciones_PRD)
        PRD_boton["cmb_min_lat"].place(relx=0.572, rely=0.64, 
                            anchor=tk.CENTER, width=40, height=20)        
    
    # -------- Agregar ajustes al mapa ----------------------------------------
    if PRD_boton['btn_ajs_PRD'] is not None:
        PRD_boton['btn_ajs_PRD'].place_forget()
        PRD_boton['btn_ajs_PRD']  = None
    
    if PRD_boton["btn_ajs_PRD"] is None:
        PRD_boton["btn_ajs_PRD"] = wnfun_lib.Button_Image('/Aplicar_Ajustes.png', 
                144, 40, cnt_container,"white",0.106,0.70,Add_Config_Map_secc2)

    # -------- Reiniciar los ajustes ------------------------------------------
    if PRD_boton['btn_rin_PRD'] is not None:
        PRD_boton['btn_rin_PRD'].place_forget()
        PRD_boton['btn_rin_PRD']  = None
    
    if PRD_boton["btn_rin_PRD"] is None:
        PRD_boton["btn_rin_PRD"] = wnfun_lib.Button_Image('/Reiniciar_Ajustes.png', 
                157, 42, cnt_container,"white",0.106,0.748,Reset_Congig_Map_secc2)
    
    # -------- Resultados por seccion PAE_COP ----------------------------------------
    if PRD_boton['btn_scc_PRD'] is not None:
        PRD_boton['btn_scc_PRD'].place_forget()
        PRD_boton['btn_scc_PRD']  = None
    
    if PRD_boton["btn_scc_PRD"] is None:
        PRD_boton["btn_scc_PRD"] = wnfun_lib.Button_Image('/Visualizar_mnz_PRD.png', 
                170, 60, cnt_container,"white",0.12,0.28, Change_To_PAEValex)
        
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton['btn_exp_PRD'] is not None:
        PRD_boton['btn_exp_PRD'].place_forget()
        PRD_boton['btn_exp_PRD']  = None
    if PRD_boton['btn_exp2_PRD'] is not None:
        PRD_boton['btn_exp2_PRD'].place_forget()
        PRD_boton['btn_exp2_PRD']  = None
    
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_scc_‰.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)
        
def Add_Config_Map_secc2():
    
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
            
    # --------- Verificar separacion horizontal -------------------------------
    if PRD_boton["cmb_lon"].get() == '':
        cmb_lon = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación horizontal/longitud")
    else:
        cmb_lon = int(PRD_boton["cmb_lon"].get())
    # --------- Verificar separacion vertical ---------------------------------    
    if PRD_boton["cmb_lat"].get() == '':
        cmb_lat = None
        tk.messagebox.showinfo("ERROR", "Selecciona una separación vertical/latitud")
    else:
        cmb_lat = int(PRD_boton["cmb_lat"].get())
    # --------- Verificar limite oeste ----------------------------------------
    if PRD_boton["cmb_min_lon"].get() == '':
        cmb_min_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al oeste del mapa")
    else:
        cmb_min_lon = int(PRD_boton["cmb_min_lon"].get())
    # --------- Verificar limite este -----------------------------------------    
    if PRD_boton["cmb_max_lon"].get() == '':
        cmb_max_lon = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al este del mapa")
    else:
        cmb_max_lon = int(PRD_boton["cmb_max_lon"].get())
    # --------- Verificar limite norte ----------------------------------------    
    if PRD_boton["cmb_max_lat"].get() == '':
        cmb_max_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al norte del mapa")
    else:
        cmb_max_lat = int(PRD_boton["cmb_max_lat"].get())
    # --------- Verificar limite sur ------------------------------------------    
    if PRD_boton["cmb_min_lat"].get() == '':
        cmb_min_lat = None
        tk.messagebox.showinfo("ERROR", "Establace el numero de km a añadir/quitar al sur del mapa")
    else:
        cmb_min_lat = int(PRD_boton["cmb_min_lat"].get())
    
    if cmb_lon is not None and cmb_lat is not None and cmb_min_lon is not None and cmb_max_lon is not None and cmb_min_lat is not None and cmb_max_lat is not None:
        # Entra aca cuando el usuario hace uso del modificador de mapa 
        
        # ....... CONFIGURACION POR DEFECTO DEL MAPA ..........................        
        User_min_lon_defecto = -0.04
        User_max_lon_defecto = 0.02 
        
        User_min_lat_defecto = -0.02
        User_max_lat_defecto = 0.02
        # .....................................................................
        
        
        Separa_x = cmb_lon
        Separa_y = cmb_lat
        
        User_min_lon = User_min_lon_defecto-1*(cmb_min_lon/100)
        User_max_lon = User_max_lon_defecto+(cmb_max_lon/100)
        User_min_lat = User_min_lat_defecto-1*(cmb_min_lat/100)
        User_max_lat = User_max_lat_defecto+(cmb_max_lat/100)
        
        PRD_canva["cnv_cv_PRD"] = wnfun_lib.canva_mapPAEValex_secc(COD_mun,CP_Name,seccion_shp,area_shp,mapdata_scc_PAE,Modelo_Expo2,cnt_container,0.598,0.575,Separa_x,Separa_y,User_min_lon,User_max_lon,User_min_lat,User_max_lat)
    else:
        tk.messagebox.showinfo("ERROR", "Ingresa todos los parámetros para modificar el mapa")
        
    # .....................................................................
    # ---- Exportar resultados:
    if PRD_boton['btn_exp_PRD'] is not None:
        PRD_boton['btn_exp_PRD'].place_forget()
        PRD_boton['btn_exp_PRD']  = None
    if PRD_boton['btn_exp2_PRD'] is not None:
        PRD_boton['btn_exp2_PRD'].place_forget()
        PRD_boton['btn_exp2_PRD']  = None
    
    if PRD_boton["btn_exp_PRD"] is None:
        PRD_boton["btn_exp_PRD"] = wnfun_lib.Label_Image('/Exportar_ResultadosV2.png', 
                                        210, 50, cnt_container,"white",0.10,0.94)
        
    if PRD_boton["btn_exp2_PRD"] is None:
        PRD_boton["btn_exp2_PRD"] = tk.Button(cnt_container, text="Exportar mapa", font=("Abadi MT", 13), bd=0, bg="#B97F73", fg="white", command=lambda:wnfun_lib.ExportarMapa_Event_Based_Risk(PRD_canva["cnv_cv_PRD"],"Figura_pae_scc_‰.jpg"))
        PRD_boton["btn_exp2_PRD"].place(relx=0.106, rely=0.935, anchor=tk.CENTER)    
    
def Reset_Congig_Map_secc2():
    Visual_Map_Secc2()


#%% ====== FUNCION >> CAMBIAR A TAXONOMIA/MANZANA =============================
def Change_To_Txn():
    
    # Borrar el grafico
    if CLB_canva["cnv_mnz_CLB"] is not None:
        CLB_canva["cnv_mnz_CLB"].get_tk_widget().destroy()
        CLB_canva["cnv_mnz_CLB"] = None
        
    # Borrar titulo del grafico
    if CLB_text["txt_gf2_CLB"] is not None:
        CLB_text["txt_gf2_CLB"].place_forget()
        CLB_text["txt_gf2_CLB"] = None
    # Borrar "Cambiar a taxonomia"
    if CLB_boton["btn_cbm_CLB"] is not None:
        CLB_boton["btn_cbm_CLB"].place_forget()
        CLB_boton["btn_cbm_CLB"] = None
    # Borrar "Cambiar manzana"
    if CLB_rect["rec_cmb_MNZ"] is not None and CLB_boton["cmb_Mnz_CLB"] is not None and CLB_boton["btn_cck_CLB"] is not None:
        CLB_rect["rec_cmb_MNZ"].place_forget()
        CLB_rect["rec_cmb_MNZ"] = None
        CLB_boton["cmb_Mnz_CLB"].place_forget()
        CLB_boton["cmb_Mnz_CLB"] = None
        CLB_boton["btn_cck_CLB"].place_forget()
        CLB_boton["btn_cck_CLB"] = None
        
        
    # .................. Generar el grafico de la taxonomia ................... 
    # ---- Generar grafico taxonomias:
    if CLB_canva["cnv_txn_CLB"] is None:
        text_title = 'Taxonomía: '+str(Txn_Predeter)
        CLB_canva["cnv_txn_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_TXN,cnt_container,text_title,0.75,0.58)
    
    # ---- Titulo del grafico:
    if CLB_text["txt_gf2_CLB"] is None:
        if datos_CP['Event_Based'][0] == "event_based_risk":
            titulo_grafico = "Pérdida anual promedio de la taxonomía"
            font_size = 14
            
        elif datos_CP['Event_Based'][0] == "event_based_damage":
            titulo_grafico = "Daño estructural anual promedio de la taxonomía"
            font_size = 13
        
        CLB_text["txt_gf2_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        CLB_text["txt_gf2_CLB"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
        
    # ---- Combo taxonomias:
    if CLB_rect["rec_cmb_MNZ"] is None:
        CLB_rect["rec_cmb_MNZ"] = wnfun_lib.Label_Image('/combo_txn.png', 250, 38, cnt_container,"white",0.75,0.91)
    if CLB_boton["cmb_Mnz_CLB"] is None:
        CLB_boton["cmb_Mnz_CLB"] = ttk.Combobox(CLB_rect["rec_cmb_MNZ"],values=opciones_txn)
        CLB_boton["cmb_Mnz_CLB"].place(relx=0.72, rely=0.48, anchor=tk.CENTER, width=119, height=20)
    if CLB_boton["btn_cck_CLB"] is None:  
        imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
        imagen = imagen.resize((28,28), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)
        CLB_boton["btn_cck_CLB"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Taxo(CLB_boton["cmb_Mnz_CLB"].get(),CLB_canva["cnv_txn_CLB"]))
        CLB_boton["btn_cck_CLB"].image = imagen
        CLB_boton["btn_cck_CLB"].place(relx=0.875, rely=0.91, anchor=tk.CENTER)
        
    # ---- Cambiar a resultados por manzana:
    if CLB_boton["btn_cbm_CLB"] is None:
        CLB_boton["btn_cbm_CLB"] = wnfun_lib.Button_Image('/pap_mnz.png', 210, 55, cnt_container,"white",0.755,0.25,Change_To_Mnz)

def Change_To_Mnz():
    # Borrar el grafico
    if CLB_canva["cnv_txn_CLB"] is not None:
        CLB_canva["cnv_txn_CLB"].get_tk_widget().destroy()
        CLB_canva["cnv_txn_CLB"] = None
    # Borrar titulo del grafico
    if CLB_text["txt_gf2_CLB"] is not None:
        CLB_text["txt_gf2_CLB"].place_forget()
        CLB_text["txt_gf2_CLB"] = None
    # Borrar "Cambiar a taxonomia"
    if CLB_boton["btn_cbm_CLB"] is not None:
        CLB_boton["btn_cbm_CLB"].place_forget()
        CLB_boton["btn_cbm_CLB"] = None
    # Borrar "Cambiar manzana"
    if CLB_rect["rec_cmb_MNZ"] is not None and CLB_boton["cmb_Mnz_CLB"] is not None and CLB_boton["btn_cck_CLB"] is not None:
        CLB_rect["rec_cmb_MNZ"].place_forget()
        CLB_rect["rec_cmb_MNZ"] = None
        CLB_boton["cmb_Mnz_CLB"].place_forget()
        CLB_boton["cmb_Mnz_CLB"] = None
        CLB_boton["btn_cck_CLB"].place_forget()
        CLB_boton["btn_cck_CLB"] = None
        
    # .................... Generar el grafico de la manzana ................... 
    # ---- Generar grafico manzanas:
    if CLB_canva["cnv_mnz_CLB"] is None:
        text_title = 'CodDANE:'+str(Mnz_Predeter[1::])
        CLB_canva["cnv_mnz_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_MNZ,cnt_container,text_title,0.75,0.58)
    
    # ---- Titulo del grafico:
    if CLB_text["txt_gf2_CLB"] is None:
        if datos_CP['Event_Based'][0] == "event_based_risk":
            titulo_grafico = "Pérdida anual promedio de la manzana"
            font_size = 14
        
        elif datos_CP['Event_Based'][0] == "event_based_damage":
            titulo_grafico = "Daño estructural anual promedio de la manzana"
            font_size = 13
    
        CLB_text["txt_gf2_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        CLB_text["txt_gf2_CLB"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
    
    # ---- Combo manzanas:
    if CLB_rect["rec_cmb_MNZ"] is None:
        CLB_rect["rec_cmb_MNZ"] = wnfun_lib.Label_Image('/combo_mnz.png', 215, 38, cnt_container,"white",0.75,0.91)
    if CLB_boton["cmb_Mnz_CLB"] is None:
        CLB_boton["cmb_Mnz_CLB"] = ttk.Combobox(CLB_rect["rec_cmb_MNZ"],values=opciones_mnz)
        CLB_boton["cmb_Mnz_CLB"].place(relx=0.78, rely=0.48, anchor=tk.CENTER, width=63, height=20)
    if CLB_boton["btn_cck_CLB"] is None:  
        imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
        imagen = imagen.resize((28,28), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)
        CLB_boton["btn_cck_CLB"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Block(CLB_boton["cmb_Mnz_CLB"].get(),CLB_canva["cnv_mnz_CLB"]))
        CLB_boton["btn_cck_CLB"].image = imagen
        CLB_boton["btn_cck_CLB"].place(relx=0.86, rely=0.91, anchor=tk.CENTER)
        
    # ---- Cambiar a resultados por taxonomia:
    if CLB_boton["btn_cbm_CLB"] is None:
        CLB_boton["btn_cbm_CLB"] = wnfun_lib.Button_Image('/pap_taxo.png', 210, 55, cnt_container,"white",0.75,0.25,Change_To_Txn)
    

def Change_To_Txn_DSP():
    # Borrar el grafico
    if DSP_canva["cnv_mnz_DSP"] is not None:
        DSP_canva["cnv_mnz_DSP"].get_tk_widget().destroy()
        DSP_canva["cnv_mnz_DSP"] = None
    # Borrar titulo del grafico
    if DSP_text["txt_gf2_DSP"] is not None:
        DSP_text["txt_gf2_DSP"].place_forget()
        DSP_text["txt_gf2_DSP"] = None
    # Borrar "Cambiar a taxonomia"
    if DSP_boton["btn_cbm_DSP"] is not None:
        DSP_boton["btn_cbm_DSP"].place_forget()
        DSP_boton["btn_cbm_DSP"] = None
    # Borrar "Cambiar manzana"
    if DSP_rect["rec_cmb_DSP"] is not None and DSP_boton["cmb_Mnz_DSP"] is not None and DSP_boton["btn_cck_DSP"] is not None:
        DSP_rect["rec_cmb_DSP"].place_forget()
        DSP_rect["rec_cmb_DSP"] = None
        DSP_boton["cmb_Mnz_DSP"].place_forget()
        DSP_boton["cmb_Mnz_DSP"] = None
        DSP_boton["btn_cck_DSP"].place_forget()
        DSP_boton["btn_cck_DSP"] = None
    # .................. Generar el grafico de la taxonomia ................... 
    # ---- Generar grafico taxonomias:
    if DSP_canva["cnv_txn_DSP"] is None:
        text_title = 'Taxonomía: '+ str(Txn_Predeter_DSP)
        DSP_canva["cnv_txn_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_TXN_DSP,cnt_container,text_title,0.75,0.58)
    # ---- Titulo del grafico:
    if DSP_text["txt_gf2_DSP"] is None:
        
        if datos_TXN_DSP['Event_Based'][0] == "event_based_risk":
            titulo_grafico = 'Dispersión de las pérdidas anuales promedio de la taxonomía'
            font_size = 13
            
        elif datos_TXN_DSP['Event_Based'][0] == "event_based_damage":
            titulo_grafico = 'Dispersión de los daños estructurales anuales promedio de la taxonomía'
            font_size = 12
        
        DSP_text["txt_gf2_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        DSP_text["txt_gf2_DSP"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
    # ---- Combo taxonomias:
        
    if DSP_rect["rec_cmb_DSP"] is not None:
        DSP_rect["rec_cmb_DSP"].place_forget()
        DSP_rect["rec_cmb_DSP"] = None       
        
    if DSP_rect["rec_cmb_DSP"] is None:
        DSP_rect["rec_cmb_DSP"] = wnfun_lib.Label_Image('/combo_txn.png', 250, 38, cnt_container,"white",0.75,0.91)
    if DSP_boton["cmb_Mnz_DSP"] is None:
        DSP_boton["cmb_Mnz_DSP"] = ttk.Combobox(DSP_rect["rec_cmb_DSP"],values=opciones_txn_DSP)
        DSP_boton["cmb_Mnz_DSP"].place(relx=0.72, rely=0.48, anchor=tk.CENTER, width=119, height=20)
    if DSP_boton["btn_cck_DSP"] is None:  
        imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
        imagen = imagen.resize((28,28), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)
        DSP_boton["btn_cck_DSP"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Taxo_DSP(DSP_boton["cmb_Mnz_DSP"].get(),DSP_canva["cnv_txn_DSP"]))
        DSP_boton["btn_cck_DSP"].image = imagen
        DSP_boton["btn_cck_DSP"].place(relx=0.875, rely=0.91, anchor=tk.CENTER)
    # ---- Cambiar a resultados por manzana:
    if DSP_boton["btn_cbm_DSP"] is not None:
        DSP_boton["btn_cbm_DSP"].place_forget()
        DSP_boton["btn_cbm_DSP"] = None
        
    if DSP_boton["btn_cbm_DSP"] is None:
        DSP_boton["btn_cbm_DSP"] = wnfun_lib.Button_Image('/pap_mnz.png', 210, 55, cnt_container,"white",0.755,0.25,Change_To_Mnz_DSP)

def Change_To_Mnz_DSP():
    # Borrar el grafico
    if DSP_canva["cnv_txn_DSP"] is not None:
        DSP_canva["cnv_txn_DSP"].get_tk_widget().destroy()
        DSP_canva["cnv_txn_DSP"] = None
    # Borrar titulo del grafico
    if DSP_text["txt_gf2_DSP"] is not None:
        DSP_text["txt_gf2_DSP"].place_forget()
        DSP_text["txt_gf2_DSP"] = None
    # Borrar "Cambiar a taxonomia"
    if DSP_boton["btn_cbm_DSP"] is not None:
        DSP_boton["btn_cbm_DSP"].place_forget()
        DSP_boton["btn_cbm_DSP"] = None
    # Borrar "Cambiar manzana"
    if DSP_rect["rec_cmb_DSP"] is not None and DSP_boton["cmb_Mnz_DSP"] is not None and DSP_boton["btn_cck_DSP"] is not None:
        DSP_rect["rec_cmb_DSP"].place_forget()
        DSP_rect["rec_cmb_DSP"] = None
        DSP_boton["cmb_Mnz_DSP"].place_forget()
        DSP_boton["cmb_Mnz_DSP"] = None
        DSP_boton["btn_cck_DSP"].place_forget()
        DSP_boton["btn_cck_DSP"] = None
    # .................. Generar el grafico de la taxonomia ................... 
    # ---- Generar grafico manzanas:
    if DSP_canva["cnv_mnz_DSP"] is None:
        text_title = 'CodDANE:'+str(Mnz_Predeter_DSP[1::])
        DSP_canva["cnv_mnz_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_MNZ_DSP,cnt_container,text_title,0.75,0.58)
    # ---- Titulo del grafico:
    if DSP_text["txt_gf2_DSP"] is None:
        
        if datos_MNZ_DSP['Event_Based'][0] == "event_based_risk":
            titulo_grafico = 'Dispersión de las pérdidas anuales promedio de la manzana'
            font_size = 13
            
        elif datos_MNZ_DSP['Event_Based'][0] == "event_based_damage":
            titulo_grafico = 'Dispersión de los daños estructurales anuales promedio de la manzana'
            font_size = 12
        
        DSP_text["txt_gf2_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        DSP_text["txt_gf2_DSP"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
    # ---- Combo manzanas:
    if DSP_rect["rec_cmb_DSP"] is not None:
        DSP_rect["rec_cmb_DSP"].place_forget()
        DSP_rect["rec_cmb_DSP"] = None    
        
    if DSP_rect["rec_cmb_DSP"] is None:
        DSP_rect["rec_cmb_DSP"] = wnfun_lib.Label_Image('/combo_mnz.png', 215, 38, cnt_container,"white",0.75,0.91)
    if DSP_boton["cmb_Mnz_DSP"] is None:
        DSP_boton["cmb_Mnz_DSP"] = ttk.Combobox(DSP_rect["rec_cmb_DSP"],values=opciones_mnz_DSP)
        DSP_boton["cmb_Mnz_DSP"].place(relx=0.78, rely=0.48, anchor=tk.CENTER, width=63, height=20)
    if DSP_boton["btn_cck_DSP"] is None:  
        imagen = Image.open(os.path.join(os.getcwd(),"icon") + '/check.png')
        imagen = imagen.resize((28,28), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)
        DSP_boton["btn_cck_DSP"] = tk.Button(cnt_container, image=imagen, bd=0, bg="white", command=lambda:Change_Block_DSP(DSP_boton["cmb_Mnz_DSP"].get(),DSP_canva["cnv_mnz_DSP"]))
        DSP_boton["btn_cck_DSP"].image = imagen
        DSP_boton["btn_cck_DSP"].place(relx=0.86, rely=0.91, anchor=tk.CENTER)
        
    # ---- Cambiar a resultados por taxonomia:
    if DSP_boton["btn_cbm_DSP"] is not None:
        DSP_boton["btn_cbm_DSP"].place_forget()
        DSP_boton["btn_cbm_DSP"] = None
        
    if DSP_boton["btn_cbm_DSP"] is None:
        DSP_boton["btn_cbm_DSP"] = wnfun_lib.Button_Image('/pap_taxo.png', 210, 55, cnt_container,"white",0.75,0.25,Change_To_Txn_DSP)

#%% ====== FUNCION >> COMBOS ==================================================
def Change_Block(combo,canvas1):
    if combo == '':
        combo = None 
        tk.messagebox.showinfo("ERROR", "Selecciona una manzana")  
    else:
        # Borrar el grafico canvas 1 para generar uno nuevo
        if canvas1 is not None:
            canvas1.get_tk_widget().destroy()
            canvas1 = None
        # Borrar titulo del grafico
        if CLB_text["txt_gf2_CLB"] is not None:
            CLB_text["txt_gf2_CLB"].place_forget()
            CLB_text["txt_gf2_CLB"] = None
        # .............. Generar el grafico con la nueva manzana ..............
        manzanapred = str(codigo_mnz[0])+str(combo)
        fila_a_graficar = simmnz_losses.loc[simmnz_losses['Manzana'] == manzanapred]
        fila_a_graficar2 = simmnz_losses2.loc[simmnz_losses2['Manzana'] == manzanapred]
        fila_a_graficar = fila_a_graficar[['Manzana']+['Sim_{}'.format(i) for i in newNsim_mnz]]
        fila_a_graficar2 = fila_a_graficar2[['Manzana']+['Sim_{}'.format(i) for i in newNsim_mnz]]
        fila_a_graficar = fila_a_graficar.drop(columns=['Manzana'])
        fila_a_graficar2 = fila_a_graficar2.drop(columns=['Manzana'])
        datos_fila = fila_a_graficar.values[0]*100
        datos_fila2 = fila_a_graficar2.values[0]
        
        datos_fila_error = [0] 
        for i in range(1, len(datos_fila2)-1):
            error1 = np.abs(1-(datos_fila2[i]/datos_fila2[i-1]))*100
            error2 = np.abs(1-(datos_fila2[i+1]/datos_fila2[i]))*100
            error_promedio = np.mean([error1,error2])
            datos_fila_error.append(float(error_promedio))
        datos_fila_error.append(np.abs(1-(datos_fila2[i+1]/datos_fila2[i]))*100)
        
        datos_MNZ_New = {'Num_Sim':newNsim_mnz,'loss':datos_fila,'error':datos_fila_error,'Num_Sim_Ev':sorted(Nevents),'Event_Based':datos_MNZ['Event_Based']}
        
        # .....................................................................
        text_title = 'CodDANE:'+str(manzanapred[1::])
        CLB_canva["cnv_mnz_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_MNZ_New,cnt_container,text_title,0.75,0.58)
        
        # Colocar titulo del grafico: 
        if datos_MNZ['Event_Based'][0] == "event_based_risk":
            titulo_grafico = 'Pérdida anual promedio de la manzana'
            font_size = 14
            
        elif datos_MNZ['Event_Based'][0] == "event_based_damage":
            titulo_grafico = 'Daño estructural anual promedio de la manzana'
            font_size = 13
        
        CLB_text["txt_gf2_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        CLB_text["txt_gf2_CLB"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
            
def Change_Taxo(combo,canvas1):
    if combo == '':
        combo = None 
        tk.messagebox.showinfo("ERROR", "Selecciona una taxonomía")  
    else:
        # Borrar el grafico canvas 1 para generar uno nuevo
        if canvas1 is not None:
            canvas1.get_tk_widget().destroy()
            canvas1 = None
        # Borrar titulo del grafico
        if CLB_text["txt_gf2_CLB"] is not None:
            CLB_text["txt_gf2_CLB"].place_forget()
            CLB_text["txt_gf2_CLB"] = None
        # .............. Generar el grafico con la nueva manzana ..............
        manzanapred = str(combo)
        fila_a_graficar = simtxn_losses.loc[simtxn_losses['Manzana'] == manzanapred]
        fila_a_graficar2 = simtxn_losses2.loc[simtxn_losses2['Manzana'] == manzanapred]
        fila_a_graficar = fila_a_graficar[['Manzana']+['Sim_{}'.format(i) for i in newNsim_txn]]
        fila_a_graficar2 = fila_a_graficar2[['Manzana']+['Sim_{}'.format(i) for i in newNsim_txn]]
        fila_a_graficar = fila_a_graficar.drop(columns=['Manzana'])
        fila_a_graficar2 = fila_a_graficar2.drop(columns=['Manzana'])
        datos_fila = fila_a_graficar.values[0]*100
        datos_fila2 = fila_a_graficar2.values[0]
        
        datos_fila_error = [0] 
        for i in range(1, len(datos_fila2)-1):
            error1 = np.abs(1-(datos_fila2[i]/datos_fila2[i-1]))*100
            error2 = np.abs(1-(datos_fila2[i+1]/datos_fila2[i]))*100
            error_promedio = np.mean([error1,error2])
            datos_fila_error.append(float(error_promedio))
        datos_fila_error.append(np.abs(1-(datos_fila2[i+1]/datos_fila2[i]))*100)
        
        datos_MNZ_New = {'Num_Sim':newNsim_txn,'loss':datos_fila,'error':datos_fila_error,'Num_Sim_Ev':sorted(Nevents),'Event_Based':datos_TXN['Event_Based']}
        
        # .....................................................................
        text_title = 'Taxonomía: '+ manzanapred
        CLB_canva["cnv_txn_CLB"] = wnfun_lib.canva_CLB_Mnz(datos_MNZ_New,cnt_container,text_title,0.75,0.58)
        
        # Colocar titulo del grafico:    
        if datos_TXN['Event_Based'][0] == "event_based_risk":
            titulo_grafico = 'Pérdida anual promedio de la taxonomía'
            font_size = 14
            
        elif datos_TXN['Event_Based'][0] == "event_based_damage":
            titulo_grafico = 'Daño estructural anual promedio de la taxonomía'
            font_size = 13
        
        CLB_text["txt_gf2_CLB"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        CLB_text["txt_gf2_CLB"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)

def Change_Block_DSP(combo,canvas1):
    if combo == '':
        combo = None 
        tk.messagebox.showinfo("ERROR", "Selecciona una manzana")  
    else:
        # Borrar el grafico canvas 1 para generar uno nuevo
        if canvas1 is not None:
            canvas1.get_tk_widget().destroy()
            canvas1 = None
        # Borrar titulo del grafico
        if DSP_text["txt_gf2_DSP"] is not None:
            DSP_text["txt_gf2_DSP"].place_forget()
            DSP_text["txt_gf2_DSP"] = None
        # .............. Generar el grafico con la nueva manzana ..............
        manzanapred = str(codigo_mnz_DSP[0])+str(combo)
        fila_a_graficar = simmnz_losses_DSP.loc[simmnz_losses_DSP['Manzana'] == manzanapred]
        fila_a_graficar = fila_a_graficar[['Manzana']+['Sim_{}'.format(i) for i in newNsim_mnz_DSP]]
        fila_a_graficar = fila_a_graficar.drop(columns=['Manzana'])
        datos_fila = fila_a_graficar.values[0]
        
        datos_MNZ_New = {'Num_Sim':newNsim_mnz_DSP,'loss':datos_fila,'Num_Sim_Ev':sorted(Nevents_DSP),'Event_Based':datos_MNZ_DSP['Event_Based']}
        # .....................................................................
        text_title = 'CodDANE:'+str(manzanapred[1::])
        DSP_canva["cnv_mnz_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_MNZ_New,cnt_container,text_title,0.75,0.58)
        
        # Colocar titulo del grafico:    
        if datos_MNZ_DSP['Event_Based'][0] == "event_based_risk":
            titulo_grafico = 'Dispersión de las pérdidas anuales promedio de la manzana'
            font_size = 13
            
        elif datos_MNZ_DSP['Event_Based'][0] == "event_based_damage":
            titulo_grafico = 'Dispersión de los daños estructurales anuales promedio de la manzana'
            font_size = 12
            
        DSP_text["txt_gf2_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        DSP_text["txt_gf2_DSP"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
        
def Change_Taxo_DSP(combo,canvas1):
    if combo == '':
        combo = None 
        tk.messagebox.showinfo("ERROR", "Selecciona una taxonomía")  
    else:
        # Borrar el grafico canvas 1 para generar uno nuevo
        if canvas1 is not None:
            canvas1.get_tk_widget().destroy()
            canvas1 = None
        # Borrar titulo del grafico
        if DSP_text["txt_gf2_DSP"] is not None:
            DSP_text["txt_gf2_DSP"].place_forget()
            DSP_text["txt_gf2_DSP"] = None
        # .............. Generar el grafico con la nueva manzana ..............
        manzanapred = str(combo)
        fila_a_graficar = simtxn_losses_DSP.loc[simtxn_losses_DSP['Taxonomia'] == manzanapred]
        fila_a_graficar = fila_a_graficar[['Taxonomia']+['Sim_{}'.format(i) for i in newNsim_txn_DSP]]
        fila_a_graficar = fila_a_graficar.drop(columns=['Taxonomia'])
        datos_fila = fila_a_graficar.values[0]
        
        datos_MNZ_New = {'Num_Sim':newNsim_txn_DSP,'loss':datos_fila,'Num_Sim_Ev':sorted(Nevents_DSP),'Event_Based':datos_TXN_DSP['Event_Based']}
        # .....................................................................
        text_title = 'Taxonomía: '+ manzanapred
        DSP_canva["cnv_txn_DSP"] = wnfun_lib.canva_DSP_Mnz(datos_MNZ_New,cnt_container,text_title,0.75,0.58)
        # Colocar titulo del grafico:
        
        if datos_TXN_DSP['Event_Based'][0] == "event_based_risk":
            titulo_grafico = 'Dispersión de las pérdidas anuales promedio de la taxonomía'
            font_size = 13
            
        elif datos_TXN_DSP['Event_Based'][0] == "event_based_damage":
            titulo_grafico = 'Dispersión de los daños estructurales anuales promedio de la taxonomía'
            font_size = 12
        
        DSP_text["txt_gf2_DSP"] = tk.Label(cnt_container, text=titulo_grafico, font=("Abadi MT", font_size, "bold"), bg="white", fg="#3B3838")
        DSP_text["txt_gf2_DSP"].place(relx=0.75, rely=0.31, anchor=tk.CENTER)
        
#%% ====== FUNCION >> SELECCIONAR CARPETA =====================================
def Select_Folder_CLB():
    global carpeta_seleccionada                                                 # El directorio lo hace una variable global
    # filedialog.askdirectory() devuelve la ruta completa del directorio 
    # seleccionado por el usuario
    carpeta_seleccionada = filedialog.askdirectory()                            # Deja que el usuario seleccione la carpeta en donde estan los resultados
    # ................ Cuando la carpeta se selecciona ........................
    if CLB_boton["btn_slc_CLB"] is not None:
        # Eliminar boton seleccionar carpeta
        CLB_boton["btn_slc_CLB"].place_forget()
        CLB_boton["btn_slc_CLB"] = None
        # Eliminar boton de informacion
        CLB_boton["btn_inf_CLB"].place_forget()
        CLB_boton["btn_inf_CLB"] = None
        # Eliminar boton calibrar
        CLB_boton["btn_clb_CLB"].place_forget()
        CLB_boton["btn_clb_CLB"] = None
    if CLB_boton["btn_slc_CLB"] is None:
        if CLB_boton2["SiNo"] is not None:
            # Crear boton seleccionar carpeta >> ya seleccionada
            CLB_boton["btn_slc_CLB"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png', 230, 50, cnt_container,"#F2F2F2",0.73,0.096,Select_Folder_CLB)
            # Crear boton de informacion
            CLB_boton["btn_inf_CLB"] = wnfun_lib.Button_Image('/Info.png', 22, 22, cnt_container,"#F2F2F2",0.82,0.084,Ventana_Info_CLB)
            # Crear boton generar
            CLB_boton["btn_clb_CLB"] = wnfun_lib.Button_Image_lambda('/Calibrate_Button.png', 144, 43, cnt_container,"#F2F2F2",0.90,0.097,Function_Calibrate,resultado_label)
        else:
            # Crear boton seleccionar carpeta >> ya seleccionada
            CLB_boton["btn_slc_CLB"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png', 320, 75, cnt_container,"white",0.78,0.5,Select_Folder_CLB)
            # Crear boton de informacion
            CLB_boton["btn_inf_CLB"] = wnfun_lib.Button_Image('/Info.png', 35, 35, cnt_container,"white",0.905,0.468,Ventana_Info_CLB)
            # Crear boton generar
            CLB_boton["btn_clb_CLB"] = wnfun_lib.Button_Image_lambda('/Calibrate_Button.png', 200, 60, cnt_container,"white",0.78 ,0.58,Function_Calibrate,resultado_label)
    # .........................................................................
    
    return carpeta_seleccionada

def Select_Folder_DSP():
    global carpeta_seleccionada_DSP                                             # El directorio lo hace una variable global
    # filedialog.askdirectory() devuelve la ruta completa del directorio 
    # seleccionado por el usuario
    carpeta_seleccionada_DSP = filedialog.askdirectory()                         # Deja que el usuario seleccione la carpeta en donde estan los resultados
    # ................ Cuando la carpeta se selecciona ........................
    if DSP_boton["btn_slc_DSP"] is not None:
        # Eliminar boton seleccionar carpeta
        DSP_boton["btn_slc_DSP"].place_forget()
        DSP_boton["btn_slc_DSP"] = None
        # Eliminar boton de informacion
        DSP_boton["btn_inf_DSP"].place_forget()
        DSP_boton["btn_inf_DSP"] = None
        # Eliminar boton calibrar
        DSP_boton["btn_clb_DSP"].place_forget()
        DSP_boton["btn_clb_DSP"] = None
    if DSP_boton["btn_slc_DSP"] is None:
        if DSP_boton2["SiNo"] is not None:
            # Crear boton seleccionar carpeta >> ya seleccionada
            DSP_boton["btn_slc_DSP"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png', 230, 50, cnt_container,"#F2F2F2",0.73,0.096,Select_Folder_DSP)
            # Crear boton de informacion
            DSP_boton["btn_inf_DSP"] = wnfun_lib.Button_Image('/Info.png', 22, 22, cnt_container,"#F2F2F2",0.82,0.084,Ventana_Info_DSP)
            # Crear boton generar
            DSP_boton["btn_clb_DSP"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 43, cnt_container,"#F2F2F2",0.90,0.097,Function_Dispersion,resultado_label_Dispersion)
        else:
            # Crear boton seleccionar carpeta >> ya seleccionada
            DSP_boton["btn_slc_DSP"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png', 320, 75, cnt_container,"white",0.78,0.5,Select_Folder_DSP)
            # Crear boton de informacion
            DSP_boton["btn_inf_DSP"] = wnfun_lib.Button_Image('/Info.png', 35, 35, cnt_container,"white",0.905,0.468,Ventana_Info_DSP)
            # Crear boton generar
            DSP_boton["btn_clb_DSP"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 200, 66, cnt_container,"white",0.78,0.58,Function_Dispersion,resultado_label_Dispersion)

    return carpeta_seleccionada_DSP

def Select_Folder_PRD():
    global carpeta_seleccionada_PRD                                             # El directorio lo hace una variable global
    # filedialog.askdirectory() devuelve la ruta completa del directorio 
    # seleccionado por el usuario
    carpeta_seleccionada_PRD = filedialog.askdirectory()                         # Deja que el usuario seleccione la carpeta en donde estan los resultados
    
    if PRD_boton["btn_slc_PRD"] is not None:
        # Eliminar boton seleccionar carpeta
        PRD_boton["btn_slc_PRD"].place_forget()
        PRD_boton["btn_slc_PRD"] = None
        # Eliminar boton de informacion
        PRD_boton["btn_inf_PRD"].place_forget()
        PRD_boton["btn_inf_PRD"] = None
        # Eliminar boton calibrar
        PRD_boton["btn_clb_PRD"].place_forget()
        PRD_boton["btn_clb_PRD"] = None
        # Eliminar ingresar periodo de analisis
        PRD_boton["btn_ing_PRD"].place_forget()
        PRD_boton["btn_ing_PRD"] = None
        PRD_rectg["rec_per_PRD"].place_forget()
        PRD_rectg["rec_per_PRD"] = None
        PRD_entry["ent_per_PRD"].place_forget()
        PRD_entry["ent_per_PRD"] = None
        
    if PRD_boton["btn_slc_PRD"] is None:
        if PRD_boton2["SiNo"] is not None:
            # Crear periodo de analisis
            PRD_boton["btn_ing_PRD"] = wnfun_lib.Label_Image('/Ingresar_Periodo.png', 240, 47, cnt_container,"#F2F2F2",0.72,0.108)
            PRD_rectg["rec_per_PRD"] = tk.Canvas(cnt_container, bg="#F2F2F2", bd=0, highlightthickness=0)
            PRD_rectg["rec_per_PRD"].place(relx=0.825, rely=0.1, anchor=tk.CENTER, width=55, height=28)
            x2, y2 = 54, 27
            x1, y1 = 10,10
            radio_esquinas = 5
            color = "#D0CECE"
            wnfun_lib.rec_redond(PRD_rectg["rec_per_PRD"], x1, y1, x2, y2, radio_esquinas, color)
            PRD_entry["ent_per_PRD"] = tk.Entry(PRD_rectg["rec_per_PRD"], bg = "#D0CECE", bd=0, highlightthickness=0)
            PRD_entry["ent_per_PRD"].place(relx=0.55, rely=0.63, anchor=tk.CENTER, width=30, height=15)
            #Crear boton seleccionar carpeta >> ya seleccionada
            PRD_boton["btn_slc_PRD"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png', 175, 41, cnt_container,"#F2F2F2",0.74,0.068, Select_Folder_PRD)
            # Crear boton de informacion
            PRD_boton["btn_inf_PRD"] = wnfun_lib.Button_Image('/Info.png', 19, 19, cnt_container,"#F2F2F2",0.81,0.055,Ventana_Info_PRD)
            # Crear boton generar
            PRD_boton["btn_clb_PRD"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 48, cnt_container,"#F2F2F2",0.92,0.097,Function_Perdidas,resultado_label_PRD)
        else:
            # Crear boton seleccionar carpeta >> ya seleccionada
            PRD_boton["btn_slc_PRD"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png', 278, 65, cnt_container,"white",0.722,0.47, Select_Folder_PRD)
            # Crear boton de informacion
            PRD_boton["btn_inf_PRD"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.829,0.442,Ventana_Info_PRD)
            # Crear boton generar
            PRD_boton["btn_clb_PRD"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 200, 66, cnt_container,"white",0.78,0.66,Function_Perdidas,resultado_label_PRD)
            # Crear periodo de analisis
            PRD_boton["btn_ing_PRD"] = wnfun_lib.Label_Image('/Ingresar_Periodo.png', 380, 75, cnt_container,"white",0.76,0.55)
            PRD_rectg["rec_per_PRD"] = tk.Canvas(cnt_container, bg="white", bd=0, highlightthickness=0)
            PRD_rectg["rec_per_PRD"].place(relx=0.921, rely=0.54, anchor=tk.CENTER, width=71, height=36)
            x2, y2 = 70, 35
            x1, y1 = 10,10
            radio_esquinas = 5
            color = "#D0CECE"
            wnfun_lib.rec_redond(PRD_rectg["rec_per_PRD"], x1, y1, x2, y2, radio_esquinas, color)
            PRD_entry["ent_per_PRD"] = tk.Entry(PRD_rectg["rec_per_PRD"], bg = "#D0CECE", bd=0, highlightthickness=0)
            PRD_entry["ent_per_PRD"].place(relx=0.55, rely=0.62, anchor=tk.CENTER, width=40, height=20)
    
    return carpeta_seleccionada_PRD

def Select_Folder_DNO():
    global carpeta_seleccionada_DNO                                                 # El directorio lo hace una variable global
    
    
    carpeta_seleccionada_DNO = filedialog.askdirectory()
    # filedialog.askdirectory() devuelve la ruta completa del directorio 
    # seleccionado por el usuario
    
    if DNO_boton["btn_slc_DNO"] is not None:
        # Eliminar boton seleccionar carpeta
        DNO_boton["btn_slc_DNO"].place_forget()
        DNO_boton["btn_slc_DNO"] = None
        # Eliminar boton de informacion
        DNO_boton["btn_inf_DNO"].place_forget()
        DNO_boton["btn_inf_DNO"] = None
        # Eliminar boton calibrar
        DNO_boton["btn_clb_DNO"].place_forget()
        DNO_boton["btn_clb_DNO"] = None
        
    if DNO_boton["btn_slc_DNO"] is None:
        if DNO_boton2["SiNo"] is not None:
            #Crear boton seleccionar carpeta >> ya seleccionada
            DNO_boton["btn_slc_DNO"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png', 175, 41, cnt_container,"#F2F2F2",0.74,0.068, Select_Folder_DNO)
            # Crear boton de informacion
            DNO_boton["btn_inf_DNO"] = wnfun_lib.Button_Image('/Info.png', 19, 19, cnt_container,"#F2F2F2",0.81,0.055,Ventana_Info_DNO)
            # Crear boton generar
            DNO_boton["btn_clb_DNO"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 144, 48, cnt_container,"#F2F2F2",0.92,0.097,Function_Danos,resultado_label_DNO)
        else:
            # Crear boton seleccionar carpeta >> ya seleccionada
            DNO_boton["btn_slc_DNO"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png',278, 65, cnt_container,"white",0.78,0.5, Select_Folder_DNO)
            # Crear boton de informacion
            DNO_boton["btn_inf_DNO"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.885,0.468,Ventana_Info_DNO)
            # Crear boton generar
            DNO_boton["btn_clb_DNO"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png',  200, 66, cnt_container,"white",0.78,0.58,Function_Danos,resultado_label_DNO)
           
     
    return carpeta_seleccionada_DNO

def Select_Folder_MAP():
    global carpeta_seleccionada_MAP                                                 # El directorio lo hace una variable global
    # filedialog.askdirectory() devuelve la ruta completa del directorio 
    # seleccionado por el usuario
   
    carpeta_seleccionada_MAP = filedialog.askdirectory() 
    
    if MAP_boton["btn_slc_MAP"] is not None:
        # Eliminar boton seleccionar carpeta
        MAP_boton["btn_slc_MAP"].place_forget()
        MAP_boton["btn_slc_MAP"] = None
        # Eliminar boton de informacion
        MAP_boton["btn_inf_MAP"].place_forget()
        MAP_boton["btn_inf_MAP"] = None
        # Eliminar boton calibrar
        MAP_boton["btn_clb_MAP"].place_forget()
        MAP_boton["btn_clb_MAP"] = None
        
    if MAP_boton["btn_slc_MAP"] is None:
        # Crear boton seleccionar carpeta >> ya seleccionada
        MAP_boton["btn_slc_MAP"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png',278, 65, cnt_container,"white",0.78,0.5, Select_Folder_MAP)
        # Crear boton de informacion
        MAP_boton["btn_inf_MAP"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.885,0.468,Ventana_Info_MAP)
        # Crear boton generar
        MAP_boton["btn_clb_MAP"] = wnfun_lib.Button_Image_lambda('/Generate_Results.png', 252, 55, cnt_container,"white",0.78,0.58,Function_Maps,resultado_label_MAP)
       

    return carpeta_seleccionada_MAP

def Select_Folder_GEN():
    global carpeta_seleccionada_GEN                                                # El directorio lo hace una variable global
    # filedialog.askdirectory() devuelve la ruta completa del directorio 
    # seleccionado por el usuario
   
    carpeta_seleccionada_GEN = filedialog.askdirectory() 
    
    if GEN_boton["btn_slc_GEN"] is not None:
        # Eliminar boton seleccionar carpeta
        GEN_boton["btn_slc_GEN"].place_forget()
        GEN_boton["btn_slc_GEN"] = None
        # Eliminar boton de informacion
        GEN_boton["btn_inf_GEN"].place_forget()
        GEN_boton["btn_inf_GEN"] = None
        # Eliminar boton calibrar
        GEN_boton["btn_clb_GEN"].place_forget()
        GEN_boton["btn_clb_GEN"] = None
        
    if GEN_boton["btn_slc_GEN"] is None:
        # Crear boton seleccionar carpeta >> ya seleccionada
        GEN_boton["btn_slc_GEN"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png',278, 65, cnt_container,"white",0.78,0.5, Select_Folder_GEN)
        # Crear boton de informacion
        GEN_boton["btn_inf_GEN"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.885,0.468,Ventana_Info_GEN)
        # Crear boton generar
        GEN_boton["btn_clb_GEN"] = wnfun_lib.Button_Image_lambda('/Generate_Results.png', 252, 55, cnt_container,"white",0.78,0.58,Function_Generador,resultado_label_GEN)
       
    return carpeta_seleccionada_GEN

def Select_Folder_FCH():
    global carpeta_seleccionada_FCH                                                # El directorio lo hace una variable global
    # filedialog.askdirectory() devuelve la ruta completa del directorio 
    # seleccionado por el usuario
   
    carpeta_seleccionada_FCH = filedialog.askdirectory() 
    
    if FCH_boton["btn_slc_FCH"] is not None:
        # Eliminar boton seleccionar carpeta
        FCH_boton["btn_slc_FCH"].place_forget()
        FCH_boton["btn_slc_FCH"] = None
        # Eliminar boton de informacion
        FCH_boton["btn_inf_FCH"].place_forget()
        FCH_boton["btn_inf_FCH"] = None
        # Eliminar boton calibrar
        FCH_boton["btn_clb_FCH"].place_forget()
        FCH_boton["btn_clb_FCH"] = None
        
    if FCH_boton["btn_slc_FCH"] is None:
        # Crear boton seleccionar carpeta >> ya seleccionada
        FCH_boton["btn_slc_FCH"] = wnfun_lib.Button_Image('/Select_Folder_Slc.png',278, 65, cnt_container,"white",0.78,0.5, Select_Folder_FCH)
        # Crear boton de informacion
        FCH_boton["btn_inf_FCH"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.885,0.468,Ventana_Info_FCH)
        # Crear boton generar
        FCH_boton["btn_clb_FCH"] = wnfun_lib.Button_Image_lambda('/Generate_Results.png', 252, 55, cnt_container,"white",0.78,0.58,Function_Ficha,resultado_label_FCH)
       
    return carpeta_seleccionada_FCH
    
#%% ====== FUNCION >> INFORMACION =============================================
def Ventana_Info():
    ventana_emergente = Toplevel()
    # Titulo de la ventana
    ventana_emergente.title("¿Qué debe haber en la carpeta?")
    
    # mensaje1 = "============= La carpeta debe contener: =============" 
    mensaje1 = "======= La carpeta debe contener una de las siguientes opciones: =======" 
    mensaje2 = "1. Carpeta 'hdf5_Mnz' con archivos .hdf5 agregados por manzana y una"
    mensaje3 = "llamada 'hdf5_Txn' con los archivos .hdf5 agregados por taxonomía."
    mensaje4 = "2. Carpeta con archivos .hdf5 agregados únicamente por manzana         "
    mensaje5 = "3. Carpeta con archivos .hdf5 agregados únicamente por taxonomía      "
    mensaje6 = "4. Carpeta con archivos .hdf5 sin agregado                                                   "
    
    texto_v = "                                                                                                                           "
    # Colocar mensajes y boton cerrar
    tk.Label(ventana_emergente, text=texto_v, padx=40, pady=90).pack()
    tk.Label(ventana_emergente, text=mensaje1).place(relx=0.5, rely=0.15, anchor=tk.CENTER) # 0.2
    tk.Label(ventana_emergente, text=mensaje2).place(relx=0.5, rely=0.30, anchor=tk.CENTER) # 0.35
    tk.Label(ventana_emergente, text=mensaje3).place(relx=0.5, rely=0.39, anchor=tk.CENTER) # 0.5
    
    tk.Label(ventana_emergente, text=mensaje4).place(relx=0.5, rely=0.51, anchor=tk.CENTER)
    
    tk.Label(ventana_emergente, text=mensaje5).place(relx=0.5, rely=0.63, anchor=tk.CENTER)
    
    tk.Label(ventana_emergente, text=mensaje6).place(relx=0.5, rely=0.75, anchor=tk.CENTER)
    
    # Cuando la ventana este mapeada
    ventana_emergente.update_idletasks()
    # Calcular la posicion de la ventana emergente
    posicion_x = window.winfo_x() + (window.winfo_width() // 2) - (ventana_emergente.winfo_width() // 2)
    posicion_y = window.winfo_y() + (window.winfo_height() // 2) - (ventana_emergente.winfo_height() // 2)
    # Posicionar la ventana
    ventana_emergente.geometry(f"+{posicion_x}+{posicion_y}")
    
def Ventana_Info_hdf5():
    ventana_emergente = Toplevel()
    # Titulo de la ventana
    ventana_emergente.title("¿Qué debe haber en la carpeta?")
   
    # mensaje1 = "============= La carpeta debe contener: =============" 
    mensaje1 = "========= La carpeta debe contener una de las siguientes opciones: =========" 
    mensaje2 = "1. Carpeta 'Archivos_hdf5' con archivo .hdf5 agregado por manzana, por                "
    mensaje3 = "taxonomía y por sección; carpeta 'Modelo_Exposicion' con un archivo         "
    mensaje4 = ".csv del modelo de exposición del municipio; carpeta 'Shapes_CP' con los    "
    mensaje5 = "shapes del área, manzana y sección del municipio.                                            "
    
    mensaje6 = "2. Carpeta 'Archivo_csv' con archivo .csv de la pérdida promedio agregado por      "
    mensaje7 = "manzana y taxonomía; carpeta 'Modelo_Exposicion' con un archivo .csv del"
    mensaje8 = "modelo de exposición del municipio; carpeta 'Shapes_CP' con los shapes    "
    mensaje9 = "del área, manzana y sección del municipio.                                                         "
    
    
    
    texto_v = "                                                                                                                           "
    # Colocar mensajes y boton cerrar
    tk.Label(ventana_emergente, text=texto_v, padx=45, pady=100).pack()
    tk.Label(ventana_emergente, text=mensaje1).place(relx=0.5, rely=0.12, anchor=tk.CENTER) 
    tk.Label(ventana_emergente, text=mensaje2).place(relx=0.5, rely=0.25, anchor=tk.CENTER) 
    tk.Label(ventana_emergente, text=mensaje3).place(relx=0.5, rely=0.34, anchor=tk.CENTER) 
    tk.Label(ventana_emergente, text=mensaje4).place(relx=0.5, rely=0.43, anchor=tk.CENTER)
    tk.Label(ventana_emergente, text=mensaje5).place(relx=0.5, rely=0.52, anchor=tk.CENTER)
    
    tk.Label(ventana_emergente, text=mensaje6).place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    tk.Label(ventana_emergente, text=mensaje7).place(relx=0.5, rely=0.74, anchor=tk.CENTER)
    tk.Label(ventana_emergente, text=mensaje8).place(relx=0.5, rely=0.83, anchor=tk.CENTER)
    tk.Label(ventana_emergente, text=mensaje9).place(relx=0.5, rely=0.92, anchor=tk.CENTER)
   
    
    # Cuando la ventana este mapeada
    ventana_emergente.update_idletasks()
    # Calcular la posicion de la ventana emergente
    posicion_x = window.winfo_x() + (window.winfo_width() // 2) - (ventana_emergente.winfo_width() // 2)
    posicion_y = window.winfo_y() + (window.winfo_height() // 2) - (ventana_emergente.winfo_height() // 2)
    # Posicionar la ventana
    ventana_emergente.geometry(f"+{posicion_x}+{posicion_y}")


def Ventana_Info_CLB(event=None):
    Ventana_Info()

def Ventana_Info_DSP(event=None):
    Ventana_Info()
    
def Ventana_Info_PRD(event=None):
    Ventana_Info_hdf5()

def Ventana_Info_DNO(event=None):
    Ventana_Info_hdf5()

def Ventana_Info_MAP(event=None):
    Ventana_Info_hdf5()

def Ventana_Info_GEN(event=None):
    Ventana_Info_hdf5()
    
def Ventana_Info_FCH(event=None):
    Ventana_Info_hdf5()
    
#%% ====== MAIN WINDOW ========================================================
"""
-------------------------------------------------------------------------------
Create the interface
-------------------------------------------------------------------------------
"""
window = tk.Tk()              # Create tkinet window
window.title("METRISK")       # Interface name

"""
-------------------------------------------------------------------------------
                               Modify upper container
                         Application and universities logo
-------------------------------------------------------------------------------
"""

# ============================== Upper container ==============================
up_container = tk.Frame(window, height=130, bg=upcnt_color)
up_container.pack(side=tk.TOP, fill=tk.X)    
# =============================================================================

# 1). ........ Interface logo: ................................................
logo_container = tk.Frame(up_container, bg=upcnt_color, width=500, height=140)    
logo_container.pack(side=tk.LEFT)
logo_Button = wnfun_lib.Button_Image('/metrisk_v2.png', 314, 58, logo_container,upcnt_color,0.5,0.5,Show_Home)
# 2). ........ UMilitar logo: .................................................
US_container = tk.Frame(up_container, bg=upcnt_color, height=140, width=200)
US_container.pack(side=tk.RIGHT)
US_label = wnfun_lib.Label_Image('/Militar.png', 162, 60, US_container,upcnt_color,0.4,0.5)
# 3). ........ UMedellin logo: ................................................
UM_container = tk.Frame(up_container, bg=upcnt_color, height=140, width=200)
UM_container.pack(side=tk.RIGHT)
UM_label = wnfun_lib.Label_Image('/Medellin.png', 142, 40, UM_container,upcnt_color,0.5,0.5)
# 4). ........ USabana logo: ..................................................
US_container = tk.Frame(up_container, bg=upcnt_color, height=140, width=200)
US_container.pack(side=tk.RIGHT)
US_label = wnfun_lib.Label_Image('/Sabana.png', 142, 40, US_container,upcnt_color,0.6,0.5)

"""
-------------------------------------------------------------------------------
                       Modify container of navigation bar
-------------------------------------------------------------------------------
"""

# ========================= Navigation bar container ==========================
left_container = tk.Frame(window, width=250)
left_container.pack(side=tk.LEFT,fill=tk.Y)
# =============================================================================

# 0). ........ Navigation bar: ................................................
navigation_bar = tk.Frame(left_container, bg = navbar_color, width = 270, height=570)
navigation_bar.pack(side=tk.TOP)

# 1). ........ HOME TAB: ......................................................
# Home button >> command action Show_Home (Line 40 to 139)
Home_Var["Tab"] = tk.Button(navigation_bar, text="Inicio             ", font=("Abadi MT", 14), bd=0, 
                            bg=navbar_color, fg="white", relief=tk.FLAT, command=Show_Home, padx=20)
Home_Var["Tab"].place(relx=0.545, rely=0.0389, anchor=tk.CENTER)
# Home icon
Home_Var["Label"] = wnfun_lib.Label_Image('/Home.png', 26, 26, navigation_bar,navbar_color,0.16,0.0359)

"""
-------------------------------------------------------------------------------
               Modify container of navigation bar/contact
-------------------------------------------------------------------------------
"""

# 0). ........ Navigation bar: ................................................
navigation_bar2 = tk.Frame(left_container, bg = '#B97F73', width = 270, height=170)
navigation_bar2.pack(side=tk.BOTTOM)

"""
-------------------------------------------------------------------------------
                            Modify content container
-------------------------------------------------------------------------------
"""
cnt_container = tk.Frame(window, bg=cnt_color, width=1400, height=780)
cnt_container.pack(side=tk.BOTTOM, after=left_container)

US_label2 = wnfun_lib.Label_Image('/upper_container_v2.png', 1880, 70, cnt_container,cnt_color,0.505    ,0.00)


Show_Home()
window.geometry("1500x880")

# .......................... Ejecutar la aplicación ...........................
window.mainloop()