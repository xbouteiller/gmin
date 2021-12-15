

print('------------------------------------------------------------------------')
print('---------------                                    ---------------------')
print('---------------            gminComputation         ---------------------')
print('---------------                  V2.0              ---------------------')
print('---------------                                    ---------------------')
print('------------------------------------------------------------------------')

import numpy as np
import matplotlib.pyplot as plt
# from scipy import signal
# from loess.loess_1d import loess_1d
# from statsmodels.nonparametric.smoothers_lowess import lowess
import pandas as pd
import time
import sys
from scipy import stats
import os
from matplotlib import colors as mcolors
import re
import time  
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import configparser
import json
from itertools import compress

time.sleep(0.5)
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

# import matplotlib
# matplotlib.use("Qt5agg")



class ParseFile():
    import pandas as pd
    import numpy as np
    import re       

    def __init__(self, path, skipr=1, sepa=',', encod = "utf-8"):
        '''
        initialization
        path of the file
        skipfoot : number of rows to skip at the end of the txt file

        portability : allow manual definition of skiprows and delimiter
                    test the file format and provide the good function for reading the file
        '''

        try:
            self.file = pd.read_csv(path,sep=sepa, skiprows=skipr)
        except:
            self.file = pd.read_csv(path, skiprows=skipr, sep=sepa, encoding=encod)
    

    def clean_file(self):
        '''
        clean the file

        Currently do nothing but can be adapted in order to clean file individually
        '''        
        return self.file





class ParseTreeFolder(): 

    def _get_valid_input(self, input_string, valid_options):
        '''
        useful function in order to ask input value and assess that the answer is allowed

        input_string : question
        valid_options : authorized answers
        '''
        input_string += "({}) ".format(", ".join(valid_options))
        response = input(input_string)
        while response.lower() not in valid_options:
            response = input(input_string)
        return response


    def __init__(self,                
                time_col, 
                sample_id,
                yvar,
                temp,
                rh,
                patm,
                area,               
                rwc_sup,
                rwc_inf,
                fresh_weight,
                dry_weight,
                screen_move
                ):

        self.TIME_COL = time_col
        self.SAMPLE_ID = sample_id
        self.YVAR = yvar
        self.T = temp
        self.RH = rh
        self.PATM = patm
        self.AREA = area   

        self.FW = fresh_weight
        self.DW = dry_weight  

        self.rwc_sup = rwc_sup
        self.rwc_inf = rwc_inf

        self.screen_move = screen_move

       

        # global class variables
        self.global_score = []        

        
        self._parse_conf() 

        self.col_T = json.loads(self.parser.get("config", "col_T"))
        #print(self.col_T)
        self.col_RH = json.loads(self.parser.get("config", "col_RH"))
        #print(self.col_RH)
        self.col_comment = json.loads(self.parser.get("config", "col_comment"))
        #print(self.col_comment)
        self.col_campaign = json.loads(self.parser.get("config", "col_campaign"))

        self.dateformat = self.parser.get("config", "dateformat")
        #print(self.dateformat)
        #time.sleep(1)
        #print(self.col_campaign + self.col_comment)
        self.col_date = json.loads(self.parser.get("config", "col_date"))

        self.outputpath = self.parser.get("config", "outputpath")

        self.use_opt = self.parser.get("optional", "use_opt")
        assert self.use_opt in ['True', 'False'], 'use_opt should be one True or False'

        self.lag = int(self.parser.get("batch", "lag"))
        self.limsup = int(self.parser.get("batch", "limsup"))
        self.liminf = int(self.parser.get("batch", "liminf"))
        self.delta = int(self.parser.get("batch", "delta"))

        if self. use_opt == 'True':
            self.path = self.parser.get("optional", "path")
            self.method = self.parser.get("optional", "method")
            assert  self.method in ['manual','semi','full', 'batch'], 'method should be one of manual, semi, full, batch' 
            self.metadata_path = self.parser.get("optional", "metadata") 
            self.file_or_folder = '1'
        else:
            print('''
            >>> What do you want to do ? 
            1: Parse all files from a folder
            2: Select some ID from a file)
            ''')        
            self.file_or_folder = self._get_valid_input('What do you want to do ? Choose one of : ', ('1','2'))

            print('''
            >>> Select the folder or the file that will be analyzed       
            ''')  
            time.sleep(0.5)
            if self.file_or_folder== '1':
                root_path = os.getcwd()
                Tk().withdraw()
                folder = askdirectory(title = 'What is the root folder that you want to parse ?',
                                    initialdir = root_path)            
                self.path = folder
                print('root path is {}'.format(self.path))
                print('\n')
                
            if self.file_or_folder== '2':
                Tk().withdraw()
                file = askopenfilename(title='What is the file that you want to check ?')
                self.path = file.replace('/','/')
                print('file path is {}'.format(self.path)) 
                print('\n')

            print('''            
            >>> Select the metadata file that will be analyzed       
            ''')  
            time.sleep(0.5)
            Tk().withdraw()
            file = askopenfilename(title='What is the metdata file ?')
            self.metadata_path = file.replace('/','/')
            print('Metadata file path is {}'.format(self.metadata_path)) 
            print('\n')



        # options allowed for the action method    
        self.choices = {
        "1": self._execute_computation,
        "2": self._execute_computation,
        "3": self._execute_computation,
        "4": self._batch_mode,
        "5": self._quit
        }    

    def _batch(self):
        pass   

    def _parse_conf(self):
        '''
        parse the conf file
        '''
        # TO DO ALLOW .CFG IN DATA FOLDER        
        self.parser = configparser.ConfigParser()
        self.parser.read("conf.cfg") 

    def _listdir_fullpath(self, p, s):
        '''
        method for creating a list of csv file
        '''

        d=os.path.join(p, s)
        return [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.csv')]

    
    def parse_folder(self):
        '''
        parse the folder tree and store the full path to target file in a list
        '''

        if self.file_or_folder=='2':
            self.listOfFiles=[[self.path]]


        if self.file_or_folder=='1':
            file_root=[]
            self.listOfFiles = []

            # method with csv detection            
            try:
                # basedir
                file_root = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith('.csv') and f.lower() != 'metadata.csv']
                self.listOfFiles.append(file_root)
                #print(file_root)
            except:
                print('no file detected within root directory')
                pass

            try:
                #subfolders
                for pa, subdirs, files in os.walk(self.path):
                    for s in subdirs:
                        self.listOfFiles.append(self._listdir_fullpath(p=pa, s=s))
            except:
                print('no file detected within childs directory')
                pass       

            print('\n')
            try:
                [print("-found : {0} matching files in folder {1}".format(len(i),j)) for i,j in zip(self.listOfFiles, range(1,len(self.listOfFiles)+1))]
                print('\n')
            except:
                print('no files detected at all')
                print('\n')
                pass

            time.sleep(1)

            return self.listOfFiles


    def display_menu(self):
        print("""
        --------------------
        -----   MENU   -----
        --------------------

        List of actions

        1. Select points on curve
        2. Compute gmin between RWC boundaries (semi auto)
        3. Compute gmin between RWC boundaries (full auto)
        4. Batch mode
        5. Exit


        """)
    
    def run(self):
        '''Display the menu and respond to choices.'''

        if self.use_opt == 'True':
            dictkey = {'manual':'1', 
            'semi':'2', 
            'full':'3',
            'batch': '4'}
            choice = dictkey[self.method]

            action = self.choices.get(choice)

            self.action_choice = choice
            

            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))
                self.run()

        else:
            self.firstchoice = 0
            while True:
                self.display_menu()
                if self.firstchoice == 0:
                    choice = input("Enter an option: ")
                else:
                    choice = '5'

                # redirection to the self.choices attribute in the __init__
                action = self.choices.get(choice)
                self.action_choice = choice

                if action:
                    action()
                else:
                    print("{0} is not a valid choice".format(choice))
                    self.run()
                self.firstchoice += 1


    def _quit(self):
        print("Thank you for using your gminComputation today.\n")
        sys.exit(0)

    def _evaluate_file(self, elem, skip):
        try:
            dffile = ParseFile(path = elem, skipr=skip).clean_file()
        except:
            encodi='latin'
            dffile = ParseFile(path = elem, skipr=skip, encod=encodi).clean_file()
            
        if dffile.shape[1] == 1:                
            separ=';'
            try:
                dffile = ParseFile(path = elem, sepa=separ, skipr=skip).clean_file()
            except:
                encodi='latin'
                dffile = ParseFile(path = elem, skipr=skip, sepa=separ, encod=encodi).clean_file()

        return dffile

    def _construct_file(self, df):
        #print(df.head())  
        colagreg = self.col_campaign + self.col_comment + self.col_T + self.col_RH
        test = [i in df.columns for i in colagreg]
        assert all(test), '{} is not in df column'.format(list(compress(colagreg,[not elem for elem in test])))

        df[self.T] =df[self.col_T].mean(axis = 1)
        df[self.RH] =df[self.col_RH].mean(axis = 1)

        assert len(self.col_date) == 1, 'col date should be be an unique column'
        df[self.TIME_COL] = df[self.col_date]

        #print(df.columns)
        df = df.drop(columns= colagreg)

        #print(df.head())
        return df

    def _check_metadata(self, df):
        dfmeta = self._evaluate_file(elem = self.metadata_path, skip = 0)
   
        expectedcol = [self.SAMPLE_ID , 'position', 'species', self.AREA , self.PATM, self.FW , self.DW  , 'rwc_sup' , 'rwc_inf' , 'a', 'b', 'c', 'd', 'e', 'eps', 'p0', 'TLP']
        #print(dfmeta.columns)
        test = [i in dfmeta.columns for i in expectedcol]
        assert all(test), 'Expecting missing column(s): {} in metadata file, please add it, even if empty'.format(list(compress(expectedcol,[not elem for elem in test])))

        return dfmeta


    def _robust_import(self, elem):

        '''
        try to open a csv file using several methods
        should be relatively robust
        future : robustness could be improved

        use parsefile class        
        '''

        skip = 0
        if self.file_or_folder == '2': 
            pass
            # TO BE REFOUNDED
            # dffile = self._evaluate_file(elem = elem, skip = skip)         

            # uniqueid = dffile[self.SAMPLE_ID].unique()
            # print('''
            # Unique ID within selected file are: 
            # {}
                        
            # '''.format(uniqueid))
            
            # listodidtoanalyse = []   
            # count = 0
            # idtoanalyse = ''
            # while True:
            #     while ((idtoanalyse not in uniqueid) and (idtoanalyse not in ['exit', 'e'])):
            #         idtoanalyse = input("\nwhich ID do you want to analyse ?\nPlease select one among:\n{}\nEnter --exit-- to stop\n\nYour choice: ".format(uniqueid))
            
            #     if  idtoanalyse in uniqueid:
            #         print(' \nAppending : {}'.format(idtoanalyse))
            #         listodidtoanalyse.append(idtoanalyse)
            #         count += 1
            #         idtoanalyse = ''
                        
            #     elif (idtoanalyse == 'exit' or idtoanalyse == 'e'):
            #         if count>0:
            #             print(' \nExiting')
            #             break
            #         else:
            #             print('\nYou need to choose at least one ID before')
            #             idtoanalyse = ''            
                
            
            # boollistofid = [True if id in listodidtoanalyse else False for id in dffile[self.SAMPLE_ID] ]
            # dffile = dffile[boollistofid].copy()
            # print('\nselected ID are: {}'.format(dffile[self.SAMPLE_ID].unique()))                        

        if self.file_or_folder == '1':            
            dffile = self._evaluate_file(elem = elem, skip = skip) 
            dffile = self._construct_file(dffile)

        return dffile
        

    def _create_saving_folder(self):
        from datetime import date

        today = date.today()
        d4 = today.strftime("%b-%d-%Y")
        
        if self.outputpath == 'None':
            self.outputpath = os.getcwd()            

        if self.batchactivated == 'batch':
            if not os.path.exists(os.path.join(self.outputpath, 'batch')): 
                self.outputpath = os.path.join(self.outputpath, 'batch')

        try:
            self.fig_folder
        except:
            self.fig_folder = 'None'

        if self.fig_folder == 'None':
            starting_name = str(d4)+'_'+'output_fig'
            i = 0
            while True:
                i+=1
                fig_folder = os.path.join(self.outputpath,starting_name+'_'+str(i))
                if not os.path.exists(fig_folder):
                    os.makedirs(fig_folder)
                    os.makedirs(fig_folder+'/'+'gmin')
                    # os.makedirs(fig_folder+'/'+'diff')
                    os.makedirs(fig_folder+'/'+'rwc')
                    break
            self.fig_folder = fig_folder 

        try:
            temp_name = self.rep_name                
        except:
            self.rep_name = 'None'
        
        if self.rep_name == 'None':
            starting_name = os.path.join(self.outputpath,str(d4)+'_'+'output_files')
            i = 0
            while True:
                i+=1
                temp_name = starting_name+'_'+str(i)
                if not os.path.exists(temp_name):
                    os.makedirs(temp_name)
                    break
            self.rep_name = temp_name

    def _match_metadata(self, df, pos):            

        df = pd.merge(df, self.dfmeta, on="position")
        df = df.dropna(subset = [self.TIME_COL]).reset_index(drop= True)
        df = df.rename(columns = {pos:self.YVAR})
        print(df.head())
        return df


    def _execute_computation(self):
        '''
        parse all the files within the folder tree       
        '''

        print('\nStarting Gmin computation\n')

        
        from .gmincomputation import gminComput

        print('\nchoices is {}\n'.format(self.action_choice ))

        self._create_saving_folder()

        dimfolder = len(self.listOfFiles)
        # li_all = []
        list_of_df = []
        global_score = []

        self.dfmeta = self._check_metadata(self.metadata_path)
        # print(self.listOfFiles)
        # time.sleep(2)

        for d in np.arange(0,dimfolder):
            print('\n\n\n---------------------------------------------------------------------')
            print(d)            
            
            try:
                self.presentfile=self.listOfFiles[d][0]
            except:
                self.presentfile = 'No file'            
            
            print('parsing list of files from : {}'.format(self.presentfile))

            if self.presentfile != 'No file':
                for elem in self.listOfFiles[d]:
                    dffile = self._robust_import(elem)
                    # remove the .csv extension from the name                    
                    temp_folder = os.path.splitext(str(os.path.basename(elem)))[0]  
                    # print('tf1: ', temp_folder)                 

                    for pos in [c for c in dffile.columns if c != self.T and c != self.RH and c != self.TIME_COL]:
                        assert pos in self.dfmeta.position.to_list(), 'position {} not in the column position of metadata file'.format(pos)

                        df = dffile.loc[:,[self.TIME_COL,self.T , self.RH, pos]]
                        
                        df[['position']] = pos
                        print(df.head())

                        assert len(list(compress(self.dfmeta.position,self.dfmeta.position == pos))) == 1, 'More than one col have the same position' 
                        df = self._match_metadata(df, pos)

                        self.sample = df[self.SAMPLE_ID].unique()[0]
                        print(self.sample)
                        #df = dffile.loc[dffile[self.SAMPLE_ID]==sample,:].copy().reset_index()
                        df_bak = df.copy()
                        # Analysing
                        print('Analysing: {}'.format(self.sample))

                        # initialising gmin computation class
                        gmc = gminComput(self.TIME_COL,
                                        self.SAMPLE_ID,
                                        self.YVAR,
                                        self.T,
                                        self.RH,
                                        self.PATM,
                                        self.AREA,
                                        self.rwc_sup,
                                        self.rwc_inf, 
                                        self.action_choice,
                                        self.fig_folder,
                                        self.rep_name,
                                        self.FW,
                                        self.DW,
                                        self.screen_move,
                                        self.dateformat)
                        # computing time delta
                        df = gmc._compute_time_delta(df)

                        # computing RWC
                        if 1>0:#(self.action_choice == '2') | (self.action_choice == '3'):
                            print('Computing RWC')
                            if self.action_choice == '2':
                                df, t80, t50, rwc_sup, rwc_inf, method_of_dfw= gmc._compute_rwc(df)
                            else:
                                df, t80, t50, rwc_sup, rwc_inf, method_of_dfw = gmc._compute_rwc(df, visualise = False)
                            # self.t80 = t80
                            # self.t50 = t50
                        else:
                            t80 = None
                            t50 = None
                            rwc_sup = None
                            rwc_inf = None
                            method_of_dfw = None

                        # plotting gmin
                        gs, selected_points, relaunch = gmc._plot_gmin(df,t80, t50)


                        # Creating a backup of action choice
                        action_choice_bak = self.action_choice


                        if relaunch:
                             # initialising gmin computation class
                            df = df_bak.copy()
                            self.action_choice = '1'
                            gmc = gminComput(self.TIME_COL,
                                            self.SAMPLE_ID,
                                            self.YVAR,
                                            self.T,
                                            self.RH,
                                            self.PATM,
                                            self.AREA,
                                            self.rwc_sup,
                                            self.rwc_inf, 
                                            self.action_choice,
                                            self.fig_folder,
                                            self.rep_name,
                                            self.FW,
                                            self.DW,
                                            self.screen_move)

                            print('choice: ', gmc.action_choice)
                            # computing time delta
                            df = gmc._compute_time_delta(df)

                            # computing RWC
                            if 1>0:#(self.action_choice == '2') | (self.action_choice == '3'):
                                print('Computing RWC')
                                if self.action_choice == '2':
                                    df, t80, t50, rwc_sup, rwc_inf, method_of_dfw= gmc._compute_rwc(df)
                                else:
                                    df, t80, t50, rwc_sup, rwc_inf, method_of_dfw = gmc._compute_rwc(df, visualise = False)
                                # self.t80 = t80
                                # self.t50 = t50
                            else:
                                t80 = None
                                t50 = None
                                rwc_sup = None
                                rwc_inf = None
                                method_of_dfw = None

                            # plotting gmin
                            gs, selected_points, relaunch = gmc._plot_gmin(df,t80, t50)

                            

                        if (self.action_choice == '1'):
                            t80 = np.max(selected_points[0][0],0)
                            t50 = selected_points[1][0]



                        gs.extend([rwc_sup, rwc_inf, t80, t50, method_of_dfw])
                        # print('gs: ', gs)

                       

                        global_score.append(gs)   

                        temp_df = pd.DataFrame(global_score, columns = ['Sample_ID', 'Interval_time','slope', 'Rsquared', 'Gmin_mean', 'pack',\
                             'percentage_rwc_sup', 'percentage_rwc_inf', 'time_sup', 'time_inf', 'method_of_rwc'])
                        temp_df2 = pd.DataFrame(temp_df["pack"].to_list(), columns=['K', 'VPD', 'mean_T', 'mean_RH', 'mean_Patm', 'mean_area'])
                        temp_df = temp_df.drop(columns='pack')
                        temp_df = pd.concat([temp_df,temp_df2], axis = 1)

                        # print('tf2: ', temp_folder) 
                        temp_df['Campaign'] = temp_folder

                        temp_df = temp_df.drop(columns='Interval_time')
                        temp_df = temp_df[['Campaign','Sample_ID', 'Gmin_mean', 'percentage_rwc_sup', 'percentage_rwc_inf', 'time_sup', 'time_inf', 'method_of_rwc', \
                                            'slope', 'Rsquared', 'K', 'VPD', 'mean_T', 'mean_RH', 'mean_Patm', 'mean_area']]
                        

                        # PROBLEM HERE ##################
                        # temp_df['percentage_rwc_sup']=rwc_sup
                        # temp_df['percentage_rwc_inf']=rwc_inf

                        # temp_df['time_rwc_sup']=t80
                        # temp_df['time_rwc_inf']=t50
                        ################################

                        if (self.action_choice == '2') | (self.action_choice == '3'):
                            temp_df['Mode']='RWC filtered'                             
                        else:
                            temp_df['Mode']='Manual Selection'

                        print('\n')

                        # append df to list
                        list_of_df.append(temp_df)
                        # print(pd.concat(list_of_df))
                        # global_score = []
                        pd.concat(list_of_df).reset_index().drop_duplicates(subset=['Campaign','index','Sample_ID','slope']).drop(columns='index').to_csv(self.rep_name+'/GMIN_df_complete.csv', index = False)
                        # time.sleep(1)
                        # print('saved !') 
                        # 
                        #  Resetting action choice to initial value
                        self.action_choice = action_choice_bak



                    global_score = []
            else:
                pass

        # save the appended df in a global file
        # explode remove the square bracket [] from cells and convert to multiline
        # pd.concat(list_of_df).reset_index().explode('Interval_time').to_csv(self.rep_name+'/RMSE_df_complete_full.csv')
        # pd.concat(list_of_df).reset_index().explode('Interval_time').to_csv(self.rep_name+'/RMSE_df_complete_full.csv')
        # pd.concat(list_of_df).reset_index().explode('Interval_time').drop_duplicates(subset=['Campaign','index','Sample_ID','slope']).to_csv(self.rep_name+'/RMSE_df_complete_full_No_duplicates.csv')
        pd.concat(list_of_df).reset_index().drop_duplicates(subset=['Campaign','index','Sample_ID','slope']).drop(columns='index').to_csv(self.rep_name+'/GMIN_df_complete.csv', index = False)

    def _batch_mode(self):
        self.action_choice = '3'
        self.batchactivated = 'batch'
     
        for rwc in range(self.limsup, self.liminf, -self.lag):
            #print(rwc)
            self.rwc_sup = rwc + self.delta//2
            self.rwc_inf = rwc - self.delta//2
            self._execute_computation()

        # HERE MERGE FILE
        

                        
