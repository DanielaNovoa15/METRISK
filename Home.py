# -----------------------------------------------------------------------------
# ------------------ HOME ELEMENTS // SHOW AND HIDE ELEMENTS ------------------
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

#%% ====== SHOW HOME ELEMENTS =================================================
def Show_Home_Elements(HME_label,HME_text,HME_rectg,cnt_container,cnt_color,User_Guide):   
    
    # -------------------------------------------------------------------------
    """........................................................................
                     The elements of the other tabs are hidden
    ........................................................................"""
    # -------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------
    """........................................................................
                                  HOME Tab Elements
    ........................................................................"""
    # ---- Interface logo:
    if HME_label["lbl_log_HME"] is None:
        HME_label["lbl_log_HME"] = wnfun_lib.Label_Image('/Metrisk_Home.png', 750, 180, cnt_container,cnt_color,0.495,0.29)
    # ---- Content Text:
    if HME_text["txt_cnt_HME1"] is None:
        HME_text["txt_cnt_HME1"] = tk.Label(cnt_container, text="METRISK te  capacita para  medir y  analizar riesgos  a", 
                         font=("Abadi MT", 25), bg="white", fg="#274151")
        HME_text["txt_cnt_HME1"].place(relx=0.496, rely=0.50, anchor=tk.CENTER) 
    if HME_text["txt_cnt_HME2"] is None:
        HME_text["txt_cnt_HME2"] = tk.Label(cnt_container, text="través de métricas exhaustivas, facilitándote la toma de", 
                         font=("Abadi MT", 25), bg="white", fg="#274151")
        HME_text["txt_cnt_HME2"].place(relx=0.498, rely=0.553, anchor=tk.CENTER)
    if HME_text["txt_cnt_HME3"] is None:
        HME_text["txt_cnt_HME3"] = tk.Label(cnt_container, text="decisiones con conocimiento de causa y  la consecución", 
                         font=("Abadi MT", 25), bg="white", fg="#274151")
        HME_text["txt_cnt_HME3"].place(relx=0.5, rely=0.606, anchor=tk.CENTER)
    if HME_text["txt_cnt_HME4"] is None:
        HME_text["txt_cnt_HME4"] = tk.Label(cnt_container, text="de mejores resultados.                                               ", 
                         font=("Abadi MT", 25), bg="white", fg="#274151")
        HME_text["txt_cnt_HME4"].place(relx=0.5, rely=0.659, anchor=tk.CENTER)
    # ---- Guide Text:
    if HME_text["txt_gid_HME1"] is None:
        HME_text["txt_gid_HME1"] = tk.Label(cnt_container, text="¡Descarga nuestra guía de usuario", 
                         font=("Abadi MT", 22), bg="white", fg="#C07960")
        HME_text["txt_gid_HME1"].place(relx=0.355, rely=0.76, anchor=tk.CENTER)
    if HME_text["txt_gid_HME2"] is None:
        HME_text["txt_gid_HME2"] = tk.Label(cnt_container, text="y comienza a usar METRISK!        ", 
                         font=("Abadi MT", 22), bg="white", fg="#C07960")
        HME_text["txt_gid_HME2"].place(relx=0.355, rely=0.807, anchor=tk.CENTER)
        
    if HME_rectg["rec_gid_HME"] is None:
        HME_rectg["rec_gid_HME"] = wnfun_lib.Button_Image('/User_Guide.png', 281, 61, cnt_container,cnt_color,0.695,0.78,User_Guide)


#%% ====== HIDE HOME ELEMENTS =================================================
def Hide_Home_Elements(label_HME,text_HME,rectg_HME,HME_label,HME_text,HME_rectg):
    # ---- Label Variables ----------------------------------------------------
    for lbl in label_HME:
        if HME_label[lbl] is not None:
            HME_label[lbl].place_forget()
            HME_label[lbl] = None
    # ---- Text Variables -----------------------------------------------------
    for txt in text_HME:
        if HME_text[txt] is not None:
            HME_text[txt].place_forget()
            HME_text[txt] = None
    # ---- Rectangle Variables ------------------------------------------------
    for rec in rectg_HME:
        if HME_rectg[rec] is not None: 
            HME_rectg[rec].place_forget()
            HME_rectg[rec] = None
    
