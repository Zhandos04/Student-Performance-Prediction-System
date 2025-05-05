document.addEventListener('DOMContentLoaded', function() {
    // Обработка кликов по уведомлениям
    const notifications = document.querySelectorAll('.message');
    notifications.forEach(notification => {
      notification.addEventListener('click', function() {
        // Здесь можно добавить логику для открытия деталей уведомления
        // или для отметки уведомления как прочитанного
        this.classList.add('read');
        
        // Для AJAX-запроса к серверу для отметки уведомления как прочитанного
        // const notificationId = this.dataset.id;
        // fetch(`/api/notifications/${notificationId}/read/`, {
        //   method: 'POST',
        //   headers: {
        //     'X-CSRFToken': getCookie('csrftoken'),
        //     'Content-Type': 'application/json'
        //   }
        // });
      });
    });
    
    // Функция для получения CSRF-токена из cookies (если используется AJAX)
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
  });