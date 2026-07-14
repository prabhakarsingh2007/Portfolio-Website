// main.js - Core application logic (mobile nav, dynamic filtering, AJAX forms)
document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Navigation Menu Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
            
            // Toggle hamburger icon animation
            const spans = menuToggle.querySelectorAll('span');
            if (menuToggle.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -7px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }

    // 2. Dynamic Project Tag Filtering
    const filterPills = document.querySelectorAll('.filter-pill');
    const projectCards = document.querySelectorAll('.project-card');

    if (filterPills.length > 0 && projectCards.length > 0) {
        filterPills.forEach(pill => {
            pill.addEventListener('click', () => {
                // Active status toggle
                filterPills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');

                const filterValue = pill.getAttribute('data-filter');

                projectCards.forEach(card => {
                    const cardTechs = card.getAttribute('data-techs').toLowerCase();
                    if (filterValue === 'all' || cardTechs.includes(filterValue.toLowerCase())) {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'scale(1)';
                        }, 50);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }

    // 3. Contact Form AJAX Submission
    const contactForm = document.getElementById('contact-form');
    const formResponse = document.getElementById('form-response');

    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Gather details
            const formData = new FormData(contactForm);
            const actionUrl = contactForm.getAttribute('action');
            
            // Show sending status
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Sending... <span class="spinner"></span>';

            // Send fetch request
            fetch(actionUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(res => {
                if (res.status === 200) {
                    showToast(res.body.message, 'success');
                    contactForm.reset();
                } else {
                    // Show field validation errors
                    let errorMsg = 'Error sending message. Please try again.';
                    if (res.body.errors) {
                        errorMsg = Object.values(res.body.errors)
                            .map(errList => errList.map(e => e.message).join(', '))
                            .join('<br>');
                    }
                    showToast(errorMsg, 'error');
                }
            })
            .catch(error => {
                console.error('Error submitting form:', error);
                showToast('Something went wrong. Please check your network connection.', 'error');
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            });
        });
    }

    // Helper Toast Notification
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = message;
        document.body.appendChild(toast);

        // Animate in
        setTimeout(() => toast.classList.add('visible'), 100);

        // Animate out and remove
        setTimeout(() => {
            toast.classList.remove('visible');
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    }
});
