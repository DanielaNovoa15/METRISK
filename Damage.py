    # -----------------------------------------------------------------------------
# -------------- CALIBRATION ELEMENTS // SHOW AND HIDE ELEMENTS ---------------
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

#%% ====== SHOW CALIBRATION ELEMENTS ==========================================
def Show_Dano_Elements(DNO_title,DNO_text,DNO_boton,cnt_container,upcnt_color,Select_Folder_DNO,Ventana_Info_DNO,Function_Danos,resultado_label_DNO):
    # ---- Titulo de la pestaña:
    if DNO_title["tlt_tlt_DNO"] is None:
        DNO_title["tlt_tlt_DNO"] = wnfun_lib.Label_Image('/Danos_title.png', 760, 163, cnt_container,"white",0.309,0.216)
        
    # ---- Descripcion introductoria:
    if DNO_text["txt_cnt_DNO"] is None:
        DNO_text["txt_cnt_DNO"] = wnfun_lib.Label_Image('/Danos_text.png', 620, 480, cnt_container,"white",0.32,0.57)
    
    # ---- Seleccionar carpeta:
    if DNO_boton["btn_slc_DNO"] is None:
        DNO_boton["btn_slc_DNO"] = wnfun_lib.Button_Image('/Select_FolderV2.png', 278, 65, cnt_container,"white",0.78,0.5,Select_Folder_DNO)
        
    # ---- Informacion:
    if DNO_boton["btn_inf_DNO"] is None:
        DNO_boton["btn_inf_DNO"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.885,0.468,Ventana_Info_DNO) 
    
    # ---- Generar:
    if DNO_boton["btn_clb_DNO"] is None:
        DNO_boton["btn_clb_DNO"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 200, 66, cnt_container,"white",0.78,0.58,Function_Danos,resultado_label_DNO)
    
#%% ====== HIDE LOSSES ELEMENTS ===============================================
def Hide_Danos_Elements(title_DNO,DNO_title,text_DNO,DNO_text,boton_DNO,DNO_boton,canva_DNO,DNO_canva):
    
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
        
#%% ====== FUNCION PERDIDAS ===================================================
def Function_Danos_Elements(carpeta_seleccionada_DNO):
    
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
        elif len(rutas_hdf5) == 1:
            warning = "Solo hay un archivo .hdf5 en la carpeta."
            tk.messagebox.showinfo("ERROR", warning)
        elif len(rutas_hdf5) == 2:
            warning = "Solo hay os archivos .hdf5 en la carpeta."
            tk.messagebox.showinfo("ERROR", warning)
        elif len(rutas_hdf5) > 3:
            warning = "Hay más de tres archivos .hdf5 en la carpeta."
            tk.messagebox.showinfo("ERROR", warning)
        else:
            # Para el primer archivo hdf5 recolectado 
            # Verificar que agregado tiene el archivo y si es probabilistico o deterministico
            with h5py.File(rutas_hdf5[0], 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                
            if oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Probabilistico"
                ruta_hdf5_mnz = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Deterministico"
                ruta_hdf5_mnz = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Probabilistico"
                ruta_hdf5_txn = rutas_hdf5[0]
            
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Deterministico"
                ruta_hdf5_txn = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Probabilistico"
                ruta_hdf5_scc = rutas_hdf5[0]
            
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Deterministico"
                ruta_hdf5_scc = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk":
                warning = "Has elegido un archivo .hdf5 de pérdidas basado en eventos. Elige el de daño basado en eventos"
                tk.messagebox.showinfo("ERROR", warning)
            else:
                warning = "El archivo no cumple con los criterios."
                tk.messagebox.showinfo("ERROR", warning)
            
            # Para el segundo archivo hdf5 recolectado 
            # Verificar que agregado tiene el archivo
            with h5py.File(rutas_hdf5[1], 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                
            if oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Probabilistico"
                ruta_hdf5_mnz = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Deterministico"
                ruta_hdf5_mnz = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Probabilistico"
                ruta_hdf5_txn = rutas_hdf5[1]
            
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Deterministico"
                ruta_hdf5_txn = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Probabilistico"
                ruta_hdf5_scc = rutas_hdf5[1]
            
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Deterministico"
                ruta_hdf5_scc = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk":
                warning = "Has elegido un archivo .hdf5 de pérdidas basado en eventos. Elige el de daño basado en eventos"
                tk.messagebox.showinfo("ERROR", warning)
            else:
                warning = "El archivo no cumple con los criterios."
                tk.messagebox.showinfo("ERROR", warning)
            
            # Para el tercer archivo hdf5 recolectado 
            # Verificar que agregado tiene el archivo
            with h5py.File(rutas_hdf5[2], 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                
            if oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Probabilistico"
                ruta_hdf5_mnz = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Deterministico"
                ruta_hdf5_mnz = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Probabilistico"
                ruta_hdf5_txn = rutas_hdf5[2]
            
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Deterministico"
                ruta_hdf5_txn = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Probabilistico"
                ruta_hdf5_scc = rutas_hdf5[2]
            
            elif oqparam_dict['calculation_mode'] == "scenario_damage" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Deterministico"
                ruta_hdf5_scc = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk":
                warning = "Has elegido un archivo .hdf5 de pérdidas basado en eventos. Elige el de daño basado en eventos"
                tk.messagebox.showinfo("ERROR", warning)
            else:
                warning = "El archivo no cumple con los criterios."
                tk.messagebox.showinfo("ERROR", warning)
        
        if calculation_mode_mnz == "Probabilistico" and calculation_mode_txn == "Probabilistico" and calculation_mode_scc == "Probabilistico":
            calculation_mode = "Probabilistico"
        elif calculation_mode_mnz == "Deterministico" and calculation_mode_txn == "Deterministico" and calculation_mode_scc == "Deterministico":
            calculation_mode = "Deterministico"
        else:
            warning = "Has elegido un archivo .hdf5, o varios, con diferentes modos de cálculo"
            tk.messagebox.showinfo("ERROR", warning)
            
        # =========================================================================
        #                        CASO PROBABILISTICO
        # =========================================================================
        
        if calculation_mode == "Probabilistico":
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
            
            seccion_shp_rt = None
            for archivo in os.listdir(Folder_SP):                                   # Lista de archivos en la carpeta shapes
                if archivo.endswith(".shp") and "MGN_SECCION" in archivo:           # Obtener solo los archivos que terminan en .shp
                    seccion_shp_rt = gpd.read_file(os.path.join(Folder_SP,archivo)) # Ruta del archivo
    
            # Verificar si se encontró el archivo
            if seccion_shp_rt is None:
                warning = "No se encontró un archivo shape sección que cumpla con los criterios."
                tk.messagebox.showinfo("ERROR", warning)
            else:
                seccion_shp = seccion_shp_rt
            
            

            with h5py.File(ruta_hdf5_scc, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8')) # Lista de parametros de OpenQuake
                mnz_list_bytes  = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:] # Lista de taxonomias
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()]  # ID del agregado
                dmg_0 = archivo["aggrisk"]["dmg_0"][()] 
                dmg_1 = archivo["aggrisk"]["dmg_1"][()]
                dmg_2 = archivo["aggrisk"]["dmg_2"][()]
                dmg_3 = archivo["aggrisk"]["dmg_3"][()]
                dmg_4 = archivo["aggrisk"]["dmg_4"][()]
                valex = archivo["assetcol"]["array"]["value-number"][()] 
                
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()] 
                
                
            Num_build = np.sum(valex)
            dic = {'agg_id':agg_id,'dmg_0':dmg_0,'dmg_1':dmg_1,'dmg_2':dmg_2,'dmg_3':dmg_3,'dmg_4':dmg_4}
            df_group = pd.DataFrame(dic) # dataframe perdidas por aggid
            # no dano
            grp_aggid_dmg0 = df_group.groupby('agg_id')['dmg_0']  # agrupa las perdidas por aggid para leve
            stats_dmg0 = grp_aggid_dmg0.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg0.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg0 = stats_dmg0[stats_dmg0['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg0.drop(stats_mnp_dmg0.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg0.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg0.reset_index(level=0, inplace=True) # resetea el indice agregado
            # ligero
            grp_aggid_dmg1 = df_group.groupby('agg_id')['dmg_1']  # agrupa las perdidas por aggid para leve
            stats_dmg1 = grp_aggid_dmg1.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg1.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg1 = stats_dmg1[stats_dmg1['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg1.drop(stats_mnp_dmg1.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg1.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg1.reset_index(level=0, inplace=True) # resetea el indice agregado
            # moderado
            grp_aggid_dmg2 = df_group.groupby('agg_id')['dmg_2']  # agrupa las perdidas por aggid para leve
            stats_dmg2 = grp_aggid_dmg2.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg2.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg2 = stats_dmg2[stats_dmg2['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg2.drop(stats_mnp_dmg2.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg2.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg2.reset_index(level=0, inplace=True) # resetea el indice agregado
            # severo
            grp_aggid_dmg3 = df_group.groupby('agg_id')['dmg_3']  # agrupa las perdidas por aggid para leve
            stats_dmg3 = grp_aggid_dmg3.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg3.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg3 = stats_dmg3[stats_dmg3['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg3.drop(stats_mnp_dmg3.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg3.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg3.reset_index(level=0, inplace=True) # resetea el indice agregado
            # colapso
            grp_aggid_dmg4 = df_group.groupby('agg_id')['dmg_4']  # agrupa las perdidas por aggid para leve
            stats_dmg4 = grp_aggid_dmg4.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg4.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg4 = stats_dmg4[stats_dmg4['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg4.drop(stats_mnp_dmg4.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg4.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg4.reset_index(level=0, inplace=True) # resetea el indice agregado

            # melted sin dano
            dfmelted_mnp_dmg0 = stats_mnp_dmg0.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg0')
            dfmelted_txn_dmg0 = stats_dmg0.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg0')
            dfmelted_txn_dmg0.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg0['stat'] = dfmelted_txn_dmg0['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg0['stat'] = dfmelted_mnp_dmg0['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg0 = dfmelted_mnp_dmg0.drop(columns=['agg_id'])
            dfmelted_txn_dmg0['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg0['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg0 = dfmelted_txn_dmg0.drop(columns=['agg_id'])
            dfmelted_txn_dmg0 = dfmelted_txn_dmg0.reset_index(drop=True)
            # melted ligero
            dfmelted_mnp_dmg1 = stats_mnp_dmg1.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg1')
            dfmelted_txn_dmg1 = stats_dmg1.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg1')
            dfmelted_txn_dmg1.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg1['stat'] = dfmelted_txn_dmg1['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg1['stat'] = dfmelted_mnp_dmg1['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg1 = dfmelted_mnp_dmg1.drop(columns=['agg_id'])
            dfmelted_txn_dmg1['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg1['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg1 = dfmelted_txn_dmg1.drop(columns=['agg_id'])
            dfmelted_txn_dmg1 = dfmelted_txn_dmg1.reset_index(drop=True)
            # melted moderado
            dfmelted_mnp_dmg2 = stats_mnp_dmg2.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg2')
            dfmelted_txn_dmg2 = stats_dmg2.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg2')
            dfmelted_txn_dmg2.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg2['stat'] = dfmelted_txn_dmg2['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg2['stat'] = dfmelted_mnp_dmg2['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg2 = dfmelted_mnp_dmg2.drop(columns=['agg_id'])
            dfmelted_txn_dmg2['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg2['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg2 = dfmelted_txn_dmg2.drop(columns=['agg_id'])
            dfmelted_txn_dmg2 = dfmelted_txn_dmg2.reset_index(drop=True)
            # melted severo
            dfmelted_mnp_dmg3 = stats_mnp_dmg3.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg3')
            dfmelted_txn_dmg3 = stats_dmg3.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg3')
            dfmelted_txn_dmg3.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg3['stat'] = dfmelted_txn_dmg3['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg3['stat'] = dfmelted_mnp_dmg3['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg3 = dfmelted_mnp_dmg3.drop(columns=['agg_id'])
            dfmelted_txn_dmg3['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg3['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg3 = dfmelted_txn_dmg3.drop(columns=['agg_id'])
            dfmelted_txn_dmg3 = dfmelted_txn_dmg3.reset_index(drop=True)
            # melted colapso
            dfmelted_mnp_dmg4 = stats_mnp_dmg4.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg4')
            dfmelted_txn_dmg4 = stats_dmg4.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg4')
            dfmelted_txn_dmg4.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg4['stat'] = dfmelted_txn_dmg4['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg4['stat'] = dfmelted_mnp_dmg4['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg4 = dfmelted_mnp_dmg4.drop(columns=['agg_id'])
            dfmelted_txn_dmg4['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg4['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg4 = dfmelted_txn_dmg4.drop(columns=['agg_id'])
            dfmelted_txn_dmg4 = dfmelted_txn_dmg4.reset_index(drop=True)

            # dataframe de solo las perdidas promedio del municipio
            dic_mnp = {'stat':dfmelted_mnp_dmg0.stat,'loss_dmg0':dfmelted_mnp_dmg0.loss_dmg0,'loss_dmg1':dfmelted_mnp_dmg1.loss_dmg1,'loss_dmg2':dfmelted_mnp_dmg2.loss_dmg2,'loss_dmg3':dfmelted_mnp_dmg3.loss_dmg3,'loss_dmg4':dfmelted_mnp_dmg4.loss_dmg4}
            dfmelted_mnp = pd.DataFrame(dic_mnp)
            aggrisk_resu = list(np.array(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg0))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg1))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg2))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg3))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg4))
            # dataframe de perdidas promedio por manzana
            dic_mnp = {'stat':dfmelted_txn_dmg0.stat,'cod_mnz':dfmelted_txn_dmg0.cod_mnz,'loss_dmg0':dfmelted_txn_dmg0.loss_dmg0,'loss_dmg1':dfmelted_txn_dmg1.loss_dmg1,'loss_dmg2':dfmelted_txn_dmg2.loss_dmg2,'loss_dmg3':dfmelted_txn_dmg3.loss_dmg3,'loss_dmg4':dfmelted_txn_dmg4.loss_dmg4}
            dfmelted_mnz = pd.DataFrame(dic_mnp)
            aggrisk_mnz = np.zeros((len(dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0),5))
            aggrisk_mnz[:,0] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0
            aggrisk_mnz[:,1] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg1
            aggrisk_mnz[:,2] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg2
            aggrisk_mnz[:,3] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg3
            aggrisk_mnz[:,4] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg4
            
            # procesar mapas
            
            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg_4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['fatalities'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()

            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_fatalities = pd.DataFrame({'cod_mnz':cod_mnzdef,'aad_secc_urb_fallecidos_hab':aggrisk_mnz})

            Expo_groupby_mnz = Modelo_Expo2.groupby('cod_secc')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_mnz':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_mnz':df_losses_fatalities.cod_mnz})

            index_mal = pruebadf1.cod_mnz[~pruebadf1.cod_mnz.isin(pruebadf2.cod_mnz)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses_fatalities['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_mnz[~pruebadf2.cod_mnz.isin(pruebadf1.cod_mnz)].dropna().tolist()
                    df_losses_fatalities.drop(np.where(df_losses_fatalities.cod_mnz == index_mal[0])[0][0], inplace=True)
                    df_losses_fatalities['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses_fatalities['poblacion'] = list(pruebadf1.poblacion)

            # -----------------------------------------------------------------
            
            df_losses_fatalities['aad_secc_urb_fallecidos_100m_hab'] = df_losses_fatalities.aad_secc_urb_fallecidos_hab*100000/df_losses_fatalities.poblacion
            mapdata_fatalities_scc = seccion_shp.merge(df_losses_fatalities, left_on='COD_SECC', right_on='cod_mnz', how='left')
            
            # -----------------------------------------------------------------
            
            grp_aggid = df_group.groupby('agg_id')['injured'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()

            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_injured = pd.DataFrame({'cod_mnz':cod_mnzdef,'aad_secc_urb_heridos_hab':aggrisk_mnz})


            # -----------------------------------------------------------------
            
            df_losses_injured['aad_secc_urb_heridos_100m_hab'] = df_losses_injured.aad_secc_urb_heridos_hab*100000/df_losses_fatalities.poblacion
            mapdata_injured_scc = seccion_shp.merge(df_losses_injured, left_on='COD_SECC', right_on='cod_mnz', how='left')
            
            # -----------------------------------------------------------------
            
            grp_aggid = df_group.groupby('agg_id')['homeless'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_homeless = pd.DataFrame({'cod_mnz':cod_mnzdef,'aac_secc_urb_colapso_hab':aggrisk_mnz})

            
            # -----------------------------------------------------------------

            mapdata_homeless_scc = seccion_shp.merge(df_losses_homeless, left_on='COD_SECC', right_on='cod_mnz', how='left')

            # -----------------------------------------------------------------
            
            grp_aggid = df_group.groupby('agg_id')['collapsed'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_collapsed = pd.DataFrame({'cod_mnz':cod_mnzdef,'aac_secc_urb_colapso_no_edis':aggrisk_mnz})

            # -----------------------------------------------------------------

            mapdata_collapsed_scc = seccion_shp.merge(df_losses_collapsed, left_on='COD_SECC', right_on='cod_mnz', how='left')
            
            # -----------------------------------------------------------------
            
       
            '''====================================================================
            
                   Procesar el archivo agregado por manzana y por taxonomia
            
            ===================================================================='''
            
            with h5py.File(ruta_hdf5_mnz, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8')) # Lista de parametros de OpenQuake
                mnz_list_bytes  = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:] # Lista de taxonomias
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()]  # ID del agregado
                dmg_0 = archivo["aggrisk"]["dmg_0"][()] 
                dmg_1 = archivo["aggrisk"]["dmg_1"][()]
                dmg_2 = archivo["aggrisk"]["dmg_2"][()]
                dmg_3 = archivo["aggrisk"]["dmg_3"][()]
                dmg_4 = archivo["aggrisk"]["dmg_4"][()]
                valex = archivo["assetcol"]["array"]["value-number"][()] 
                
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()] 
                
                
            Num_build = np.sum(valex)
            dic = {'agg_id':agg_id,'dmg_0':dmg_0,'dmg_1':dmg_1,'dmg_2':dmg_2,'dmg_3':dmg_3,'dmg_4':dmg_4}
            df_group = pd.DataFrame(dic) # dataframe perdidas por aggid
            # no dano
            grp_aggid_dmg0 = df_group.groupby('agg_id')['dmg_0']  # agrupa las perdidas por aggid para leve
            stats_dmg0 = grp_aggid_dmg0.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg0.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg0 = stats_dmg0[stats_dmg0['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg0.drop(stats_mnp_dmg0.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg0.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg0.reset_index(level=0, inplace=True) # resetea el indice agregado
            # ligero
            grp_aggid_dmg1 = df_group.groupby('agg_id')['dmg_1']  # agrupa las perdidas por aggid para leve
            stats_dmg1 = grp_aggid_dmg1.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg1.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg1 = stats_dmg1[stats_dmg1['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg1.drop(stats_mnp_dmg1.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg1.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg1.reset_index(level=0, inplace=True) # resetea el indice agregado
            # moderado
            grp_aggid_dmg2 = df_group.groupby('agg_id')['dmg_2']  # agrupa las perdidas por aggid para leve
            stats_dmg2 = grp_aggid_dmg2.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg2.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg2 = stats_dmg2[stats_dmg2['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg2.drop(stats_mnp_dmg2.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg2.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg2.reset_index(level=0, inplace=True) # resetea el indice agregado
            # severo
            grp_aggid_dmg3 = df_group.groupby('agg_id')['dmg_3']  # agrupa las perdidas por aggid para leve
            stats_dmg3 = grp_aggid_dmg3.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg3.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg3 = stats_dmg3[stats_dmg3['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg3.drop(stats_mnp_dmg3.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg3.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg3.reset_index(level=0, inplace=True) # resetea el indice agregado
            # colapso
            grp_aggid_dmg4 = df_group.groupby('agg_id')['dmg_4']  # agrupa las perdidas por aggid para leve
            stats_dmg4 = grp_aggid_dmg4.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg4.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg4 = stats_dmg4[stats_dmg4['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg4.drop(stats_mnp_dmg4.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg4.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg4.reset_index(level=0, inplace=True) # resetea el indice agregado

            # melted sin dano
            dfmelted_mnp_dmg0 = stats_mnp_dmg0.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg0')
            dfmelted_txn_dmg0 = stats_dmg0.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg0')
            dfmelted_txn_dmg0.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg0['stat'] = dfmelted_txn_dmg0['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg0['stat'] = dfmelted_mnp_dmg0['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg0 = dfmelted_mnp_dmg0.drop(columns=['agg_id'])
            dfmelted_txn_dmg0['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg0['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg0 = dfmelted_txn_dmg0.drop(columns=['agg_id'])
            dfmelted_txn_dmg0 = dfmelted_txn_dmg0.reset_index(drop=True)
            # melted ligero
            dfmelted_mnp_dmg1 = stats_mnp_dmg1.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg1')
            dfmelted_txn_dmg1 = stats_dmg1.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg1')
            dfmelted_txn_dmg1.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg1['stat'] = dfmelted_txn_dmg1['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg1['stat'] = dfmelted_mnp_dmg1['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg1 = dfmelted_mnp_dmg1.drop(columns=['agg_id'])
            dfmelted_txn_dmg1['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg1['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg1 = dfmelted_txn_dmg1.drop(columns=['agg_id'])
            dfmelted_txn_dmg1 = dfmelted_txn_dmg1.reset_index(drop=True)
            # melted moderado
            dfmelted_mnp_dmg2 = stats_mnp_dmg2.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg2')
            dfmelted_txn_dmg2 = stats_dmg2.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg2')
            dfmelted_txn_dmg2.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg2['stat'] = dfmelted_txn_dmg2['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg2['stat'] = dfmelted_mnp_dmg2['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg2 = dfmelted_mnp_dmg2.drop(columns=['agg_id'])
            dfmelted_txn_dmg2['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg2['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg2 = dfmelted_txn_dmg2.drop(columns=['agg_id'])
            dfmelted_txn_dmg2 = dfmelted_txn_dmg2.reset_index(drop=True)
            # melted severo
            dfmelted_mnp_dmg3 = stats_mnp_dmg3.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg3')
            dfmelted_txn_dmg3 = stats_dmg3.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg3')
            dfmelted_txn_dmg3.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg3['stat'] = dfmelted_txn_dmg3['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg3['stat'] = dfmelted_mnp_dmg3['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg3 = dfmelted_mnp_dmg3.drop(columns=['agg_id'])
            dfmelted_txn_dmg3['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg3['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg3 = dfmelted_txn_dmg3.drop(columns=['agg_id'])
            dfmelted_txn_dmg3 = dfmelted_txn_dmg3.reset_index(drop=True)
            # melted colapso
            dfmelted_mnp_dmg4 = stats_mnp_dmg4.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg4')
            dfmelted_txn_dmg4 = stats_dmg4.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg4')
            dfmelted_txn_dmg4.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg4['stat'] = dfmelted_txn_dmg4['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg4['stat'] = dfmelted_mnp_dmg4['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg4 = dfmelted_mnp_dmg4.drop(columns=['agg_id'])
            dfmelted_txn_dmg4['cod_mnz'] = np.array(mnz_list)[(dfmelted_txn_dmg4['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg4 = dfmelted_txn_dmg4.drop(columns=['agg_id'])
            dfmelted_txn_dmg4 = dfmelted_txn_dmg4.reset_index(drop=True)

            # dataframe de solo las perdidas promedio del municipio
            dic_mnp = {'stat':dfmelted_mnp_dmg0.stat,'loss_dmg0':dfmelted_mnp_dmg0.loss_dmg0,'loss_dmg1':dfmelted_mnp_dmg1.loss_dmg1,'loss_dmg2':dfmelted_mnp_dmg2.loss_dmg2,'loss_dmg3':dfmelted_mnp_dmg3.loss_dmg3,'loss_dmg4':dfmelted_mnp_dmg4.loss_dmg4}
            dfmelted_mnp = pd.DataFrame(dic_mnp)
            aggrisk_resu = list(np.array(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg0))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg1))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg2))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg3))
            aggrisk_resu.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg4))
            # dataframe de perdidas promedio por manzana
            dic_mnp = {'stat':dfmelted_txn_dmg0.stat,'cod_mnz':dfmelted_txn_dmg0.cod_mnz,'loss_dmg0':dfmelted_txn_dmg0.loss_dmg0,'loss_dmg1':dfmelted_txn_dmg1.loss_dmg1,'loss_dmg2':dfmelted_txn_dmg2.loss_dmg2,'loss_dmg3':dfmelted_txn_dmg3.loss_dmg3,'loss_dmg4':dfmelted_txn_dmg4.loss_dmg4}
            dfmelted_mnz = pd.DataFrame(dic_mnp)
            aggrisk_mnz = np.zeros((len(dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0),5))
            aggrisk_mnz[:,0] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0
            aggrisk_mnz[:,1] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg1
            aggrisk_mnz[:,2] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg2
            aggrisk_mnz[:,3] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg3
            aggrisk_mnz[:,4] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg4
            
            # procesar mapas
            
            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg_4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['fatalities'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()

            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_fatalities = pd.DataFrame({'cod_mnz':cod_mnzdef,'aad_mnz_fallecidos_hab':aggrisk_mnz})

            Expo_groupby_mnz = Modelo_Expo2.groupby('cod_mnz')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_mnz':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_mnz':df_losses_fatalities.cod_mnz})

            index_mal = pruebadf1.cod_mnz[~pruebadf1.cod_mnz.isin(pruebadf2.cod_mnz)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses_fatalities['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_mnz[~pruebadf2.cod_mnz.isin(pruebadf1.cod_mnz)].dropna().tolist()
                    df_losses_fatalities.drop(np.where(df_losses_fatalities.cod_mnz == index_mal[0])[0][0], inplace=True)
                    df_losses_fatalities['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses_fatalities['poblacion'] = list(pruebadf1.poblacion)

            # -----------------------------------------------------------------
            
            df_losses_fatalities['aad_mnz_fallecidos_100m_hab'] = df_losses_fatalities.aad_mnz_fallecidos_hab*100000/df_losses_fatalities.poblacion
            mapdata_fatalities = manzana_shp.merge(df_losses_fatalities, left_on='COD_DANE', right_on='cod_mnz', how='left')
            
            # -----------------------------------------------------------------
            
            grp_aggid = df_group.groupby('agg_id')['injured'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()

            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_injured = pd.DataFrame({'cod_mnz':cod_mnzdef,'aad_mnz_heridos_hab':aggrisk_mnz})


            # -----------------------------------------------------------------
            
            df_losses_injured['aad_mnz_heridos_100m_hab'] = df_losses_injured.aad_mnz_heridos_hab*100000/df_losses_fatalities.poblacion
            mapdata_injured = manzana_shp.merge(df_losses_injured, left_on='COD_DANE', right_on='cod_mnz', how='left')
            
            # -----------------------------------------------------------------
            
            grp_aggid = df_group.groupby('agg_id')['homeless'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_homeless = pd.DataFrame({'cod_mnz':cod_mnzdef,'aac_mnz_urb_colapso_hab':aggrisk_mnz})

            
            # -----------------------------------------------------------------

            mapdata_homeless = manzana_shp.merge(df_losses_homeless, left_on='COD_DANE', right_on='cod_mnz', how='left')

            # -----------------------------------------------------------------
            
            grp_aggid = df_group.groupby('agg_id')['collapsed'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses_collapsed = pd.DataFrame({'cod_mnz':cod_mnzdef,'aac_mnz_colapso_no_edis':aggrisk_mnz})

            # -----------------------------------------------------------------

            mapdata_collapsed = manzana_shp.merge(df_losses_collapsed, left_on='COD_DANE', right_on='cod_mnz', how='left')
            
            # -----------------------------------------------------------------
            
            with h5py.File(ruta_hdf5_txn, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8')) # Lista de parametros de OpenQuake
                mnz_list_bytes  = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:] # Lista de taxonomias
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                txn_list_bytes  = archivo["assetcol"]["tagcol"]["taxonomy"][()][1:] # Lista de taxonomias
                txn_list = [item.decode('utf-8') for item in txn_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()]  # ID del agregado
                dmg_0 = archivo["aggrisk"]["dmg_0"][()] 
                dmg_1 = archivo["aggrisk"]["dmg_1"][()]
                dmg_2 = archivo["aggrisk"]["dmg_2"][()]
                dmg_3 = archivo["aggrisk"]["dmg_3"][()]
                dmg_4 = archivo["aggrisk"]["dmg_4"][()]
                valex = archivo["assetcol"]["array"]["value-number"][()] 
                txn_valex = archivo["assetcol"]["array"]["taxonomy"][()] 
                
            dic = {'agg_id':agg_id,'dmg_0':dmg_0,'dmg_1':dmg_1,'dmg_2':dmg_2,'dmg_3':dmg_3,'dmg_4':dmg_4}
            df_group = pd.DataFrame(dic) # dataframe perdidas por aggid
            # no dano
            grp_aggid_dmg0 = df_group.groupby('agg_id')['dmg_0']  # agrupa las perdidas por aggid para leve
            stats_dmg0 = grp_aggid_dmg0.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg0.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg0 = stats_dmg0[stats_dmg0['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg0.drop(stats_mnp_dmg0.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg0.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg0.reset_index(level=0, inplace=True) # resetea el indice agregado
            # ligero
            grp_aggid_dmg1 = df_group.groupby('agg_id')['dmg_1']  # agrupa las perdidas por aggid para leve
            stats_dmg1 = grp_aggid_dmg1.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg1.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg1 = stats_dmg1[stats_dmg1['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg1.drop(stats_mnp_dmg1.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg1.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg1.reset_index(level=0, inplace=True) # resetea el indice agregado
            # moderado
            grp_aggid_dmg2 = df_group.groupby('agg_id')['dmg_2']  # agrupa las perdidas por aggid para leve
            stats_dmg2 = grp_aggid_dmg2.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg2.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg2 = stats_dmg2[stats_dmg2['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg2.drop(stats_mnp_dmg2.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg2.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg2.reset_index(level=0, inplace=True) # resetea el indice agregado
            # severo
            grp_aggid_dmg3 = df_group.groupby('agg_id')['dmg_3']  # agrupa las perdidas por aggid para leve
            stats_dmg3 = grp_aggid_dmg3.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg3.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg3 = stats_dmg3[stats_dmg3['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg3.drop(stats_mnp_dmg3.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg3.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg3.reset_index(level=0, inplace=True) # resetea el indice agregado
            # colapso
            grp_aggid_dmg4 = df_group.groupby('agg_id')['dmg_4']  # agrupa las perdidas por aggid para leve
            stats_dmg4 = grp_aggid_dmg4.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_dmg4.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_mnp_dmg4 = stats_dmg4[stats_dmg4['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_dmg4.drop(stats_mnp_dmg4.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_mnp_dmg4.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_dmg4.reset_index(level=0, inplace=True) # resetea el indice agregado

            # melted sin dano
            dfmelted_mnp_dmg0 = stats_mnp_dmg0.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg0')
            dfmelted_txn_dmg0 = stats_dmg0.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg0')
            dfmelted_txn_dmg0.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg0['stat'] = dfmelted_txn_dmg0['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg0['stat'] = dfmelted_mnp_dmg0['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg0 = dfmelted_mnp_dmg0.drop(columns=['agg_id'])
            dfmelted_txn_dmg0['taxonomy'] = np.array(txn_list)[(dfmelted_txn_dmg0['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg0 = dfmelted_txn_dmg0.drop(columns=['agg_id'])
            dfmelted_txn_dmg0 = dfmelted_txn_dmg0.reset_index(drop=True)
            # melted ligero
            dfmelted_mnp_dmg1 = stats_mnp_dmg1.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg1')
            dfmelted_txn_dmg1 = stats_dmg1.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg1')
            dfmelted_txn_dmg1.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg1['stat'] = dfmelted_txn_dmg1['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg1['stat'] = dfmelted_mnp_dmg1['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg1 = dfmelted_mnp_dmg1.drop(columns=['agg_id'])
            dfmelted_txn_dmg1['taxonomy'] = np.array(txn_list)[(dfmelted_txn_dmg1['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg1 = dfmelted_txn_dmg1.drop(columns=['agg_id'])
            dfmelted_txn_dmg1 = dfmelted_txn_dmg1.reset_index(drop=True)
            # melted moderado
            dfmelted_mnp_dmg2 = stats_mnp_dmg2.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg2')
            dfmelted_txn_dmg2 = stats_dmg2.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg2')
            dfmelted_txn_dmg2.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg2['stat'] = dfmelted_txn_dmg2['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg2['stat'] = dfmelted_mnp_dmg2['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg2 = dfmelted_mnp_dmg2.drop(columns=['agg_id'])
            dfmelted_txn_dmg2['taxonomy'] = np.array(txn_list)[(dfmelted_txn_dmg2['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg2 = dfmelted_txn_dmg2.drop(columns=['agg_id'])
            dfmelted_txn_dmg2 = dfmelted_txn_dmg2.reset_index(drop=True)
            # melted severo
            dfmelted_mnp_dmg3 = stats_mnp_dmg3.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg3')
            dfmelted_txn_dmg3 = stats_dmg3.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg3')
            dfmelted_txn_dmg3.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg3['stat'] = dfmelted_txn_dmg3['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg3['stat'] = dfmelted_mnp_dmg3['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg3 = dfmelted_mnp_dmg3.drop(columns=['agg_id'])
            dfmelted_txn_dmg3['taxonomy'] = np.array(txn_list)[(dfmelted_txn_dmg3['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg3 = dfmelted_txn_dmg3.drop(columns=['agg_id'])
            dfmelted_txn_dmg3 = dfmelted_txn_dmg3.reset_index(drop=True)
            # melted colapso
            dfmelted_mnp_dmg4 = stats_mnp_dmg4.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg4')
            dfmelted_txn_dmg4 = stats_dmg4.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss_dmg4')
            dfmelted_txn_dmg4.sort_values(by='agg_id', inplace=True)
            dfmelted_txn_dmg4['stat'] = dfmelted_txn_dmg4['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg4['stat'] = dfmelted_mnp_dmg4['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp_dmg4 = dfmelted_mnp_dmg4.drop(columns=['agg_id'])
            dfmelted_txn_dmg4['taxonomy'] = np.array(txn_list)[(dfmelted_txn_dmg4['agg_id'] / 1).astype(int)]
            dfmelted_txn_dmg4 = dfmelted_txn_dmg4.drop(columns=['agg_id'])
            dfmelted_txn_dmg4 = dfmelted_txn_dmg4.reset_index(drop=True)

            # dataframe de solo las perdidas promedio del municipio
            dic_mnp = {'stat':dfmelted_mnp_dmg0.stat,'loss_dmg0':dfmelted_mnp_dmg0.loss_dmg0,'loss_dmg1':dfmelted_mnp_dmg1.loss_dmg1,'loss_dmg2':dfmelted_mnp_dmg2.loss_dmg2,'loss_dmg3':dfmelted_mnp_dmg3.loss_dmg3,'loss_dmg4':dfmelted_mnp_dmg4.loss_dmg4}
            dfmelted_mnp = pd.DataFrame(dic_mnp)
            aggrisk = list(np.array(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg0))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg1))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg2))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg3))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg4))
            # dataframe de perdidas promedio por manzana
            dic_mnp = {'stat':dfmelted_txn_dmg0.stat,'taxonomy':dfmelted_txn_dmg0.taxonomy,'loss_dmg0':dfmelted_txn_dmg0.loss_dmg0,'loss_dmg1':dfmelted_txn_dmg1.loss_dmg1,'loss_dmg2':dfmelted_txn_dmg2.loss_dmg2,'loss_dmg3':dfmelted_txn_dmg3.loss_dmg3,'loss_dmg4':dfmelted_txn_dmg4.loss_dmg4}
            dfmelted_mnz = pd.DataFrame(dic_mnp)
            aggrisk_mnz = np.zeros((len(dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0),5))
            aggrisk_mnz[:,0] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0
            aggrisk_mnz[:,1] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg1
            aggrisk_mnz[:,2] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg2
            aggrisk_mnz[:,3] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg3
            aggrisk_mnz[:,4] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg4
            taxonomias = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].taxonomy.tolist()

            taxo_def = []
            for txn in taxonomias:
                parte = txn.split('/')
                taxo_def.append(parte[0]+'/'+parte[1]+'/'+parte[2])
                    
            df_losses = pd.DataFrame({'dmg0':aggrisk_mnz[:,0],'dmg1':aggrisk_mnz[:,1],'dmg2':aggrisk_mnz[:,2],'dmg3':aggrisk_mnz[:,3],'dmg4':aggrisk_mnz[:,4],'taxonomy':taxo_def})
            df_lossesgrup = df_losses.groupby('taxonomy')['dmg0','dmg1','dmg2','dmg3','dmg4'].sum().reset_index()
            df_valex = pd.DataFrame({'valex':valex,'index':txn_valex})
            df_codtxn = pd.DataFrame({'taxonomy':taxo_def,'index':range(1,len(taxonomias)+1)})
            df_prom = pd.merge(df_valex, df_codtxn, on='index', how='left') 
            grouped_df = df_prom.groupby('taxonomy')['valex'].sum().reset_index()

                
            # ------- Nombre del municipio --------------------------------------------
            CP_Name = oqparam_dict['description'].split('_')[3].strip()            # Nombre del centro poblado inicial
            if CP_Name[0].islower():
                CP_Name = CP_Name[0].upper() + CP_Name[1:]                              # Si el nombre del centro poblado no comienza con una mayuscula
            
                
            df_expotax = pd.merge(df_lossesgrup, grouped_df, on='taxonomy', how='left') 
            
            # ------- Codigo del municipio ------------------------------------
            COD_mun = cod_mnzdef[0][0:4] 
            
            
            
            
    return Num_build,aggrisk_resu,df_expotax,taxonomias,aggrisk_mnz,mapdata_fatalities,mapdata_injured,mapdata_homeless,mapdata_collapsed,manzana_shp,seccion_shp,area_shp, calculation_mode, Modelo_Expo2, CP_Name, COD_mun, mapdata_fatalities_scc, mapdata_homeless_scc, mapdata_injured_scc, mapdata_collapsed_scc
    

def carpetas_en_folder(rootdir1):
    
    Ver_Folder_hdf5 = None                                                      # Verificar carpeta 'Archivos_hdf5'
    Ver_Folder_csv = None                                                       # Verificar carpeta 'Archivo_csv'
    Ver_Folder_ME = None                                                        # Verificar carpeta 'Modelo_Exposicion'
    Ver_Folder_SP = None                                                        # Verificar carpeta 'Shapes_CP'
        
    for folder in os.listdir(rootdir1):                                         # Obtiene la lista de archivos en la carpeta 
        
        # Si existe la carpeta 'Archivos_hdf5' o 'Archivo_csv'
        if "Archivos_hdf5" in folder:
            Ver_Folder_hdf5 = 1
        elif "Archivo_csv" in folder:
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
#%% Distribuir resultados en tabla por taxonomia

def Gen_Elements_Tax(df_expotax_DNO,DNO_table,DNO_boton,Contador_Valores):
    
    # Edificios por cada taxonomia
    Total_taxo = []
    for index in range(len(df_expotax_DNO)):
        sumatotal = df_expotax_DNO.dmg0[index]+df_expotax_DNO.dmg1[index]+df_expotax_DNO.dmg2[index]+df_expotax_DNO.dmg3[index]+df_expotax_DNO.dmg4[index]
        Total_taxo.append(np.around(sumatotal,0))
        
    # Colocar tipología constructiva en la tabla   
    suma = 0
    for index in range(len(df_expotax_DNO)):
        Variable_Name = 'tbl_TC'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=df_expotax_DNO.taxonomy[index], 
                                font=("Abadi MT", 13), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.0835, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Sin Daño en la tabla 
        Variable_Name = 'tbl_DS1_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg0[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.21, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS1_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg0[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.295, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Leve en la tabla 
        Variable_Name = 'tbl_DS2_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg1[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.375, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS2_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg1[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.456, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Moderado en la tabla 
        Variable_Name = 'tbl_DS3_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg2[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.537, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS3_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg2[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.627, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Severo en la tabla 
        Variable_Name = 'tbl_DS4_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg3[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.717, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS4_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg3[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.799, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Colapso Leve en la tabla 
        Variable_Name = 'tbl_DS5_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg4[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.881, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS5_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg4[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.963, rely=0.294+suma, anchor=tk.CENTER)
        
        suma = suma + 0.13
    
    return Contador_Valores

def Gen_Elements_Tax_6(df_expotax_DNO,DNO_table,DNO_boton):
    
    # Edificios por cada taxonomia
    Total_taxo = []
    for index in range(len(df_expotax_DNO)):
        sumatotal = df_expotax_DNO.dmg0[index]+df_expotax_DNO.dmg1[index]+df_expotax_DNO.dmg2[index]+df_expotax_DNO.dmg3[index]+df_expotax_DNO.dmg4[index]
        Total_taxo.append(np.around(sumatotal,0))
        
    # Colocar tipología constructiva en la tabla   
    suma = 0
    for index in range(len(df_expotax_DNO)):
        Variable_Name = 'tbl_TC'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=df_expotax_DNO.taxonomy[index], 
                                font=("Abadi MT", 13), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.0835, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Sin Daño en la tabla 
        Variable_Name = 'tbl_DS1_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg0[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.21, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS1_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg0[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.295, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Leve en la tabla 
        Variable_Name = 'tbl_DS2_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg1[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.375, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS2_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg1[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.456, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Moderado en la tabla 
        Variable_Name = 'tbl_DS3_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg2[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.537, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS3_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg2[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.627, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Severo en la tabla 
        Variable_Name = 'tbl_DS4_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg3[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.717, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS4_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg3[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.799, rely=0.294+suma, anchor=tk.CENTER)
        
        # Colocar Daño Colapso Leve en la tabla 
        Variable_Name = 'tbl_DS5_'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around(df_expotax_DNO.dmg4[index],0), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.881, rely=0.294+suma, anchor=tk.CENTER)
        
        Variable_Name = 'tbl_DS5_prc'+str(index+1)
        if DNO_table[Variable_Name] is None:
            DNO_table[Variable_Name] = tk.Label(DNO_boton["tbl_CP_DNO"], text=np.around((np.around(df_expotax_DNO.dmg4[index],0)/Total_taxo[index])*100,2), 
                                font=("Abadi MT", 11), bg="#C6CFD4", fg="#000000")
            DNO_table[Variable_Name].place(relx=0.963, rely=0.294+suma, anchor=tk.CENTER)
        
        suma = suma + 0.13
    