def analyze_subject_performance(df, subject):
    """Analisis performa per mata pelajaran"""
    subject_data = df[df['mata_pelajaran'] == subject]
    
    return {
        'total_students': len(subject_data),
        'average_score': subject_data['nilai'].mean(),
        'pass_rate': (subject_data['nilai'] >= 70).sum() / len(subject_data) * 100
    }
