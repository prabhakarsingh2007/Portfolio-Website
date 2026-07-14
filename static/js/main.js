// main.js - Core application logic (mobile nav, dynamic filtering, AJAX forms, PWA, loaders, testimonials)
document.addEventListener('DOMContentLoaded', () => {
    // 1. Preloader Fade-out
    const preloader = document.getElementById('preloader');
    if (preloader) {
        // Safe timeout in case load event already fired
        window.addEventListener('load', () => {
            preloader.classList.add('fade-out');
            setTimeout(() => preloader.remove(), 500);
        });
        // Fallback for slower assets or caches
        setTimeout(() => {
            if (document.body.contains(preloader)) {
                preloader.classList.add('fade-out');
                setTimeout(() => preloader.remove(), 500);
            }
        }, 3000);
    }

    // 2. Mobile Navigation Menu Toggle
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

    // 3. Scroll Progress Indicator & Sticky Header & Scroll To Top
    const scrollProgress = document.getElementById('scroll-progress');
    const header = document.querySelector('header');
    const scrollToTopBtn = document.getElementById('scroll-to-top');

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Scroll progress width mapping
        if (scrollProgress) {
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrolledVal = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            scrollProgress.style.width = scrolledVal + '%';
        }

        // Header scrolled classes toggle
        if (header) {
            if (scrollTop > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }

        // Scroll to Top visibility toggle
        if (scrollToTopBtn) {
            if (scrollTop > 350) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        }
    });

    if (scrollToTopBtn) {
        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // 4. Integrated Projects Search & Tag Filtering Logic
    const searchInput = document.getElementById('project-search');
    const filterPills = document.querySelectorAll('.filter-pill');
    const projectCards = document.querySelectorAll('.project-card');

    if (projectCards.length > 0) {
        let activeTag = 'all';
        let searchQuery = '';

        const filterProjects = () => {
            projectCards.forEach(card => {
                const title = (card.getAttribute('data-title') || '').toLowerCase();
                const summary = (card.getAttribute('data-summary') || '').toLowerCase();
                const techs = (card.getAttribute('data-techs') || '').toLowerCase();
                
                const matchesTag = (activeTag === 'all' || techs.includes(activeTag.toLowerCase()));
                const matchesSearch = (title.includes(searchQuery) || summary.includes(searchQuery) || techs.includes(searchQuery));

                if (matchesTag && matchesSearch) {
                    card.style.display = 'block';
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.85)';
                    setTimeout(() => {
                        if (card.style.opacity === '0') {
                            card.style.display = 'none';
                        }
                    }, 300);
                }
            });
        };

        if (filterPills.length > 0) {
            filterPills.forEach(pill => {
                pill.addEventListener('click', () => {
                    filterPills.forEach(p => p.classList.remove('active'));
                    pill.classList.add('active');
                    activeTag = pill.getAttribute('data-filter');
                    filterProjects();
                });
            });
        }

        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                searchQuery = e.target.value.toLowerCase().trim();
                filterProjects();
            });
        }
    }

    // 5. Testimonial Slider Controls
    const testimonialsTrack = document.querySelector('.testimonial-track');
    const testimonialsSlides = document.querySelectorAll('.testimonial-slide');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    if (testimonialsTrack && testimonialsSlides.length > 0) {
        let currentSlide = 0;
        const totalSlides = testimonialsSlides.length;

        const updateSlide = () => {
            testimonialsTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
        };

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                currentSlide = (currentSlide === 0) ? totalSlides - 1 : currentSlide - 1;
                updateSlide();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                currentSlide = (currentSlide === totalSlides - 1) ? 0 : currentSlide + 1;
                updateSlide();
            });
        }

        // Auto slide interval
        setInterval(() => {
            currentSlide = (currentSlide === totalSlides - 1) ? 0 : currentSlide + 1;
            updateSlide();
        }, 5500);
    }

    // 6. Dynamic GitHub Profile & Repos Fetching
    const githubHeader = document.getElementById('github-header');
    if (githubHeader) {
        const profileLink = document.getElementById('github-profile-link');
        let username = 'prabhakarsingh2007'; // Default username
        if (profileLink) {
            const href = profileLink.getAttribute('href');
            if (href && href !== 'https://github.com' && href.includes('github.com/')) {
                const parts = href.replace(/\/$/, "").split('/');
                username = parts[parts.length - 1] || username;
            }
        }

        // Fetch profile
        fetch(`https://api.github.com/users/${username}`)
            .then(res => res.json())
            .then(profile => {
                if (profile && !profile.message) {
                    const nameEl = document.getElementById('github-user-name');
                    const bioEl = document.getElementById('github-user-bio');
                    const reposEl = document.getElementById('github-repos-count');
                    const followersEl = document.getElementById('github-followers-count');
                    const gistsEl = document.getElementById('github-gists-count');

                    if (nameEl) nameEl.textContent = profile.name || username;
                    if (bioEl) bioEl.textContent = profile.bio || 'Open source engineer & developer';
                    if (reposEl) reposEl.textContent = profile.public_repos;
                    if (followersEl) followersEl.textContent = profile.followers;
                    if (gistsEl) gistsEl.textContent = profile.public_gists;
                    
                    const avatarImg = document.getElementById('github-user-avatar');
                    const avatarFallback = document.getElementById('github-avatar-fallback');
                    if (avatarImg && profile.avatar_url) {
                        avatarImg.src = profile.avatar_url;
                        avatarImg.style.display = 'block';
                        if (avatarFallback) avatarFallback.style.display = 'none';
                    }
                }
            })
            .catch(err => console.error("Error fetching GitHub profile:", err));

        // Fetch popular repos
        fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=6`)
            .then(res => res.json())
            .then(repos => {
                const grid = document.getElementById('github-repos-grid');
                if (grid && Array.isArray(repos)) {
                    grid.innerHTML = '';
                    // Exclude forks and limit to 4
                    const ownRepos = repos.filter(r => !r.fork).slice(0, 4);
                    if (ownRepos.length === 0) {
                        ownRepos.push(...repos.slice(0, 4));
                    }
                    
                    ownRepos.forEach(repo => {
                        const card = document.createElement('div');
                        card.className = 'glass-card github-repo-card';
                        card.innerHTML = `
                            <div class="github-repo-title">
                                <svg viewBox="0 0 24 24" width="16" height="16" stroke="var(--accent-primary)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                                <a href="${repo.html_url}" target="_blank" rel="noopener noreferrer">${repo.name}</a>
                            </div>
                            <p class="github-repo-desc">${repo.description || 'Custom open source development repository.'}</p>
                            <div class="github-repo-meta">
                                <span>
                                    <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2.5" fill="none"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                                    ${repo.language || 'Python'}
                                </span>
                                <span>
                                    <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2.5" fill="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                                    ${repo.stargazers_count}
                                </span>
                            </div>
                        `;
                        grid.appendChild(card);
                    });
                }
            })
            .catch(err => {
                console.error("Error fetching GitHub repos:", err);
                const grid = document.getElementById('github-repos-grid');
                if (grid) {
                    grid.innerHTML = '<p style="color:var(--text-secondary); margin-bottom:0;">Could not connect to GitHub at this time.</p>';
                }
            });
    }

    // 7. Contact Form AJAX Submission & Validation
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        const nameInput = contactForm.querySelector('input[name="name"]');
        const emailInput = contactForm.querySelector('input[name="email"]');
        const messageInput = contactForm.querySelector('textarea[name="message"]');

        const validateEmail = (email) => {
            return String(email)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                );
        };

        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Client side validations
            let valid = true;
            if (!nameInput.value.trim()) {
                nameInput.style.borderColor = '#ef4444';
                valid = false;
            } else {
                nameInput.style.borderColor = '';
            }

            if (!emailInput.value.trim() || !validateEmail(emailInput.value.trim())) {
                emailInput.style.borderColor = '#ef4444';
                valid = false;
            } else {
                emailInput.style.borderColor = '';
            }

            if (!messageInput.value.trim()) {
                messageInput.style.borderColor = '#ef4444';
                valid = false;
            } else {
                messageInput.style.borderColor = '';
            }

            if (!valid) {
                showToast('Please verify your input details before sending.', 'error');
                return;
            }

            const formData = new FormData(contactForm);
            const actionUrl = contactForm.getAttribute('action');
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Sending... <span class="spinner"></span>';

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
                    showToast(res.body.message || 'Thank you! Your message was sent successfully.', 'success');
                    contactForm.reset();
                } else {
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
        }, 4500);
    }

    // 8. Register Service Worker for PWA Offline Support
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then(reg => console.log('ServiceWorker registered with scope: ', reg.scope))
                .catch(err => console.error('ServiceWorker registration failed: ', err));
        });
    }
});
