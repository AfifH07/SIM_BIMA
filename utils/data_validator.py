def validate_student_data(df):
    """Validasi struktur data siswa"""
    required_columns = ['id_siswa', 'nama', 'kelas']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Kolom yang hilang: {', '.join(missing_columns)}"
    
    return True, "Data valid"
