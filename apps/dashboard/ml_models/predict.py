import numpy as np
import pickle
import os
from django.conf import settings
import random  # Для демонстрационных данных

def predict_student_performance(attendance_rate, participation_score, avg_assignment_score):
    """
    Прогнозирует успеваемость студента на основе заданных параметров.
    
    Для демонстрации используем простую модель, основанную на весах параметров.
    В реальной системе здесь будет загружаться обученная модель ML.
    """
    try:
        # Путь к файлу модели
        model_path = os.path.join(settings.BASE_DIR, 'apps/dashboard/ml_models/model.pkl')
        
        # Проверка наличия файла модели
        if os.path.exists(model_path):
            # Загрузка обученной модели
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            # Подготовка данных для прогноза
            features = np.array([[attendance_rate, participation_score, avg_assignment_score]])
            
            # Прогнозирование
            predicted_score = model.predict(features)[0]
            
            # Оценка уверенности прогноза (зависит от модели)
            # Для демонстрации используем случайное значение
            confidence = random.uniform(0.7, 0.95)
            
            return predicted_score, confidence
        
        else:
            # Если модель не найдена, используем простую формулу
            predicted_score = (
                0.4 * attendance_rate + 
                0.3 * participation_score + 
                0.3 * avg_assignment_score
            )
            
            # Генерируем случайную уверенность для демонстрации
            confidence = random.uniform(0.7, 0.95)
            
            return predicted_score, confidence
            
    except Exception as e:
        print(f"Error in prediction: {e}")
        
        # Возвращаем значения по умолчанию в случае ошибки
        predicted_score = 70  # Средний балл
        confidence = 0.6  # Низкая уверенность
        
        return predicted_score, confidence