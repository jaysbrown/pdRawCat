# pdRawCat
Concat Raw Files Return Pandas DataFrame

docstring from get_raw_files:

Glob searches in folder path for job folders to match re_job_pattern, excludes non-matches
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

