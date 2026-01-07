import pandas as pd

def calculate_student_average(df, student_id):
    """Hitung rata-rata nilai siswa"""
    student_data = df[df['id_siswa'] == student_id]
    return student_data['nilai'].mean()

def get_student_performance_trend(df, student_id):
    """Dapatkan tren performa siswa"""
    student_data = df[df['id_siswa'] == student_id]
    return student_data.groupby('semester')['nilai'].mean()
