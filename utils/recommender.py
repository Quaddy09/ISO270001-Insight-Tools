def generate_recommendations(df):
    recommendations = []

    for _, row in df.iterrows():
        status = str(row.get('Status', '')).strip().lower()
        control = str(row.get('Control', '')).strip()

        if status in ['not implemented', 'tidak diterapkan']:
            recommendations.append({
                'Control': control,
                'Status': row['Status'],
                'Next Step': 'Segera implementasikan kontrol ini sesuai panduan ISO/IEC 27001.'
            })
        elif status in ['partial', 'sebagian']:
            recommendations.append({
                'Control': control,
                'Status': row['Status'],
                'Next Step': 'Lengkapi implementasi kontrol ini dan dokumentasikan buktinya.'
            })

    return recommendations if recommendations else [{"Message": "Semua kontrol sudah diterapkan sepenuhnya."}]