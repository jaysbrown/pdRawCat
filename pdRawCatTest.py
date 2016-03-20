# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 12:13:14 2016

@author: jsbrown
"""

import pdRawCat
import unittest
import os

print('Current working directory: {}'.format(os.getcwd()))

class KnownInput(unittest.TestCase):
    
    TestPath = os.path.join(os.getcwd(),'Input_Test','RawJobs',)
    #print('TestPath={}'.format(TestPath))
    TestJobPattern = r'JobTest.*'
    #TestSamPattern = r'.*'
    TestSamPattern = r'untitled.*'
    TestJobsDict = {'JobTest1':[os.path.join(TestPath,'JobTest1','untitled2.csv',)
                                ,os.path.join(TestPath,'JobTest1','untitled3.csv',)]
                    ,'JobTest2':[os.path.join(TestPath,'JobTest2','untitled4.csv',)
                                ,os.path.join(TestPath,'JobTest2','untitled5.csv',)]}
    
    def test_known_input_jobs(self):
        '''pdRawCat.get_raw_files should return a dictionary with keys JobTest1 and JobTest2 testing dictionary keys and explicit dictionary match'''
        result = pdRawCat.get_raw_files(self.TestPath, self.TestJobPattern, self.TestSamPattern)[0]
        self.assertDictEqual(self.TestJobsDict,result)
        self.assertIn('JobTest1',result)
        self.assertIn('JobTest2',result)
        self.assertIn(os.path.join(self.TestPath,'JobTest2','untitled4.csv',),result['JobTest2'])
    
    def test_known_input_files(self):
        '''pdRawCat.get_raw_files should find 4 Input Files'''
        result = pdRawCat.get_raw_files(self.TestPath, self.TestJobPattern, self.TestSamPattern)[1]
        self.assertEqual(4,result)
        
class BadInput(unittest.TestCase):

    TestPath = os.path.join(os.getcwd(),'Input_Test','RawJobs',)    
    #print('TestPath={}'.format(TestPath))
    TestJobPattern = r'JobTest.*'
    #TestSamPattern = r'.*'
    TestSamPattern = r'untitled.*'
    TestMismatchJobPattern = r'OtherPattern'
    TestMismatchSamPattern = r'OtherPattern'
    
    EmptyTestPath = os.path.join(os.getcwd(),'Input_Test','NoRawJobs',)
    
    MissingDataJobPath = os.path.join(os.getcwd(),'Input_Test','MissingDataRawJob',)
    
    def test_bad_dir(self):
        '''pdRawCat.get_raw_files should raise NoDirError exception if bad directory is called'''
        self.assertRaises(pdRawCat.NoDirError, pdRawCat.get_raw_files, '','','')
    
    def test_unknown_filetype(self):
        '''pdRawCat.get_raw_files should raise FileTypeError exception if called with unknown file type'''
        self.assertRaises(pdRawCat.FileTypeError, pdRawCat.get_raw_files, self.TestPath, self.TestJobPattern, self.TestSamPattern,'crazyunknownfileext')
    
    def test_empty_raw_jobs(self):
        '''pdRawCat.get_raw_files should raise NoDirError exception if no InputJobs are found in called folder'''
        self.assertRaises(pdRawCat.NoDirError, pdRawCat.get_raw_files, self.EmptyTestPath, self.TestJobPattern, self.TestSamPattern)
        
    def test_no_raw_files(self):
        '''pdRawCat.get_raw_files should raise NoFileError exception if no Input Raw files are found in any individual Job folder'''
        self.assertRaises(pdRawCat.NoFileError, pdRawCat.get_raw_files, self.MissingDataJobPath, self.TestJobPattern, self.TestSamPattern)
        
    def test_mismatch_job_pattern_to_input_jobs(self):
        '''pdRawCat.get_raw_files should raise JobPatternMismatchError exception if no Job Folders match job_pattern'''
        self.assertRaises(pdRawCat.JobPatternMismatchError, pdRawCat.get_raw_files, self.TestPath, self.TestMismatchJobPattern, self.TestSamPattern)
        
    def test_mismatch_sample_pattern_to_input_samples(self):
        '''pdRawCat.get_raw_files should raise SamplePatternMismatchError exception if any Job Folder contains *NO* samples matching sample_pattern'''
        self.assertRaises(pdRawCat.SamplePatternMismatchError, pdRawCat.get_raw_files, self.TestPath, self.TestJobPattern, self.TestMismatchSamPattern)

if __name__=='__main__':
    unittest.main()


    