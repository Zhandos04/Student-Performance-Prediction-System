document.addEventListener('DOMContentLoaded', function() {
    // Показывать/скрывать сообщения об ошибках/успехе
    const messages = document.querySelectorAll('.alert');
    if (messages.length > 0) {
      messages.forEach(message => {
        setTimeout(() => {
          message.classList.add('fade-out');
          setTimeout(() => {
            message.remove();
          }, 500);
        }, 5000);
      });
    }
    
    // Обработка мобильного меню (если есть)
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.menu-container');
    
    if (menuToggle && mobileMenu) {
      menuToggle.addEventListener('click', function() {
        mobileMenu.classList.toggle('show');
      });
    }
    
    // Инициализация всплывающих подсказок (если используются)
    const tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
    if (typeof bootstrap !== 'undefined' && tooltips.length > 0) {
      tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
      });
    }
  });