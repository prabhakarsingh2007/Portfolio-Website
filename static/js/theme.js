// theme.js - Theme toggle and persistence logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const root = document.documentElement;

    // Check for saved theme preference or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    // Apply saved theme
    if (savedTheme === 'light') {
        root.classList.add('light-mode');
        if (themeToggleBtn) themeToggleBtn.innerHTML = '🌙'; // Icon for changing back to dark
    } else {
        root.classList.remove('light-mode');
        if (themeToggleBtn) themeToggleBtn.innerHTML = '☀️'; // Icon for changing to light
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const isLight = root.classList.contains('light-mode');
            if (isLight) {
                root.classList.remove('light-mode');
                localStorage.setItem('theme', 'dark');
                themeToggleBtn.innerHTML = '☀️';
            } else {
                root.classList.add('light-mode');
                localStorage.setItem('theme', 'light');
                themeToggleBtn.innerHTML = '🌙';
            }
        });
    }
});
