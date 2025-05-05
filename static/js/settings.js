document.addEventListener('DOMContentLoaded', function() {
    // Валидация формы изменения пароля
    const passwordForm = document.querySelector('form');
    if (passwordForm) {
      passwordForm.addEventListener('submit', function(e) {
        const newPassword = document.getElementById('new').value;
        const confirmPassword = document.getElementById('confirm').value;
        
        if (newPassword !== confirmPassword) {
          e.preventDefault();
          alert('Пароли не совпадают!');
        }
      });
    }
  });