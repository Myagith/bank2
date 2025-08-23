document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.toggle-password').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetId = btn.getAttribute('data-target');
      var input = document.getElementById(targetId);
      if (!input) return;
      if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = 'Masquer';
      } else {
        input.type = 'password';
        btn.textContent = 'Afficher';
      }
    });
  });

  var form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      var username = document.getElementById('id_username');
      var password = document.getElementById('id_password');
      if (username && username.value.trim().length === 0) {
        e.preventDefault();
        alert("Veuillez saisir le nom d'utilisateur.");
        username.focus();
        return;
      }
      if (password && password.value.trim().length === 0) {
        e.preventDefault();
        alert('Veuillez saisir le mot de passe.');
        password.focus();
        return;
      }
    });
  }
});