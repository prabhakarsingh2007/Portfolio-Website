// animation.js - Typewriter, Interactive Floating Particle background, and GSAP/AOS animations
document.addEventListener('DOMContentLoaded', () => {
    // 1. Typewriter Effect
    const typingElement = document.querySelector('.typing-text');
    if (typingElement) {
        const words = JSON.parse(typingElement.getAttribute('data-words') || '["Full Stack Developer", "Django Architect", "UI/UX Designer"]');
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        
        function type() {
            const currentWord = words[wordIndex];
            if (isDeleting) {
                typingElement.textContent = currentWord.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingElement.textContent = currentWord.substring(0, charIndex + 1);
                charIndex++;
            }
            
            let typeSpeed = isDeleting ? 50 : 100;
            
            if (!isDeleting && charIndex === currentWord.length) {
                typeSpeed = 1500; // Pause at end of word
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                typeSpeed = 500; // Pause before typing next word
            }
            
            setTimeout(type, typeSpeed);
        }
        
        setTimeout(type, 500);
    }

    // 2. Interactive Hero Particle Background Canvas
    const canvas = document.getElementById('hero-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particles = [];
        
        const resize = () => {
            const parent = canvas.parentElement;
            canvas.width = parent.clientWidth;
            canvas.height = parent.clientHeight;
        };
        window.addEventListener('resize', resize);
        resize();
        
        // Initialize particle array
        const particleCount = Math.min(60, Math.floor(canvas.width / 20));
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.6,
                vy: (Math.random() - 0.5) * 0.6,
                r: Math.random() * 2 + 1
            });
        }
        
        const draw = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            const isLight = document.documentElement.classList.contains('light-mode');
            ctx.fillStyle = isLight ? 'rgba(79, 70, 229, 0.2)' : 'rgba(168, 85, 247, 0.12)';
            ctx.strokeStyle = isLight ? 'rgba(79, 70, 229, 0.05)' : 'rgba(168, 85, 247, 0.03)';
            
            particles.forEach(p => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
                
                p.x += p.vx;
                p.y += p.vy;
                
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
            });
            
            // Connect coordinates close to each other
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 110) {
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
            
            requestAnimationFrame(draw);
        };
        draw();
    }

    // 3. Register GSAP Plugins & Initializations
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Numeric counters count-up animation
        const counters = document.querySelectorAll('.count-value');
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target') || '0');
            gsap.fromTo(counter, {
                textContent: 0
            }, {
                textContent: target,
                duration: 2,
                ease: 'power2.out',
                snap: { textContent: 1 },
                scrollTrigger: {
                    trigger: counter,
                    start: 'top 85%',
                    toggleActions: 'play none none none'
                }
            });
        });

        // Skill progress bar animations using GSAP ScrollTrigger
        const skillBars = document.querySelectorAll('.skill-bar-progress');
        skillBars.forEach(bar => {
            const percent = bar.getAttribute('data-percent') || '0';
            gsap.fromTo(bar, {
                width: '0%'
            }, {
                width: percent + '%',
                duration: 1.5,
                ease: 'power1.out',
                scrollTrigger: {
                    trigger: bar,
                    start: 'top 90%',
                    toggleActions: 'play none none none'
                }
            });
        });
    }

    // 4. Initialize Animate on Scroll (AOS)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            mirror: false
        });
    }
});
