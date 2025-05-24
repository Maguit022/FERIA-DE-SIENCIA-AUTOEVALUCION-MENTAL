def calcular_resultado(respuestas):
    puntaje = sum(respuestas)
    if puntaje <= 4:
        nivel = "Ansiedad mínima"
        recomendaciones = "Todo bien. Mantén hábitos saludables y sigue atento a tu bienestar."
    elif puntaje <= 9:
        nivel = "Ansiedad leve"
        recomendaciones = "Intenta reducir el estrés con ejercicios o hablar con alguien de confianza."
    elif puntaje <= 14:
        nivel = "Ansiedad moderada"
        recomendaciones = "Considera hablar con un profesional de salud mental."
    else:
        nivel = "Ansiedad severa"
        recomendaciones = "Es importante que busques ayuda profesional lo antes posible."
    return puntaje, nivel, recomendaciones
