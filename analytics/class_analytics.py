def calculate_class_statistics(df, class_name):
    """Hitung statistik kelas"""
    class_data = df[df['kelas'] == class_name]
    
    stats = {
        'mean': class_data['nilai'].mean(),
        'median': class_data['nilai'].median(),
        'std': class_data['nilai'].std(),
        'min': class_data['nilai'].min(),
        'max': class_data['nilai'].max()
    }
    
    return stats
