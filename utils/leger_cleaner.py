"""
Modul untuk membersihkan data leger nilai rapor dari format Excel ke format tidy
"""
import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

def clean_leger_data(file_path, sheet_name=None):
    """
    Fungsi utama untuk membersihkan data leger nilai rapor
    
    Parameters:
    -----------
    file_path : str
        Path ke file Excel
    sheet_name : str, optional
        Nama sheet (default: sheet pertama)
    
    Returns:
    --------
    df_clean : DataFrame
        Data dalam format long/tidy yang siap untuk analisis
    """
    
    try:
        # Load data dari Excel
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        else:
            df = pd.read_excel(file_path, header=None)
        
        # Jika df adalah dictionary (multiple sheets), ambil sheet pertama
        if isinstance(df, dict):
            df = df[list(df.keys())[0]]
        
        # Find data start position
        data_start = 0
        for i in range(len(df)):
            row_text = ' '.join([str(val).upper() for val in df.iloc[i].values if pd.notna(val)])
            if 'SMT1' in row_text or 'SMT2' in row_text:
                data_start = i + 1
                break
        
        # Extract data
        df_data = df.iloc[data_start:].reset_index(drop=True)
        
        # Initialize list untuk menyimpan data
        data_list = []
        
        # Process setiap baris
        for idx, row in df_data.iterrows():
            # Ambil identitas siswa
            no = row.iloc[0]
            nama = row.iloc[1]
            nisn = row.iloc[2]
            nis = row.iloc[3]
            
            # Skip jika baris kosong
            if pd.isna(no) or pd.isna(nama):
                continue
            
            # Clean identitas
            try:
                no = int(float(no))
                nisn = str(int(float(nisn))) if pd.notna(nisn) else None
                nis = str(int(float(nis))) if pd.notna(nis) else None
                nama = str(nama).strip()
            except:
                continue
            
            # Process nilai dari kolom 4 sampai akhir
            # Asumsi: setiap 7 kolom = 1 mata pelajaran (Smt1-6 + Rerata)
            col_idx = 4
            mapel_num = 1
            
            while col_idx < len(row):
                # Ambil 7 kolom untuk 1 mata pelajaran
                for i in range(7):
                    if col_idx + i >= len(row):
                        break
                    
                    nilai = row.iloc[col_idx + i]
                    
                    if pd.notna(nilai):
                        try:
                            # Convert nilai (handle koma)
                            if isinstance(nilai, str):
                                nilai = float(nilai.replace(',', '.'))
                            else:
                                nilai = float(nilai)
                            
                            # Validasi range
                            if 0 <= nilai <= 100:
                                # Tentukan komponen
                                if i < 6:
                                    komponen = f"Smt{i+1}"
                                    semester = i + 1
                                    is_rerata = False
                                else:
                                    komponen = "Rerata"
                                    semester = 0
                                    is_rerata = True
                                
                                data_list.append({
                                    'NO': no,
                                    'NAMA_SISWA': nama,
                                    'NISN': nisn,
                                    'NIS': nis,
                                    'MAPEL_ID': f"Mapel_{mapel_num}",
                                    'KOMPONEN': komponen,
                                    'SEMESTER': semester,
                                    'NILAI': nilai,
                                    'IS_RERATA': is_rerata
                                })
                        except:
                            pass
                
                col_idx += 7
                mapel_num += 1
        
        # Create DataFrame
        df_clean = pd.DataFrame(data_list)
        
        # Optimize dtypes
        if not df_clean.empty:
            df_clean['NO'] = df_clean['NO'].astype('int16')
            df_clean['SEMESTER'] = df_clean['SEMESTER'].astype('int8')
            df_clean['NILAI'] = df_clean['NILAI'].astype('float32')
            df_clean['IS_RERATA'] = df_clean['IS_RERATA'].astype('bool')
            df_clean['MAPEL_ID'] = df_clean['MAPEL_ID'].astype('category')
            df_clean['KOMPONEN'] = df_clean['KOMPONEN'].astype('category')
        
        return df_clean
        
    except Exception as e:
        st.error(f"Error dalam membersihkan data: {str(e)}")
        return pd.DataFrame()


def calculate_basic_statistics(df_clean):
    """
    Menghitung statistik dasar dari data yang sudah dibersihkan
    """
    if df_clean.empty:
        return {}
    
    stats = {
        'total_records': len(df_clean),
        'total_students': df_clean['NISN'].nunique(),
        'total_subjects': df_clean['MAPEL_ID'].nunique(),
        'total_semesters': df_clean['SEMESTER'].nunique() - 1,  # tanpa 0 untuk rerata
        'nilai_mean': df_clean['NILAI'].mean(),
        'nilai_std': df_clean['NILAI'].std(),
        'nilai_min': df_clean['NILAI'].min(),
        'nilai_max': df_clean['NILAI'].max(),
    }
    
    # Grade distribution
    bins = [0, 60, 70, 80, 90, 100]
    labels = ['E (<60)', 'D (60-70)', 'C (70-80)', 'B (80-90)', 'A (90-100)']
    grades = pd.cut(df_clean['NILAI'], bins=bins, labels=labels)
    stats['grade_distribution'] = grades.value_counts().to_dict()
    
    return stats


def create_student_summary(df_clean):
    """
    Membuat summary per siswa dari data yang sudah dibersihkan
    """
    if df_clean.empty:
        return pd.DataFrame()
    
    # Filter hanya nilai rerata
    df_rerata = df_clean[df_clean['IS_RERATA'] == True]
    
    if df_rerata.empty:
        return pd.DataFrame()
    
    # Pivot table untuk summary
    summary = df_rerata.pivot_table(
        index=['NO', 'NISN', 'NAMA_SISWA'],
        columns='MAPEL_ID',
        values='NILAI',
        aggfunc='first'
    ).reset_index()
    
    # Hitung rata-rata semua mata pelajaran
    nilai_cols = [col for col in summary.columns if col.startswith('Mapel_')]
    summary['RATA_RATA'] = summary[nilai_cols].mean(axis=1).round(2)
    summary['JUMLAH_MAPEL'] = summary[nilai_cols].notna().sum(axis=1)
    
    # Sort berdasarkan rata-rata
    summary = summary.sort_values('RATA_RATA', ascending=False)
    
    # Tambahkan ranking
    summary['RANKING'] = range(1, len(summary) + 1)
    
    return summary


def create_subject_analysis(df_clean):
    """
    Analisis per mata pelajaran
    """
    if df_clean.empty:
        return pd.DataFrame()
    
    # Filter hanya nilai rerata
    df_rerata = df_clean[df_clean['IS_RERATA'] == True]
    
    if df_rerata.empty:
        return pd.DataFrame()
    
    # Analisis per mata pelajaran
    subject_stats = df_rerata.groupby('MAPEL_ID').agg({
        'NILAI': ['count', 'mean', 'std', 'min', 'max'],
        'NAMA_SISWA': 'nunique'
    }).round(2)
    
    # Flatten column multi-index
    subject_stats.columns = ['_'.join(col).strip() for col in subject_stats.columns.values]
    subject_stats = subject_stats.reset_index()
    
    return subject_stats


def save_clean_data(df_clean, output_dir='data/processed'):
    """
    Menyimpan data yang sudah dibersihkan
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    
    # CSV
    csv_path = Path(output_dir) / f'leger_clean_{timestamp}.csv'
    df_clean.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    # Excel dengan multiple sheets
    excel_path = Path(output_dir) / f'leger_clean_{timestamp}.xlsx'
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # Sheet 1: Data lengkap
        df_clean.to_excel(writer, sheet_name='Data_Lengkap', index=False)
        
        # Sheet 2: Summary per siswa
        summary = create_student_summary(df_clean)
        if not summary.empty:
            summary.to_excel(writer, sheet_name='Summary_Siswa', index=False)
        
        # Sheet 3: Analisis per mapel
        subject_stats = create_subject_analysis(df_clean)
        if not subject_stats.empty:
            subject_stats.to_excel(writer, sheet_name='Analisis_Mapel', index=False)
    
    return {
        'csv_path': str(csv_path),
        'excel_path': str(excel_path),
        'timestamp': timestamp
    }