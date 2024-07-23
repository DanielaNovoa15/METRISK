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

#%% ====== SHOW CALIBRATION ELEMENTS ==========================================
def Show_GEN_Elements(MAP_title,MAP_text,MAP_boton,cnt_container,upcnt_color,Select_Folder_MAP,Ventana_Info_MAP,Function_Maps,resultado_label_MAP):
    
    # ---- Titulo de la pestaña:
    if MAP_title["tlt_tlt_GEN"] is None:
        MAP_title["tlt_tlt_GEN"] = wnfun_lib.Label_Image('/Generador_title.png', 1100, 65, cnt_container,"white",0.495,0.13)

    #---- Descripcion introductoria:
    if MAP_text["txt_cnt_GEN"] is None:
        MAP_text["txt_cnt_GEN"] = wnfun_lib.Label_Image('/Generador_text.png', 532, 404, cnt_container,"white",0.30  ,0.55)
        
    # ---- Seleccionar carpeta:
    if MAP_boton["btn_slc_GEN"] is None:
        MAP_boton["btn_slc_GEN"] = wnfun_lib.Button_Image('/Select_FolderV2.png', 278, 65, cnt_container,"white",0.78,0.5,Select_Folder_MAP) 
    
    # ---- Informacion:
    if MAP_boton["btn_inf_GEN"] is None:
        MAP_boton["btn_inf_GEN"] = wnfun_lib.Button_Image('/Info.png', 27, 27, cnt_container,"white",0.885,0.468,Ventana_Info_MAP)
        
    # ---- Generar:
    if MAP_boton["btn_clb_GEN"] is None:
        MAP_boton["btn_clb_GEN"] = wnfun_lib.Button_Image_lambda('/Generate_Results.png', 252, 55, cnt_container,"white",0.78,0.58,Function_Maps,resultado_label_MAP) 
    
    resultado_label_MAP = tk.Label(cnt_container, text="", fg="red")
    resultado_label_MAP.pack()
    resultado_label_MAP.pack_forget()

#%% ====== HIDE CALIBRATION ELEMENTS ==========================================
def Hide_GEN_Elements(title_MAP,MAP_title,text_MAP,MAP_text,boton_MAP,MAP_boton):
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
def Function_GEN_Elements(carpeta_seleccionada_DNO):
    
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
        elif len(rutas_hdf5) < 6:
            warning = "En la carpeta no estan todos los archivos .hdf5 que se requieren"
            tk.messagebox.showinfo("ERROR", warning)
        elif len(rutas_hdf5) > 6:
            warning = "Hay más de seis archivos .hdf5 en la carpeta."
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
                    elif oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                        CalcMode_PRD_scc = "Probabilistico"
                        PRD_pbl_scc = ruta
                    elif oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                        CalcMode_PRD_txn = "Probabilistico"
                        PRD_pbl_txn = ruta
                # Si el archivo es de daños - probabilistico
                elif oqparam_dict['calculation_mode'] == 'event_based_damage':
                    # ¿Cuál es el agregado del archivo?
                    if oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                        CalcMode_DNO_mnz = "Probabilistico"
                        DNO_pbl_mnz = ruta
                    elif oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                        CalcMode_DNO_scc = "Probabilistico"
                        DNO_pbl_scc = ruta
                    elif oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                        CalcMode_DNO_txn = "Probabilistico"
                        DNO_pbl_txn = ruta
                
                # Si el arcjhivo es de perdidas - deterministicos
                elif oqparam_dict['calculation_mode'] == 'scenario_risk': 
                    # ¿Cuál es el agregado del archivo?
                    if oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                        CalcMode_PRD_mnz = "Deterministico"
                        PRD_det_mnz = ruta
                    elif oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                        CalcMode_PRD_scc = "Deterministico"
                        PRD_det_scc = ruta
                    elif oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                        CalcMode_PRD_txn = "Deterministico"
                        PRD_det_txn = ruta
                # Si el arcjhivo es de daños - deterministicos
                elif oqparam_dict['calculation_mode'] == 'scenario_damage':  
                    # ¿Cuál es el agregado del archivo?
                    if oqparam_dict['aggregate_by'] == [["cod_mnz"]]:
                        CalcMode_DNO_mnz = "Deterministico"
                        DNO_det_mnz = ruta
                    elif oqparam_dict['aggregate_by'] == [["cod_secc"]]:
                        CalcMode_DNO_scc = "Deterministico"
                        DNO_det_scc = ruta
                    elif oqparam_dict['aggregate_by'] == [["taxonomy"]]:
                        CalcMode_DNO_txn = "Deterministico"
                        DNO_det_txn = ruta
                    
                else:
                    warning = "El/los archivo no cumple con los criterios."
                    tk.messagebox.showinfo("ERROR", warning)
            

        if CalcMode_PRD_mnz == "Probabilistico" and CalcMode_PRD_scc == "Probabilistico" and CalcMode_PRD_txn == "Probabilistico" and CalcMode_DNO_mnz == "Probabilistico"  and CalcMode_DNO_scc == "Probabilistico" and CalcMode_DNO_txn == "Probabilistico":
            calculation_mode = "Probabilistico"
        elif CalcMode_PRD_mnz == "Deterministico" and CalcMode_PRD_scc == "Deterministico" and CalcMode_PRD_txn == "Deterministico" and CalcMode_DNO_mnz == "Deterministico" and CalcMode_DNO_scc == "Deterministico" and CalcMode_DNO_txn == "Deterministico":
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
            
            
            """ ---------------------------------------------------------------------------
              Figura 1 -- Area construida de la manzana para la taxonomia representativa
            --------------------------------------------------------------------------- """ 

            # Obtener taxonomia representativa
            Expo_groupby_txn = Modelo_Expo2.groupby('tipologia')['area_cons'] 
            Expo_groupby_mnz = Modelo_Expo2.groupby('cod_mnz')['area_cons'].sum()

            Area_constr_txn = Expo_groupby_txn.sum()
            df_area = pd.DataFrame({'tipologia':Area_constr_txn.index,'area':Area_constr_txn})
            Txn_Rep = df_area.loc[df_area.area == df_area.area.max()].values[0][0]          
            # Obtener el % de area construida de las manzanas con esa taxonomia representativa
            df_mnz_txn = Modelo_Expo2.loc[Modelo_Expo2.tipologia == Txn_Rep]
            area_constr_total = df_mnz_txn.area_cons.sum()
            df_mnz_groupbymnz = df_mnz_txn.groupby('cod_mnz')['area_cons'].sum()
            df_final = pd.DataFrame({'cod_mnz2':df_mnz_groupbymnz.index,'area':df_mnz_groupbymnz})
            df_final = df_final.merge(Expo_groupby_mnz, left_on='cod_mnz2', right_on='cod_mnz', how='left')
            df_final['area_cons'] = (df_final.area/df_final.area_cons)*100 
            
            # Generar el map_data y el csv limite                  
            mapdata_AreaCons = manzana_shp.merge(df_final, left_on='COD_DANE', right_on='cod_mnz2', how='left')
            
            # -----------------------------------------------------------------
            # Geopandas para definir los limites del mapa
            mapdata_Limits = df_final.merge(manzana_shp, left_on='cod_mnz2', right_on='COD_DANE', how='left')
            # -----------------------------------------------------------------
            
            
            """ ---------------------------------------------------------------------------
                Figuras 2 -- Area construida para edificaciones segun el rango de piso
            --------------------------------------------------------------------------- """ 
            
            # Numero de pisos segun modedo de exposicion
            Npisos = Modelo_Expo2.groupby('n_piso')['area_cons'].sum()
            lista_pisos_agrupados, lista_nombre_pisos = agrupar_pisos(Npisos.index)
            
            valores_unidos = unir_valores(lista_pisos_agrupados)

            mapdata_Pisos,title_npiso = [],[]
            for index in range(len(lista_pisos_agrupados)): 
                # Numero de piso
                piso_aggr = lista_pisos_agrupados[index]
                if len(piso_aggr) == 1:
                    # agrupar por numero de piso
                    groupby_npiso = Modelo_Expo2.loc[Modelo_Expo2['n_piso']==piso_aggr[0]]
                else:
                    groupby_npiso = filtrar_por_pisos(Modelo_Expo2, lista_pisos_agrupados[index])
                    
                # agrupar por manzana y obtener area construida total de la manzana
                groupby_codmnz = groupby_npiso.groupby('cod_mnz')['area_cons'].sum()
                area_constr_total = Modelo_Expo2.groupby('cod_mnz')['area_cons'].sum()
                df_final = pd.DataFrame({'cod_mnz2':groupby_codmnz.index,'area':groupby_codmnz})
                df_final = df_final.merge(area_constr_total, left_on='cod_mnz2', right_on='cod_mnz', how='left')
                df_final['area_cons2'] = (df_final.area/df_final.area_cons)*100
                # Generar el map_data
                mapdata_Pisos.append(manzana_shp.merge(df_final, left_on='COD_DANE', right_on='cod_mnz2', how='left'))
                
                title_npiso.append(lista_nombre_pisos[index])
                
            """ ---------------------------------------------------------------------------
                       Anexo 1 --MANZANA-- Pérdida anual promedio al millar
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(PRD_pbl_mnz, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]           # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()]                                   # ID del agregado
                loss = archivo["aggrisk"]["loss"][()]                                       # perdidas segun el aggregate ID
                valex = archivo["assetcol"]["array"]["value-structural"][()]                # Valor estructural
                cod_mnz_valex = archivo["assetcol"]["array"]["cod_mnz"][()]                 # Valor estructural por manzana

            # Dataframe perdidas por aggregate ID
            df_group = pd.DataFrame({'agg_id':agg_id, 'loss':loss})                         # Dataframe perdidas por aggid
            # Agrupa por agg_id
            grp_aggid = df_group.groupby('agg_id')['loss']                                  # Agrupa las perdidas por aggid
            # Calcular percentiles
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])           # Calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True)                                    # genera un indice, agg_id se vuelve en columna
            # Obtener datos por municipio
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']]             # genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True)                               # dataframe de perdidas por manzana o por manzana + taxonomia
            # Peridas por municipio
            stats_agg_mnp.reset_index(level=0, inplace=True)                                # resetea el indice municipio
            # Perdidas por manzana
            stats_agg.reset_index(level=0, inplace=True)                                    # resetea el indice agregado

            # Obtener estadisticas necesarias de perdidas
            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz.sort_values(by='agg_id', inplace=True)
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])
            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)]
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)
            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()

            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses = pd.DataFrame({'loss':aggrisk_mnz,'cod_mnz':cod_mnzdef})

            df_valex = pd.DataFrame({'valex':valex,'index':cod_mnz_valex})
            df_codmnz = pd.DataFrame({'cod_mnz':cod_mnzdef,'index':range(1,len(cod_mnzdef)+1)})
            df_prom = pd.merge(df_valex, df_codmnz, on='index', how='left') 
            grouped_df = df_prom.groupby('cod_mnz')['valex'].sum().reset_index()
                
            df_expotax = pd.merge(df_losses, grouped_df, on='cod_mnz', how='left') 
            df_losses2 = df_losses
            df_losses['aal_mnz_mllr'] = (df_expotax.loss)*1000
            
            # -----------------------------------------------------------------
            mapdata_allmnzmll = manzana_shp.merge(df_losses, left_on='COD_DANE', right_on='cod_mnz', how='left')
            # -----------------------------------------------------------------
            
            df_losses2['aal_mnz_cop'] = (df_expotax.loss)*0.001
            
            # -----------------------------------------------------------------
            mapdata_allmnzcop = manzana_shp.merge(df_losses2, left_on='COD_DANE', right_on='cod_mnz', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
                  Anexo 2 --MANZANA-- Fallecidos anuales promedio por 100m habitantes
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_mnz, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8')) # Lista de parametros de OpenQuake
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:] # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()] 

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
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

            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()

            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses = pd.DataFrame({'cod_mnz':cod_mnzdef,'aad_mnz_fallecidos_hab':aggrisk_mnz})

            Expo_groupby_mnz = Modelo_Expo.groupby('cod_mnz')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_mnz':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_mnz':df_losses.cod_mnz})

            index_mal = pruebadf1.cod_mnz[~pruebadf1.cod_mnz.isin(pruebadf2.cod_mnz)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_mnz[~pruebadf2.cod_mnz.isin(pruebadf1.cod_mnz)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_mnz == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)

            # -----------------------------------------------------------------

            df_losses['aad_mnz_fallecidos_100m_hab'] = df_losses.aad_mnz_fallecidos_hab*100000/df_losses.poblacion
            
            # -----------------------------------------------------------------
            mapdata_fallmnz = manzana_shp.merge(df_losses, left_on='COD_DANE', right_on='cod_mnz', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
                 Anexo 3 --MANZANA-- Heridos anuales promedio por cada 100m habitantes
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_mnz, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]           # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()]

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
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

            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses = pd.DataFrame({'cod_mnz':cod_mnzdef,'aai_mnz_heridos_hab':aggrisk_mnz})

            Expo_groupby_mnz = Modelo_Expo.groupby('cod_mnz')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_mnz':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_mnz':df_losses.cod_mnz})

            index_mal = pruebadf1.cod_mnz[~pruebadf1.cod_mnz.isin(pruebadf2.cod_mnz)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_mnz[~pruebadf2.cod_mnz.isin(pruebadf1.cod_mnz)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_mnz == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)


            df_losses['aai_mnz_heridos_100m_hab'] = df_losses.aai_mnz_heridos_hab*100000/df_losses.poblacion
            
            # -----------------------------------------------------------------
            mapdata_injuredmnz = manzana_shp.merge(df_losses, left_on='COD_DANE', right_on='cod_mnz', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
            Anexo 4 --MANZANA-- Numero anual promedio de ocupantes en edificios colapsados
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_mnz, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:] # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()]

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
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

            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses = pd.DataFrame({'cod_mnz':cod_mnzdef,'aac_mnz_colapso_hab':aggrisk_mnz})

            Expo_groupby_mnz = Modelo_Expo.groupby('cod_mnz')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_mnz':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_mnz':df_losses.cod_mnz})

            index_mal = pruebadf1.cod_mnz[~pruebadf1.cod_mnz.isin(pruebadf2.cod_mnz)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_mnz[~pruebadf2.cod_mnz.isin(pruebadf1.cod_mnz)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_mnz == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)

            # -----------------------------------------------------------------
            mapdata_homelessmnz = manzana_shp.merge(df_losses, left_on='COD_DANE', right_on='cod_mnz', how='left')
            # -----------------------------------------------------------------
            
            
            """ ---------------------------------------------------------------------------
             Anexo 5 --MANZANA-- No. anual promedio de edificios colapsados, No. edificios
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_mnz, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]           # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()]

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
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

            aggrisk_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss.tolist()
            manzanas_mnz = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            cod_mnzdef = []
            for mnz in manzanas_mnz:
                cod_mnzdef.append(str(mnz[1:]))
            df_losses = pd.DataFrame({'cod_mnz':cod_mnzdef,'aac_mnz_colapso_no_edis':aggrisk_mnz})

            Expo_groupby_mnz = Modelo_Expo.groupby('cod_mnz')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_mnz':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_mnz':df_losses.cod_mnz})

            index_mal = pruebadf1.cod_mnz[~pruebadf1.cod_mnz.isin(pruebadf2.cod_mnz)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_mnz[~pruebadf2.cod_mnz.isin(pruebadf1.cod_mnz)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_mnz == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)

            # -----------------------------------------------------------------
            mapdata_colapsedmnz = manzana_shp.merge(df_losses, left_on='COD_DANE', right_on='cod_mnz', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
                       Anexo 1 --SECCION-- Pérdida anual promedio al millar
            --------------------------------------------------------------------------- """
            
            with h5py.File(PRD_pbl_scc, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                secc_list_bytes = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:]         # Lista de secciones
                secc_list = [item.decode('utf-8') for item in secc_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()]                                   # ID del agregado
                loss = archivo["aggrisk"]["loss"][()]                                       # perdidas segun el aggregate ID
                valex = archivo["assetcol"]["array"]["value-structural"][()]                # Valor estructural
                cod_secc_valex = archivo["assetcol"]["array"]["cod_secc"][()]               # Valor estructural por seccion urbana

            # Dataframe perdidas por aggregate ID
            df_group = pd.DataFrame({'agg_id':agg_id, 'loss':loss})                         # Dataframe perdidas por aggid
            # Agrupa por agg_id
            grp_aggid = df_group.groupby('agg_id')['loss']                                  # Agrupa las perdidas por aggid
            # Calcular percentiles
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])           # Calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True)                                    # genera un indice, agg_id se vuelve en columna
            # Obtener datos por municipio
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']]             # genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True)                               # dataframe de perdidas por manzana o por manzana + taxonomia
            # Peridas por municipio
            stats_agg_mnp.reset_index(level=0, inplace=True)                                # resetea el indice municipio
            # Perdidas por manzana
            stats_agg.reset_index(level=0, inplace=True)                                    # resetea el indice agregado
            # Obtener estadisticas necesarias de perdidas
            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_scc = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            # Ordenar los datos por agg_id
            dfmelted_scc.sort_values(by='agg_id', inplace=True)
            # Generar una columna llamada stat que represente las estadisticas
            dfmelted_scc['stat'] = dfmelted_scc['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            # Eliminar la columna agg_id
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])
            # Añadir al dataframe una columna con el codigo correspondiente de la seccion
            dfmelted_scc['cod_secc'] = np.array(secc_list)[(dfmelted_scc['agg_id'] / 1).astype(int)]
            # eliminar la columna agg_id
            dfmelted_scc = dfmelted_scc.drop(columns=['agg_id'])
            # Resetear el index
            dfmelted_scc = dfmelted_scc.reset_index(drop=True)
            # Dataframe de secciones filtrado por los valores promedio de perdidas
            aggrisk_secc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].loss.tolist()
            secciones_secc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].cod_secc.tolist()

            # Lista definitiva de secciones
            cod_seccdef = []
            for secc in secciones_secc:
                cod_seccdef.append(str(secc[1:]))
            # Dataframe de perdidas promedio por seccion urbana
            df_losses = pd.DataFrame({'loss':aggrisk_secc,'cod_secc':cod_seccdef})
            # Dataframe de valor expuesto
            df_valex = pd.DataFrame({'valex':valex,'index':cod_secc_valex})
            df_codsecc = pd.DataFrame({'cod_secc':cod_seccdef,'index':range(1,len(cod_seccdef)+1)})
            df_prom = pd.merge(df_valex, df_codsecc, on='index', how='left') 
            grouped_df = df_prom.groupby('cod_secc')['valex'].sum().reset_index()
            # Dataframe perdidas promedio y valor expuesto por seccion urbana
            df_expotax = pd.merge(df_losses, grouped_df, on='cod_secc', how='left') 
            df_losses2 = df_losses
            # df_losses['loss2'] = (df_expotax.loss/df_expotax.valex)*1000
            df_losses['aal_secc_urb_mllr'] = (df_expotax.loss)*1000
            
            # -----------------------------------------------------------------
            mapdata_allsccmll = seccion_shp.merge(df_losses, left_on='COD_SECC', right_on='cod_secc', how='left')
            # -----------------------------------------------------------------
            
            df_losses2['aal_secc_urb_cop'] = (df_expotax.loss)*0.001
            
            # -----------------------------------------------------------------
            mapdata_allscccop = seccion_shp.merge(df_losses2, left_on='COD_SECC', right_on='cod_secc', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
                 Anexo 2 --SECCION-- Fallecidos anuales promedio por 100m habitantes
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_scc, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                secc_list_bytes = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:]         # Lista de secciones
                secc_list = [item.decode('utf-8') for item in secc_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()] 

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
            # .... Agrupar por fatalities .................................................
            grp_aggid = df_group.groupby('agg_id')['fatalities'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_scc = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_scc.sort_values(by='agg_id', inplace=True)
            dfmelted_scc['stat'] = dfmelted_scc['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])
            dfmelted_scc['cod_secc'] = np.array(secc_list)[(dfmelted_scc['agg_id'] / 1).astype(int)]
            dfmelted_scc = dfmelted_scc.drop(columns=['agg_id'])
            dfmelted_scc = dfmelted_scc.reset_index(drop=True)

            aggrisk_scc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].loss.tolist()
            secciones_secc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].cod_secc.tolist()

            # Lista definitiva de secciones
            cod_seccdef = []
            for secc in secciones_secc:
                cod_seccdef.append(str(secc[1:]))
                
            df_losses = pd.DataFrame({'cod_secc':cod_seccdef,'aad_secc_urb_fallecidos_hab':aggrisk_scc})

            # Anadir al modelo el codigo de la seccion 
            cod_secc_Modelo = []
            for mnz in Modelo_Expo.cod_mnz:
                cod_secc_Modelo.append(mnz[0:-2])
                
            Modelo_Expo["cod_secc"] = cod_secc_Modelo

            Expo_groupby_mnz = Modelo_Expo.groupby('cod_secc')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_secc':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_secc':df_losses.cod_secc})

            index_mal = pruebadf1.cod_secc[~pruebadf1.cod_secc.isin(pruebadf2.cod_secc)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_secc[~pruebadf2.cod_secc.isin(pruebadf1.cod_secc)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_secc == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)


            df_losses['aad_secc_urb_fallecidos_100m_hab'] = df_losses.aad_secc_urb_fallecidos_hab*100000/df_losses.poblacion

            # -----------------------------------------------------------------
            mapdata_fallscc = seccion_shp.merge(df_losses, left_on='COD_SECC', right_on='cod_secc', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
                 Anexo 3 --SECCION-- Heridos anuales promedio por cada 100m habitantes
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_scc, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                secc_list_bytes = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:]         # Lista de secciones
                secc_list = [item.decode('utf-8') for item in secc_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()]

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['injured'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_scc = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_scc.sort_values(by='agg_id', inplace=True)
            dfmelted_scc['stat'] = dfmelted_scc['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_scc['cod_secc'] = np.array(secc_list)[(dfmelted_scc['agg_id'] / 1).astype(int)]
            dfmelted_scc = dfmelted_scc.drop(columns=['agg_id'])
            dfmelted_scc = dfmelted_scc.reset_index(drop=True)

            aggrisk_scc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].loss.tolist()
            secciones_secc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].cod_secc.tolist()

            # Lista definitiva de secciones
            cod_seccdef = []
            for secc in secciones_secc:
                cod_seccdef.append(str(secc[1:]))
                
            df_losses = pd.DataFrame({'cod_secc':cod_seccdef,'aai_secc_urb_heridos_hab':aggrisk_scc})

            # Anadir al modelo el codigo de la seccion 
            cod_secc_Modelo = []
            for mnz in Modelo_Expo.cod_mnz:
                cod_secc_Modelo.append(mnz[0:-2])
                
            Modelo_Expo["cod_secc"] = cod_secc_Modelo

            Expo_groupby_mnz = Modelo_Expo.groupby('cod_secc')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_secc':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_secc':df_losses.cod_secc})

            index_mal = pruebadf1.cod_secc[~pruebadf1.cod_secc.isin(pruebadf2.cod_secc)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_secc[~pruebadf2.cod_secc.isin(pruebadf1.cod_secc)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_secc == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)

            df_losses['aai_secc_urb_heridos_100m_hab'] = df_losses.aai_secc_urb_heridos_hab*100000/df_losses.poblacion

            # -----------------------------------------------------------------
            mapdata_injuredscc = seccion_shp.merge(df_losses, left_on='COD_SECC', right_on='cod_secc', how='left')
            # -----------------------------------------------------------------
            
            
            """ ---------------------------------------------------------------------------
            Anexo 4 --SECCION-- Numero anual promedio de ocupantes en edificios colapsados
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_scc, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                secc_list_bytes = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:]         # Lista de secciones
                secc_list = [item.decode('utf-8') for item in secc_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()]

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['homeless'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_scc = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_scc.sort_values(by='agg_id', inplace=True)
            dfmelted_scc['stat'] = dfmelted_scc['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_scc['cod_secc'] = np.array(secc_list)[(dfmelted_scc['agg_id'] / 1).astype(int)]
            dfmelted_scc = dfmelted_scc.drop(columns=['agg_id'])
            dfmelted_scc = dfmelted_scc.reset_index(drop=True)

            aggrisk_scc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].loss.tolist()
            secciones_secc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].cod_secc.tolist()

            # Lista definitiva de secciones
            cod_seccdef = []
            for secc in secciones_secc:
                cod_seccdef.append(str(secc[1:]))
                
            df_losses = pd.DataFrame({'cod_secc':cod_seccdef,'aac_secc_urb_colapso_hab':aggrisk_scc})

            # Anadir al modelo el codigo de la seccion 
            cod_secc_Modelo = []
            for mnz in Modelo_Expo.cod_mnz:
                cod_secc_Modelo.append(mnz[0:-2])
                
            Modelo_Expo["cod_secc"] = cod_secc_Modelo
            Expo_groupby_mnz = Modelo_Expo.groupby('cod_secc')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_secc':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_secc':df_losses.cod_secc})

            index_mal = pruebadf1.cod_secc[~pruebadf1.cod_secc.isin(pruebadf2.cod_secc)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_secc[~pruebadf2.cod_secc.isin(pruebadf1.cod_secc)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_secc == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)

            # -----------------------------------------------------------------
            mapdata_homelessscc = seccion_shp.merge(df_losses, left_on='COD_SECC', right_on='cod_secc', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
             Anexo 5 --SECCION-- No. anual promedio de edificios colapsados, No. edificios
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_scc, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))           # Lista de parametros de OpenQuake
                secc_list_bytes = archivo["assetcol"]["tagcol"]["cod_secc"][()][1:]         # Lista de secciones
                secc_list = [item.decode('utf-8') for item in secc_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()] 
                dmg4 = archivo["aggrisk"]["dmg_4"][()] 
                collapsed = archivo["aggrisk"]["collapsed"][()] 
                fatalities = archivo["aggrisk"]["fatalities"][()] 
                homeless = archivo["aggrisk"]["homeless"][()]
                injured = archivo["aggrisk"]["injured"][()]

            df_group = pd.DataFrame({'agg_id':agg_id, 'dmg4':dmg4, 'collapsed':collapsed,'fatalities':fatalities,'homeless':homeless,'injured':injured}) # dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['collapsed'] 
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])
            stats_agg.reset_index(level=0, inplace=True) 
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] 
            stats_agg.drop(stats_agg_mnp.index, inplace=True) 
            stats_agg_mnp.reset_index(level=0, inplace=True) 
            stats_agg.reset_index(level=0, inplace=True)

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_scc = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_scc.sort_values(by='agg_id', inplace=True)
            dfmelted_scc['stat'] = dfmelted_scc['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_scc['cod_secc'] = np.array(secc_list)[(dfmelted_scc['agg_id'] / 1).astype(int)]
            dfmelted_scc = dfmelted_scc.drop(columns=['agg_id'])
            dfmelted_scc = dfmelted_scc.reset_index(drop=True)

            aggrisk_scc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].loss.tolist()
            secciones_secc = dfmelted_scc.loc[dfmelted_scc.stat=='mean'].cod_secc.tolist()

            # Lista definitiva de secciones
            cod_seccdef = []
            for secc in secciones_secc:
                cod_seccdef.append(str(secc[1:]))
                
            df_losses = pd.DataFrame({'cod_secc':cod_seccdef,'aac_secc_urb_colapso_no_edis':aggrisk_scc})

            # Anadir al modelo el codigo de la seccion 
            cod_secc_Modelo = []
            for mnz in Modelo_Expo.cod_mnz:
                cod_secc_Modelo.append(mnz[0:-2])
                
            Modelo_Expo["cod_secc"] = cod_secc_Modelo
            Expo_groupby_mnz = Modelo_Expo.groupby('cod_secc')['poblacion'].sum()

            # SI HAY ALGUN ERROR CON EL MODELO DE EXPOSICION
            pruebadf1 = pd.DataFrame({'cod_secc':Expo_groupby_mnz.index,'poblacion':Expo_groupby_mnz})
            pruebadf2 = pd.DataFrame({'cod_secc':df_losses.cod_secc})

            index_mal = pruebadf1.cod_secc[~pruebadf1.cod_secc.isin(pruebadf2.cod_secc)].dropna().tolist()
            if index_mal == []:
                if len(pruebadf1) == len(pruebadf2):
                    df_losses['poblacion'] = list(Expo_groupby_mnz)
                else:
                    # cuando el modelo de exposicion no tiene la seccion que los resultados si **raro**
                    index_mal = pruebadf2.cod_secc[~pruebadf2.cod_secc.isin(pruebadf1.cod_secc)].dropna().tolist()
                    df_losses.drop(np.where(df_losses.cod_secc == index_mal[0])[0][0], inplace=True)
                    df_losses['poblacion'] = list(pruebadf1.poblacion)
            else:
                # cuando el modelo de exposicion tiene secciones de mas
                pruebadf1.drop(index_mal, inplace=True)
                df_losses['poblacion'] = list(pruebadf1.poblacion)

            # -----------------------------------------------------------------
            mapdata_colapsedsecc = seccion_shp.merge(df_losses, left_on='COD_SECC', right_on='cod_secc', how='left')
            # -----------------------------------------------------------------
            
            """ ---------------------------------------------------------------------------
                   Resultados de daños -----MANZANA-- Tabla resumen/Mapas de dano
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(DNO_pbl_mnz, 'r') as archivo: 
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
            aggrisk = list(np.array(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg0))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg1))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg2))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg3))
            aggrisk.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg4))
            # dataframe de perdidas promedio por manzana
            dic_mnp = {'stat':dfmelted_txn_dmg0.stat,'cod_mnz':dfmelted_txn_dmg0.cod_mnz,'loss_dmg0':dfmelted_txn_dmg0.loss_dmg0,'loss_dmg1':dfmelted_txn_dmg1.loss_dmg1,'loss_dmg2':dfmelted_txn_dmg2.loss_dmg2,'loss_dmg3':dfmelted_txn_dmg3.loss_dmg3,'loss_dmg4':dfmelted_txn_dmg4.loss_dmg4}
            dfmelted_mnz = pd.DataFrame(dic_mnp)
            aggrisk_mnz = np.zeros((len(dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0),5))
            aggrisk_mnz[:,0] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0
            aggrisk_mnz[:,1] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg1
            aggrisk_mnz[:,2] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg2
            aggrisk_mnz[:,3] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg3
            aggrisk_mnz[:,4] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg4
            manzanas = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()

            cod_mnzdef = []
            for mnz in manzanas:
                cod_mnzdef.append(str(mnz[1:]))
                
            danio_extensivo,colapso = [], []
            for index in range(len(manzanas)):
                severo = (aggrisk_mnz[index,3]/np.sum(aggrisk_mnz[index,:]))*100
                danio_extensivo.append(severo)
                colaps = (aggrisk_mnz[index,4]/np.sum(aggrisk_mnz[index,:]))*100
                colapso.append(colaps)

            dic_def = {'dmg3':danio_extensivo,'dmg4':colapso,'cod_mnz':cod_mnzdef}
            df_losses_def = pd.DataFrame(dic_def)
            # Mezclar modelo de exposicion con el shape file de las manzanas
            mapdata_danosmnz = manzana_shp.merge(df_losses_def, left_on='COD_DANE', right_on='cod_mnz', how='left')
            
            """ ---------------------------------------------------------------------------
                             Resultados de perdidas --MANZANA-- PAE
            --------------------------------------------------------------------------- """ 
            
            with h5py.File(PRD_pbl_mnz, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8')) # Lista de parametros de OpenQuake
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:] # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()]  # ID del agregado
                loss = archivo["aggrisk"]["loss"][()] # perdidas segun el aggregate ID
                valex = archivo["assetcol"]["array"]["value-structural"][()] 
                cod_mnz_valex = archivo["assetcol"]["array"]["cod_mnz"][()] 

            df_group = pd.DataFrame({'agg_id':agg_id, 'loss':loss}) # dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['loss']  # agrupa las perdidas por aggid
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_agg_mnp.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_agg.reset_index(level=0, inplace=True) # resetea el indice agregado

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
            df_losses = pd.DataFrame({'pae_mnz_cop':aggrisk_mnz,'cod_mnz':cod_mnzdef})

            df_valex = pd.DataFrame({'valex':valex,'index':cod_mnz_valex})
            df_codmnz = pd.DataFrame({'cod_mnz':cod_mnzdef,'index':range(1,len(cod_mnzdef)+1)})
            df_prom = pd.merge(df_valex, df_codmnz, on='index', how='left') 
            grouped_df = df_prom.groupby('cod_mnz')['valex'].sum().reset_index()

                
            df_expotax = pd.merge(df_losses, grouped_df, on='cod_mnz', how='left') 
            df_expotax['pae_mnz_prc'] = (df_expotax.pae_mnz_cop/df_expotax.valex)*1000

            df_losses_prc = pd.merge(df_losses, grouped_df, on='cod_mnz', how='left') 
            df_losses_prc['pae_mnz_prc'] = (df_losses_prc.pae_mnz_cop/df_losses_prc.valex)*1000
            # Mezclar modelo de exposicion con el shape file de las manzanas
            mapdata_perdidasmnz = manzana_shp.merge(df_losses_prc, left_on='COD_DANE', right_on='cod_mnz', how='left')
            
            """ ---------------------------------------------------------------------------
                   Resultados de daños -----MANZANA-- Tabla resumen/Mapas de dano
            --------------------------------------------------------------------------- """ 

            with h5py.File(DNO_pbl_mnz, 'r') as archivo: 
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
                colapsosss = archivo["aggrisk"]["collapsed"][()]
                valex = archivo["assetcol"]["array"]["value-number"][()] 
                txn_valex = archivo["assetcol"]["array"]["taxonomy"][()] 
                mnz_valex = archivo["assetcol"]["array"]["cod_mnz"][()]

            Num_build_table1 = np.sum(valex)
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
            aggrisk_table1 = list(np.array(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg0))
            aggrisk_table1.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg1))
            aggrisk_table1.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg2))
            aggrisk_table1.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg3))
            aggrisk_table1.append(float(dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss_dmg4))
            # dataframe de perdidas promedio por manzana
            dic_mnp = {'stat':dfmelted_txn_dmg0.stat,'cod_mnz':dfmelted_txn_dmg0.cod_mnz,'loss_dmg0':dfmelted_txn_dmg0.loss_dmg0,'loss_dmg1':dfmelted_txn_dmg1.loss_dmg1,'loss_dmg2':dfmelted_txn_dmg2.loss_dmg2,'loss_dmg3':dfmelted_txn_dmg3.loss_dmg3,'loss_dmg4':dfmelted_txn_dmg4.loss_dmg4}
            dfmelted_mnz = pd.DataFrame(dic_mnp)
            aggrisk_mnz = np.zeros((len(dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0),5))
            aggrisk_mnz[:,0] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg0
            aggrisk_mnz[:,1] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg1
            aggrisk_mnz[:,2] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg2
            aggrisk_mnz[:,3] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg3
            aggrisk_mnz[:,4] = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss_dmg4
            manzanas = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].cod_mnz.tolist()
            
            """ ---------------------------------------------------------------------------
                   Resultados de daños -----MANZANA-- Tabla resumen/Mapas de dano
            --------------------------------------------------------------------------- """
            
            with h5py.File(DNO_pbl_txn, 'r') as archivo: 
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
                mnz_valex = archivo["assetcol"]["array"]["cod_mnz"][()]
                
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
            df_lossesgrup = df_losses.groupby('taxonomy')[['dmg0', 'dmg1', 'dmg2', 'dmg3', 'dmg4']].sum().reset_index()
            df_valex = pd.DataFrame({'valex':valex,'index':txn_valex})
            df_codtxn = pd.DataFrame({'taxonomy':taxo_def,'index':range(1,len(taxonomias)+1)})
            df_prom = pd.merge(df_valex, df_codtxn, on='index', how='left') 
            grouped_df = df_prom.groupby('taxonomy')['valex'].sum().reset_index()

                
            df_expotax_table2 = pd.merge(df_lossesgrup, grouped_df, on='taxonomy', how='left') 


            categorias = taxonomias
            sin_danio,danio_leve,danio_moderado,danio_extensivo,colapso = [], [], [], [], []
            for index in range(len(taxonomias)):
                sindano = (aggrisk_mnz[index,0]/np.sum(aggrisk_mnz[index,:]))*100
                sin_danio.append(sindano)
                leve = (aggrisk_mnz[index,1]/np.sum(aggrisk_mnz[index,:]))*100
                danio_leve.append(leve)
                moderado = (aggrisk_mnz[index,2]/np.sum(aggrisk_mnz[index,:]))*100
                danio_moderado.append(moderado)
                severo = (aggrisk_mnz[index,3]/np.sum(aggrisk_mnz[index,:]))*100
                danio_extensivo.append(severo)
                colaps = (aggrisk_mnz[index,4]/np.sum(aggrisk_mnz[index,:]))*100
                colapso.append(colaps)
            
            """ ---------------------------------------------------------------------------
                    Resultados de perdidas --MANZANA-- Tabla PAE y diagrama
            --------------------------------------------------------------------------- """ 
            
            # ============================ VARIABLES MODIFICAR ============================
            #      [  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  | 10  | 11  | 12  | 13  | 14  | 15  ]
            xpos = [-0.15,-0.35,-0.00,+0.00,+0.10,+0.15,+0.30,+0.55,+0.55,-0.18,+0.00,+0.00,+0.00,+0.40,+0.00,+0.55,-0.18,+0.00,+0.00,+0.00,+0.40,+0.00]
            ypos = [+0.12,+0.00,-0.35,+0.25,+0.25,-0.35,-0.30,+0.12,-0.20,+0.12,+0.12,-0.35,+0.12,+0.12,-0.20,-0.20,+0.12,+0.12,-0.35,+0.12,+0.12,-0.20]
            # ============================================================================


            with h5py.File(PRD_pbl_txn, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8')) # Lista de parametros de OpenQuake
                txn_list_bytes  = archivo["assetcol"]["tagcol"]["taxonomy"][()][1:] # Lista de taxonomias
                txn_list = [item.decode('utf-8') for item in txn_list_bytes]
                agg_id = archivo["aggrisk"]["agg_id"][()]  # ID del agregado
                loss = archivo["aggrisk"]["loss"][()] # perdidas segun el aggregate ID
                valex = archivo["assetcol"]["array"]["value-structural"][()] 
                txn_valex = archivo["assetcol"]["array"]["taxonomy"][()] 

            df_group = pd.DataFrame({'agg_id':agg_id, 'loss':loss}) # dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['loss']  # agrupa las perdidas por aggid
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles']) # calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True) # genera un indice, agg_id se vuelve en columna
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']] # genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True) # dataframe de perdidas por manzana o por manzana + taxonomia
            stats_agg_mnp.reset_index(level=0, inplace=True) # resetea el indice municipio
            stats_agg.reset_index(level=0, inplace=True) # resetea el indice agregado

            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_txn = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')

            dfmelted_txn.sort_values(by='agg_id', inplace=True)
            dfmelted_txn['stat'] = dfmelted_txn['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})

            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])

            dfmelted_txn['taxonomy'] = np.array(txn_list)[(dfmelted_txn['agg_id'] / 1).astype(int)]
            dfmelted_txn = dfmelted_txn.drop(columns=['agg_id'])
            dfmelted_txn = dfmelted_txn.reset_index(drop=True)

            aggrisk = dfmelted_mnp.loc[dfmelted_mnp.stat=='mean'].loss
            aggrisk_txn = dfmelted_txn.loc[dfmelted_txn.stat=='mean'].loss.tolist()
            taxonomias = dfmelted_txn.loc[dfmelted_txn.stat=='mean'].taxonomy.tolist()

            taxo_def = []
            for txn in taxonomias:
                parte = txn.split('/')
                taxo_def.append(parte[0]+'/'+parte[1]+'/'+parte[2])
                    
            df_losses = pd.DataFrame({'loss':aggrisk_txn,'taxonomy':taxo_def})
            df_lossesgrup = df_losses.groupby('taxonomy')['loss'].sum().reset_index()
            df_valex = pd.DataFrame({'valex':valex,'index':txn_valex})
            df_codtxn = pd.DataFrame({'taxonomy':taxo_def,'index':range(1,len(taxonomias)+1)})
            df_prom = pd.merge(df_valex, df_codtxn, on='index', how='left') 
            grouped_df = df_prom.groupby('taxonomy')['valex'].sum().reset_index()


            df_expotax_table3 = pd.merge(df_lossesgrup, grouped_df, on='taxonomy', how='left') 
            df_expotax_table3['loss2'] = (df_expotax_table3.loss/df_expotax_table3.valex)*1000
            
            with h5py.File(PRD_pbl_mnz, 'r') as archivo:
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
                # Para obtener datos aggcurves
                aggmnz_matrix = archivo["agg_curves-stats"]['structural'][()]

            """
            ---------------------------------------------------------------------------
                                         Curva de excedencia
            ---------------------------------------------------------------------------
            """
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
            
            # 5). Se obtienen los datos de entrada y se configuran los condicionales
            # ------- Valor expuesto --------------------------------------------------
            valexpuesto = np.sum(exposicion_mnz)/1e6                                    # Valor expuesto en billones de pesos            
            
            """
            ---------------------------------------------------------------------------
                                      Tabla de resumen PAE
            ---------------------------------------------------------------------------
            """
            index_addid = np.where(agg_id_mnz==oqparam_dict_mnz['K'])[0]                 # Indices de el aggid a utilizar
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
            valorexp = valexpuesto*1e6
            
            
            # ------- Nombre del municipio ------------------------------------
            CP_Name = oqparam_dict['description'].split('_')[3].strip()          # Nombre del centro poblado inicial
            if CP_Name[0].islower():
                CP_Name = CP_Name[0].upper() + CP_Name[1:]                       # Si el nombre del centro poblado no comienza con una mayuscula
        
            # ------- Codigo del municipio ------------------------------------
            COD_mun = cod_mnzdef[0][0:4]
            
    return df_EBR,valexpuesto,valorexp,PAE_mill,PE_mill,Num_build_table1,aggrisk_table1,df_expotax_table2,categorias,aggrisk_mnz,df_expotax_table3,manzana_shp,seccion_shp,area_shp, calculation_mode, Modelo_Expo2, CP_Name, COD_mun, mapdata_AreaCons, Txn_Rep, mapdata_Limits, mapdata_Pisos, title_npiso, valores_unidos, mapdata_allmnzmll, mapdata_allmnzcop, mapdata_fallmnz, mapdata_injuredmnz, mapdata_homelessmnz, mapdata_colapsedmnz, mapdata_allsccmll, mapdata_allscccop, mapdata_fallscc, mapdata_injuredscc, mapdata_homelessscc, mapdata_colapsedsecc, mapdata_danosmnz, mapdata_perdidasmnz



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
#%% Lista de pisos agrupados
def agrupar_pisos(lista_pisos):
    # Grupos definidos
    grupos = [
        (1, [1]),             # Edificios de 1 piso
        (2, [2]),             # Edificios de 2 pisos
        (3, [3, 4]),          # Edificios de 3 y 4 pisos
        (4, range(5, 8)),     # Edificios de 5 a 7 pisos
        (5, range(8, 11))     # Edificios de 8 a 10 pisos
    ]

    # Diccionario para almacenar los grupos
    grupos_pisos = {grupo: [] for grupo, _ in grupos}
    grupos_pisos[6] = []  # Grupo para edificios de más de 10 pisos

    # Asignar cada piso a su grupo correspondiente
    for piso in lista_pisos:
        asignado = False
        for grupo, rango in grupos:
            if piso in rango:
                grupos_pisos[grupo].append(piso)
                asignado = True
                break
        if not asignado:
            grupos_pisos[6].append(piso)  # Añadir a 'más de 10'

    # Crear las listas finales
    lista_pisos_agrupados = [grupos_pisos[grupo] for grupo, _ in grupos if grupos_pisos[grupo]]
    if grupos_pisos[6]:
        lista_pisos_agrupados.append(grupos_pisos[6])
    lista_nombre_pisos = ['un piso', 'dos pisos', '3 y 4 pisos', '5 a 7 pisos', '8 a 10 pisos', '12 y 17 pisos']

    return lista_pisos_agrupados, lista_nombre_pisos

def unir_valores(lista):
    resultado = []
    for sublista in lista:
        # Convertir cada número a string y luego unirlos
        texto = ''.join(str(num) for num in sublista)
        resultado.append(texto)
    return resultado

def filtrar_por_pisos(df, pisos):
    """
    Filtra el DataFrame 'df' para incluir solo las filas donde 'n_piso' está en la lista 'pisos'.

    :param df: DataFrame a filtrar.
    :param pisos: Lista de números de pisos a incluir.
    :return: DataFrame filtrado.
    """
    return df[df['n_piso'].isin(pisos)]