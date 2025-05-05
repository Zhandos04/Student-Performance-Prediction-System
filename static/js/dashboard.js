document.addEventListener('DOMContentLoaded', function() {
    // Активация кнопок курсов
    const courseButtons = document.querySelectorAll('.courses button');
    courseButtons.forEach(button => {
      button.addEventListener('click', function() {
        courseButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
      });
    });
    
    // Инициализация графика успеваемости (если используется Chart.js)
    // Эта часть опциональна, если вы хотите реализовать более сложную визуализацию
    if (typeof Chart !== 'undefined' && document.getElementById('performanceChart')) {
      const ctx = document.getElementById('performanceChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: chartLabels, // Эти данные должны передаваться из вашего шаблона Django
          datasets: [{
            label: 'Прогноз успеваемости',
            data: chartData, // Эти данные должны передаваться из вашего шаблона Django
            backgroundColor: '#605BFF',
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      });
    }
  });