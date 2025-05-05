import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os
from django.conf import settings
import random

def generate_synthetic_data(n_samples=1000):
    """
    Генерирует синтетические данные для обучения моделей.
    
    Parameters:
    -----------
    n_samples : int
        Количество генерируемых примеров.
    
    Returns:
    --------
    pandas.DataFrame
        Датафрейм с синтетическими данными.
    """
    # Генерируем случайные данные
    np.random.seed(42)
    
    # Attendance rate (0-100%)
    attendance = np.random.uniform(50, 100, n_samples)
    
    # Participation score (0-100)
    participation = np.random.uniform(0, 100, n_samples)
    
    # Assignment scores (0-100)
    assignments = np.random.uniform(50, 100, n_samples)
    
    # Генерируем целевую переменную (performance) с небольшим шумом
    # 40% влияния от посещаемости, 30% от участия, 30% от оценок за задания
    performance = (
        0.4 * attendance + 
        0.3 * participation + 
        0.3 * assignments + 
        np.random.normal(0, 5, n_samples)
    )
    
    # Создаем DataFrame
    data = pd.DataFrame({
        'attendance_rate': attendance,
        'participation_score': participation,
        'assignment_score': assignments,
        'performance': performance
    })
    
    # Обрезаем performance до диапазона [0, 100]
    data['performance'] = data['performance'].clip(0, 100)
    
    return data

def train_decision_tree(X_train, y_train):
    """
    Обучает модель Decision Tree.
    
    Parameters:
    -----------
    X_train : numpy.ndarray
        Признаки для обучения.
    y_train : numpy.ndarray
        Целевые значения для обучения.
    
    Returns:
    --------
    sklearn.tree.DecisionTreeRegressor
        Обученная модель Decision Tree.
    """
    # Создаем и обучаем модель Decision Tree
    dt_model = DecisionTreeRegressor(max_depth=5, random_state=42)
    dt_model.fit(X_train, y_train)
    
    return dt_model

def evaluate_model(model, X_test, y_test):
    """
    Оценивает производительность модели.
    
    Parameters:
    -----------
    model : object
        Обученная модель.
    X_test : numpy.ndarray
        Тестовые признаки.
    y_test : numpy.ndarray
        Тестовые целевые значения.
    
    Returns:
    --------
    tuple
        (mean_squared_error, r2_score)
    """
    # Делаем прогнозы
    y_pred = model.predict(X_test)
    
    # Вычисляем метрики
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R² Score: {r2:.2f}")
    
    return mse, r2

def save_model(model, filename='model.pkl'):
    """
    Сохраняет модель в файл.
    
    Parameters:
    -----------
    model : object
        Модель для сохранения.
    filename : str
        Имя файла для сохранения модели.
    """
    # Создаем директорию, если она не существует
    model_dir = os.path.join(settings.BASE_DIR, 'apps/dashboard/ml_models')
    os.makedirs(model_dir, exist_ok=True)
    
    # Путь для сохранения модели
    model_path = os.path.join(model_dir, filename)
    
    # Сохраняем модель
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")

def train_models():
    """
    Основная функция для обучения моделей.
    """
    print("Generating synthetic data...")
    data = generate_synthetic_data(n_samples=1000)
    
    print("Preparing data...")
    X = data[['attendance_rate', 'participation_score', 'assignment_score']].values
    y = data['performance'].values
    
    # Разделяем данные на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("Training Decision Tree model...")
    dt_model = train_decision_tree(X_train, y_train)
    
    print("Evaluating Decision Tree model...")
    evaluate_model(dt_model, X_test, y_test)
    
    print("Saving model...")
    save_model(dt_model)
    
    print("Model training completed!")

# Эта функция может быть вызвана из management command
if __name__ == "__main__":
    train_models()
