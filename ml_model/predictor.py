import os
import joblib
import numpy as np
from django.conf import settings

def predict_student_performance(avg_grade, attendance_rate, participation_level):
    """
    Предсказывает итоговую оценку студента на основе средней оценки, 
    посещаемости и уровня участия.
    
    Параметры:
    avg_grade (float): средний балл студента (0-100)
    attendance_rate (float): процент посещаемости (0-100)
    participation_level (int): уровень участия (0, 1, 2)
    
    Возвращает:
    tuple: (predicted_score, confidence)
    """
    # Путь к сохраненным моделям
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    
    try:
        # Загрузка моделей и scaler
        rf_model = joblib.load(os.path.join(models_dir, 'random_forest_model.pkl'))
        lr_model = joblib.load(os.path.join(models_dir, 'logistic_regression_model.pkl'))
        scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
        
        # Подготовка входных данных
        X = np.array([[avg_grade, attendance_rate, participation_level]])
        X_scaled = scaler.transform(X)
        
        # Прогнозирование итоговой оценки
        predicted_score = rf_model.predict(X_scaled)[0]
        
        # Расчет уверенности в предсказании
        probabilities = lr_model.predict_proba(X_scaled)[0]
        confidence = probabilities[1] if predicted_score >= 70 else probabilities[0]
        
        return predicted_score, confidence
        
    except (FileNotFoundError, joblib.JoblibError) as e:
        # Если файлы моделей не найдены, возвращаем простое прогнозирование
        print(f"Error loading models: {e}")
        
        # Простая эвристика для прогнозирования
        predicted_score = 0.6 * avg_grade + 0.3 * attendance_rate + 10 * participation_level
        predicted_score = min(100, max(0, predicted_score))  # Обрезание до [0, 100]
        
        # Уверенность на основе количества данных
        confidence = 0.5  # Низкая уверенность из-за отсутствия модели
        
        return predicted_score, confidence