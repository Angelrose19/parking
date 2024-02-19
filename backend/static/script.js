// script.js

const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');

loginBtn.addEventListener('click', () => {
  window.location.href = '/login'; // Redirect to the login route
});

signupBtn.addEventListener('click', () => {
  window.location.href = '/register'; // Redirect to the register route
});
