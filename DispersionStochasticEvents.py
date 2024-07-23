# -----------------------------------------------------------------------------
# -------------- DISPERSION ELEMENTS // SHOW AND HIDE ELEMENTS ----------------
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
# -------- Data processing libraries ------------------------------------------
import pandas as pd
import numpy as np

#%% ====== SHOW DISPERSION ELEMENTS ===========================================
def Show_Dispersion_Elements(DSP_title,DSP_text,DSP_boton,cnt_container,upcnt_color,Select_Folder_DSP,Ventana_Info_DSP,Function_Dispersion,resultado_label_Dispersion):
    # ---- Titulo de la pestaña:
    if DSP_title["tlt_tlt_DSP"] is None:
        DSP_title["tlt_tlt_DSP"] = wnfun_lib.Label_Image('/Dispersion_titleV2.png', 760, 95, cnt_container,"white",0.309,0.182)

    # ---- Descripcion introductoria:
    if DSP_text["txt_cnt_DSP1"] is None:
        DSP_text["txt_cnt_DSP1"] = wnfun_lib.Label_Image('/Dispersion_textV2.png', 620, 430, cnt_container,"white",0.32,0.55)
        
    # ---- Seleccionar carpeta:
    if DSP_boton["btn_slc_DSP"] is None:
        DSP_boton["btn_slc_DSP"] = wnfun_lib.Button_Image('/Select_FolderV2.png', 320, 75, cnt_container,"white",0.78,0.5,Select_Folder_DSP) 
    
    # ---- Informacion:
    if DSP_boton["btn_inf_DSP"] is None:
        DSP_boton["btn_inf_DSP"] = wnfun_lib.Button_Image('/Info.png', 35, 35, cnt_container,"white",0.905,0.468,Ventana_Info_DSP)
        
    # ---- Calibrar:
    if DSP_boton["btn_clb_DSP"] is None:
        DSP_boton["btn_clb_DSP"] = wnfun_lib.Button_Image_lambda('/Generate_Button.png', 200, 66, cnt_container,"white",0.78,0.58,Function_Dispersion,resultado_label_Dispersion)
    
    resultado_label = tk.Label(cnt_container, text="", fg="red")
    resultado_label.pack()
    resultado_label.pack_forget()
#%% ====== HIDE DISPERSION ELEMENTS ===========================================
def Hide_Dispersion_Elements(title_DSP,DSP_title,text_DSP,DSP_text,boton_DSP,DSP_boton,canva_DSP,DSP_canva,label_DSP,DSP_label,rect_DSP,DSP_rect):
    for tlt in title_DSP:
        if DSP_title[tlt] is not None:
            DSP_title[tlt].place_forget()
            DSP_title[tlt] = None
            
    for txt in text_DSP:
        if DSP_text[txt] is not None:
            DSP_text[txt].place_forget()
            DSP_text[txt] = None
            
    for btn in boton_DSP:
        if DSP_boton[btn] is not None:
            DSP_boton[btn].place_forget()
            DSP_boton[btn] = None
    
    for cnv in canva_DSP:
        if DSP_canva[cnv] is not None:
            DSP_canva[cnv].get_tk_widget().destroy()
            DSP_canva[cnv] = None
            
    for lbl in label_DSP:
        if DSP_label[lbl] is not None:
            DSP_label[lbl].place_forget()
            DSP_label[lbl] = None
    
    for rct in rect_DSP:
        if DSP_rect[rct] is not None:
            DSP_rect[rct].place_forget()
            DSP_rect[rct] = None

#%% ====== FUNCTION DISPERSION ================================================
def Function_Dispersion_Elements(carpeta_seleccionada_DSP):
    global datos_CP,CP_Name,datos_MNZ,Mnz_Predeter
    
    # Primero hay que identificar el caso que se esta presentando:
        # 1. En la carpeta seleccionada existe la carpeta hdf5_Mnz y hdf5_Txn.
        # 2. La carpeta seleccionada contiene archivos hdf5 agregados por taxonomia
        # 3. La carpeta seleccionada contiene archivos hdf5 agergados por manzana
        # 4. La carpeta seleccionada contiene archivos hdf5 agergados por taxonomia y por manzana
        # 5. La carpeta seleccionada contiene archivos hdf5 sin agregado
    
    # 0). Hay que saber primero si la carpeta tiene las carpetas agregadas por manzana y por taxonomia o solo son archivos hdf5

    rootdir1 = carpeta_seleccionada_DSP                                         # Obtiene el directorio de la carpeta seleccionada  
    Verifi_Mnz,Verifi_Txn,Verifi_Hdf5 = carpetas_en_folder(rootdir1)            # Verificacion del contenido de la carpeta
    
    """------------------------------------------------------------------------    
    ================================== CASO 1 =================================
    ------------------------------------------------------------------------"""
    
    if Verifi_Mnz is not None and Verifi_Txn is not None:
        # 1). Esta sección busca los directorios que hay en la carpeta y 
        # obtiene la ruta de las carpetas necesarias
        for folder in os.listdir(rootdir1):                                     # Ciclo for para la lista de directorios dentro del directorio actual
            if "hdf5_Mnz" in folder:                                            # Si existe una carpeta llamada "hdf5_Mnz"
                Folder_Mnz = os.path.join(rootdir1, folder)                     # Obtiene la ruta de la carpeta llamada "hdf5_Mnz"    
            if "hdf5_Txn" in folder:                                            # Si existe una carpeta llamada "hdf5_Txn"
                Folder_Txn = os.path.join(rootdir1, folder)                     # Obtiene la ruta de la carpeta llamada "hdf5_Txn"  
        """ -------------------------------------------------------------------
                            Obtener datos para la manzana
        ------------------------------------------------------------------- """
        # 2). Obtener la lista de archivos en la carpeta "hdf5_Mnz".
        # Esta lista de archivos obtiene unicamente los que comienzan con calc_
        # y terminan en .hdf5
        archivos_hdf5 = []
        for archivo in os.listdir(Folder_Mnz):                                  # Lista de archivos en "hdf5_Mnz"
            if archivo.startswith("calc_") and archivo.endswith(".hdf5"):       # Obtener solo los archivos que comienzan con "calc_" y terminan en ".hdf5"
                archivos_hdf5.append(os.path.join(Folder_Mnz, archivo))
        # 3). Procesar datos del hdf5.
        Nsim2 = []                      # Numero de simulaciones
        Nevents = []                    # Numero de eventos
        agg_risk = []                   # Perdidas del municipio
        df_AGR_list = []                # Lista de los dataframes de cada simulacion (Municipio)
        df_AGRmnz_list = []             # Lista de los dataframes de cada simulacion (Aggregate by)
        for arch_hdf5 in archivos_hdf5:
            ruta_hdf5 = arch_hdf5
            # 3.1). Cargar archivos de entrada.
            with h5py.File(ruta_hdf5, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))  # Lista de parametros de OpenQuake
                mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]  # Lista de manzanas
                mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                aggrisk_aggid = archivo["aggrisk"]["agg_id"][()]                # ID del agregado
                aggrisk_loss = archivo["aggrisk"]["loss"][()]                   # Perdidas segun el aggregate ID
                events = archivo["events"][()]                                  # eventos de la simulacion
            
            # ............. Lista de eventos y ses_per_logic_tree .............
            Nevents.append(len(events))                                         # Numero de eventos
            Nsim2.append(oqparam_dict['ses_per_logic_tree_path'])               # Numero de simulaciones
            # .................................................................
            
            # ...................... Lista de quantiles .......................
            list_stats = ['mean']
            for quant in oqparam_dict['quantiles']:
                list_stats.append('quantile-'+str(quant))                       # Lista de estadisticas
            # .................................................................
            
            # ................... Nombre del centro poblado ...................
            CP_Name = oqparam_dict['description'].split('-')[-1].strip()        # Nombre del centro poblado inicial
            if CP_Name[0].islower():
                CP_Name = CP_Name[0].upper() + CP_Name[1:]                      # Si el nombre del centro poblado no comienza con una mayuscula
            # .................................................................
            
            # ...................... Catalogo de manzanas .....................
            opcion_mnz = mnz_list                                               # Opcion catalogo de manzanas
            # .................................................................
            
            # 3.2). Procesado:
            df_group = pd.DataFrame({'agg_id':aggrisk_aggid, 'loss':aggrisk_loss})  # Dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['loss']                          # Agrupa las perdidas por aggid
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])   # Calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True)                            # Genera un indice, agg_id se vuelve en columna
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']]     # Genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True)                       # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_agg_mnp.reset_index(level=0, inplace=True)                        # Resetea el indice municipio
            stats_agg.reset_index(level=0, inplace=True)                            # Resetea el indice agregado
            # Agrupar por estadisticas
            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz.sort_values(by='agg_id', inplace=True)                 # Ordenar de menor a mayor los agg_id
            # Cambiar el nombre de las estadisticas
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])                # Eliminar la columna agg_id
            # -----------------------------------------------------------------
            # --------------------- Segun el aggregate by ---------------------
            # -----------------------------------------------------------------
            dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)] # Asignar las manzanas a cada agg_id
            lossopcion = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss       # Perdidas promedio anual por manzana
            dfopcion = pd.DataFrame({'cod_mnz':opcion_mnz,'loss':lossopcion})   # Dataframe de perdidas promedio anual por manzana
            df_sorted = dfopcion.sort_values(by='loss', ascending=False)        # Organizar de mayor a menor perdida las manzanas
            sorted_opcion = df_sorted.cod_mnz.tolist()                          # Obtener la lista de manzanas ordenada 
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])                # Eliminar la columna agg_id
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)                  # Resetear el index
            # ------------------ LISTAS A EXPORTAR/ PROCESAR ------------------
            df_AGR_list.append(dfmelted_mnp)                                    # Lista de los dataframes de cada simulacion (Municipio)
            lnPAE85 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.85'].loss).values[0]
            lnPAE15 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.15'].loss).values[0]
            
            agg_risk.append((lnPAE85-lnPAE15)/2)                                # Lista de las perdidas por simulacion (Municipio) 
            
            df_AGRmnz_list.append(dfmelted_mnz)                                 # Lista de los dataframes de cada simulacion (Aggregate by)
            
        # ....................... Dataframes a utilizar .......................
        datos_CP = {'Num_Sim':Nsim2,'loss':agg_risk,'Num_Sim_Ev':Nevents,'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}
        # .....................................................................
        
        # 5). Obtener dataframe de perdidas para la manzana predominante y 
        # dataframe de error promedio entre datos adyacentes de las simulaciones
        
        # Se crea la lista que ira en el combo de las manzanas
        opciones_mnz, codigo_mnz = [], []
        for op in sorted_opcion:
            codigo_mnz.append(op[:-5])
        for op in opcion_mnz:
            opciones_mnz.append(op[-5:])
        
        # 5.1). Se generan los datos a graficar
        # Se debe obtener una lista con las perdidas promedio de una manzana en 
        # especifico por simulacion. En porcentaje
        lossnew, max_loss_manzana = [], []
        for ind, loss in enumerate(df_AGRmnz_list):
            # Obtener una lista con los resultados del dataframe filtrado 
            # solamente para los valores quantile 85 y 15
            loss85n = loss[loss['stat'] == 'quantile-0.85']
            loss15n = loss[loss['stat'] == 'quantile-0.15']
            disp85,disp15 = [],[]
            for ind2 in loss85n.index.tolist():
                disp85.append(np.log(loss85n['loss'][ind2]))
            for ind2 in loss15n.index.tolist():
                disp15.append(np.log(loss15n['loss'][ind2]))
                
            Dispersion_values = []
            for ind3 in range(len(disp15)):
                Dispersion_values.append((disp85[ind3]-disp15[ind3])/2)
            
            loss_new = pd.DataFrame({'cod_mnz':mnz_list,'Dispersion':Dispersion_values})
            lossnew.append(loss_new)
            
            # Otener la manzana predominante del municipio
            max_loss_manzana.append(loss_new[loss_new['Dispersion']==loss_new['Dispersion'].max()])
        
        # Obtiene un dataframe cuyas columnas son las dispersiones por simulacion
        simmnz_losses = pd.concat([df.set_index('cod_mnz')['Dispersion'] for df in lossnew], axis=1).reset_index()     
        # Cambia el nombre de las columnas Dispersion por Sim_'numero de ses'
        nombres_simulaciones = ['Sim_{}'.format(i) for i in Nsim2]
        simmnz_losses.columns = ['Manzana'] + nombres_simulaciones
        # Obtener manzana predominante
        maxloss = max_loss_manzana[0]
        Mnz_Predeter = maxloss['cod_mnz'].values[0]
        newNsim_mnz = sorted(Nsim2)
        # Obtener los datos de la manzana predominante
        fila_a_graficar = simmnz_losses.loc[simmnz_losses['Manzana'] == Mnz_Predeter]
        # Cambia los titulos de las simulaciones por numeros
        fila_a_graficar = fila_a_graficar[['Manzana']+['Sim_{}'.format(i) for i in newNsim_mnz]]
        # Elimina la columna del codigo de la manzana
        fila_a_graficar = fila_a_graficar.drop(columns=['Manzana'])
        # Obtiene los valores de dispersion por simulacion
        datos_fila = fila_a_graficar.values[0]
        
        # ....................... Dataframes a utilizar .......................
        datos_MNZ = {'Num_Sim':newNsim_mnz,'loss':datos_fila,'Num_Sim_Ev':sorted(Nevents),'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}
        # .....................................................................
        
        """ -------------------------------------------------------------------
                           Obtener datos para la taxonomia
        ------------------------------------------------------------------- """
        # 2). Obtener la lista de archivos en la carpeta "hdf5_Mnz".
        # Esta lista de archivos obtiene unicamente los que comienzan con calc_
        # y terminan en .hdf5
        archivos_hdf5 = []
        for archivo in os.listdir(Folder_Txn):                                  # Lista de archivos en "hdf5_Mnz"
            if archivo.startswith("calc_") and archivo.endswith(".hdf5"):       # Obtener solo los archivos que comienzan con "calc_" y terminan en ".hdf5"
                archivos_hdf5.append(os.path.join(Folder_Txn, archivo))
        # 3). Procesar datos del hdf5.
        Nsim2 = []                      # Numero de simulaciones
        Nevents = []                    # Numero de eventos
        df_AGRtxn_list = []             # Lista de los dataframes de cada simulacion (Aggregate by)
        for arch_hdf5 in archivos_hdf5:
            ruta_hdf5 = arch_hdf5
            # 3.1). Cargar archivos de entrada.
            with h5py.File(ruta_hdf5, 'r') as archivo: 
                oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))  # Lista de parametros de OpenQuake
                txn_list_bytes = archivo["assetcol"]["tagcol"]["taxonomy"][()][1:] # Lista de taxonomias
                txn_list = [item.decode('utf-8') for item in txn_list_bytes]
                aggrisk_aggid = archivo["aggrisk"]["agg_id"][()]                # ID del agregado
                aggrisk_loss = archivo["aggrisk"]["loss"][()]                   # Perdidas segun el aggregate ID
                events = archivo["events"][()]                                  # eventos de la simulacion
        
            # ............. Lista de eventos y ses_per_logic_tree .............
            Nevents.append(len(events))                                         # Numero de eventos
            Nsim2.append(oqparam_dict['ses_per_logic_tree_path'])               # Numero de simulaciones
            # .................................................................
            
            # ...................... Lista de quantiles .......................
            list_stats = ['mean']
            for quant in oqparam_dict['quantiles']:
                list_stats.append('quantile-'+str(quant))                       # Lista de estadisticas
            # .................................................................
            
            # ................... Nombre del centro poblado ...................
            CP_Name = oqparam_dict['description'].split('-')[-1].strip()        # Nombre del centro poblado inicial
            if CP_Name[0].islower():
                CP_Name = CP_Name[0].upper() + CP_Name[1:]                      # Si el nombre del centro poblado no comienza con una mayuscula
            # .................................................................
            
            # ...................... Catalogo de manzanas .....................
            opcion_txn = txn_list                                               # Opcion catalogo de taxonomias
            # .................................................................
            
            # 3.2). Procesado:
            df_group = pd.DataFrame({'agg_id':aggrisk_aggid, 'loss':aggrisk_loss})  # Dataframe perdidas por aggid
            grp_aggid = df_group.groupby('agg_id')['loss']                          # Agrupa las perdidas por aggid
            stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])   # Calcula mediana y percentiles de las perdidas por aggid
            stats_agg.reset_index(level=0, inplace=True)                            # Genera un indice, agg_id se vuelve en columna
            stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']]     # Genera un dataframe para municipio
            stats_agg.drop(stats_agg_mnp.index, inplace=True)                       # Dataframe de perdidas por manzana o por manzana + taxonomia
            stats_agg_mnp.reset_index(level=0, inplace=True)                        # Resetea el indice municipio
            stats_agg.reset_index(level=0, inplace=True)                            # Resetea el indice agregado
            # Agrupar por estadisticas
            dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
            dfmelted_mnz.sort_values(by='agg_id', inplace=True)                 # Ordenar de menor a mayor los agg_id
            # Cambiar el nombre de las estadisticas
            dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
            dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])                # Eliminar la columna agg_id
            # -----------------------------------------------------------------
            # --------------------- Segun el aggregate by ---------------------
            # -----------------------------------------------------------------
            dfmelted_mnz['taxonomy'] = np.array(txn_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)] # Asignar las taxonomias a cada agg_id
            lossopcion = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss       # Perdidas promedio anual por taxonomia
            dfopcion = pd.DataFrame({'taxonomy':opcion_txn,'loss':lossopcion})  # Dataframe de perdidas promedio anual por taxonomia
            df_sorted = dfopcion.sort_values(by='loss', ascending=False)        # Organizar de mayor a menor perdida las taxonomias
            sorted_opcion = df_sorted.taxonomy.tolist()                         # Obtener la lista de taxonomias ordenada 
            dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])                # Eliminar la columna agg_id
            dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)                  # Resetear el index
            # ------------------ LISTAS A EXPORTAR/ PROCESAR ------------------
            df_AGRtxn_list.append(dfmelted_mnz)                                 # Lista de los dataframes de cada simulacion (Aggregate by)
            
        # 4). Obtener dataframe de perdidas para la manzana predominante y 
        # dataframe de error promedio entre datos adyacentes de las simulaciones
        
        # Se crea la lista que ira en el combo de las manzanas
        opciones_txn, codigo_txn = [], []
        for op in sorted_opcion:
            opciones_txn.append(op)
            codigo_txn.append(op)
        
        # 5.1). Se generan los datos a graficar
        # Se debe obtener una lista con las perdidas promedio de una manzana en 
        # especifico por simulacion. En porcentaje
        lossnew, max_loss_taxonomy = [], []
        for ind, loss in enumerate(df_AGRtxn_list):
            # Obtener una lista con los resultados del dataframe filtrado 
            # solamente para los valores quantile 85 y 15
            loss85n = loss[loss['stat'] == 'quantile-0.85']
            loss15n = loss[loss['stat'] == 'quantile-0.15']
            disp85,disp15 = [],[]
            for ind2 in loss85n.index.tolist():
                disp85.append(np.log(loss85n['loss'][ind2]))
            for ind2 in loss15n.index.tolist():
                disp15.append(np.log(loss15n['loss'][ind2]))
                
            Dispersion_values = []
            for ind3 in range(len(disp15)):
                Dispersion_values.append((disp85[ind3]-disp15[ind3])/2)
            
            loss_new = pd.DataFrame({'taxonomy':txn_list,'Dispersion':Dispersion_values})
            lossnew.append(loss_new)
            
            # Otener la manzana predominante del municipio
            max_loss_taxonomy.append(loss_new[loss_new['Dispersion']==loss_new['Dispersion'].max()])
            
    
        # DEBE SACAR UN DATAFRAME POR CADA ITERACION
        
        # Obtiene un dataframe cuyas columnas son las dispersiones por simulacion
        simtxn_losses = pd.concat([df.set_index('taxonomy')['Dispersion'] for df in lossnew], axis=1).reset_index()     
        # Cambia el nombre de las columnas Dispersion por Sim_'numero de ses'
        nombres_simulaciones = ['Sim_{}'.format(i) for i in Nsim2]
        simtxn_losses.columns = ['Taxonomia'] + nombres_simulaciones
        # Obtener manzana predominante
        maxloss = max_loss_taxonomy[0]
        Txn_Predeter = maxloss['taxonomy'].values[0]
        newNsim_txn = sorted(Nsim2)
        # Obtener los datos de la manzana predominante
        fila_a_graficar = simtxn_losses.loc[simtxn_losses['Taxonomia'] == Txn_Predeter]
        # Cambia los titulos de las simulaciones por numeros
        fila_a_graficar = fila_a_graficar[['Taxonomia']+['Sim_{}'.format(i) for i in newNsim_txn]]
        # Elimina la columna del codigo de la manzana
        fila_a_graficar = fila_a_graficar.drop(columns=['Taxonomia'])
        # Obtiene los valores de dispersion por simulacion
        datos_fila = fila_a_graficar.values[0]
        
        # ....................... Dataframes a utilizar .......................
        datos_TXN = {'Num_Sim':newNsim_txn,'loss':datos_fila,'Num_Sim_Ev':sorted(Nevents),'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}
        # .....................................................................
        
    # Definir el caso 2 a caso 5:
    elif Verifi_Hdf5 is not None:
        archivos_hdf5 = []
        # Verificar que existe al menos 1 archivo .hdf5
        for archivo in os.listdir(rootdir1): 
            # Arhivos .hdf5?
            if archivo.endswith(".hdf5"): 
                archivos_hdf5.append(os.path.join(rootdir1, archivo))           # Guarda en una lista todos los archivos hdf5 encontrados
        # Hay archivos hdf5?
        if archivos_hdf5 == []:
            warning = "En la carpeta seleccionada no hay archivos .hdf5'." 
            tk.messagebox.showinfo("ERROR", warning)
        else:
            # Con esa lista de archivos empezamos a agruparlos de acuerdo a su agregado.
            # Si hay mas de un agregado debe saltar una advertencia, si solo es uno 
            # se definenn los demas casos
            aggregate_type = []
            for ruta_archivo in archivos_hdf5:
                with h5py.File(ruta_archivo, 'r') as archivo:                   # Se abre el arhivo hdf5
                    oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))   # Lista de parametros de OpenQuake
                # Revisar si hay o no un agergado en los hdf5
                for keys in oqparam_dict.keys():
                    if 'aggregate_by' in keys:
                        aggregate_type.append(oqparam_dict['aggregate_by'])
   
            if aggregate_type == []:
                aggregate_type = ['Sin agregado']*len(archivos_hdf5)
                        
            # Definir casos
            aggby_mnz, aggby_txn, aggby_mnz_txn, agg_wh = [], [], [], []
            for agg in aggregate_type:
                # Definir caso 2:
                if agg == [['taxonomy']]:
                    aggby_txn.append(agg)
                # Definir caso 3:
                elif agg == [['cod_mnz']]:
                    aggby_mnz.append(agg)
                # Definir caso 4:
                elif agg == [['cod_mnz'],['taxonomy']] or agg == [['taxonomy'],['cod_mnz']]:
                    aggby_mnz_txn.append(agg)
                # Definir caso 5:
                elif agg == 'Sin agregado':
                    agg_wh.append(agg)
            
   
            if len(aggby_txn) == len(aggregate_type): 
                # todos son hdf5 agregados por taxonomia == Saca resultados
                # por taxonomia y del municipio
                
                """ -------------------------------------------------------------------
                                   Obtener datos para la taxonomia
                ------------------------------------------------------------------- """
                # 3). Procesar datos del hdf5.
                Nsim2 = []                      # Numero de simulaciones
                Nevents = []                    # Numero de eventos
                df_AGRtxn_list = []             # Lista de los dataframes de cada simulacion (Aggregate by)
                df_AGR_list = []
                agg_risk = []
                for arch_hdf5 in archivos_hdf5:
                    ruta_hdf5 = arch_hdf5
                    # 3.1). Cargar archivos de entrada.
                    with h5py.File(ruta_hdf5, 'r') as archivo: 
                        oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))  # Lista de parametros de OpenQuake
                        txn_list_bytes = archivo["assetcol"]["tagcol"]["taxonomy"][()][1:] # Lista de taxonomias
                        txn_list = [item.decode('utf-8') for item in txn_list_bytes]
                        aggrisk_aggid = archivo["aggrisk"]["agg_id"][()]                # ID del agregado
                        aggrisk_loss = archivo["aggrisk"]["loss"][()]                   # Perdidas segun el aggregate ID
                        events = archivo["events"][()]                                  # eventos de la simulacion
                
                    # ............. Lista de eventos y ses_per_logic_tree .............
                    Nevents.append(len(events))                                         # Numero de eventos
                    Nsim2.append(oqparam_dict['ses_per_logic_tree_path'])               # Numero de simulaciones
                    # .................................................................
                    
                    # ...................... Lista de quantiles .......................
                    list_stats = ['mean']
                    for quant in oqparam_dict['quantiles']:
                        list_stats.append('quantile-'+str(quant))                       # Lista de estadisticas
                    # .................................................................
                    
                    # ................... Nombre del centro poblado ...................
                    CP_Name = oqparam_dict['description'].split('-')[-1].strip()        # Nombre del centro poblado inicial
                    if CP_Name[0].islower():
                        CP_Name = CP_Name[0].upper() + CP_Name[1:]                      # Si el nombre del centro poblado no comienza con una mayuscula
                    # .................................................................
                    
                    # ...................... Catalogo de manzanas .....................
                    opcion_txn = txn_list                                               # Opcion catalogo de taxonomias
                    # .................................................................
                    
                    # 3.2). Procesado:
                    df_group = pd.DataFrame({'agg_id':aggrisk_aggid, 'loss':aggrisk_loss})  # Dataframe perdidas por aggid
                    grp_aggid = df_group.groupby('agg_id')['loss']                          # Agrupa las perdidas por aggid
                    stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])   # Calcula mediana y percentiles de las perdidas por aggid
                    stats_agg.reset_index(level=0, inplace=True)                            # Genera un indice, agg_id se vuelve en columna
                    stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']]     # Genera un dataframe para municipio
                    stats_agg.drop(stats_agg_mnp.index, inplace=True)                       # Dataframe de perdidas por manzana o por manzana + taxonomia
                    stats_agg_mnp.reset_index(level=0, inplace=True)                        # Resetea el indice municipio
                    stats_agg.reset_index(level=0, inplace=True)                            # Resetea el indice agregado
                    # Agrupar por estadisticas
                    dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
                    dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
                    dfmelted_mnz.sort_values(by='agg_id', inplace=True)                 # Ordenar de menor a mayor los agg_id
                    # Cambiar el nombre de las estadisticas
                    dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
                    dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
                    dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])                # Eliminar la columna agg_id
                    # -----------------------------------------------------------------
                    # --------------------- Segun el aggregate by ---------------------
                    # -----------------------------------------------------------------
                    dfmelted_mnz['taxonomy'] = np.array(txn_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)] # Asignar las taxonomias a cada agg_id
                    lossopcion = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss       # Perdidas promedio anual por taxonomia
                    dfopcion = pd.DataFrame({'taxonomy':opcion_txn,'loss':lossopcion})  # Dataframe de perdidas promedio anual por taxonomia
                    df_sorted = dfopcion.sort_values(by='loss', ascending=False)        # Organizar de mayor a menor perdida las taxonomias
                    sorted_opcion = df_sorted.taxonomy.tolist()                         # Obtener la lista de taxonomias ordenada 
                    dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])                # Eliminar la columna agg_id
                    dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)                  # Resetear el index
                    # ------------------ LISTAS A EXPORTAR/ PROCESAR ------------------
                    df_AGRtxn_list.append(dfmelted_mnz)                                 # Lista de los dataframes de cada simulacion (Aggregate by)
                    
                    # ------------------ LISTAS A EXPORTAR/ PROCESAR ------------------
                    df_AGR_list.append(dfmelted_mnp)                                    # Lista de los dataframes de cada simulacion (Municipio)
                    lnPAE85 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.85'].loss).values[0]
                    lnPAE15 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.15'].loss).values[0]
                    
                    agg_risk.append((lnPAE85-lnPAE15)/2)                                # Lista de las perdidas por simulacion (Municipio) 
                                        
                # ....................... Dataframes a utilizar .......................
                datos_CP = {'Num_Sim':Nsim2,'loss':agg_risk,'Num_Sim_Ev':Nevents,'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}

                # .....................................................................
                
                # 4). Obtener dataframe de perdidas para la manzana predominante y 
                # dataframe de error promedio entre datos adyacentes de las simulaciones
                
                # Se crea la lista que ira en el combo de las manzanas
                opciones_txn, codigo_txn = [], []
                for op in sorted_opcion:
                    opciones_txn.append(op)
                    codigo_txn.append(op)
                
                # 5.1). Se generan los datos a graficar
                # Se debe obtener una lista con las perdidas promedio de una manzana en 
                # especifico por simulacion. En porcentaje
                lossnew, max_loss_taxonomy = [], []
                for ind, loss in enumerate(df_AGRtxn_list):
                    # Obtener una lista con los resultados del dataframe filtrado 
                    # solamente para los valores quantile 85 y 15
                    loss85n = loss[loss['stat'] == 'quantile-0.85']
                    loss15n = loss[loss['stat'] == 'quantile-0.15']
                    disp85,disp15 = [],[]
                    for ind2 in loss85n.index.tolist():
                        disp85.append(np.log(loss85n['loss'][ind2]))
                    for ind2 in loss15n.index.tolist():
                        disp15.append(np.log(loss15n['loss'][ind2]))
                        
                    Dispersion_values = []
                    for ind3 in range(len(disp15)):
                        Dispersion_values.append((disp85[ind3]-disp15[ind3])/2)
                    
                    loss_new = pd.DataFrame({'taxonomy':txn_list,'Dispersion':Dispersion_values})
                    lossnew.append(loss_new)
                    
                    # Otener la manzana predominante del municipio
                    max_loss_taxonomy.append(loss_new[loss_new['Dispersion']==loss_new['Dispersion'].max()])
                    
            
                # DEBE SACAR UN DATAFRAME POR CADA ITERACION
                
                # Obtiene un dataframe cuyas columnas son las dispersiones por simulacion
                simtxn_losses = pd.concat([df.set_index('taxonomy')['Dispersion'] for df in lossnew], axis=1).reset_index()     
                # Cambia el nombre de las columnas Dispersion por Sim_'numero de ses'
                nombres_simulaciones = ['Sim_{}'.format(i) for i in Nsim2]
                simtxn_losses.columns = ['Taxonomia'] + nombres_simulaciones
                # Obtener manzana predominante
                maxloss = max_loss_taxonomy[0]
                Txn_Predeter = maxloss['taxonomy'].values[0]
                newNsim_txn = sorted(Nsim2)
                # Obtener los datos de la manzana predominante
                fila_a_graficar = simtxn_losses.loc[simtxn_losses['Taxonomia'] == Txn_Predeter]
                # Cambia los titulos de las simulaciones por numeros
                fila_a_graficar = fila_a_graficar[['Taxonomia']+['Sim_{}'.format(i) for i in newNsim_txn]]
                # Elimina la columna del codigo de la manzana
                fila_a_graficar = fila_a_graficar.drop(columns=['Taxonomia'])
                # Obtiene los valores de dispersion por simulacion
                datos_fila = fila_a_graficar.values[0]
                
                # ....................... Dataframes a utilizar .......................
                datos_TXN = {'Num_Sim':newNsim_txn,'loss':datos_fila,'Num_Sim_Ev':sorted(Nevents),'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}
                # .....................................................................
                
                # Definir dataframe manzanas como None
                datos_MNZ = None
                
                # Otras variables asiganas valor None
                Mnz_Predeter = None
                opciones_mnz = None
                codigo_mnz = None
                simmnz_losses = None
                newNsim_mnz = None
                
            elif len(aggby_mnz) == len(aggregate_type):

                """ -------------------------------------------------------------------
                                    Obtener datos para la manzana
                ------------------------------------------------------------------- """
                # 3). Procesar datos del hdf5.
                Nsim2 = []                      # Numero de simulaciones
                Nevents = []                    # Numero de eventos
                agg_risk = []                   # Perdidas del municipio
                df_AGR_list = []                # Lista de los dataframes de cada simulacion (Municipio)
                df_AGRmnz_list = []             # Lista de los dataframes de cada simulacion (Aggregate by)
                for arch_hdf5 in archivos_hdf5:
                    ruta_hdf5 = arch_hdf5
                    # 3.1). Cargar archivos de entrada.
                    with h5py.File(ruta_hdf5, 'r') as archivo: 
                        oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))  # Lista de parametros de OpenQuake
                        mnz_list_bytes = archivo["assetcol"]["tagcol"]["cod_mnz"][()][1:]  # Lista de manzanas
                        mnz_list = [item.decode('utf-8') for item in mnz_list_bytes]
                        aggrisk_aggid = archivo["aggrisk"]["agg_id"][()]                # ID del agregado
                        aggrisk_loss = archivo["aggrisk"]["loss"][()]                   # Perdidas segun el aggregate ID
                        events = archivo["events"][()]                                  # eventos de la simulacion
                    
                    # ............. Lista de eventos y ses_per_logic_tree .............
                    Nevents.append(len(events))                                         # Numero de eventos
                    Nsim2.append(oqparam_dict['ses_per_logic_tree_path'])               # Numero de simulaciones
                    # .................................................................
                    
                    # ...................... Lista de quantiles .......................
                    list_stats = ['mean']
                    for quant in oqparam_dict['quantiles']:
                        list_stats.append('quantile-'+str(quant))                       # Lista de estadisticas
                    # .................................................................
                    
                    # ................... Nombre del centro poblado ...................
                    CP_Name = oqparam_dict['description'].split('-')[-1].strip()        # Nombre del centro poblado inicial
                    if CP_Name[0].islower():
                        CP_Name = CP_Name[0].upper() + CP_Name[1:]                      # Si el nombre del centro poblado no comienza con una mayuscula
                    # .................................................................
                    
                    # ...................... Catalogo de manzanas .....................
                    opcion_mnz = mnz_list                                               # Opcion catalogo de manzanas
                    # .................................................................
                    
                    # 3.2). Procesado:
                    df_group = pd.DataFrame({'agg_id':aggrisk_aggid, 'loss':aggrisk_loss})  # Dataframe perdidas por aggid
                    grp_aggid = df_group.groupby('agg_id')['loss']                          # Agrupa las perdidas por aggid
                    stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])   # Calcula mediana y percentiles de las perdidas por aggid
                    stats_agg.reset_index(level=0, inplace=True)                            # Genera un indice, agg_id se vuelve en columna
                    stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']]     # Genera un dataframe para municipio
                    stats_agg.drop(stats_agg_mnp.index, inplace=True)                       # Dataframe de perdidas por manzana o por manzana + taxonomia
                    stats_agg_mnp.reset_index(level=0, inplace=True)                        # Resetea el indice municipio
                    stats_agg.reset_index(level=0, inplace=True)                            # Resetea el indice agregado
                    # Agrupar por estadisticas
                    dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
                    dfmelted_mnz = stats_agg.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
                    dfmelted_mnz.sort_values(by='agg_id', inplace=True)                 # Ordenar de menor a mayor los agg_id
                    # Cambiar el nombre de las estadisticas
                    dfmelted_mnz['stat'] = dfmelted_mnz['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
                    dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
                    dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])                # Eliminar la columna agg_id
                    # -----------------------------------------------------------------
                    # --------------------- Segun el aggregate by ---------------------
                    # -----------------------------------------------------------------
                    dfmelted_mnz['cod_mnz'] = np.array(mnz_list)[(dfmelted_mnz['agg_id'] / 1).astype(int)] # Asignar las manzanas a cada agg_id
                    lossopcion = dfmelted_mnz.loc[dfmelted_mnz.stat=='mean'].loss       # Perdidas promedio anual por manzana
                    dfopcion = pd.DataFrame({'cod_mnz':opcion_mnz,'loss':lossopcion})   # Dataframe de perdidas promedio anual por manzana
                    df_sorted = dfopcion.sort_values(by='loss', ascending=False)        # Organizar de mayor a menor perdida las manzanas
                    sorted_opcion = df_sorted.cod_mnz.tolist()                          # Obtener la lista de manzanas ordenada 
                    dfmelted_mnz = dfmelted_mnz.drop(columns=['agg_id'])                # Eliminar la columna agg_id
                    dfmelted_mnz = dfmelted_mnz.reset_index(drop=True)                  # Resetear el index
                    
                    # ------------------ LISTAS A EXPORTAR/ PROCESAR ------------------
                    df_AGR_list.append(dfmelted_mnp)                                    # Lista de los dataframes de cada simulacion (Municipio)
                    lnPAE85 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.85'].loss).values[0]
                    lnPAE15 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.15'].loss).values[0]
                    
                    agg_risk.append((lnPAE85-lnPAE15)/2)                                # Lista de las perdidas por simulacion (Municipio) 
                    
                    df_AGRmnz_list.append(dfmelted_mnz)                                 # Lista de los dataframes de cada simulacion (Aggregate by)
                    
                # ....................... Dataframes a utilizar .......................
                datos_CP = {'Num_Sim':Nsim2,'loss':agg_risk,'Num_Sim_Ev':Nevents,'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}
                # .....................................................................
                
                # 5). Obtener dataframe de perdidas para la manzana predominante y 
                # dataframe de error promedio entre datos adyacentes de las simulaciones
                
                # Se crea la lista que ira en el combo de las manzanas
                opciones_mnz, codigo_mnz = [], []
                for op in sorted_opcion:
                    codigo_mnz.append(op[:-5])
                for op in opcion_mnz:
                    opciones_mnz.append(op[-5:])
                
                # 5.1). Se generan los datos a graficar
                # Se debe obtener una lista con las perdidas promedio de una manzana en 
                # especifico por simulacion. En porcentaje
                lossnew, max_loss_manzana = [], []
                for ind, loss in enumerate(df_AGRmnz_list):
                    # Obtener una lista con los resultados del dataframe filtrado 
                    # solamente para los valores quantile 85 y 15
                    loss85n = loss[loss['stat'] == 'quantile-0.85']
                    loss15n = loss[loss['stat'] == 'quantile-0.15']
                    disp85,disp15 = [],[]
                    for ind2 in loss85n.index.tolist():
                        disp85.append(np.log(loss85n['loss'][ind2]))
                    for ind2 in loss15n.index.tolist():
                        disp15.append(np.log(loss15n['loss'][ind2]))
                        
                    Dispersion_values = []
                    for ind3 in range(len(disp15)):
                        Dispersion_values.append((disp85[ind3]-disp15[ind3])/2)
                    
                    loss_new = pd.DataFrame({'cod_mnz':mnz_list,'Dispersion':Dispersion_values})
                    lossnew.append(loss_new)
                    
                    # Otener la manzana predominante del municipio
                    max_loss_manzana.append(loss_new[loss_new['Dispersion']==loss_new['Dispersion'].max()])
                
                # Obtiene un dataframe cuyas columnas son las dispersiones por simulacion
                simmnz_losses = pd.concat([df.set_index('cod_mnz')['Dispersion'] for df in lossnew], axis=1).reset_index()     
                # Cambia el nombre de las columnas Dispersion por Sim_'numero de ses'
                nombres_simulaciones = ['Sim_{}'.format(i) for i in Nsim2]
                simmnz_losses.columns = ['Manzana'] + nombres_simulaciones
                # Obtener manzana predominante
                maxloss = max_loss_manzana[0]
                Mnz_Predeter = maxloss['cod_mnz'].values[0]
                newNsim_mnz = sorted(Nsim2)
                # Obtener los datos de la manzana predominante
                fila_a_graficar = simmnz_losses.loc[simmnz_losses['Manzana'] == Mnz_Predeter]
                # Cambia los titulos de las simulaciones por numeros
                fila_a_graficar = fila_a_graficar[['Manzana']+['Sim_{}'.format(i) for i in newNsim_mnz]]
                # Elimina la columna del codigo de la manzana
                fila_a_graficar = fila_a_graficar.drop(columns=['Manzana'])
                # Obtiene los valores de dispersion por simulacion
                datos_fila = fila_a_graficar.values[0]
                
                # ....................... Dataframes a utilizar .......................
                datos_MNZ = {'Num_Sim':newNsim_mnz,'loss':datos_fila,'Num_Sim_Ev':sorted(Nevents),'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}
                # .....................................................................
                
                # Definir dataframe taxonomias como None
                datos_TXN = None
                
                # Otras variables asiganas valor None
                Txn_Predeter = None
                opciones_txn = None
                codigo_txn = None
                simtxn_losses = None
                newNsim_txn = None
                
            elif len(agg_wh) == len(aggregate_type):
                
                """ -------------------------------------------------------------------
                                    Obtener datos del municipio
                ------------------------------------------------------------------- """
                # 3). Procesar datos del hdf5.
                Nsim2 = []                      # Numero de simulaciones
                Nevents = []                    # Numero de eventos
                agg_risk = []                   # Perdidas del municipio
                df_AGR_list = []                # Lista de los dataframes de cada simulacion (Municipio)
                for arch_hdf5 in archivos_hdf5:
                    ruta_hdf5 = arch_hdf5
                    # 3.1). Cargar archivos de entrada.
                    with h5py.File(ruta_hdf5, 'r') as archivo: 
                        oqparam_dict = json.loads(archivo["oqparam"][()].decode('utf-8'))  # Lista de parametros de OpenQuake
                        aggrisk_aggid = archivo["aggrisk"]["agg_id"][()]                # ID del agregado
                        aggrisk_loss = archivo["aggrisk"]["loss"][()]                   # Perdidas segun el aggregate ID
                        events = archivo["events"][()]                                  # eventos de la simulacion
                    
                    # ............. Lista de eventos y ses_per_logic_tree .............
                    Nevents.append(len(events))                                         # Numero de eventos
                    Nsim2.append(oqparam_dict['ses_per_logic_tree_path'])               # Numero de simulaciones
                    # .................................................................
                    
                    # ...................... Lista de quantiles .......................
                    list_stats = ['mean']
                    for quant in oqparam_dict['quantiles']:
                        list_stats.append('quantile-'+str(quant))                       # Lista de estadisticas
                    # .................................................................
                    
                    # ................... Nombre del centro poblado ...................
                    CP_Name = oqparam_dict['description'].split('-')[-1].strip()        # Nombre del centro poblado inicial
                    if CP_Name[0].islower():
                        CP_Name = CP_Name[0].upper() + CP_Name[1:]                      # Si el nombre del centro poblado no comienza con una mayuscula
                    # .................................................................
                    
                    # 3.2). Procesado:
                    df_group = pd.DataFrame({'agg_id':aggrisk_aggid, 'loss':aggrisk_loss})  # Dataframe perdidas por aggid
                    grp_aggid = df_group.groupby('agg_id')['loss']                          # Agrupa las perdidas por aggid
                    stats_agg = grp_aggid.describe(percentiles=oqparam_dict['quantiles'])   # Calcula mediana y percentiles de las perdidas por aggid
                    stats_agg.reset_index(level=0, inplace=True)                            # Genera un indice, agg_id se vuelve en columna
                    stats_agg_mnp = stats_agg[stats_agg['agg_id'] == oqparam_dict['K']]     # Genera un dataframe para municipio
                    stats_agg.drop(stats_agg_mnp.index, inplace=True)                       # Dataframe de perdidas por manzana o por manzana + taxonomia
                    stats_agg_mnp.reset_index(level=0, inplace=True)                        # Resetea el indice municipio
                    stats_agg.reset_index(level=0, inplace=True)                            # Resetea el indice agregado
                    # Agrupar por estadisticas
                    dfmelted_mnp = stats_agg_mnp.melt(id_vars=['agg_id'], value_vars=['mean', '15%', '50%', '85%'], var_name='stat', value_name='loss')
                    dfmelted_mnp['stat'] = dfmelted_mnp['stat'].replace({'15%': 'quantile-0.15', '85%': 'quantile-0.85', '50%': 'quantile-0.5'})
                    dfmelted_mnp = dfmelted_mnp.drop(columns=['agg_id'])                # Eliminar la columna agg_id
                    # -----------------------------------------------------------------
                    # ------------------ LISTAS A EXPORTAR/ PROCESAR ------------------
                    df_AGR_list.append(dfmelted_mnp)                                    # Lista de los dataframes de cada simulacion (Municipio)
                    lnPAE85 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.85'].loss).values[0]
                    lnPAE15 = np.log(dfmelted_mnp.loc[dfmelted_mnp.stat=='quantile-0.15'].loss).values[0]
                    
                    agg_risk.append((lnPAE85-lnPAE15)/2)                                # Lista de las perdidas por simulacion (Municipio) 
                                        
                # ....................... Dataframes a utilizar .......................
                datos_CP = {'Num_Sim':Nsim2,'loss':agg_risk,'Num_Sim_Ev':Nevents,'Event_Based':[oqparam_dict['calculation_mode']]*len(Nevents)}
                # .....................................................................
                
                # Definir dataframe taxonomias y manzanas como None
                datos_TXN = None
                datos_MNZ = None
                
                # Otras variables asiganas valor None
                Txn_Predeter = None
                opciones_txn = None
                codigo_txn = None
                simtxn_losses = None
                newNsim_txn = None
                
                # Otras variables asiganas valor None
                Mnz_Predeter = None
                opciones_mnz = None
                codigo_mnz = None
                simmnz_losses = None
                newNsim_mnz = None
                
            else: 
                warning = "En la carpeta hay uno o mas de un archivo agregado de manera diferente." 
                tk.messagebox.showinfo("ERROR", warning)
                
    return CP_Name,datos_CP,datos_MNZ,datos_TXN,Mnz_Predeter,Txn_Predeter,opciones_mnz,opciones_txn,codigo_mnz,codigo_txn,simmnz_losses,simtxn_losses,newNsim_mnz,newNsim_txn,Nevents


def carpetas_en_folder(rootdir1):
    Verifi_Mnz = None                # Verificar carpeta hdf5 agregados por manzana
    Verifi_Txn = None                # Verificar carpeta hdf5 agergados por taxonomia
    Verifi_Hdf5 = None               # Verificar hdf5s en carpeta

    for folder in os.listdir(rootdir1):                                         # Obtiene la lista de archivos en la carpeta 
        if "hdf5_Mnz" in folder:                                                # Si existe una carpeta llamada "hdf5_Mnz"
            Verifi_Mnz = 1
        else: 
            Verifi_Hdf5 = 1
        if "hdf5_Txn" in folder:                                                # Si existe una carpeta llamada "hdf5_Txn"
            Verifi_Txn = 1
        else: 
            Verifi_Hdf5 = 1
    # Si no esta la carpeta hdf5_Mnz
    if Verifi_Mnz is None and Verifi_Txn is not None:
        warning = "En la carpeta seleccionada no existe la carpeta 'hdf5_Mnz'." 
        tk.messagebox.showinfo("ERROR", warning)
    # Si no esta la carpeta hdf5_Txn
    if Verifi_Txn is None and Verifi_Txn is not None:
        warning = "En la carpeta seleccionada no existe la carpeta 'hdf5_Txn'." 
        tk.messagebox.showinfo("ERROR", warning)
        
    return Verifi_Mnz,Verifi_Txn,Verifi_Hdf5


