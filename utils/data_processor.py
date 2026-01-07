"""
Modul untuk pemrosesan data umum
"""
import pandas as pd
import numpy as np
import streamlit as st
from utils.leger_cleaner import clean_leger_data, calculate_basic_statistics

def clean_data(df):
    """Membersihkan data dari nilai null dan duplikat"""
    # Hapus duplikat
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.fillna(method='ffill')
    
    return df


def preprocess_student_data(df):
    """Preprocessing data siswa"""
    # Implementasi preprocessing
    return df


def load_and_process_excel(file, file_type='leger'):
    """
    Load dan proses file Excel berdasarkan tipe
    
    Parameters:
    -----------
    file : UploadedFile
        File yang diupload melalui Streamlit
    file_type : str
        Tipe file: 'leger', 'siswa', 'nilai', 'presensi'
    
    Returns:
    --------
    df : DataFrame
        Data yang sudah diproses
    stats : dict
        Statistik data
    """
    
    try:
        if file_type == 'leger':
            # Simpan file sementara
            temp_path = f"temp_{file.name}"
            with open(temp_path, 'wb') as f:
                f.write(file.getbuffer())
            
            # Bersihkan data leger
            df_clean = clean_leger_data(temp_path)
            
            # Hapus file temporary
            import os
            os.remove(temp_path)
            
            # Hitung statistik
            stats = calculate_basic_statistics(df_clean)
            
            return df_clean, stats
        
        else:
            # Untuk file lainnya, baca langsung
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Bersihkan data
            df = clean_data(df)
            
            return df, {}
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return pd.DataFrame(), {}