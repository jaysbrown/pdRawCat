# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 12:16:45 2016

@author: jmac
"""

import glob
import os
import re
import pandas as pd

class NoDirError(Exception):
    pass

class NoFileError(Exception):
    pass

class FileTypeError(Exception):
    pass

class JobPatternMismatchError(Exception):
    pass

class SamplePatternMismatchError(Exception):
    pass

def remove_nonmatch(string_list,re_pattern):
    ''' Given a list of strings and re_pattern, iterate through list and remove non-matching items
        Return string_list with non-matches removed and compiled re_pattern
    '''
    
    pattern = re.compile(re_pattern)    
    MismatchList = []
    
    for item in string_list:
        if pattern.search(item) == None:
            #print('.....Removed job={0} \n.......did not match re_job_pattern={1}'.format(j.replace(folder,''),re_job_pattern))
            MismatchList.append(item)
        #else: print('kept job={}'.format(j))
            
    for r in MismatchList:
        string_list.remove(r)
    
    return string_list,pattern

def get_raw_files(folder,re_job_pattern=r'.*',re_sample_pattern=r'.*',raw_file_type='csv',names=None):
    ''' Glob searches in folder path for job folders to match re_job_pattern, excludes non-matches
        then for each job_folder, glob searches for sample files of type raw_file_type, 
        excludes sample files that do not match re_sample_pattern
        raw_file_types handled ('csv' or 'xlsx')
        Return InputFilesDict, with Jobs as keys, values are list of sample files for each each job
        With InputFilesDict, uses pd.read_ to create individual dataframes by sample (uses re_sample_pattern)
        Concatenates individual dataframes with multilevel index by sample,index and stores these 
        df in a dictionary by job as key in CatDFDict which is returned
        Concatenates all raw files into a multi-level index by Job, Sample, Index and returns this as BigDF

                a. Exceptions Raised:
                    i. folder path does not exist
                    ii. called file type is not 'csv' or 'xlsx'
                    iii. no job folders in search path
                    iv. no job folders matching re_job_pattern
                    v. no matching data files in any job folder for re_sample_pattern
    '''
    
    if not os.path.exists(folder): 
        raise NoDirError('folder={} does not exist'.format(folder))
    
    FileTypeDict = {'csv':'*.csv','xlsx': '*.xlsx'}
                    
    if not raw_file_type in FileTypeDict.keys(): 
        raise FileTypeError("Unsupported File Type={}\nSupported File Types: \n..'csv'\n..'xlsx'".format(raw_file_type))
    
    print('\n pdRawCat_Inputs \n..folder={}'.format(folder))
    
    SearchPath = os.path.join(folder,'*',)
    print('...SearchPath = {}'.format(SearchPath.replace(folder,'')))
    
    InputJobs = glob.glob(SearchPath)
    
    if len(InputJobs) == 0: 
        raise NoDirError('No Input Job folders found in SearchPath={}'.format(SearchPath))
    print('....Found {} InputJobs'.format(len(InputJobs)))
    
    InputJobs,JobPattern = remove_nonmatch(InputJobs,re_job_pattern)

    if len(InputJobs) == 0:
        raise JobPatternMismatchError('No job folders remained after removing non-matching Jobs from re_job_pattern={} '.format(re_job_pattern))
    
    
    InputFilesDict={}
    InputFilesCount=0
    
    for jobfolder in InputJobs:
        job=JobPattern.search(jobfolder).group()
        print('.....job{0}={1}'.format(InputJobs.index(jobfolder)+1,job))
        files = glob.glob(os.path.join(jobfolder,FileTypeDict[raw_file_type],))
        print('......number of files found={}'.format(len(files)))
        
        if len(files)==0: 
            raise NoFileError('No files found in any Job folders')
        
        files,samplePattern = remove_nonmatch(files,re_sample_pattern)
        
        if len(files)==0: 
            raise SamplePatternMismatchError('No sample files remained in jobfolder={} \n..after removing non-matching Jobs from re_sample_pattern={} '.format(job,re_sample_pattern))
        
        for f in files: 
            print('.......file{0}={1}'.format(files.index(f)+1,f.replace(jobfolder,'')))
        InputFilesDict[job]=files
        InputFilesCount+=len(files)
    
    CatDFDict={}        
    for k in InputFilesDict:
        SamDFDict={}
        for s in InputFilesDict[k]:
            sample=samplePattern.search(s).group()
            if raw_file_type == 'csv':
                SamDF = pd.read_csv(s,names=names)
                SamDF['Sample']=sample
                SamDF['Job']=k
            if raw_file_type == 'xlsx':
                SamDF = pd.read_excel(s)
            SamDFDict[sample]=SamDF
        CatDF=pd.concat(SamDFDict, keys=SamDFDict.keys(), names=['Sample','Index'])
        CatDFDict[k]=CatDF
    BDF=pd.concat(CatDFDict,keys=CatDFDict.keys(), names=['Job','Sample','Index'])
        
    return InputFilesDict,InputFilesCount,BDF,CatDFDict
    
   
if __name__=='__main__':
    
    TestPath = os.path.join(os.getcwd(),'Input_Test','RawJobs',)
    TestJobPattern = r'JobTest.*'
    TestSamPattern = r'untitled.*'
    
    Dict,FileCount,BigDF,CatDFDict=get_raw_files(TestPath,TestJobPattern,TestSamPattern,raw_file_type='csv')