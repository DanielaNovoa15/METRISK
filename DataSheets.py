# -----------------------------------------------------------------------------
# ------------------ MAPS ELEMENTS // SHOW AND HIDE ELEMENTS ------------------
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
import FuntionsLibrary as wnfun_lib
# -------- HDF5 libraries -----------------------------------------------------
import h5py
import json
import geopandas as gpd
import contextily as ctx
# -------- Data processing libraries ------------------------------------------
import pandas as pd
import numpy as np
import math
import re
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.offsetbox as offsetbox
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import ListedColormap
# -------- Librerias para generar las tablas de resumen -----------------------
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side

import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from PIL import Image
import io
#%% ====== SHOW CALIBRATION ELEMENTS ==========================================
def Show_FCH_Elements(FCH_title,FCH_text,FCH_boton,cnt_container,upcnt_color,Select_Folder_MAP,Ventana_Info_MAP,Function_Maps,resultado_label_MAP):
    
    # ---- Titulo de la pestaña:
    if FCH_title["tlt_tlt_FCH"] is None:
        FCH_title["tlt_tlt_FCH"] = wnfun_lib.Label_Image('/Ficha_title.png', 1100, 65, cnt_container,"white",0.495,0.13)

    #---- Descripcion introductoria:
    if FCH_text["txt_cnt_FCH"] is None:
        FCH_text["txt_cnt_FCH"] = wnfun_lib.Label_Image('/Ficha_text.png', 532, 263, cnt_container,"white",0.30  ,0.55)
        
    # ---- Seleccionar carpeta:
    if FCH_boton["btn_slc_FCH"] is None:
        FCH_boton["btn_slc_FCH"] = wnfun_lib.Button_Image('/Select_FolderV2.png', 278, 65, cnt_container,"white",0.78,0.5,Select_Folder_MAP) 
    
    # ---- Informacion:
    if FCH_boton["btn_inf_FCH"] is None:
        FCH_boton["btn_inf_FCH"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.885,0.468,Ventana_Info_MAP)
        
    # ---- Generar:
    if FCH_boton["btn_clb_FCH"] is None:
        FCH_boton["btn_clb_FCH"] = wnfun_lib.Button_Image_lambda('/Generate_Results.png', 252, 55, cnt_container,"white",0.78,0.58,Function_Maps,resultado_label_MAP) 
    
    resultado_label_MAP = tk.Label(cnt_container, text="", fg="red")
    resultado_label_MAP.pack()
    resultado_label_MAP.pack_forget()

#%% ====== HIDE CALIBRATION ELEMENTS ==========================================
def Hide_FCH_Elements(title_MAP,MAP_title,text_MAP,MAP_text,boton_MAP,MAP_boton):
    for tlt in title_MAP:
        if MAP_title[tlt] is not None:
            MAP_title[tlt].place_forget()
            MAP_title[tlt] = None
    
    for txt in text_MAP:
        if MAP_text[txt] is not None:
            MAP_text[txt].place_forget()
            MAP_text[txt] = None
            
    for btn in boton_MAP:
        if MAP_boton[btn] is not None:
            MAP_boton[btn].place_forget()
            MAP_boton[btn] = None
        
#%% ====== FUNCION PERDIDAS ===================================================
def Function_FCH_Elements(carpeta_seleccionada_DNO):
    
    '''========================================================================
    
    En la carpeta puede haber los siguientes dos casos:
        Caso 1:
            - Carpeta "Archivos_hdf5": hdf5 agregado por taxonomía y manzana.
            - Carpeta "Modelo_Exposicion": Modelo exposicion .csv
            - Carpeta "Shapes_CP": Shapes área, manzana y sección del municipio.
        Caso 2:
            - Carpeta "Archivo_csv": csv pérdidas promedio taxonomía y manzana.
            - Carpeta "Modelo_Exposicion": Modelo exposicion .csv
            - Carpeta "Shapes_CP": Shapes área, manzana y sección del municipio.
    
    ========================================================================'''
    
    rootdir1 = carpeta_seleccionada_DNO                                         # Obtiene el directorio de la carpeta seleccionada  
    # Hacer la verificacion y enviar mensajes si es necesario
    Ver_Folder_hdf5,Ver_Folder_csv,Ver_Folder_ME,Ver_Folder_SP = carpetas_en_folder(rootdir1)

    # Salir del proceso si no estan las carpetas
    if Ver_Folder_hdf5 is None and Ver_Folder_csv is None:
        warning = "Intentelo de nuevo" 
        tk.messagebox.showinfo("ERROR", warning)
    elif Ver_Folder_ME is None:
        warning = "Intentelo de nuevo" 
        tk.messagebox.showinfo("ERROR", warning)
    elif Ver_Folder_SP is None:
        warning = "Intentelo de nuevo" 
        tk.messagebox.showinfo("ERROR", warning)
    
    # Verificar si la carpeta tiene la carpeta de hdf5s o de cvss
    for folder in os.listdir(rootdir1):                                     
        if "Archivos_hdf5" in folder:                                      
            Ver_Folder_hdf5 = 1
            Ver_Folder_csv = None
        if "Archivos_csv" in folder:                                      
            Ver_Folder_csv = 1
            Ver_Folder_hdf5 = None
    
    # =========================================================================
    # DESARROLLAR CASO 1
    # =========================================================================
    
    if Ver_Folder_hdf5 is not None and Ver_Folder_ME is not None and Ver_Folder_SP is not None:
    # Cuando en la carpeta estan los resultados de riesgo en hdf5 por seccion,
    # manzana y taxonomia, junto con las carpetas del modelo y los shapes.
        '''====================================================================
        
                      Verificar el contenido de las carpetas
        
        ===================================================================='''
        
        # Verificar primero qué hay en las carpetas y devolver si hay error
        
        # 1). Buscar en la carpeta la dirección de la carpeta 'Archivos_hdf5', 'Modelo_Exposicion', 'Shapes_CP'
        for folder in os.listdir(rootdir1):                                     # Ciclo for para la lista de directorios dentro del directorio actual
            if "Archivos_hdf5" in folder:                                       # Si existe una carpeta llamada "Archivos_hdf5"
                Folder_hdf5 = os.path.join(rootdir1, folder)                    # Obtiene la ruta de la carpeta llamada "Archivos_hdf5" 
            if "Modelo_Exposicion" in folder:                                   # Si existe una carpeta llamada "Modelo_Exposicion"
                Folder_ME = os.path.join(rootdir1, folder)                      # Obtiene la ruta de la carpeta llamada "Modelo_Exposicion" 
            if "Shapes_CP" in folder:                                           # Si existe una carpeta llamada "Shapes_CP"
                Folder_SP = os.path.join(rootdir1, folder)                      # Obtiene la ruta de la carpeta llamada "Shapes_CP" 
        
        # 2). Verificar lo que hay en la carpeta 'Archivos_hdf5'
        rutas_hdf5 = []
        for archivo in os.listdir(Folder_hdf5):                                 # Lista de archivos en la carpeta hdf5
            if archivo.endswith(".hdf5"):                                       # Obtener solo los archivos que terminan en .hdf5
                rutas_hdf5.append(os.path.join(Folder_hdf5,archivo))            # Ruta de los archivos (debe haber 2)
        
        # Verificar si hay 2 archivos y tienen el formato adecuado
        if rutas_hdf5 == []:
            warning = "No se encontraron los archivos .hdf5."
            tk.messagebox.showinfo("ERROR", warning)
        elif len(rutas_hdf5) < 3:
            warning = "En la carpeta no estan todos los archivos .hdf5 que se requieren"
            tk.messagebox.showinfo("ERROR", warning)
        elif len(rutas_hdf5) > 3:
            warning = "Hay más de tres archivos .hdf5 en la carpeta."
            tk.messagebox.showinfo("ERROR", warning)
        else:
                
            for ruta in rutas_hdf5:
                with h5py.File(ruta, 'r') as archivo: 
                    oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))  # Lista de parametros OpenQuake
                
                # Si el archivo es de perdidas - probabilistico
                if oqparam_dict['calculation_mode'] == 'event_based_risk':
                    # ¿Cuál es el agregado del archivo?
                    if oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                        CalcMode_PRD_mnz = "Probabilistico"
                        PRD_pbl_mnz = ruta
                # Si el archivo es de daños - probabilistico
                elif oqparam_dict['calculation_mode'] == 'event_based_damage':
                    # ¿Cuál es el agregado del archivo?
                    if oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                        CalcMode_DNO_mnz = "Probabilistico"
                        DNO_pbl_mnz = ruta
                    elif oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                        CalcMode_DNO_txn = "Probabilistico"
                        DNO_pbl_txn = ruta
                
                # Si el arcjhivo es de perdidas - deterministicos
                elif oqparam_dict['calculation_mode'] == 'scenario_risk': 
                    # ¿Cuál es el agregado del archivo?
                    if oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                        CalcMode_PRD_mnz = "Deterministico"
                        PRD_det_mnz = ruta
                # Si el arcjhivo es de daños - deterministicos
                elif oqparam_dict['calculation_mode'] == 'scenario_damage':  
                    # ¿Cuál es el agregado del archivo?
                    if oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                        CalcMode_DNO_mnz = "Deterministico"
                        DNO_det_mnz = ruta
                    elif oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                        CalcMode_DNO_txn = "Deterministico"
                        DNO_det_txn = ruta
                    
                else:
                    warning = "El/los archivo no cumple con los criterios."
                    tk.messagebox.showinfo("ERROR", warning)
            

        if CalcMode_PRD_mnz == "Probabilistico" and CalcMode_DNO_mnz == "Probabilistico" and CalcMode_DNO_txn == "Probabilistico":
            calculation_mode = "Probabilistico"
        elif CalcMode_PRD_mnz == "Deterministico" and CalcMode_DNO_mnz == "Deterministico" and CalcMode_DNO_txn == "Deterministico":
            calculation_mode = "Deterministico"
        else:
            warning = "Has elegido un archivo .hdf5, o varios, con diferentes modos de cálculo"
            tk.messagebox.showinfo("ERROR", warning)
            
        # =====================================================================
        # =====================================================================
        # =====================================================================
        #              CASO PROBABILISTICO -- PERDIDAS Y DAÑOS
        # =====================================================================
        # =====================================================================
        # =====================================================================        
        
        # 3). Verificar lo que hay en la carpeta 'Modelo_Exposicion'
        Modelo_Expo = None
        for archivo in os.listdir(Folder_ME):                                   # Lista de archivos en la carpeta modelo
            if archivo.endswith(".csv") and "ModeloExposicion" in archivo:      # Obtener solo los archivos terminan en .csv
                Modelo_Expo = pd.read_csv(os.path.join(Folder_ME,archivo))      # Ruta del archivo
            
        # Verificar si se encontró el modelo
        if Modelo_Expo is None:
            warning = "No se encontró un archivo de modelo de exposición que cumpla con los criterios."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            Modelo_Expo2 = Modelo_Expo
        
        # arreglar Modelo:

        # Codigo de las manzanas corregido

        cod_mnzdef_model = []
        for mnz in Modelo_Expo2.cod_mnz:
            if mnz[0].isalpha():
                mnz2 = str(mnz)
                cod_mnzdef_model.append(mnz2[1::])   
        Modelo_Expo2.cod_mnz = cod_mnzdef_model

        cod_sccdef_model = []
        for scc in Modelo_Expo2.cod_secc:
            if scc[0].isalpha():
                cod_sccdef_model.append(scc[1::])
        Modelo_Expo2.cod_secc = cod_sccdef_model

        # Codigo y nombre del municipio
        # Modificar modelo de exposicion para añadir secciones
        cod_secc_Modelo = []
        for val in Modelo_Expo2.cod_mnz:
            cod_secc_Modelo.append(val[:-2])
        Modelo_Expo2['cod_secc'] = cod_secc_Modelo
        
        
        # 4). Verificar lo que hay en la carpeta 'Modelo_Exposicion'
        manzana_shp_rt = None
        for archivo in os.listdir(Folder_SP):                                   # Lista de archivos en la carpeta shapes
            if archivo.endswith(".shp") and "MGN_MANZANA" in archivo:           # Obtener solo los archivos que terminan en .shp
                manzana_shp_rt = gpd.read_file(os.path.join(Folder_SP,archivo)) # Ruta del archivo

        # Verificar si se encontró el archivo
        if manzana_shp_rt is None:
            warning = "No se encontró un archivo shape manzanas que cumpla con los criterios."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            manzana_shp = manzana_shp_rt
            
        area_shp_rt = None
        for archivo in os.listdir(Folder_SP):                                   # Lista de archivos en la carpeta shapes
            if archivo.endswith(".shp") and "MGN_AREA" in archivo:              # Obtener solo los archivos que terminan en .shp
                area_shp_rt = gpd.read_file(os.path.join(Folder_SP,archivo))    # Ruta del archivo

        # Verificar si se encontró el archivo
        if area_shp_rt is None:
            warning = "No se encontró un archivo shape área que cumpla con los criterios."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            area_shp = area_shp_rt
        
        
        '''----------------------------------------------------------------
        -------------------------------------------------------------------
                  PROCESAR Y GENERAR LOS DATOS PARA LA FICHA
        -------------------------------------------------------------------
        ----------------------------------------------------------------'''
        
        with h5py.File(PRD_pbl_mnz, 'r') as archivo: 
            oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
            agg_id = archivo["aggrisk"]["agg_id"][()]                                   # ID del agregado
            loss = archivo["aggrisk"]["loss"][()]                                       # perdidas segun el aggregate ID
            valex = archivo["assetcol"]["array"]["value-structural"][()]                # Valor estructural

        # Dataframe perdidas por aggregate ID
        df_group = pd.DataFrame({'agg_id':agg_id, 'loss':loss})                         # Dataframe perdidas por aggid
        data_mun = df_group[df_group['agg_id'] == oqparam_dict['K']]
        PAE_COP_Mun = data_mun.loss.mean()                                              # PAE del municipio en millones de pesos COP
        Valexpuesto = valex.sum()                                                       # Valor expuesto del municipio
        PAE_PRC_Mun = (PAE_COP_Mun/Valexpuesto)*1000                                    # PAE en porcentaje por mil
        Poblacion = Modelo_Expo.poblacion.sum()
        No_edis_total = Modelo_Expo.no_edificaciones.sum()
        
        # obtener todos los resultados de daños
        with h5py.File(DNO_pbl_mnz, 'r') as archivo: 
            oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
            mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]           # Lista de manzanas
            mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
            agg_id = archivo["aggrisk"]["agg_id"][()] 
            dmg0 = archivo["aggrisk"]["dmg_0"][()] 
            dmg1 = archivo["aggrisk"]["dmg_1"][()] 
            dmg2 = archivo["aggrisk"]["dmg_2"][()]
            dmg3 = archivo["aggrisk"]["dmg_3"][()]
            dmg4 = archivo["aggrisk"]["dmg_4"][()] 
            collapsed = archivo["aggrisk"]["collapsed"][()] 
            fatalities = archivo["aggrisk"]["fatalities"][()] 
            injured = archivo["aggrisk"]["injured"][()] 

        # Dataframe sin daño por aggregate ID
        df_dmg0 = pd.DataFrame({'agg_id':agg_id, 'dmg0':dmg0})
        data_mun_dmg0 = df_dmg0[df_dmg0['agg_id'] == oqparam_dict['K']]
        dmg0_no_edis = np.around(data_mun_dmg0.dmg0.mean(),0)
        dmg0_hab = np.around((Poblacion/No_edis_total)*dmg0_no_edis,0)
        dmg0_hab_PRC = (dmg0_hab/Poblacion)*100
            
        # Dataframe daño leve por aggregate ID
        df_dmg1 = pd.DataFrame({'agg_id':agg_id, 'dmg1':dmg1})
        data_mun_dmg1 = df_dmg1[df_dmg1['agg_id'] == oqparam_dict['K']]
        dmg1_no_edis = np.around(data_mun_dmg1.dmg1.mean(),0)
        dmg1_hab = np.around((Poblacion/No_edis_total)*dmg1_no_edis,0)
        dmg1_hab_PRC = (dmg1_hab/Poblacion)*100

        # Dataframe daño moderado por aggregate ID
        df_dmg2 = pd.DataFrame({'agg_id':agg_id, 'dmg2':dmg2})
        data_mun_dmg2 = df_dmg2[df_dmg2['agg_id'] == oqparam_dict['K']]
        dmg2_no_edis = np.around(data_mun_dmg2.dmg2.mean(),0)
        dmg2_hab = np.around((Poblacion/No_edis_total)*dmg2_no_edis,0)
        dmg2_hab_PRC = (dmg2_hab/Poblacion)*100

        # Dataframe daño extensivo por aggregate ID
        df_dmg3 = pd.DataFrame({'agg_id':agg_id, 'dmg3':dmg3})
        data_mun_dmg3 = df_dmg3[df_dmg3['agg_id'] == oqparam_dict['K']]
        dmg3_no_edis = np.around(data_mun_dmg3.dmg3.mean(),0)
        dmg3_hab = np.around((Poblacion/No_edis_total)*dmg3_no_edis,0)
        dmg3_hab_PRC = (dmg3_hab/Poblacion)*100

        # Dataframe colapso por aggregate ID
        df_dmg4 = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4})
        data_mun_dmg4 = df_dmg4[df_dmg4['agg_id'] == oqparam_dict['K']]
        dmg4_no_edis = np.around(data_mun_dmg4.dmg4.mean(),0)
        dmg4_hab = np.around((Poblacion/No_edis_total)*dmg4_no_edis,0)
        dmg4_hab_PRC = (dmg4_hab/Poblacion)*100

        # Dataframe fallecidos por aggregate ID
        df_fatalities = pd.DataFrame({'agg_id':agg_id, 'fatal':fatalities})
        data_mun_fatal = df_fatalities[df_fatalities['agg_id'] == oqparam_dict['K']]
        fatalities_val = np.around(data_mun_fatal.fatal.mean(),0)
        if fatalities_val == 0.0:
            fatalities_PRC = 0.0
        else:
            fatalities_PRC = (fatalities_val/Poblacion)*100

        # Dataframe heridos por aggregate ID
        df_injured = pd.DataFrame({'agg_id':agg_id, 'injured':injured})
        data_mun_injured = df_injured[df_injured['agg_id'] == oqparam_dict['K']]
        injured_val = np.around(data_mun_injured.injured.mean(),0)
        if injured_val == 0.0:
            injured_PRC = 0.0
        else:
            injured_PRC = (injured_val/Poblacion)*100

        # Dataframe de colapsos por manzana censal
        df_collapsed = pd.DataFrame({'agg_id':agg_id, 'collapsed':collapsed})
        df_group_collapsed = df_collapsed.groupby('agg_id')['collapsed'].mean()  
        df_group_collapsed = df_group_collapsed[:-1]

        df_collapsed = pd.DataFrame({'collapsed':df_group_collapsed})

        cod_mnzdef = []
        for mnz in mnz_list:
            cod_mnzdef.append(str(mnz[1:]))

        df_collapsed['cod_mnz'] = cod_mnzdef

        mapdata_collapsed = manzana_shp.merge(df_collapsed, left_on='COD_DANE', right_on='cod_mnz', how='left')

        # Filtrar gdf1 para eliminar filas con NaN en 'collapsed'
        mapdata_collapsed = mapdata_collapsed.dropna(subset=['collapsed'])

        # Extraer los valores de 'cod_mnz' de gdf1 filtrado
        cod_mnz_values = mapdata_collapsed['cod_mnz'].dropna().tolist()

        # Filtrar gdf2 para que contenga solo las filas con 'cod_mnz' en cod_mnz_values
        manzana_shp = manzana_shp[manzana_shp['COD_DANE'].isin(cod_mnz_values)]

        # Obtener todos los datos de daños por taxonomia
        with h5py.File(DNO_pbl_txn, 'r') as archivo: 
            oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8')) # Lista de parametros de OpenQuake
            txn_list_bytes  = archivo["assetcol"]["tagcol"]["taxonomy"][()][1:] # Lista de taxonomias
            txn_list = [item.decode('utf-8') for item in txn_list_bytes]
            agg_id = archivo["aggrisk"]["agg_id"][()]  # ID del agregado
            dmg_3 = archivo["aggrisk"]["dmg_3"][()]
            dmg_4 = archivo["aggrisk"]["dmg_4"][()]

        # Dataframe pr daño extensivo
        df_dmg3txn = pd.DataFrame({'agg_id':agg_id, 'dmg3':dmg_3})
        df_group_dmg3txn = df_dmg3txn.groupby('agg_id')['dmg3'].mean().tolist()
        df_group_dmg3txn = df_group_dmg3txn[:-1]
        No_edis_txn = Modelo_Expo.groupby('tipologia')['no_edificaciones'].sum().tolist()

        nueva_tipologias = [tip.split('/H')[0] for tip in txn_list]
        df_dmg3txn = pd.DataFrame({'taxonomy':nueva_tipologias,'dmg3':df_group_dmg3txn,'no_edis':No_edis_txn})

        df_grp_dmg3txn = df_dmg3txn.groupby('taxonomy')[['dmg3','no_edis']].mean()

        df_dmg3txn = pd.DataFrame({'taxonomy':df_grp_dmg3txn.index,'dmg3':df_grp_dmg3txn.dmg3,'no_edis':df_grp_dmg3txn.no_edis})
        df_dmg3txn = df_dmg3txn.reset_index(drop=True)

        for index,txn in enumerate(df_dmg3txn.taxonomy):
            if txn == "NI/NI/NI":
                df_dmg3txn.drop(df_dmg3txn.index[index], inplace=True) 
                df_dmg3txn = df_dmg3txn.reset_index(drop=True)
            
        df_dmg3txn['dmg3_prc'] = (df_dmg3txn.dmg3/df_dmg3txn.no_edis)*100
        df_dmg3txn['description'] = wnfun_lib.Taxo_Description(df_dmg3txn)
        # Encuentra el índice del valor máximo en la columna 'dmg3_prc'
        max_idx = df_dmg3txn['dmg3_prc'].idxmax()
        # Selecciona la fila correspondiente al valor máximo
        maxrow_dmg3txn = df_dmg3txn.loc[max_idx]

        # Dataframe para colapso
        df_dmg4txn = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg_4})
        df_group_dmg4txn = df_dmg4txn.groupby('agg_id')['dmg4'].mean().tolist()
        df_group_dmg4txn = df_group_dmg4txn[:-1]

        df_dmg4txn = pd.DataFrame({'taxonomy':nueva_tipologias,'dmg4':df_group_dmg4txn,'no_edis':No_edis_txn})

        df_grp_dmg4txn = df_dmg4txn.groupby('taxonomy')[['dmg4','no_edis']].mean()

        df_dmg4txn = pd.DataFrame({'taxonomy':df_grp_dmg4txn.index,'dmg4':df_grp_dmg4txn.dmg4,'no_edis':df_grp_dmg4txn.no_edis})
        df_dmg4txn = df_dmg4txn.reset_index(drop=True)

        for index,txn in enumerate(df_dmg4txn.taxonomy):
            if txn == "NI/NI/NI":
                df_dmg4txn.drop(df_dmg4txn.index[index], inplace=True) 
                df_dmg4txn = df_dmg4txn.reset_index(drop=True)      

        df_dmg4txn['dmg4_prc'] = (df_dmg4txn.dmg4/df_dmg4txn.no_edis)*100
        df_dmg4txn['description'] = wnfun_lib.Taxo_Description(df_dmg4txn)
        # Encuentra el índice del valor máximo en la columna 'dmg3_prc'
        max_idx = df_dmg4txn['dmg4_prc'].idxmax()
        # Selecciona la fila correspondiente al valor máximo
        maxrow_dmg4txn = df_dmg4txn.loc[max_idx]

        # ------- Nombre del municipio ------------------------------------
        CP_Name = oqparam_dict['description'].split('_')[3].strip()          # Nombre del centro poblado inicial
        if CP_Name[0].islower():
            CP_Name = CP_Name[0].upper() + CP_Name[1:].upper()               # Si el nombre del centro poblado no comienza con una mayuscula

        # ------- Codigo del municipio ------------------------------------
        COD_mun = cod_mnzdef[0][0:5]
       
        
        '''----------------------------------------------------------------
        -------------------------------------------------------------------
                           GENERAR DIAGRAMAS Y MAPAS
        -------------------------------------------------------------------
        ----------------------------------------------------------------'''
        
        categorias = ['Sin Daño','Leve','Moderado','Extensivo','Colapso']
        Colapsos_no_edis = [dmg0_hab_PRC,dmg1_hab_PRC,dmg2_hab_PRC,dmg3_hab_PRC,dmg4_hab_PRC]

        # Definir el colormap
        colors = plt.cm.get_cmap('bone').reversed()(np.linspace(0.1, 0.7, len(categorias)))

        # Crear el diagrama circular
        fig = plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(Colapsos_no_edis, colors=colors, autopct='%1.1f%%', startangle=140)

        # Añadir la leyenda
        # plt.legend(wedges, categorias, loc="center left", bbox_to_anchor=(0.92, 0.5),fontsize=14, frameon=False, handlelength=1, handletextpad=0.4)
        plt.setp(autotexts, size=13, weight="bold")

        # Eliminar el título del gráfico
        plt.title('')

        # Ajustar márgenes para reducir el espacio en blanco
        plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)

        # Guardar la imagen con bordes ajustados
        # Se guarda la imagen en la carpeta de la misma app
        plt.savefig(os.path.join(os.path.join(os.getcwd(),"css"), "Diagrama_Circular.jpg"), dpi=300, bbox_inches='tight', pad_inches=0)
        plt.show()
        
        # -----------------------------------------------------------------
        # Obtener el colormap 'bone' con 256 colores
        bone = plt.cm.get_cmap('Blues', 180)

        # El primer color de 'bone' invertido es el último color de 'bone'
        # Para obtener el último color, puedes usar el valor 1.0
        primer_color_bone_inverted = bone(0.2)

        # Crear un colormap personalizado que consiste solo en ese color
        colormap_personalizado = ListedColormap([primer_color_bone_inverted])

        wnfun_lib.mapa_gen_Infograph(0,area_shp,manzana_shp,mapdata_collapsed,'collapsed','Blues','Map_Collapsed.jpg',0.5,2,6.5,'Edificios colapsados')
        
        wnfun_lib.Diagrama_no_edis(df_dmg3txn.taxonomy,df_dmg3txn.dmg3_prc,"Barras_Extensivo.jpg")
        wnfun_lib.Diagrama_no_edis(df_dmg4txn.taxonomy,df_dmg4txn.dmg4_prc,"Barras_Colapso.jpg")
        
        '''----------------------------------------------------------------
                                    GENERAR PDF
        ----------------------------------------------------------------'''
        # Rutas de los archivos
        if calculation_mode == 'Probabilistico':
            pdf_base_path = os.path.join(os.path.join(os.getcwd(),"css"), "FichaTecnica_Probabilista.pdf")
        else:
            pdf_base_path = os.path.join(os.path.join(os.getcwd(),"css"), "FichaTecnica_Determinista.pdf")
        output_pdf_path = os.path.join(os.path.join(os.getcwd(),"css"), "Output_Ficha_tecnica.pdf")
        image_path_circular = os.path.join(os.path.join(os.getcwd(),"css"), "Diagrama_Circular.jpg")
        image_path_mapa = os.path.join(os.path.join(os.getcwd(),"css"), "Map_Collapsed.jpg")
        image_path_severo = os.path.join(os.path.join(os.getcwd(),"css"), "Barras_Extensivo.jpg")
        image_path_colapso = os.path.join(os.path.join(os.getcwd(),"css"), "Barras_Colapso.jpg")

        # Crear un nuevo PDF con el contenido adicional
        # packet = io.BytesIO()
        # c = canvas.Canvas(packet, pagesize=letter)
        # width, height = letter

        #Conversión de centímetros a puntos
        def cm_to_points(cm):
            return cm * 72 / 2.54
        # Dimensiones personalizadas en puntos
        custom_width = cm_to_points(33.867)  # Ancho en puntos
        custom_height = cm_to_points(19.05)  # Alto en puntos
        # Crear un nuevo tamaño de página personalizado
        custom_page_size = (custom_width, custom_height)
        # Crear un buffer para el PDF
        packet = io.BytesIO()
        # Crear un lienzo con el tamaño de página personalizado
        c = canvas.Canvas(packet, pagesize=custom_page_size)
        # Ahora puedes usar `width` y `height` como el ancho y alto de la página personalizada
        width, height = custom_page_size

        # Registrar la fuente Abadi MT
        # pdfmetrics.registerFont(TTFont('AbadiMT', '/path/to/AbadiMT.ttf'))

        # Registrar la fuente Aptos Display
        pdfmetrics.registerFont(TTFont('AbadiMT', os.path.join(os.path.join(os.getcwd(),"css"), "abadi-mt.ttf")))
        pdfmetrics.registerFont(TTFont('AbadiMT_Bold', os.path.join(os.path.join(os.getcwd(),"css"), "abadi-mt-std-bold.ttf")))
        pdfmetrics.registerFont(TTFont('Aptos', os.path.join(os.path.join(os.getcwd(),"css"), "aptos.ttf")))
        pdfmetrics.registerFont(TTFont('Aptos_Bold', os.path.join(os.path.join(os.getcwd(),"css"), "aptos-bold.ttf")))

        # Agregar textos
        if calculation_mode == 'Probabilistico':
            c.setFont("AbadiMT_Bold", 10.5)
            c.setFillColorRGB(217/255, 217/255, 217/255) #------------------------------ Color blanco
            c.drawString(841, 480, 'PROBABILÍSTICO') #---------------------------------- Nombre del modo de calculo
        else:
            c.setFont("AbadiMT_Bold", 10.5)
            c.setFillColorRGB(217/255, 217/255, 217/255) #------------------------------ Color blanco
            c.drawString(841, 480, 'DETERMINÍSTICO') #---------------------------------- Nombre del modo de calculo
        
        c.setFont("AbadiMT_Bold", 36)
        c.setFillColorRGB(242/255, 242/255, 242/255) #---------------------------------- Color blanco
        c.drawString(50, 499, CP_Name) #------------------------------------------------ Nombre del municipio

        c.setFont("AbadiMT_Bold", 11)
        c.setFillColorRGB(191/255, 191/255, 191/255) #---------------------------------- Color #BFBFBF
        c.drawString(82, 472, 'COD DANE:'+COD_mun) #------------------------------------ Código del municipio

        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(165, 337, f"$ {np.around(Valexpuesto,2):,.2f}") #------------------ Valor expuesto

        c.setFont("Aptos_Bold", 11)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(60, 275, f"$ {int(PAE_COP_Mun):,}") #------------------------------ PAE en cop millones
        
        if calculation_mode == 'Probabilistico':
            c.setFont("Aptos_Bold", 11)
            c.setFillColorRGB(51/255, 86/255, 107/255) #-------------------------------- Color #33566B
            c.drawString(188, 275, f"{np.around(PAE_PRC_Mun,2):.3}"+'‰') #-------------- PAE en porcentaje por mil
        else:
            c.setFont("Aptos_Bold", 11)
            c.setFillColorRGB(51/255, 86/255, 107/255) #-------------------------------- Color #33566B
            c.drawString(188, 275, f"{np.around(PAE_PRC_Mun,2):.3}"+'%') #-------------- PAE en porcentaje por mil
        
        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(164, 242, f"{int(Poblacion):,}") #--------------------------------- PAE en cop millones

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(105, 200.5, f"{int(dmg3_hab):,}") #-------------------------------- Hab en daño severo

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(135, 200.5, f"{np.around(dmg3_hab_PRC,1):.2}") #------------------- Hab prc en daño severo

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(97, 188, f"{int(dmg4_hab):,}") #----------------------------------- Hab en colapso

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(126, 188, f"{np.around(dmg4_hab_PRC,1):.2}") #--------------------- Hab prc en colapso

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(104, 164, f"{int(injured_val):,}") #---------------------------- fallecidos

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(158, 164, f"{np.around(injured_PRC,1):.2}") #------------------- fallecidos prc

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(285, 164, f"{int(fatalities_val):,}") #------------------------------- heridos

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(90, 152, f"{np.around(fatalities_PRC,1):.2}") #----------------------- heridos prc

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_circular)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 120
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_circular, 140, 32 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_mapa)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 220
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_mapa, 370, 42 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_colapso)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 170
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_colapso, 700, 260 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_severo)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 170
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_severo, 700, 45 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(691, 243,f"{int(np.around(maxrow_dmg4txn.dmg4_prc,0))}") #--------- Porcentaje de edificaciones en tipologia predominante

        c.setFont("Aptos", 8)
        c.setFillColorRGB(89/255, 89/255, 89/255) #------------------------------------- Color #595959
        c.drawString(733, 243, maxrow_dmg4txn.description + ' colapsan') #-------------- Descripcion de la tipologia predominante

        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(691, 25,f"{int(np.around(maxrow_dmg3txn.dmg3_prc,0))}") #---------- Porcentaje de edificaciones en tipologia predominante

        c.setFont("Aptos", 8)
        c.setFillColorRGB(89/255, 89/255, 89/255) #------------------------------------- Color #595959
        c.drawString(733, 25, maxrow_dmg3txn.description + ' tienen daño severo') #-------------- Descripcion de la tipologia predominante


        # Guardar el nuevo contenido en memoria
        c.save()
        packet.seek(0)

        # Leer el PDF base y el nuevo PDF
        pdf_base = PyPDF2.PdfReader(open(pdf_base_path, "rb"))
        new_pdf = PyPDF2.PdfReader(packet)

        # Crear un objeto de escritura para el PDF de salida
        pdf_writer = PyPDF2.PdfWriter()

        # Obtener la primera página del PDF base
        page = pdf_base.pages[0]

        # Obtener el contenido del nuevo PDF (solo una página)
        new_page = new_pdf.pages[0]

        # Superponer el nuevo contenido en la primera página del PDF base
        page.merge_page(new_page)

        # Agregar la página modificada al escritor de PDF
        pdf_writer.add_page(page)

        # Agregar las demás páginas del PDF base
        for page_num in range(1, len(pdf_base.pages)):
            page = pdf_base.pages[page_num]
            pdf_writer.add_page(page)

        # Guardar el PDF combinado
        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

    # =========================================================================
    # DESARROLLAR CASO 2
    # =========================================================================
    
    if Ver_Folder_csv is not None and Ver_Folder_ME is not None and Ver_Folder_SP is not None:
        
        '''====================================================================
        
                      Verificar el contenido de las carpetas
        
        ===================================================================='''
        
        # Verificar primero qué hay en las carpetas y devolver si hay error
        
        # 1). Buscar en la carpeta la dirección de la carpeta 'Archivos_csv', 'Modelo_Exposicion', 'Shapes_CP'
        for folder in os.listdir(rootdir1):                                     # Ciclo for para la lista de directorios dentro del directorio actual
            if "Archivos_csv" in folder:                                        # Si existe una carpeta llamada "Archivos_hdf5"
                Folder_csv = os.path.join(rootdir1, folder)                     # Obtiene la ruta de la carpeta llamada "Archivos_hdf5" 
            if "Modelo_Exposicion" in folder:                                   # Si existe una carpeta llamada "Modelo_Exposicion"
                Folder_ME = os.path.join(rootdir1, folder)                      # Obtiene la ruta de la carpeta llamada "Modelo_Exposicion" 
            if "Shapes_CP" in folder:                                           # Si existe una carpeta llamada "Shapes_CP"
                Folder_SP = os.path.join(rootdir1, folder)                      # Obtiene la ruta de la carpeta llamada "Shapes_CP" 
        
        # 2). Verificar lo que hay en la carpeta 'Archivos_csv'
        rutas_csv = []
        for archivo in os.listdir(Folder_csv):                                  # Lista de archivos en la carpeta hdf5
            if archivo.endswith(".csv") and "avg_losses-mean" in archivo:       # Obtener solo los archivos que terminan en .hdf5
                rutas_csv.append(os.path.join(Folder_csv,archivo))              # Ruta de los archivos (debe haber 2)
            if archivo.endswith(".csv") and "avg_damages-mean" in archivo:      # Obtener solo los archivos que terminan en .hdf5
                rutas_csv.append(os.path.join(Folder_csv,archivo))              # Ruta de los archivos (debe haber 2)
        
        # Verificar si la carpeta tiene 2:
        if rutas_csv == []:
            warning = "No se encontraron los archivos .csv."
            tk.messagebox.showinfo("ERROR", warning)
        elif len(rutas_csv) < 2:
            warning = "En la carpeta no estan todos los archivos .csv que se requieren"
            tk.messagebox.showinfo("ERROR", warning)
        elif len(rutas_csv) > 2:
            warning = "Hay más de dos archivos .csv en la carpeta."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            # Mirar que hay en la carpeta
            CalcMode_PRD, CalcMode_DET  = [], []
            for ruta in rutas_csv:
                if "PLB" in archivo:                                            # Saber si los resultados son probabilisticos
                    CalcMode_PRD.append("Probabilistico")
                elif "DET" in archivo:                                          # Saber si los resultados son deterministicos
                    CalcMode_DET.append("Deterministico")
                else:
                    warning = "Los archivos .csv no cumplen con los criterios requiridos."
                    tk.messagebox.showinfo("ERROR", warning)
                
            if len(CalcMode_PRD) == 2:
                calculation_mode = "Probabilistico"
            elif len(CalcMode_DET) == 2:
                calculation_mode = "Deterministico"
            else:
                warning = "Has elegido un archivo .csv, o varios, con diferentes modos de cálculo"
                tk.messagebox.showinfo("ERROR", warning)
                
        # =====================================================================
        # =====================================================================    
        
        # 3). Verificar lo que hay en la carpeta 'Modelo_Exposicion'
        Modelo_Expo = None
        for archivo in os.listdir(Folder_ME):                                   # Lista de archivos en la carpeta modelo
            if archivo.endswith(".csv") and "ModeloExposicion" in archivo:      # Obtener solo los archivos terminan en .csv
                Modelo_Expo = pd.read_csv(os.path.join(Folder_ME,archivo))      # Ruta del archivo
                # CODIGO Y NOMBRE DEL MUNICIPIO
                CP_Name = archivo.split('_')[2].strip()
                CP_Name = CP_Name[0:].upper()
                CP_Name = CP_Name.split('.')[0].strip()
                COD_mun = archivo[0:5]
            
        # Verificar si se encontró el modelo
        if Modelo_Expo is None:
            warning = "No se encontró un archivo de modelo de exposición que cumpla con los criterios."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            Modelo_Expo2 = Modelo_Expo
        
        # arreglar Modelo:
        # Codigo de las manzanas corregido

        cod_mnzdef_model = []
        for mnz in Modelo_Expo2.cod_mnz:
            if mnz[0].isalpha():
                mnz2 = str(mnz)
                cod_mnzdef_model.append(mnz2[1::])   
        Modelo_Expo2.cod_mnz = cod_mnzdef_model

        cod_sccdef_model = []
        for scc in Modelo_Expo2.cod_secc:
            if scc[0].isalpha():
                cod_sccdef_model.append(scc[1::])
        Modelo_Expo2.cod_secc = cod_sccdef_model

        # Codigo y nombre del municipio
        # Modificar modelo de exposicion para añadir secciones
        cod_secc_Modelo = []
        for val in Modelo_Expo2.cod_mnz:
            cod_secc_Modelo.append(val[:-2])
        Modelo_Expo2['cod_secc'] = cod_secc_Modelo
        
        
        # 4). Verificar lo que hay en la carpeta 'Modelo_Exposicion'
        manzana_shp_rt = None
        for archivo in os.listdir(Folder_SP):                                   # Lista de archivos en la carpeta shapes
            if archivo.endswith(".shp") and "MGN_MANZANA" in archivo:           # Obtener solo los archivos que terminan en .shp
                manzana_shp_rt = gpd.read_file(os.path.join(Folder_SP,archivo)) # Ruta del archivo

        # Verificar si se encontró el archivo
        if manzana_shp_rt is None:
            warning = "No se encontró un archivo shape manzanas que cumpla con los criterios."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            manzana_shp = manzana_shp_rt
            
        area_shp_rt = None
        for archivo in os.listdir(Folder_SP):                                   # Lista de archivos en la carpeta shapes
            if archivo.endswith(".shp") and "MGN_AREA" in archivo:              # Obtener solo los archivos que terminan en .shp
                area_shp_rt = gpd.read_file(os.path.join(Folder_SP,archivo))    # Ruta del archivo

        # Verificar si se encontró el archivo
        if area_shp_rt is None:
            warning = "No se encontró un archivo shape área que cumpla con los criterios."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            area_shp = area_shp_rt
            
        # =====================================================================
        # =====================================================================
        
        for archivo in rutas_csv:
            if archivo.endswith(".csv") and "avg_losses-mean" in archivo:       # Obtener solo los archivos que terminan en .hdf5
                df_aggrisk = pd.read_csv(archivo,skiprows=1)                    # Ruta de los archivos
            if archivo.endswith(".csv") and "avg_damages-mean" in archivo:      # Obtener solo los archivos que terminan en .hdf5
                df_aggdamage = pd.read_csv(archivo,skiprows=1)                  # Ruta de los archivos
        
        # Codigo de las manzanas corregido
        cod_mnzdef = []
        for mnz in df_aggrisk.cod_mnz:
            cod_mnzdef.append(mnz[1::])
        df_aggrisk.cod_mnz = cod_mnzdef
        df_aggdamage.cod_mnz = cod_mnzdef

        # Codigo de las secciones corregido
        cod_seccdef = []
        for scc in df_aggrisk.cod_secc:
            cod_seccdef.append(scc[1::])
        df_aggrisk.cod_secc = cod_seccdef
        df_aggdamage.cod_secc = cod_seccdef

        columns_to_convert = [col for col in df_aggdamage.columns if re.search('structural', col)]

        for col in columns_to_convert:
            # Reemplaza 'NAN' con 0 antes de convertir a numérico
            df_aggdamage[col] = df_aggdamage[col].replace('NAN', 0).astype(float)
            
        
        
        # =====================================================================
        # RESULTADOS PROBABILISTICOS 
        # =====================================================================
        
        # Valor expuesto
        Valexpuesto = Modelo_Expo2['val_fisico'].sum()                          # Valor expuesto en millones COP
        # Perdida esperada
        PAE_COP_Mun = df_aggrisk['structural'].sum()                            # Perdida esperada en millones COP
        PAE_PRC_Mun = (PAE_COP_Mun/Valexpuesto)*100                             # Perdida esperada % por mil
        # Afectaciones humanas
        Poblacion = Modelo_Expo2['poblacion'].sum()                             # Poblacion total
        # Numero de edificaciones
        Num_Edificios = Modelo_Expo2['no_edificaciones'].sum()                  # Numero de edificaciones totales
        
        # Poblacion en dano extensivo
        dmg3_no_edis = df_aggdamage['structural~Severo'].sum()                  # Numero de ediciaciones en severo
        dmg3_hab = np.around((Poblacion/Num_Edificios)*dmg3_no_edis,0)          # Poblacion en severo
        dmg3_hab_PRC = (dmg3_hab/Poblacion)*100                                 # % de la poblacion en severo
        
        # Poblacion en dano extensivo
        dmg4_no_edis = df_aggdamage['structural~Completo'].sum()                # Numero de ediciaciones en colapso
        dmg4_hab = np.around((Poblacion/Num_Edificios)*dmg4_no_edis,0)          # Poblacion en colapso
        dmg4_hab_PRC = (dmg4_hab/Poblacion)*100                                     # % de la poblacion en colapso
        
        # Fallecidos
        fatalities_val = np.around(df_aggdamage['structural~fatalities'].sum(),0)  # Numero de fallecidos
        fatalities_PRC = (fatalities_val/Poblacion)*100                         # % de fallecidos
        
        # Heridos
        injured_val = np.around(df_aggdamage['structural~injured'].sum(),0)     # Numero de heridos
        injured_PRC = (injured_val/Poblacion)*100                               # % de heridos
        
        
        # Dataframe de daño colapso por manzana
        collapsed_mnz = df_aggdamage.groupby('cod_mnz')['structural~collapsed'].sum()
        aggdamage_mnz = pd.DataFrame({'cod_mnz':collapsed_mnz.index.tolist(),'collapsed':collapsed_mnz.tolist()})
            
        mapdata_collapsed = manzana_shp.merge(aggdamage_mnz, left_on='COD_DANE', right_on='cod_mnz', how='left')
        
        # Filtrar gdf1 para eliminar filas con NaN en 'collapsed'
        mapdata_collapsed = mapdata_collapsed.dropna(subset=['collapsed'])

        # Extraer los valores de 'cod_mnz' de gdf1 filtrado
        cod_mnz_values = mapdata_collapsed['cod_mnz'].dropna().tolist()

        # Filtrar gdf2 para que contenga solo las filas con 'cod_mnz' en cod_mnz_values
        manzana_shp = manzana_shp[manzana_shp['COD_DANE'].isin(cod_mnz_values)]
        
        
        # Dataframe dano severo por taxonomia
        txn_list2 = df_aggdamage.groupby('taxonomy')['asset_id'].sum()
        txn_list = txn_list2.index.tolist()
        
        df_group_dmg3txn = df_aggdamage.groupby('taxonomy')['structural~Severo'].sum()
        No_edis_txn = Modelo_Expo2.groupby('tipologia')['no_edificaciones'].sum()                  
        
        nueva_tipologias = [tip.split('/H')[0] for tip in txn_list]
        df_dmg3txn = pd.DataFrame({'taxonomy':nueva_tipologias,'dmg3':df_group_dmg3txn,'no_edis':No_edis_txn})
        

        df_grp_dmg3txn = df_dmg3txn.groupby('taxonomy')[['dmg3','no_edis']].sum()

        df_dmg3txn = pd.DataFrame({'taxonomy':df_grp_dmg3txn.index,'dmg3':df_grp_dmg3txn.dmg3,'no_edis':df_grp_dmg3txn.no_edis})
        df_dmg3txn = df_dmg3txn.reset_index(drop=True)

        for index,txn in enumerate(df_dmg3txn.taxonomy):
            if txn == "NI/NI/NI":
                df_dmg3txn.drop(df_dmg3txn.index[index], inplace=True) 
                df_dmg3txn = df_dmg3txn.reset_index(drop=True)
                
            
        df_dmg3txn['dmg3_prc'] = (df_dmg3txn.dmg3/df_dmg3txn.no_edis)*100
        
        print(df_dmg3txn.taxonomy)
        
        df_dmg3txn['description'] = wnfun_lib.Taxo_Description(df_dmg3txn)
        
        # Encuentra el índice del valor máximo en la columna 'dmg3_prc'
        max_idx = df_dmg3txn['dmg3_prc'].idxmax()
        # Selecciona la fila correspondiente al valor máximo
        maxrow_dmg3txn = df_dmg3txn.loc[max_idx]
        
        # Dataframe colapso por taxonomia
        df_group_dmg4txn = df_aggdamage.groupby('taxonomy')['structural~Completo'].sum()            
        
        df_dmg4txn = pd.DataFrame({'taxonomy':nueva_tipologias,'dmg4':df_group_dmg4txn,'no_edis':No_edis_txn})

        df_grp_dmg4txn = df_dmg4txn.groupby('taxonomy')[['dmg4','no_edis']].sum()

        df_dmg4txn = pd.DataFrame({'taxonomy':df_grp_dmg4txn.index,'dmg4':df_grp_dmg4txn.dmg4,'no_edis':df_grp_dmg4txn.no_edis})
        df_dmg4txn = df_dmg4txn.reset_index(drop=True)

        for index,txn in enumerate(df_dmg4txn.taxonomy):
            if txn == "NI/NI/NI":
                df_dmg4txn.drop(df_dmg4txn.index[index], inplace=True) 
                df_dmg4txn = df_dmg4txn.reset_index(drop=True)
            
        df_dmg4txn['dmg4_prc'] = (df_dmg4txn.dmg4/df_dmg4txn.no_edis)*100
        df_dmg4txn['description'] = wnfun_lib.Taxo_Description(df_dmg4txn)
        # Encuentra el índice del valor máximo en la columna 'dmg4_prc'
        max_idx = df_dmg4txn['dmg4_prc'].idxmax()
        # Selecciona la fila correspondiente al valor máximo
        maxrow_dmg4txn = df_dmg4txn.loc[max_idx]
        
        
        # -------------------------- Digrama circular -------------------------
        dmg0_no_edis = df_aggdamage['structural~no_damage'].sum()
        dmg0_hab_PRC = (np.around((Poblacion/Num_Edificios)*dmg0_no_edis,0)/Poblacion)*100  
        
        dmg1_no_edis = df_aggdamage['structural~Leve'].sum()
        dmg1_hab_PRC = (np.around((Poblacion/Num_Edificios)*dmg1_no_edis,0)/Poblacion)*100  
        
        dmg2_no_edis = df_aggdamage['structural~Moderado'].sum()
        dmg2_hab_PRC = (np.around((Poblacion/Num_Edificios)*dmg2_no_edis,0)/Poblacion)*100  
        
        categorias = ['Sin Daño','Leve','Moderado','Extensivo','Colapso']
        Colapsos_no_edis = [dmg0_hab_PRC,dmg1_hab_PRC,dmg2_hab_PRC,dmg3_hab_PRC,dmg4_hab_PRC]

        # Definir el colormap
        colors = plt.cm.get_cmap('bone').reversed()(np.linspace(0.1, 0.7, len(categorias)))

        # Crear el diagrama circular
        fig = plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(Colapsos_no_edis, colors=colors, autopct='%1.1f%%', startangle=140)

        # Añadir la leyenda
        # plt.legend(wedges, categorias, loc="center left", bbox_to_anchor=(0.92, 0.5),fontsize=14, frameon=False, handlelength=1, handletextpad=0.4)
        plt.setp(autotexts, size=13, weight="bold")

        # Eliminar el título del gráfico
        plt.title('')

        # Ajustar márgenes para reducir el espacio en blanco
        plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)

        # Guardar la imagen con bordes ajustados
        # Se guarda la imagen en la carpeta de la misma app
        plt.savefig(os.path.join(os.path.join(os.getcwd(),"css"), "Diagrama_Circular.jpg"), dpi=300, bbox_inches='tight', pad_inches=0)
        plt.show()
        
        # -----------------------------------------------------------------
        # Obtener el colormap 'bone' con 256 colores
        bone = plt.cm.get_cmap('Blues', 180)

        # El primer color de 'bone' invertido es el último color de 'bone'
        # Para obtener el último color, puedes usar el valor 1.0
        primer_color_bone_inverted = bone(0.2)

        # Crear un colormap personalizado que consiste solo en ese color
        colormap_personalizado = ListedColormap([primer_color_bone_inverted])

        wnfun_lib.mapa_gen_Infograph(0,area_shp,manzana_shp,mapdata_collapsed,'collapsed','Blues','Map_Collapsed.jpg',0.5,2,6.5,'Edificios colapsados')
        
        
        
        wnfun_lib.Diagrama_no_edis(df_dmg3txn.taxonomy,df_dmg3txn.dmg3_prc,"Barras_Extensivo.jpg")
        wnfun_lib.Diagrama_no_edis(df_dmg4txn.taxonomy,df_dmg4txn.dmg4_prc,"Barras_Colapso.jpg")
        
        '''----------------------------------------------------------------
                                    GENERAR PDF
        ----------------------------------------------------------------'''
        # Rutas de los archivos
        if calculation_mode == 'Probabilistico':
            pdf_base_path = os.path.join(os.path.join(os.getcwd(),"css"), "FichaTecnica_Probabilista.pdf")
        else:
            pdf_base_path = os.path.join(os.path.join(os.getcwd(),"css"), "FichaTecnica_Determinista.pdf")
        output_pdf_path = os.path.join(os.path.join(os.getcwd(),"css"), "Output_Ficha_tecnica.pdf")
        
        image_path_circular = os.path.join(os.path.join(os.getcwd(),"css"), "Diagrama_Circular.jpg")
        image_path_mapa = os.path.join(os.path.join(os.getcwd(),"css"), "Map_Collapsed.jpg")
        image_path_severo = os.path.join(os.path.join(os.getcwd(),"css"), "Barras_Extensivo.jpg")
        image_path_colapso = os.path.join(os.path.join(os.getcwd(),"css"), "Barras_Colapso.jpg")

        # Crear un nuevo PDF con el contenido adicional
        # packet = io.BytesIO()
        # c = canvas.Canvas(packet, pagesize=letter)
        # width, height = letter

        #Conversión de centímetros a puntos
        def cm_to_points(cm):
            return cm * 72 / 2.54
        # Dimensiones personalizadas en puntos
        custom_width = cm_to_points(33.867)  # Ancho en puntos
        custom_height = cm_to_points(19.05)  # Alto en puntos
        # Crear un nuevo tamaño de página personalizado
        custom_page_size = (custom_width, custom_height)
        # Crear un buffer para el PDF
        packet = io.BytesIO()
        # Crear un lienzo con el tamaño de página personalizado
        c = canvas.Canvas(packet, pagesize=custom_page_size)
        # Ahora puedes usar `width` y `height` como el ancho y alto de la página personalizada
        width, height = custom_page_size

        # Registrar la fuente Abadi MT
        # pdfmetrics.registerFont(TTFont('AbadiMT', '/path/to/AbadiMT.ttf'))

        # Registrar la fuente Aptos Display
        pdfmetrics.registerFont(TTFont('AbadiMT', os.path.join(os.path.join(os.getcwd(),"css"), "abadi-mt.ttf")))
        pdfmetrics.registerFont(TTFont('AbadiMT_Bold', os.path.join(os.path.join(os.getcwd(),"css"), "abadi-mt-std-bold.ttf")))
        pdfmetrics.registerFont(TTFont('Aptos', os.path.join(os.path.join(os.getcwd(),"css"), "aptos.ttf")))
        pdfmetrics.registerFont(TTFont('Aptos_Bold', os.path.join(os.path.join(os.getcwd(),"css"), "aptos-bold.ttf")))

        # Agregar textos
        if calculation_mode == 'Probabilistico':
            c.setFont("AbadiMT_Bold", 10.5)
            c.setFillColorRGB(217/255, 217/255, 217/255) #------------------------------ Color blanco
            c.drawString(841, 480, 'PROBABILÍSTICO') #---------------------------------- Nombre del modo de calculo
        else:
            c.setFont("AbadiMT_Bold", 10.5)
            c.setFillColorRGB(217/255, 217/255, 217/255) #------------------------------ Color blanco
            c.drawString(841, 480, 'DETERMINÍSTICO') #---------------------------------- Nombre del modo de calculo
        
        c.setFont("AbadiMT_Bold", 36)
        c.setFillColorRGB(242/255, 242/255, 242/255) #---------------------------------- Color blanco
        c.drawString(50, 499, CP_Name) #------------------------------------------------ Nombre del municipio

        c.setFont("AbadiMT_Bold", 11)
        c.setFillColorRGB(191/255, 191/255, 191/255) #---------------------------------- Color #BFBFBF
        c.drawString(82, 472, 'COD DANE:'+COD_mun) #------------------------------------ Código del municipio

        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(165, 337, f"$ {np.around(Valexpuesto,2):,.2f}") #------------------ Valor expuesto

        c.setFont("Aptos_Bold", 11)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(60, 275, f"$ {int(PAE_COP_Mun):,}") #------------------------------ PAE en cop millones
        
        if calculation_mode == 'Probabilistico':
            c.setFont("Aptos_Bold", 11)
            c.setFillColorRGB(51/255, 86/255, 107/255) #-------------------------------- Color #33566B
            c.drawString(188, 275, f"{np.around(PAE_PRC_Mun,2):.3}"+'‰') #-------------- PAE en porcentaje por mil
        else:
            c.setFont("Aptos_Bold", 11)
            c.setFillColorRGB(51/255, 86/255, 107/255) #-------------------------------- Color #33566B
            c.drawString(187, 275, f"{np.around(PAE_PRC_Mun,2):}"+'%') #-------------- PAE en porcentaje por mil
        
        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(164, 242, f"{int(Poblacion):,}") #--------------------------------- PAE en cop millones

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(103, 200.5, f"{int(dmg3_hab):,}") #-------------------------------- Hab en daño severo

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(133, 200.5, f"{np.around(dmg3_hab_PRC,1):}") #------------------- Hab prc en daño severo

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(95, 188, f"{int(dmg4_hab):,}") #----------------------------------- Hab en colapso

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(124, 188, f"{np.around(dmg4_hab_PRC,1):}") #--------------------- Hab prc en colapso

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(103, 164, f"{int(injured_val):,}") #---------------------------- heridos

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(159, 164, f"{np.around(injured_PRC,1):.2}") #------------------- heridos prc

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(285, 164, f"{int(fatalities_val):,}") #------------------------------- fallecidos

        c.setFont("Aptos_Bold", 10)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(91, 152, f"{np.around(fatalities_PRC,1):.2}") #----------------------- fallecidos prc

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_circular)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 120
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_circular, 140, 32 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_mapa)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 220
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_mapa, 370, 42 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_colapso)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 170
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_colapso, 700, 260 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # Agregar una imagen
        image = Image.open(image_path_severo)
        image_width, image_height = image.size
        aspect_ratio = image_height / float(image_width)
        new_image_width = 170
        new_image_height = new_image_width * aspect_ratio
        c.drawImage(image_path_severo, 700, 45 , width=new_image_width, height=new_image_height)
        # -----------------------------------------------------------------------------

        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(691, 243,f"{int(np.around(maxrow_dmg4txn.dmg4_prc,0))}") #--------- Porcentaje de edificaciones en tipologia predominante

        c.setFont("Aptos", 8)
        c.setFillColorRGB(89/255, 89/255, 89/255) #------------------------------------- Color #595959
        c.drawString(733, 243, maxrow_dmg4txn.description + ' colapsan') #-------------- Descripcion de la tipologia predominante

        c.setFont("Aptos_Bold", 18)
        c.setFillColorRGB(51/255, 86/255, 107/255) #------------------------------------ Color #33566B
        c.drawString(691, 25,f"{int(np.around(maxrow_dmg3txn.dmg3_prc,0))}") #---------- Porcentaje de edificaciones en tipologia predominante

        c.setFont("Aptos", 8)
        c.setFillColorRGB(89/255, 89/255, 89/255) #------------------------------------- Color #595959
        c.drawString(733, 25, maxrow_dmg3txn.description + ' tienen daño severo') #-------------- Descripcion de la tipologia predominante


        # Guardar el nuevo contenido en memoria
        c.save()
        packet.seek(0)

        # Leer el PDF base y el nuevo PDF
        pdf_base = PyPDF2.PdfReader(open(pdf_base_path, "rb"))
        new_pdf = PyPDF2.PdfReader(packet)

        # Crear un objeto de escritura para el PDF de salida
        pdf_writer = PyPDF2.PdfWriter()

        # Obtener la primera página del PDF base
        page = pdf_base.pages[0]

        # Obtener el contenido del nuevo PDF (solo una página)
        new_page = new_pdf.pages[0]

        # Superponer el nuevo contenido en la primera página del PDF base
        page.merge_page(new_page)

        # Agregar la página modificada al escritor de PDF
        pdf_writer.add_page(page)

        # Agregar las demás páginas del PDF base
        for page_num in range(1, len(pdf_base.pages)):
            page = pdf_base.pages[page_num]
            pdf_writer.add_page(page)

        # Guardar el PDF combinado
        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)
        
    return output_pdf_path,calculation_mode,CP_Name

def carpetas_en_folder(rootdir1):
    
    Ver_Folder_hdf5 = None                                                      # Verificar carpeta 'Archivos_hdf5'
    Ver_Folder_csv = None                                                       # Verificar carpeta 'Archivo_csv'
    Ver_Folder_ME = None                                                        # Verificar carpeta 'Modelo_Exposicion'
    Ver_Folder_SP = None                                                        # Verificar carpeta 'Shapes_CP'
        
    for folder in os.listdir(rootdir1):                                         # Obtiene la lista de archivos en la carpeta 
        
        # Si existe la carpeta 'Archivos_hdf5' o 'Archivo_csv'
        if "Archivos_hdf5" in folder:
            Ver_Folder_hdf5 = 1
        elif "Archivos_csv" in folder:
            Ver_Folder_csv = 1

        # Si existe la carpeta 'Modelo_Exposicion'
        if "Modelo_Exposicion" in folder:
            Ver_Folder_ME = 1
        
        # Si existe la carpeta 'Shapes_CP'
        if "Shapes_CP" in folder:
            Ver_Folder_SP = 1
            
    # Si no esta la carpeta 'Archivos_hdf5' ni 'Archivo_csv'
    if Ver_Folder_hdf5 is None and Ver_Folder_csv is None:
        warning = "En la carpeta seleccionada no existe la carpeta 'Archivos_hdf5' ni la carpeta 'Archivo_csv'." 
        tk.messagebox.showinfo("ERROR", warning)
        
    # Si no esta la carpeta 'Modelo_Exposicion'
    if Ver_Folder_ME is None:
        warning = "En la carpeta seleccionada no existe la carpeta 'Modelo_Exposicion'." 
        tk.messagebox.showinfo("ERROR", warning)
        
    # Si no esta la carpeta 'Shapes_CP'
    if Ver_Folder_SP is None:
        warning = "En la carpeta seleccionada no existe la carpeta 'Shapes_CP'." 
        tk.messagebox.showinfo("ERROR", warning)    
        

    return Ver_Folder_hdf5,Ver_Folder_csv,Ver_Folder_ME,Ver_Folder_SP
