# -----------------------------------------------------------------------------
# ------------------ PYD ELEMENTS // SHOW AND HIDE ELEMENTS -------------------
# -----------------------------------------------------------------------------
"""
-------------------------------------------------------------------------------
---------------------------- Author: Daniela Novoa ----------------------------
-------------------------------------------------------------------------------
"""
#%% ====== IMPORT LIBRARIES ===================================================
# ........ Tkinter Library ....................................................
import tkinter as tk
# ........ Graphics TKinter Library ...........................................
from PIL import Image, ImageTk
# ........ Directory Library ..................................................
import os
# -------- Own libraries ------------------------------------------------------
import FunctionsLibrary as wnfun_lib

#%% ====== SHOW EVENTS ELEMENTS =================================================
def Show_PyD_Elements(PyD_title,PyD_text,PyD_boton,cnt_container,cnt_color,upcnt_color,nada1,nada2):   
    
    # -------------------------------------------------------------------------
    """........................................................................
                                  HOME Tab Elements
    ........................................................................"""
    # ---- Titulo de la pestaña:
    if PyD_title["tlt_tlt_PyD"] is None:
        PyD_title["tlt_tlt_PyD"] = wnfun_lib.Label_Image('/PerdidaDano_title.png', 1100, 65, cnt_container,cnt_color,0.495,0.13)
        
    # ---- Informacion de la pestaña:
    if PyD_text["txt_cnt_PyD1"] is None:
        PyD_text["txt_cnt_PyD1"] = wnfun_lib.Label_Image('/PerdidaDano_text.png', 500, 350, cnt_container,cnt_color,0.28,0.52)
        
    # ---- Perdidas label -----------------------------------------------------
    if PyD_boton["btn_prd_PyD"] is None:
        PyD_boton["btn_prd_PyD"] = wnfun_lib.Button_Image('/FondoPerdidas.png', 410, 140, cnt_container,cnt_color,0.73,0.43,nada1)
    # ---- Danos label --------------------------------------------------------
    if PyD_boton["btn_dno_PyD"] is None:
        PyD_boton["btn_dno_PyD"] = wnfun_lib.Button_Image('/FondoDanos.png', 410, 140, cnt_container,cnt_color,0.73,0.65,nada2)
        
#%% ====== HIDE EVENTS ELEMENTS ===============================================
def Hide_PyD_Elements(title_PyD,PyD_title,text_PyD,PyD_text,boton_PyD,PyD_boton):
    # ---- title Variables ----------------------------------------------------
    for tlt in title_PyD:
        if PyD_title[tlt] is not None:
            PyD_title[tlt].place_forget()
            PyD_title[tlt] = None
    # ---- text Variables -----------------------------------------------------
    for txt in text_PyD:
        if PyD_text[txt] is not None:
            PyD_text[txt].place_forget()
            PyD_text[txt] = None
    # ---- button Variables ---------------------------------------------------
    for btn in boton_PyD:
        if PyD_boton[btn] is not None:
            PyD_boton[btn].place_forget()
            PyD_boton[btn] = None
#%% Desglosar es seleccionado

def Select_Desglo_PyD_Elements(Desglo_PyD_Var,navigation_bar,navbar_color,nada1,nada2):
    # Desglosar calibrar y dispersion
    Desglo_PyD_Var["PRD"] = tk.Button(navigation_bar, text="Pérdidas", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=nada1, padx=20)
    Desglo_PyD_Var["PRD"].place(relx=0.393, rely=0.323, anchor=tk.CENTER)
    
    Desglo_PyD_Var["DNO"] = tk.Button(navigation_bar, text="Daños", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=nada2, padx=20)
    Desglo_PyD_Var["DNO"].place(relx=0.35, rely=0.393, anchor=tk.CENTER)
    
#%% Quitar es desglose es seleccionado
def Select_UnDesglo_PyD_Elements(Desglo_PyD_Variables,Desglo_PyD_Var):
    # borrar el desglose de variables
    for dsg in Desglo_PyD_Variables:
        if Desglo_PyD_Var[dsg] is not None:
            Desglo_PyD_Var[dsg].place_forget()
            Desglo_PyD_Var[dsg] = None
