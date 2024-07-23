# -----------------------------------------------------------------------------
# ------------------ EVENT ELEMENTS // SHOW AND HIDE ELEMENTS -----------------
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
def Show_Events_Elements(EVNT_title,EVNT_text,EVNT_label,EVNT_boton,cnt_container,cnt_color,upcnt_color,Show_Calibrate,Show_Dispersion):   
    
    # -------------------------------------------------------------------------
    """........................................................................
                                  HOME Tab Elements
    ........................................................................"""

    # ---- Titulo de la pestaña:
    if EVNT_title["tlt_tlt_EVNT"] is None:
        EVNT_title["tlt_tlt_EVNT"] = wnfun_lib.Label_Image('/Calibration_title.png', 1100, 65, cnt_container,cnt_color,0.495,0.13)
        
    # ---- Informacion de la pestaña:
    if EVNT_text["txt_cnt_EVNT1"] is None:  
        EVNT_text["txt_cnt_EVNT1"] = wnfun_lib.Label_Image('/Calibration_text.png', 500, 400, cnt_container,cnt_color,0.28,0.55)
        
    # ---- Calibracion label --------------------------------------------------
    if EVNT_label["lbl_clb_EVNT"] is None:
        EVNT_label["lbl_clb_EVNT"] = wnfun_lib.Button_Image('/FondoCalibrarV2.png', 410, 140, cnt_container,cnt_color,0.73,0.43,Show_Calibrate)

    # ---- Dispersion label ---------------------------------------------------
    if EVNT_label["lbl_dsp_EVNT"] is None:
        EVNT_label["lbl_dsp_EVNT"] = wnfun_lib.Button_Image('/FondoDispersionV2.png', 410, 140, cnt_container,cnt_color,0.73,0.65,Show_Dispersion)

#%% ====== HIDE EVENTS ELEMENTS ===============================================
def Hide_Events_Elements(title_EVNT,EVNT_title,text_EVNT,EVNT_text,label_EVNT,EVNT_label,boton_EVNT,EVNT_boton):
    # ---- title Variables ----------------------------------------------------
    for tlt in title_EVNT:
        if EVNT_title[tlt] is not None:
            EVNT_title[tlt].place_forget()
            EVNT_title[tlt] = None
    # ---- text Variables -----------------------------------------------------
    for txt in text_EVNT:
        if EVNT_text[txt] is not None:
            EVNT_text[txt].place_forget()
            EVNT_text[txt] = None
    # ---- label Variables ----------------------------------------------------
    for lbl in label_EVNT:
        if EVNT_label[lbl] is not None:
            EVNT_label[lbl].place_forget()
            EVNT_label[lbl] = None
    # ---- button Variables ---------------------------------------------------
    for btn in boton_EVNT:
        if EVNT_boton[btn] is not None:
            EVNT_boton[btn].place_forget()
            EVNT_boton[btn] = None
#%% Desglosar es seleccionado

def Select_Desglo_Events_Elements(Desglo_Var,navigation_bar,navbar_color,Show_Calibrate,Show_Dispersion):
    # Desglosar calibrar y dispersion
    Desglo_Var["CLB"] = tk.Button(navigation_bar, text="Calibrar eventos", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=Show_Calibrate, padx=20)
    Desglo_Var["CLB"].place(relx=0.5, rely=0.22, anchor=tk.CENTER)
    Desglo_Var["DSP"] = tk.Button(navigation_bar, text="Dispersión de eventos", font=("Abadi MT", 14), bd=0, 
                                bg=navbar_color, fg="#F2F2F2", relief=tk.FLAT, command=Show_Dispersion, padx=20)
    Desglo_Var["DSP"].place(relx=0.59, rely=0.29, anchor=tk.CENTER)
    
#%% Quitar es desglose es seleccionado
def Select_UnDesglo_Events_Elements(Desglo_Variables,Desglo_Var):
    # borrar el desglose de variables
    for dsg in Desglo_Variables:
        if Desglo_Var[dsg] is not None:
            Desglo_Var[dsg].place_forget()
            Desglo_Var[dsg] = None
