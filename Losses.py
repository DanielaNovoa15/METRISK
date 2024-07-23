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
import FunctionsLibrary as wnfun_lib
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
def Show_Perdidas_Elements(PRD_title,PRD_text,PRD_boton,PRD_entry,PRD_rectg,cnt_container,upcnt_color,Select_Folder_PRD,Ventana_Info_PRD,Function_Perdidas,resultado_label_PRD):
    # ---- Titulo de la pestaña:
    if PRD_title["tlt_tlt_PRD"] is None:
        PRD_title["tlt_tlt_PRD"] = wnfun_lib.Label_Image('/Perdidas_title.png', 760, 125, cnt_container,"white",0.309,0.188)
        
    # ---- Descripcion introductoria:
    if PRD_text["txt_cnt_PRD1"] is None:
        PRD_text["txt_cnt_PRD1"] = wnfun_lib.Label_Image('/Perdidas_text.png', 620, 480, cnt_container,"white",0.32,0.57)
    
    # ---- Seleccionar carpeta:
    if PRD_boton["btn_slc_PRD"] is None:
        PRD_boton["btn_slc_PRD"] = wnfun_lib.Button_Image('/Select_FolderV2.png', 278, 65, cnt_container,"white",0.722,0.47,Select_Folder_PRD)
        
    # ---- Informacion:
    if PRD_boton["btn_inf_PRD"] is None:
        PRD_boton["btn_inf_PRD"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.829,0.442,Ventana_Info_PRD) 
    
    # ---- Ingresar periodo de analisis:
    if PRD_boton["btn_ing_PRD"] is None:
        PRD_boton["btn_ing_PRD"] = wnfun_lib.Label_Image('/Ingresar_Periodo.png', 380, 75, cnt_container,"white",0.76,0.55)
    
    # ---- Ingresar numero
    if PRD_rectg["rec_per_PRD"] is None:
        PRD_rectg["rec_per_PRD"] = tk.Canvas(cnt_container, bg="white", bd=0, highlightthickness=0)
        PRD_rectg["rec_per_PRD"].place(relx=0.921, rely=0.54, anchor=tk.CENTER, width=71, height=36)
        x2, y2 = 70, 35
        x1, y1 = 10,10
        radio_esquinas = 5
        color = "#D0CECE"
        wnfun_lib.rec_redond(PRD_rectg["rec_per_PRD"], x1, y1, x2, y2, radio_esquinas, color)
    if PRD_entry["ent_per_PRD"] is None:
        PRD_entry["ent_per_PRD"] = tk.Entry(PRD_rectg["rec_per_PRD"], bg = "#D0CECE", bd=0, highlightthickness=0)
        PRD_entry["ent_per_PRD"].place(relx=0.55, rely=0.62, anchor=tk.CENTER, width=40, height=20)
    
    # ---- Generar:
    if PRD_boton["btn_clb_PRD"] is None:
        PRD_boton["btn_clb_PRD"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 200, 66, cnt_container,"white",0.78,0.66,Function_Perdidas,resultado_label_PRD)
    
#%% ====== HIDE LOSSES ELEMENTS ===============================================
def Hide_Perdidas_Elements(title_PRD,PRD_title,text_PRD,PRD_text,boton_PRD,PRD_boton,entry_PRD,PRD_entry,rectg_PRD,PRD_rectg,canva_PRD,PRD_canva,label_PRD,PRD_label):
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
    
    for lbl in label_PRD:
        if PRD_label[lbl] is not None:
            PRD_label[lbl].place_forget()
            PRD_label[lbl] = None
    
    for cnv in canva_PRD:
        if PRD_canva[cnv] is not None:
            PRD_canva[cnv].get_tk_widget().destroy()
            PRD_canva[cnv] = None
#%% ====== FUNCION PERDIDAS ===================================================
def Function_Perdidas_Elements(carpeta_seleccionada_PRD):
    
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
    
    rootdir1 = carpeta_seleccionada_PRD                                         # Obtiene el directorio de la carpeta seleccionada  
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
    # DESARROLLAR CASO 1 -- SON ARCHIVOS .HDF5
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
                
            if oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Probabilistico"
                ruta_hdf5_mnz = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Deterministico"
                ruta_hdf5_mnz = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Probabilistico"
                ruta_hdf5_txn = rutas_hdf5[0]
            
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Deterministico"
                ruta_hdf5_txn = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Probabilistico"
                ruta_hdf5_scc = rutas_hdf5[0]
            
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Deterministico"
                ruta_hdf5_scc = rutas_hdf5[0]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage":
                warning = "Has elegido un archivo .hdf5 de daño basado en eventos. Elige el de pérdidas basado en eventos"
                tk.messagebox.showinfo("ERROR", warning)
            else:
                warning = "El archivo no cumple con los criterios."
                tk.messagebox.showinfo("ERROR", warning)
            
            # Para el segundo archivo hdf5 recolectado 
            # Verificar que agregado tiene el archivo
            with h5py.File(rutas_hdf5[1], 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                
            if oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Probabilistico"
                ruta_hdf5_mnz = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Deterministico"
                ruta_hdf5_mnz = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Probabilistico"
                ruta_hdf5_txn = rutas_hdf5[1]
            
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Deterministico"
                ruta_hdf5_txn = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Probabilistico"
                ruta_hdf5_scc = rutas_hdf5[1]
            
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Deterministico"
                ruta_hdf5_scc = rutas_hdf5[1]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage":
                warning = "Has elegido un archivo .hdf5 de daño basado en eventos. Elige el de pérdidas basado en eventos"
                tk.messagebox.showinfo("ERROR", warning)
            else:
                warning = "El archivo no cumple con los criterios."
                tk.messagebox.showinfo("ERROR", warning)
            
            # Para el tercer archivo hdf5 recolectado 
            # Verificar que agregado tiene el archivo
            with h5py.File(rutas_hdf5[2], 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                
            if oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Probabilistico"
                ruta_hdf5_mnz = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                calculation_mode_mnz = "Deterministico"
                ruta_hdf5_mnz = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Probabilistico"
                ruta_hdf5_txn = rutas_hdf5[2]
            
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                calculation_mode_txn = "Deterministico"
                ruta_hdf5_txn = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "event_based_risk" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Probabilistico"
                ruta_hdf5_scc = rutas_hdf5[2]
            
            elif oqparam_dict['calculation_mode'] == "scenario_risk" and oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                calculation_mode_scc = "Deterministico"
                ruta_hdf5_scc = rutas_hdf5[2]
                
            elif oqparam_dict['calculation_mode'] == "event_based_damage":
                warning = "Has elegido un archivo .hdf5 de daño basado en eventos. Elige el de pérdidas basado en eventos"
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
            
            '''====================================================================
            
                   Procesar el archivo agregado por manzana y por taxonomia
            
            ===================================================================='''
            # 1). Obtener archivos hdf5 agregado por seccion
            with h5py.File(ruta_hdf5_scc, 'r') as archivo:
                # Para obtener los parametros ingresados desde Openquake del modelo
                oqparam = archivo["oqparam"][()].decode('utf-8') 
                oqparam_dict_scc = json.loads(oqparam)                                  # Lista de los parámetros de OpenQuake
                # Para obtener datos aggrisk
                scc_list_bytes = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:]      # Lista de secciones
                scc_list = [item.decode('utf-8') for item in scc_list_bytes]
                agg_id_scc = archivo["aggrisk"]["agg_id"][()]                           # ID del agregado
                loss_scc = archivo["aggrisk"]["loss"][()]                               # Perdidas segun el aggregate ID
                # Codigo de la manzana segun modelo de exposicion
                cod_scc_valex = archivo["assetcol"]["array"]["cod_secc"][()] 
                valex_scc = archivo["assetcol"]["array"]["value-structural"][()] 
            
            # 2). Obtener archivos hdf5 agregado por manzana
            with h5py.File(ruta_hdf5_mnz, 'r') as archivo:
                # Para obtener los parametros ingresados desde Openquake del modelo
                oqparam = archivo["oqparam"][()].decode('utf-8') 
                oqparam_dict_mnz = json.loads(oqparam)                                  # Lista de los parámetros de OpenQuake
                # Para obtener valor expuesto
                exposicion_mnz = archivo["assetcol"]["array"]["value-structural"][()]   # Lista del valor de la pérdida segun agg_id
                # Para obtener datos risk by event
                riskbyevent_aggid = archivo["risk_by_event"]["agg_id"][()]              # Aggregate id
                riskbyevent_eventid = archivo["risk_by_event"]["event_id"][()]          # ID del evento
                riskbyevent_loss = archivo["risk_by_event"]["loss"][()]                 # Perdida
                event_eventid = archivo["events"]["id"][()]                             # ID del evento
                event_rupid = archivo["events"]["rup_id"][()]                           # ID de la ruptura
                event_year = archivo["events"]["year"][()]                              # Year (ventana de tiempo)
                # Para obtener datos aggrisk
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]       # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id_mnz = archivo["aggrisk"]["agg_id"][()]                           # ID del agregado
                loss_mnz = archivo["aggrisk"]["loss"][()]                               # Perdidas segun el aggregate ID
                # Codigo de la manzana segun modelo de exposicion
                cod_mnz_valex = archivo["assetcol"]["array"]["cod_mnz"][()] 
                valex_mnz = archivo["assetcol"]["array"]["value-structural"][()] 
                # Para obtener datos aggcurves
                aggmnz_matrix = archivo["agg_curves-stats"]['structural'][()]
                
            # 3). Obtener archivos hdf5 agregado por taxonomia
            with h5py.File(ruta_hdf5_txn, 'r') as archivo:
                # Para obtener los parametros ingresados desde Openquake del modelo
                oqparam_dict_txn = json.loads(archivo["oqparam"][()].decode('utf-8'))   # Lista de parametros de OpenQuake
                # Valor expuesto
                exposicion_txn = archivo["assetcol"]["array"]["value-structural"][()] 
                # Para obtener datos aggrisk
                txn_list_bytes  = archivo["assetcol"]["tagcol"]["taxonomy"][()][1:]
                txn_list = [item.decode('utf-8') for item in txn_list_bytes]            # Lista de taxonomias
                agg_id_txn = archivo["aggrisk"]["agg_id"][()]                           # ID del agregado
                loss_txn = archivo["aggrisk"]["loss"][()]                               # Perdidas segun el aggregate ID
                # Codigo de la taxonomia segun modelo de exposicion
                txn_valex = archivo["assetcol"]["array"]["taxonomy"][()]                # Codigo de la taxonomia segun exposicion
            
            # 5). Se obtienen los datos de entrada y se configuran los condicionales
            # ------- Valor expuesto --------------------------------------------------
            valexpuesto = np.sum(exposicion_mnz)/1e6                                    # Valor expuesto en billones de pesos            
            # ------- Nombre del municipio --------------------------------------------
            CP_Name = oqparam_dict_mnz['description'].split('_')[3].strip()            # Nombre del centro poblado inicial
            if CP_Name[0].islower():
                CP_Name = CP_Name[0].upper() + CP_Name[1:]                              # Si el nombre del centro poblado no comienza con una mayuscula
            
                
             
            '''====================================================================
            
                                  Primera pagina de resultados
                                  
               En esta pagina se muestra la curva de excedencia del municipio 
               para periodos de retorno 47, 975 y 2475. Tambien la tabla de
               resumen PAE.
               
            ===================================================================='''    
              
                
            """--------------------------------------------------------------------
               1). Curva de excedencia
            --------------------------------------------------------------------"""
            
            # Dataframe de ID_rupturas segun ID_evento
            dc1_EBR = {'event_id':event_eventid,'rup_id':event_rupid,'year':event_year} # Diccionario ruptura del evento
            df1_EBR = pd.DataFrame(dc1_EBR)                                             # Dataframe ruptura del evento
            # Dataframe de perdidas segun ID_evento
            index_addid = np.where(riskbyevent_aggid==oqparam_dict_mnz['K'])[0]         # Index de los resultados que hay que procesar
            event_id, loss, agg_id = [], [], []
            for index in index_addid:
                event_id.append(riskbyevent_eventid[index])
                loss.append(riskbyevent_loss[index])
                agg_id.append(riskbyevent_aggid[index])
            dc2_EBR = {'event_id':event_id,'loss':loss,'agg_id':agg_id}                 # Diccionario perdidas por evento
            df_EBR = pd.DataFrame(dc2_EBR)                                              # Dataframe perdidas por evento
            df_EBR = df_EBR.sort_values(by='event_id', ascending=True)                  # Organiza ID del elemento de menor a mayor
            df_EBR = df_EBR.merge(df1_EBR, on='event_id', how='left')                   # agrega columnas del DataFrame 1 que coincidan con el ID del evento
            # Dataframe risk-by-event
            df_EBR.rename(columns={'agg_id': 'loss_type'}, inplace=True)                # add_id por loss_type
            df_EBR['loss_type'] = df_EBR['loss_type'].replace({oqparam_dict_mnz['K']: 'structural'}) # Loss_type es structural
            df_EBR = df_EBR.reset_index(drop=True)                                      # Reset el index del dataframe
            # Agregar tasa anual de excedencia al dataframe
            df_EBR.sort_values(by='loss',ascending=True,inplace=True)                   # Valores de menor a mayor
            tasa_list = np.zeros(len(df_EBR))
            tasa_list[0] = 1
            for i in range(1,len(df_EBR)):
                tasa_list[i] = tasa_list[i-1]-1/len(df_EBR)
            df_EBR['perdidaTA'] = tasa_list
            
            """--------------------------------------------------------------------
               2). Tabla de resumen PAE
            --------------------------------------------------------------------"""
            
            index_addid = np.where(agg_id_mnz==oqparam_dict_mnz['K'])[0]                # Indices de el aggid a utilizar
            agg_id, loss = [], []
            for index in index_addid:
                agg_id.append(agg_id_mnz[index])
                loss.append(loss_mnz[index])
            dc1_AGR = {'agg_id':agg_id,'loss':loss}   
            df1_AGR = pd.DataFrame(dc1_AGR) 
            aggsts_loss = [np.mean(df1_AGR.loss)]
            # Obtener el valor de perdida anual promedio de la simulacion
            for stats in oqparam_dict_mnz['quantiles']:
                aggsts_loss.append(np.quantile(df1_AGR.loss,stats))
            # Lista de estadisticas
            list_stats = ['mean']
            for quant in oqparam_dict_mnz['quantiles']:
                list_stats.append('quantile-'+str(quant))
            # Generar datos para el dataframe PAE
            aggcrv_loss,aggcrv_rtn,aggcrv_sts = [],[],[]
            for indT, per in enumerate(oqparam_dict_mnz['return_periods']):
                for indST, sts in enumerate(list_stats):
                    aggcrv_loss.append(aggmnz_matrix[:,indST,:][:,indT][-1])
                    aggcrv_rtn.append(per)
                    aggcrv_sts.append(sts)    
            dc_AGcrv = {'return_period':aggcrv_rtn,'loss_type':[oqparam_dict_mnz['all_cost_types'][0]]*len(aggcrv_rtn),
                        'loss':aggcrv_loss,'stat':aggcrv_sts}
            df_AGcrv = pd.DataFrame(dc_AGcrv)
            PE_mill = df_AGcrv[df_AGcrv['stat'] == 'mean']['loss'].tolist()
            dic = {'Col1':['Valor_expuesto[B$]','Perdida_anual_estimada[M$]','Perdida_anual_estimada[%.]']
                             , 'Col2':[valexpuesto,aggsts_loss[0],(aggsts_loss[0]/(valexpuesto*1e6))*1000]}
            df_resultados = pd.DataFrame(dic)
            Pr50_Val = []
            per = [31,225,475,975,1475]
            for pr in per:
                Pr50_Val.append((1-np.exp(-50/pr))*100)
            
            PAE_mill = aggsts_loss[0]
                
            '''====================================================================
            
                                  Segunda pagina de resultados
                                  
               En esta pagina esta la tabla PAE agregada por tipologia 
               constructiva. Tambien el diagrama PAE por tipologia constructiva.
               
            ====================================================================''' 
            
            """--------------------------------------------------------------------
               1). PAE agregada por tipologia constructiva
            --------------------------------------------------------------------"""
            
            df_group = pd.DataFrame({'agg_id':agg_id_txn, 'loss':loss_txn})             # Dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['loss']                              # Agrupa las perdidas por aggid
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict_txn['quantiles'])   # Calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True)                                # Genera un indice, agg_id se vuelve en columna
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict_txn['K']]     # Genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True)                           # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_agg_mnp.reset_index(level=0, inplace=True)                            # Resetea el indice municipio
            stats_agg.reset_index(level=0, inplace=True)                                # Resetea el indice agregado
            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_txn = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_txn.sort_values(by='agg_id', inplace=True)
            dfmelted_txn['stat'] = dfmelted_txn['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])
            dfmelted_txn['taxonomy'] = np.array(txn_list)[(dfmelted_txn['agg_id'] / 1).astype(int)]
            dfmelted_txn = dfmelted_txn.drop(columns=['agg_id'])
            dfmelted_txn = dfmelted_txn.reset_index(drop=True)
            aggrisk_txn = dfmelted_txn.loc[dfmelted_txn.stat=='mean'].loss.tolist()
            taxonomias = dfmelted_txn.loc[dfmelted_txn.stat=='mean'].taxonomy.tolist()
            taxo_def = []
            for txn in taxonomias:
                parte = txn.split('/')
                taxo_def.append(parte[0]+'/'+parte[1]+'/'+parte[2])
            df_losses = pd.DataFrame({'loss':aggrisk_txn,'taxonomy':taxo_def})
            df_lossesgrup = df_losses.groupby('taxonomy')['loss'].sum().reset_index()
            df_valex = pd.DataFrame({'valex':exposicion_txn,'index':txn_valex})
            df_codtxn = pd.DataFrame({'taxonomy':taxo_def,'index':range(1,len(taxonomias)+1)})
            df_prom = pd.merge(df_valex, df_codtxn, on='index', how='left') 
            grouped_df = df_prom.groupby('taxonomy')['valex'].sum().reset_index()
            df_expotax = pd.merge(df_lossesgrup, grouped_df, on='taxonomy', how='left') 
            df_expotax['loss2'] = (df_expotax.loss/df_expotax.valex)*1000
            taxo_description = descriptiontaxo(df_expotax.taxonomy)
            
            '''====================================================================
            
                                 Cuarta pagina de resultados
                                  
               En esta pagina se muestra el mapa de PAE en millones de pesos 
               colombianos o en %. para manzanas y secciones.
               
            ====================================================================''' 
            
            """--------------------------------------------------------------------
               1). Procesar PAE por manzana
            --------------------------------------------------------------------"""
            
            dataframe_mnz = pd.DataFrame({'agg_id':agg_id_mnz, 'loss':loss_mnz})    # Dataframe perdidas por aggid
            datafrane_mnz_gpb = dataframe_mnz.groupby('agg_id')['loss']             # Agrupa las perdidas por aggid
            stats_df = datafrane_mnz_gpb.describe(
                              percentiles=oqparam_dict_mnz['quantiles'])            # Calcula mediana y percentiles de las perdidas por aggid
            stats_df.reset_index(level=0, inplace=True)                             # Genera un indice, agg_id se vuelve en columna
            stats_CP = stats_df[stats_df['agg_id'] == oqparam_dict_mnz['K']]        # Genera un dataframe para municipio
            stats_df.drop(stats_CP.index, inplace=True)                             # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_CP.reset_index(level=0, inplace=True)                             # Resetea el indice municipio
            stats_df.reset_index(level=0, inplace=True)                             # Resetea el indice agregado
            
            dfmelted_CP = stats_CP.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50 y Q85 del municipio
            dfmelted_MNZ = stats_df.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50, Q85 de la manzana
            
            dfmelted_MNZ.sort_values(by='agg_id', inplace=True)
            dfmelted_MNZ['stat'] = dfmelted_MNZ['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            
            dfmelted_CP['stat'] = dfmelted_CP['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            dfmelted_CP = dfmelted_CP.drop(columns=['agg_id'])
            
            dfmelted_MNZ['cod_mnz'] = np.array(mnz_list)[(dfmelted_MNZ['agg_id']
                                                          / 1).astype(int)]         # Agregar codigo de la manzana al dataframe
            dfmelted_MNZ = dfmelted_MNZ.drop(columns=['agg_id'])
            dfmelted_MNZ = dfmelted_MNZ.reset_index(drop=True)
            
            # Obtener solo resultados promedio para municipio y manzana
            aggrisk_MNZ = dfmelted_MNZ.loc[dfmelted_MNZ.stat=='mean'].loss.tolist() 
            manzanas_mnz = dfmelted_MNZ.loc[dfmelted_MNZ.stat=='mean'].cod_mnz.tolist()
            
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
                
            # ------- Codigo del municipio ------------------------------------
            COD_mun = cod_mnzdef[0][0:4]  
            
            df_losses_mnz = pd.DataFrame({'pae_mnz_cop':aggrisk_MNZ,'cod_mnz':cod_mnzdef})
            
            df_valex_mnz = pd.DataFrame({'valex':valex_mnz,'index':cod_mnz_valex})
            dframe_codmnz = pd.DataFrame({'cod_mnz':cod_mnzdef,'index':range(1,len(cod_mnzdef)+1)})
            
            df_prom_mnz = pd.merge(df_valex_mnz, dframe_codmnz, on='index', how='left') 
            grouped_df_mnz = df_prom_mnz.groupby('cod_mnz')['valex'].sum().reset_index()
            
            df_expotax_mnz = pd.merge(df_losses_mnz, grouped_df_mnz, on='cod_mnz', how='left') 
            df_expotax_mnz['pae_mnz_prc'] = (df_expotax_mnz.pae_mnz_cop/df_expotax_mnz.valex)*1000
            
            df_losses_prc_mnz = pd.merge(df_losses_mnz, grouped_df_mnz, on='cod_mnz', how='left') 
            df_losses_prc_mnz['pae_mnz_prc'] = (df_losses_prc_mnz.pae_mnz_cop/df_losses_prc_mnz.valex)*1000
            
            mapdata_mnz_PAE = manzana_shp.merge(df_losses_prc_mnz, left_on='COD_DANE', right_on='cod_mnz', how='left')
            
            """--------------------------------------------------------------------
               2). Procesar PAE por seccion
            --------------------------------------------------------------------"""
            
            dataframe_scc = pd.DataFrame({'agg_id':agg_id_scc, 'loss':loss_scc})    # Dataframe perdidas por aggid
            datafrane_scc_gpb = dataframe_scc.groupby('agg_id')['loss']             # Agrupa las perdidas por aggid
            stats_df = datafrane_scc_gpb.describe(
                              percentiles=oqparam_dict_scc['quantiles'])            # Calcula mediana y percentiles de las perdidas por aggid
            stats_df.reset_index(level=0, inplace=True)                             # Genera un indice, agg_id se vuelve en columna
            stats_CP = stats_df[stats_df['agg_id'] == oqparam_dict_scc['K']]        # Genera un dataframe para municipio
            stats_df.drop(stats_CP.index, inplace=True)                             # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_CP.reset_index(level=0, inplace=True)                             # Resetea el indice municipio
            stats_df.reset_index(level=0, inplace=True)                             # Resetea el indice agregado
            
            dfmelted_CP = stats_CP.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50 y Q85 del municipio
            dfmelted_SCC = stats_df.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50, Q85 de la manzana
            
            dfmelted_SCC.sort_values(by='agg_id', inplace=True)
            dfmelted_SCC['stat'] = dfmelted_SCC['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            
            dfmelted_CP['stat'] = dfmelted_CP['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            dfmelted_CP = dfmelted_CP.drop(columns=['agg_id'])
            
            dfmelted_SCC['cod_secc'] = np.array(scc_list)[(dfmelted_SCC['agg_id']
                                                          / 1).astype(int)]         # Agregar codigo de la seccion al dataframe
            dfmelted_SCC = dfmelted_SCC.drop(columns=['agg_id'])
            dfmelted_SCC = dfmelted_SCC.reset_index(drop=True)
            
            # Obtener solo resultados promedio para municipio y manzana
            aggrisk_SCC = dfmelted_SCC.loc[dfmelted_SCC.stat=='mean'].loss.tolist() 
            manzanas_scc = dfmelted_SCC.loc[dfmelted_SCC.stat=='mean'].cod_secc.tolist()
            
            cod_sccdef = []
            for scc in manzanas_scc:
                cod_sccdef.append(str(scc[1:]))
            df_losses_scc = pd.DataFrame({'pae_scc_cop':aggrisk_SCC,'cod_secc':cod_sccdef})
            
            df_valex_scc = pd.DataFrame({'valex':valex_scc,'index':cod_scc_valex})
            dframe_codscc = pd.DataFrame({'cod_secc':cod_sccdef,'index':range(1,len(cod_sccdef)+1)})
            
            df_prom_scc = pd.merge(df_valex_scc, dframe_codscc, on='index', how='left') 
            grouped_df_scc = df_prom_scc.groupby('cod_secc')['valex'].sum().reset_index()
            
            df_expotax_scc = pd.merge(df_losses_scc, grouped_df_scc, on='cod_secc', how='left') 
            df_expotax_scc['pae_scc_prc'] = (df_expotax_scc.pae_scc_cop/df_expotax_scc.valex)*1000
            
            df_losses_prc_scc = pd.merge(df_losses_scc, grouped_df_scc, on='cod_secc', how='left') 
            df_losses_prc_scc['pae_scc_prc'] = (df_losses_prc_scc.pae_scc_cop/df_losses_prc_scc.valex)*1000
            
            mapdata_scc_PAE = seccion_shp.merge(df_losses_prc_scc, left_on='COD_SECC', right_on='cod_secc', how='left')

        # =========================================================================
        #                        CASO DETERMINISTICO
        # =========================================================================
        
        if calculation_mode == "Deterministico":
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
            
            # --------- Procesar hdf5 agregado por manzana --------------------
            # 1). Obtener archivos hdf5 agregado por manzana
            with h5py.File(ruta_hdf5_mnz, 'r') as archivo:
                # Para obtener los parametros ingresados desde Openquake del modelo
                oqparam = archivo["oqparam"][()].decode('utf-8') 
                oqparam_dict_mnz = json.loads(oqparam)                                  # Lista de los parámetros de OpenQuake
                # Para obtener valor expuesto
                exposicion_mnz = archivo["assetcol"]["array"]["value-structural"][()]   # Lista del valor de la pérdida segun agg_id
                # Para obtener datos aggrisk
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]       # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id_mnz = archivo["aggrisk"]["agg_id"][()]                           # ID del agregado
                loss_mnz = archivo["aggrisk"]["loss"][()]                               # Perdidas segun el aggregate ID
                # Codigo de la manzana segun modelo de exposicion
                cod_mnz_valex = archivo["assetcol"]["array"]["cod_mnz"][()] 
                valex_mnz = archivo["assetcol"]["array"]["value-structural"][()] 
                
            # # 1). Obtener archivos hdf5 agregado por seccion
            # with h5py.File(ruta_hdf5_scc, 'r') as archivo:
            #     # Para obtener los parametros ingresados desde Openquake del modelo
            #     oqparam = archivo["oqparam"][()].decode('utf-8') 
            #     oqparam_dict_scc = json.loads(oqparam)                                  # Lista de los parámetros de OpenQuake
            #     # Para obtener datos aggrisk
            #     scc_list_bytes = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:]      # Lista de secciones
            #     scc_list = [item.decode('utf-8') for item in scc_list_bytes]
            #     agg_id_scc = archivo["aggrisk"]["agg_id"][()]                           # ID del agregado
            #     loss_scc = archivo["aggrisk"]["loss"][()]                               # Perdidas segun el aggregate ID
            #     # Codigo de la manzana segun modelo de exposicion
            #     cod_scc_valex = archivo["assetcol"]["array"]["cod_secc"][()] 
            #     valex_scc = archivo["assetcol"]["array"]["value-structural"][()] 
            
            

            # # 3). Obtener archivos hdf5 agregado por taxonomia
            # with h5py.File(ruta_hdf5_txn, 'r') as archivo:
            #     # Para obtener los parametros ingresados desde Openquake del modelo
            #     oqparam_dict_txn = json.loads(archivo["oqparam"][()].decode('utf-8'))   # Lista de parametros de OpenQuake
            #     # Valor expuesto
            #     exposicion_txn = archivo["assetcol"]["array"]["value-structural"][()] 
            #     # Para obtener datos aggrisk
            #     txn_list_bytes  = archivo["assetcol"]["tagcol"]["taxonomy"][()][1:]
            #     txn_list = [item.decode('utf-8') for item in txn_list_bytes]            # Lista de taxonomias
            #     agg_id_txn = archivo["aggrisk"]["agg_id"][()]                           # ID del agregado
            #     loss_txn = archivo["aggrisk"]["loss"][()]                               # Perdidas segun el aggregate ID
            #     # Codigo de la taxonomia segun modelo de exposicion
            #     txn_valex = archivo["assetcol"]["array"]["taxonomy"][()]                # Codigo de la taxonomia segun exposicion
            
            '''====================================================================
            
                                  Primera pagina de resultados
                                  
               En esta pagina se muestra una tabla de resumen Valor expuesto
               y pérdida estimada del municipio y por taxonomia.
               
            ===================================================================='''   
            
            # Tabla resumen municipio:
            # Contiene ->
                # Valor expuesto en millones de pesos colombianos
                # Pérdida estimada del municipio en millones de pesos y en %
                
            # -----------------------------------------------------------------
            valexpuesto = np.sum(exposicion_mnz)                                # Valor expuesto en millones de pesos
            # -----------------------------------------------------------------
            
            index_addid = np.where(agg_id_mnz==oqparam_dict_mnz['K'])[0]        # Indices de aggid para resultados de todo el municipio
            agg_id, loss = [], []
            for index in index_addid:
                agg_id.append(agg_id_mnz[index])
                loss.append(loss_mnz[index])
            df1_AGR = pd.DataFrame({'agg_id':agg_id,'loss':loss}) 
            aggsts_loss = [np.mean(df1_AGR.loss)]
            
            # -----------------------------------------------------------------
            PAE_mill = [0]*2
            PAE_mill[0] = aggsts_loss[0]                                        # Pérdida estimada del municipio
            PAE_mill[1] = (aggsts_loss[0]/valexpuesto)*100                      # Pérdida estimada del municipio en %
            # -----------------------------------------------------------------
            
            
            
            
            
            df_EBR,aggsts_loss,PE_mill,df_resultados,Pr50_Val,CP_Name, COD_mun, df_expotax,taxo_description, mapdata_mnz_PAE, mapdata_scc_PAE
            
            
            
            
            
            # ------- Nombre del municipio ------------------------------------
            CP_Name = oqparam_dict_mnz['description'].split('_')[3].strip()     # Nombre del centro poblado inicial
            if CP_Name[0].islower():
                CP_Name = CP_Name[0].upper() + CP_Name[1:]                      # Si el nombre del centro poblado no comienza con una mayuscula
            
            
            index_addid = np.where(agg_id_txn==oqparam_dict_txn['K'])[0]        # Indices de el aggid a utilizar
            agg_id, loss = [], []
            for index in index_addid:
                agg_id.append(agg_id_txn[index])
                loss.append(loss_txn[index])
            dc1_AGR = {'agg_id':agg_id,'loss':loss}   
            df1_AGR = pd.DataFrame(dc1_AGR) 
            aggsts_loss = [np.mean(df1_AGR.loss)]
            
            PE_mill = [aggsts_loss[0],(aggsts_loss[0]/(valexpuesto))*1000]

            # Tabla resumen por taxonomia
            
            df_group = pd.DataFrame({'agg_id':agg_id_txn, 'loss':loss_txn})             # Dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['loss']                              # Agrupa las perdidas por aggid
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict_txn['quantiles'])   # Calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True)                                # Genera un indice, agg_id se vuelve en columna
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict_txn['K']]     # Genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True)                           # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_agg_mnp.reset_index(level=0, inplace=True)                            # Resetea el indice municipio
            stats_agg.reset_index(level=0, inplace=True)                                # Resetea el indice agregado
            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_txn = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_txn.sort_values(by='agg_id', inplace=True)
            dfmelted_txn['stat'] = dfmelted_txn['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])
            dfmelted_txn['taxonomy'] = np.array(txn_list)[(dfmelted_txn['agg_id'] / 1).astype(int)]
            dfmelted_txn = dfmelted_txn.drop(columns=['agg_id'])
            dfmelted_txn = dfmelted_txn.reset_index(drop=True)
            aggrisk_txn = dfmelted_txn.loc[dfmelted_txn.stat=='mean'].loss.tolist()
            taxonomias = dfmelted_txn.loc[dfmelted_txn.stat=='mean'].taxonomy.tolist()
            taxo_def = []
            for txn in taxonomias:
                parte = txn.split('/')
                taxo_def.append(parte[0]+'/'+parte[1]+'/'+parte[2])
            df_losses = pd.DataFrame({'loss':aggrisk_txn,'taxonomy':taxo_def})
            df_lossesgrup = df_losses.groupby('taxonomy')['loss'].sum().reset_index()
            df_valex = pd.DataFrame({'valex':exposicion_txn,'index':txn_valex})
            df_codtxn = pd.DataFrame({'taxonomy':taxo_def,'index':range(1,len(taxonomias)+1)})
            df_prom = pd.merge(df_valex, df_codtxn, on='index', how='left') 
            grouped_df = df_prom.groupby('taxonomy')['valex'].sum().reset_index()
            df_expotax = pd.merge(df_lossesgrup, grouped_df, on='taxonomy', how='left') 
            df_expotax['loss2'] = (df_expotax.loss/df_expotax.valex)*1000
            taxo_description = descriptiontaxo(df_expotax.taxonomy)
            
            '''====================================================================
            
                                 Segunda pagina de resultados
                                  
               En esta pagina se muestra el mapa de PAE en millones de pesos 
               colombianos o en %. para manzanas y secciones.
               
            ====================================================================''' 
            
            """--------------------------------------------------------------------
               1). Procesar PAE por manzana
            --------------------------------------------------------------------"""
            
            dataframe_mnz = pd.DataFrame({'agg_id':agg_id_mnz, 'loss':loss_mnz})    # Dataframe perdidas por aggid
            datafrane_mnz_gpb = dataframe_mnz.groupby('agg_id')['loss']             # Agrupa las perdidas por aggid
            stats_df = datafrane_mnz_gpb.describe(
                              percentiles=oqparam_dict_mnz['quantiles'])            # Calcula mediana y percentiles de las perdidas por aggid
            stats_df.reset_index(level=0, inplace=True)                             # Genera un indice, agg_id se vuelve en columna
            stats_CP = stats_df[stats_df['agg_id'] == oqparam_dict_mnz['K']]        # Genera un dataframe para municipio
            stats_df.drop(stats_CP.index, inplace=True)                             # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_CP.reset_index(level=0, inplace=True)                             # Resetea el indice municipio
            stats_df.reset_index(level=0, inplace=True)                             # Resetea el indice agregado
            
            dfmelted_CP = stats_CP.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50 y Q85 del municipio
            dfmelted_MNZ = stats_df.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50, Q85 de la manzana
            
            dfmelted_MNZ.sort_values(by='agg_id', inplace=True)
            dfmelted_MNZ['stat'] = dfmelted_MNZ['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            
            dfmelted_CP['stat'] = dfmelted_CP['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            dfmelted_CP = dfmelted_CP.drop(columns=['agg_id'])
            
            dfmelted_MNZ['cod_mnz'] = np.array(mnz_list)[(dfmelted_MNZ['agg_id']
                                                          / 1).astype(int)]         # Agregar codigo de la manzana al dataframe
            dfmelted_MNZ = dfmelted_MNZ.drop(columns=['agg_id'])
            dfmelted_MNZ = dfmelted_MNZ.reset_index(drop=True)
            
            # Obtener solo resultados promedio para municipio y manzana
            aggrisk_MNZ = dfmelted_MNZ.loc[dfmelted_MNZ.stat=='mean'].loss.tolist() 
            manzanas_mnz = dfmelted_MNZ.loc[dfmelted_MNZ.stat=='mean'].cod_mnz.tolist()
            
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
                
            # ------- Codigo del municipio ------------------------------------
            COD_mun = cod_mnzdef[0][0:4]  
            
            df_losses_mnz = pd.DataFrame({'pae_mnz_cop':aggrisk_MNZ,'cod_mnz':cod_mnzdef})
            
            df_valex_mnz = pd.DataFrame({'valex':valex_mnz,'index':cod_mnz_valex})
            dframe_codmnz = pd.DataFrame({'cod_mnz':cod_mnzdef,'index':range(1,len(cod_mnzdef)+1)})
            
            df_prom_mnz = pd.merge(df_valex_mnz, dframe_codmnz, on='index', how='left') 
            grouped_df_mnz = df_prom_mnz.groupby('cod_mnz')['valex'].sum().reset_index()
            
            df_expotax_mnz = pd.merge(df_losses_mnz, grouped_df_mnz, on='cod_mnz', how='left') 
            df_expotax_mnz['pae_mnz_prc'] = (df_expotax_mnz.pae_mnz_cop/df_expotax_mnz.valex)*1000
            
            df_losses_prc_mnz = pd.merge(df_losses_mnz, grouped_df_mnz, on='cod_mnz', how='left') 
            df_losses_prc_mnz['pae_mnz_prc'] = (df_losses_prc_mnz.pae_mnz_cop/df_losses_prc_mnz.valex)*1000
            
            mapdata_mnz_PAE = manzana_shp.merge(df_losses_prc_mnz, left_on='COD_DANE', right_on='cod_mnz', how='left')
            
            """--------------------------------------------------------------------
               2). Procesar PAE por seccion
            --------------------------------------------------------------------"""
            
            dataframe_scc = pd.DataFrame({'agg_id':agg_id_scc, 'loss':loss_scc})    # Dataframe perdidas por aggid
            datafrane_scc_gpb = dataframe_scc.groupby('agg_id')['loss']             # Agrupa las perdidas por aggid
            stats_df = datafrane_scc_gpb.describe(
                              percentiles=oqparam_dict_scc['quantiles'])            # Calcula mediana y percentiles de las perdidas por aggid
            stats_df.reset_index(level=0, inplace=True)                             # Genera un indice, agg_id se vuelve en columna
            stats_CP = stats_df[stats_df['agg_id'] == oqparam_dict_scc['K']]        # Genera un dataframe para municipio
            stats_df.drop(stats_CP.index, inplace=True)                             # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_CP.reset_index(level=0, inplace=True)                             # Resetea el indice municipio
            stats_df.reset_index(level=0, inplace=True)                             # Resetea el indice agregado
            
            dfmelted_CP = stats_CP.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50 y Q85 del municipio
            dfmelted_SCC = stats_df.melt(id_vars=['agg_id'], value_vars=['mean', 
                        '15%', '50%', '85%'], var_name='stat', value_name='loss')   # Obtener solo resultados de mean, Q15, Q50, Q85 de la manzana
            
            dfmelted_SCC.sort_values(by='agg_id', inplace=True)
            dfmelted_SCC['stat'] = dfmelted_SCC['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            
            dfmelted_CP['stat'] = dfmelted_CP['stat'].replace({'15%': 
                'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})    # Cambiar nombre de las estadisticas
            dfmelted_CP = dfmelted_CP.drop(columns=['agg_id'])
            
            dfmelted_SCC['cod_secc'] = np.array(scc_list)[(dfmelted_SCC['agg_id']
                                                          / 1).astype(int)]         # Agregar codigo de la seccion al dataframe
            dfmelted_SCC = dfmelted_SCC.drop(columns=['agg_id'])
            dfmelted_SCC = dfmelted_SCC.reset_index(drop=True)
            
            # Obtener solo resultados promedio para municipio y manzana
            aggrisk_SCC = dfmelted_SCC.loc[dfmelted_SCC.stat=='mean'].loss.tolist() 
            manzanas_scc = dfmelted_SCC.loc[dfmelted_SCC.stat=='mean'].cod_secc.tolist()
            
            cod_sccdef = []
            for scc in manzanas_scc:
                cod_sccdef.append(str(scc[1:]))
            df_losses_scc = pd.DataFrame({'pae_scc_cop':aggrisk_SCC,'cod_secc':cod_sccdef})
            
            df_valex_scc = pd.DataFrame({'valex':valex_scc,'index':cod_scc_valex})
            dframe_codscc = pd.DataFrame({'cod_secc':cod_sccdef,'index':range(1,len(cod_sccdef)+1)})
            
            df_prom_scc = pd.merge(df_valex_scc, dframe_codscc, on='index', how='left') 
            grouped_df_scc = df_prom_scc.groupby('cod_secc')['valex'].sum().reset_index()
            
            df_expotax_scc = pd.merge(df_losses_scc, grouped_df_scc, on='cod_secc', how='left') 
            df_expotax_scc['pae_scc_prc'] = (df_expotax_scc.pae_scc_cop/df_expotax_scc.valex)*1000
            
            df_losses_prc_scc = pd.merge(df_losses_scc, grouped_df_scc, on='cod_secc', how='left') 
            df_losses_prc_scc['pae_scc_prc'] = (df_losses_prc_scc.pae_scc_cop/df_losses_prc_scc.valex)*1000
            
            mapdata_scc_PAE = seccion_shp.merge(df_losses_prc_scc, left_on='COD_SECC', right_on='cod_secc', how='left')

            PAE_mill = None
            df_resultados = None
            Pr50_Val = None
            
    # =========================================================================
    # DESARROLLAR CASO 2
    # =========================================================================
    
    if Ver_Folder_csv is not None and Ver_Folder_ME is not None and Ver_Folder_SP is not None:
    # Cuando en la carpeta estan los resultados de riesgo en csv por seccion,
    # manzana y taxonomia, junto con las carpetas del modelo y los shapes.
        print('entra')
        
                
    return df_EBR, valexpuesto,aggsts_loss,PE_mill,PAE_mill,df_resultados,Pr50_Val,CP_Name, COD_mun, df_expotax,taxo_description, mapdata_mnz_PAE, mapdata_scc_PAE, manzana_shp, seccion_shp, area_shp, calculation_mode, Modelo_Expo2


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

#%% Crear Tabla PAE taxonomia 8 partes o menos

def PaeTaxo_8menos(df_expotax,taxo_description,cnt_container,description_list,PRD_Description,taxo_list,PRD_Taxonomia,valexCop_list,PRD_ValexCOP,valexPrc_list,PRD_ValexPRC,PaeCop_list,PRD_PaeCOP,PaePrc_list,PRD_PaePRC,PaePrcM_list,PRD_PaePRCM,PRD_boton,Change_To_PAE):
    # Aqui entra cuando el municipio tiene 8 o menos de 8 taxonomias 
    
    if len(df_expotax) < len(description_list):
        description_list = description_list[0:len(df_expotax)]
        
    
    # Crear mas variables si la descripcion del municipio es muy larga
    description_list_2 = []
    suma_indx = []
    for index,txt in enumerate(description_list):
        parte = taxo_description[index].split(' ') 
        suma_indx.append(len(parte))
        if len(parte) >= 5:
            description_list_2.append("Description2_"+str(index+1))
            PRD_Description["Description2_"+str(index+1)] = None
    
    lista_combinada = description_list.copy()  # Copiamos la primera lista para evitar modificarla directamente
    lista_combinada.extend(description_list_2)
    
    # Espacios que debe haber entre cada dato
    sumydef = []
    for index in range(len(suma_indx)-1):
        if suma_indx[index] >=5 and suma_indx[index+1] >=5:
            sumydef.append(0.065)
        if suma_indx[index] >=5 and suma_indx[index+1] <5:
            sumydef.append(0.065)
        if suma_indx[index] <5 and suma_indx[index+1] <5:
            sumydef.append(0.071)
        if suma_indx[index] <5 and suma_indx[index+1] >=5:
            sumydef.append(0.065)
    sumydef.append(0.065)
    
    # ---- Tabla taxonomia ------------------------------------------------
    rlx = 0.281
    rly = 0.393
    # ---------------------------------------------------------------------
    
    suma = 0
    for index in range(len(df_expotax)):
        parte = taxo_description[index].split(' ')
        if len(parte) >= 5:
            # Si la descripcion tiene mas o 5 partes, entonces:
            # -------- Descripcion tipologia ------------------------------
            if PRD_Description[description_list[index]] is None:
                texto_description = parte[0]+' '+parte[1]+' '+parte[2]+' '+parte[3]
                PRD_Description[description_list[index]] = tk.Label(cnt_container, text=texto_description, font=("Abadi MT", 10), bg='#C6CFD4', fg='#000000')
                PRD_Description[description_list[index]].place(relx=rlx, rely=rly+suma, anchor=tk.CENTER)
            
            texto_description2 = []
            sumaprt = ''
            for index2 in range(4,len(parte)):
                sumaprt = sumaprt + ' ' + parte[index2]
                texto_description2.append(sumaprt)
            
            if PRD_Description["Description2_"+str(index+1)] is None:
                PRD_Description["Description2_"+str(index+1)] = tk.Label(cnt_container, text=texto_description2[-1], font=("Abadi MT", 10), bg='#C6CFD4', fg='#000000')
                PRD_Description["Description2_"+str(index+1)].place(relx=rlx, rely=rly+suma+0.02, anchor=tk.CENTER)
                
            # -------- Tipologia ------------------------------------------
            if PRD_Taxonomia[taxo_list[index]] is None:
                texto_tipologia = df_expotax.taxonomy[index]
                PRD_Taxonomia[taxo_list[index]] = tk.Label(cnt_container, text=texto_tipologia, font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_Taxonomia[taxo_list[index]].place(relx=rlx+0.17, rely=rly+suma, anchor=tk.CENTER)
                
            # -------- Valor expuesto en COP ----------------------------------
            if PRD_ValexCOP[valexCop_list[index]] is None:
                valex_Cop = np.around(df_expotax.valex[index],3)
                PRD_ValexCOP[valexCop_list[index]] = tk.Label(cnt_container, text=str(valex_Cop), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_ValexCOP[valexCop_list[index]].place(relx=rlx+0.29, rely=rly+suma, anchor=tk.CENTER)
            
            # -------- Valor expuesto en % ----------------------------------
            if PRD_ValexPRC[valexPrc_list[index]] is None:
                valex_Prc = np.around((df_expotax.valex[index]/np.sum(df_expotax.valex))*100,3)
                PRD_ValexPRC[valexPrc_list[index]] = tk.Label(cnt_container, text=str(valex_Prc), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_ValexPRC[valexPrc_list[index]].place(relx=rlx+0.38, rely=rly+suma, anchor=tk.CENTER)
            
            # -------- Perdida anual esperada en COP --------------------------
            if PRD_PaeCOP[PaeCop_list[index]] is None:
                valex_Cop = np.around(df_expotax.loss[index],3)
                PRD_PaeCOP[PaeCop_list[index]] = tk.Label(cnt_container, text=str(valex_Cop), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_PaeCOP[PaeCop_list[index]].place(relx=rlx+0.47, rely=rly+suma, anchor=tk.CENTER)
                
            # -------- Perdida anual esperada en % ----------------------------
            if PRD_PaePRC[PaePrc_list[index]] is None:
                valex_Prc = np.around((df_expotax.loss[index]/df_expotax.valex[index])*100,3)
                PRD_PaePRC[PaePrc_list[index]] = tk.Label(cnt_container, text=str(valex_Prc), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_PaePRC[PaePrc_list[index]].place(relx=rlx+0.556, rely=rly+suma, anchor=tk.CENTER)
                
            # -------- Perdida anual esperada en %. ---------------------------
            if PRD_PaePRCM[PaePrcM_list[index]] is None:
                valex_Pmll = np.around((df_expotax.loss[index]/df_expotax.valex[index])*1000,3)
                PRD_PaePRCM[PaePrcM_list[index]] = tk.Label(cnt_container, text=str(valex_Pmll), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_PaePRCM[PaePrcM_list[index]].place(relx=rlx+0.615, rely=rly+suma, anchor=tk.CENTER)
            
            suma = suma + sumydef[index]
            
        else:
            # -------- Descripcion tipologia ------------------------------         
            if PRD_Description[description_list[index]] is None:
                PRD_Description[description_list[index]] = tk.Label(cnt_container, text=taxo_description[index], font=("Abadi MT", 10), bg='#C6CFD4', fg='#000000')
                PRD_Description[description_list[index]].place(relx=rlx, rely=rly+suma, anchor=tk.CENTER)
            # -------- Tipologia ------------------------------------------
            if PRD_Taxonomia[taxo_list[index]] is None:
                texto_tipologia = df_expotax.taxonomy[index]
                PRD_Taxonomia[taxo_list[index]] = tk.Label(cnt_container, text=texto_tipologia, font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_Taxonomia[taxo_list[index]].place(relx=rlx+0.17, rely=rly+suma, anchor=tk.CENTER)
            # -------- Valor expuesto en COP ----------------------------------
            if PRD_ValexCOP[valexCop_list[index]] is None:
                valex_Cop = np.around(df_expotax.valex[index],3)
                PRD_ValexCOP[valexCop_list[index]] = tk.Label(cnt_container, text=str(valex_Cop), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_ValexCOP[valexCop_list[index]].place(relx=rlx+0.29, rely=rly+suma, anchor=tk.CENTER)
            # -------- Valor expuesto en % ----------------------------------
            if PRD_ValexPRC[valexPrc_list[index]] is None:
                valex_Prc = np.around((df_expotax.valex[index]/np.sum(df_expotax.valex))*100,3)
                PRD_ValexPRC[valexPrc_list[index]] = tk.Label(cnt_container, text=str(valex_Prc), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_ValexPRC[valexPrc_list[index]].place(relx=rlx+0.38, rely=rly+suma, anchor=tk.CENTER)
            # -------- Perdida anual esperada en COP --------------------------
            if PRD_PaeCOP[PaeCop_list[index]] is None:
                valex_Cop = np.around(df_expotax.loss[index],3)
                PRD_PaeCOP[PaeCop_list[index]] = tk.Label(cnt_container, text=str(valex_Cop), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_PaeCOP[PaeCop_list[index]].place(relx=rlx+0.47, rely=rly+suma, anchor=tk.CENTER)                    
            # -------- Perdida anual esperada en % ----------------------------
            if PRD_PaePRC[PaePrc_list[index]] is None:
                valex_Prc = np.around((df_expotax.loss[index]/df_expotax.valex[index])*100,3)
                PRD_PaePRC[PaePrc_list[index]] = tk.Label(cnt_container, text=str(valex_Prc), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_PaePRC[PaePrc_list[index]].place(relx=rlx+0.556, rely=rly+suma, anchor=tk.CENTER)
            # -------- Perdida anual esperada en %. ---------------------------
            if PRD_PaePRCM[PaePrcM_list[index]] is None:
                valex_Pmll = np.around((df_expotax.loss[index]/df_expotax.valex[index])*1000,3)
                PRD_PaePRCM[PaePrcM_list[index]] = tk.Label(cnt_container, text=str(valex_Pmll), font=("Abadi MT", 11), bg='#C6CFD4', fg='#000000')
                PRD_PaePRCM[PaePrcM_list[index]].place(relx=rlx+0.615, rely=rly+suma, anchor=tk.CENTER)
            
            suma = suma + sumydef[index]
    
    return lista_combinada
        
#%% Descripcion de la taxonomia
def descriptiontaxo(taxonomy_list):
    taxo_description = []
    for txn in taxonomy_list:
        parte = txn.split('/')
        if parte[0] == 'VG':
            if parte[1] == 'CE':
                if parte[2] == 'DU':
                    taxo_description.append('Cerchas de material vegetal (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Cerchas de material vegetal (no ingenieril)')
                else:
                    taxo_description.append('Cerchas de material vegetal (NI)')
        elif parte[0] == 'AC':
            if parte[1] == 'CE':
                if parte[2] == 'DU':
                    taxo_description.append('Cerchas de acero (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Cerchas de acero (no ingenieril)')
                else:
                    taxo_description.append('Cerchas de acero (NI)')
            if parte[1] == 'MD':
                if parte[2] == 'DU':
                    taxo_description.append('Muros delgados en acero (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Muros delgados en acero (no ingenieril)')
                else:
                    taxo_description.append('Muros delgados en acero(NI)')
            elif parte[1] == 'PRM':
                if parte[2] == 'DU':
                    taxo_description.append('Pórticos resistentes a momento de acero (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Pórticos resistentes a momento de acero (no ingenieril)')
                else:
                    taxo_description.append('Pórticos resistentes a momento de acero (NI)')
            elif parte[1] == 'PA':
                if parte[2] == 'DU':
                    taxo_description.append('Pórticos arriostrados de acero (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Pórticos arriostrados de acero (no ingenieril)')
                else:
                    taxo_description.append('Pórticos arriostrados de acero (NI)')
            elif parte[1] == 'PI':
                if parte[2] == 'DU':
                    taxo_description.append('Péndulo invertido de acero (ingenieril)')
                else:
                    taxo_description.append('Péndulo invertido de acero (no ingenieril)')
        elif parte[0] == 'AD':
            taxo_description.append('Adobe no-reforzado')
        elif parte[0] == 'BQ':
            taxo_description.append('Bahareque no-reforzado')
        elif parte[0] == 'MZ':
            if parte[1] == 'OT':
                taxo_description.append('Madera-zinc')
            else:
                taxo_description.append('Madera-zinc no-reforzada')
        elif parte[0] == 'MX':
            taxo_description.append('Mixto (No ingenieril)')
        elif parte[0] == 'CR':
            if parte[1] == 'MR':
                if parte[2] == 'DU':
                    taxo_description.append('Muros de concreto reforzado (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Muros de concreto reforzado (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Muros de concreto reforzado (NI)')
            elif parte[1] == 'MD':
                if parte[2] == 'DU':
                    taxo_description.append('Muros delgados de concreto reforzado (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Muros delgados de concreto reforzado (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Muros delgados de concreto reforzado (NI)')
            elif parte[1] == 'PRM':
                if parte[2] == 'DU':
                    taxo_description.append('Pórticos resistentes a momento de concreto reforzado (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Pórticos resistentes a momento de concreto reforzado (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Pórticos resistentes a momento de concreto reforzado (NI)')
            elif parte[1] == 'PRMM':
                if parte[2] == 'DU':
                    taxo_description.append('Pórticos resistentes a momento de concreto reforzado con relleno en mampostería (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Pórticos resistentes a momento de concreto reforzado con relleno en mampostería (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Pórticos resistentes a momento de concreto reforzado con relleno en mampostería (NI)')
            elif parte[1] == 'PA':
                if parte[2] == 'DU':
                    taxo_description.append('Pórticos arriostrados de concreto reforzado (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Pórticos arriostrados de concreto reforzado (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Pórticos arriostrados de concreto reforzado (NI)')
            elif parte[1] == 'LC':
                taxo_description.append('Losa-Columna de concreto reforzado (ingenieril)')
            elif parte[1] == 'SC':
                if parte[2] == 'DU':
                    taxo_description.append('Sistema combinado (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Sistema combinado (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Sistema combinado (NI)')
        elif parte[0] == 'MA':
            if parte[1] == 'MR':
                if parte[2] == 'DU':
                    taxo_description.append('Muros de mampostería reforzada (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Muros de mampostería reforzada (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Muros de mampostería reforzada (NI)')
            elif parte[1] == 'PRM':
                if parte[2] == 'DU':
                    taxo_description.append('Pórticos resistentes a momento de mampostería reforzada (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Pórticos resistentes a momento de mampostería reforzada (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Pórticos resistentes a momento de mampostería reforzada (NI)')
            elif parte[1] == 'MNR':
                taxo_description.append('Mampostería no-reforzada')
            elif parte[1] == 'MPC':
                taxo_description.append('Mampostería parcialmente confinada')
            elif parte[1] == 'MC':
                if parte[2] == 'DU':
                    taxo_description.append('Mampostería confinada (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Mampostería confinada (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Mampostería confinada (NI)')
        elif parte[0] == 'MC':
            if parte[1] == 'MR':
                if parte[2] == 'DU':
                    taxo_description.append('Muros de mampostería en bloque de concreto reforzada (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Muros de mampostería en bloque de concreto reforzada (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Muros de mampostería en bloque de concreto reforzada (NI)')
            elif parte[1] == 'PRM':
                if parte[2] == 'DU':
                    taxo_description.append('Pórticos resistentes a momento de mampostería en bloque de concreto reforzada (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Pórticos resistentes a momento de mampostería en bloque de concreto reforzada (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Pórticos resistentes a momento de mampostería en bloque de concreto reforzada (NI)')
            elif parte[1] == 'MNR':
                taxo_description.append('Mampostería en bloque de concreto no-reforzada')
            elif parte[1] == 'MPC':
                taxo_description.append('Mampostería en bloque de concreto parcialmente confinada')
            elif parte[1] == 'MC':
                if parte[2] == 'DU':
                    taxo_description.append('Mampostería en bloque de concreto confinada (ingenieril)')
                elif parte[2] == 'ND':
                    taxo_description.append('Mampostería en bloque de concreto confinada (no ingenieril)')
                elif parte[2] == 'NI':
                    taxo_description.append('Mampostería en bloque de concreto confinada (NI)')
        elif parte[0]=='MD':
            taxo_description.append('Madera no-reforzada')
        elif parte[0] == 'PMC':
            taxo_description.append('Prefabricado (madera-concreto) no-reforzado')
        elif parte[0] == 'TA':
            taxo_description.append('Tapia pisada no-reforzada')
        elif parte[0] == 'MP':
            taxo_description.append('Mampostería de piedra no-reforzada')
        elif parte[0] == 'PMF':
            taxo_description.append('Prefabricado: metálico-fibrocemento')
        elif parte[0] == 'NI':
            taxo_description.append('Taxonomía no identificada')
        
    return taxo_description
