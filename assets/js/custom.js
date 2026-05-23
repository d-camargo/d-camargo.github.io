/**
 * Diego Camargo - Interactions & Animations
 */

document.addEventListener('DOMContentLoaded', () => {

    /* 
     * 1. Navbar Scroll Effect 
     * Adds a background and slight blur to the navbar when scrolling down
     */
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.add('scrolled'); // Force keep scrolled or remove depends on design
            if(window.scrollY < 10) {
               navbar.classList.remove('scrolled'); 
            }
        }
    });

    // Check initial position on load
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    }


    /* 
     * 2. Smooth Scrolling for Anchor Links 
     */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            
            // Ignorar links apenas com #
            if(targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });


    /* 
     * 3. Scroll Reveal Animations
     * Adds 'reveal' class to elements as they enter the viewport
     */
    const revealElements = document.querySelectorAll('.reveal, section:not(.hero), .social-card, .portfolio-item, .blog-preview');
    
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const elementVisible = 50;

        revealElements.forEach((el) => {
            const elementTop = el.getBoundingClientRect().top;
            if (elementTop < windowHeight - elementVisible) {
                el.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', revealOnScroll);
    
    // Trigger once on load
    document.addEventListener('DOMContentLoaded', revealOnScroll);
    // Also trigger immediately in case it's already loaded
    revealOnScroll();


    /*
     * 4. Hero Entry Animations
     * Slight delay for elements in the hero section for a smooth entrance
     */
    const subtitle = document.querySelector('.subtitle_fade');
    const title = document.querySelector('.title_reveal');
    const desc = document.querySelector('.description_fade');
    const actions = document.querySelector('.hero-actions');
    const scrollInd = document.querySelector('.scroll-indicator');

    if(subtitle) subtitle.style.opacity = '0';
    if(title) { title.style.opacity = '0'; title.style.transform = 'translateY(20px)'; }
    if(desc) { desc.style.opacity = '0'; desc.style.transform = 'translateY(20px)'; }
    if(actions) { actions.style.opacity = '0'; actions.style.transform = 'translateY(20px)'; }
    if(scrollInd) scrollInd.style.opacity = '0';

    setTimeout(() => {
        if(subtitle) {
            subtitle.style.transition = 'opacity 1s ease';
            subtitle.style.opacity = '1';
        }
    }, 100);

    setTimeout(() => {
        if(title) {
            title.style.transition = 'all 1s cubic-bezier(0.165, 0.84, 0.44, 1)';
            title.style.opacity = '1';
            title.style.transform = 'translateY(0)';
        }
    }, 300);

    setTimeout(() => {
        if(desc) {
            desc.style.transition = 'all 1s cubic-bezier(0.165, 0.84, 0.44, 1)';
            desc.style.opacity = '1';
            desc.style.transform = 'translateY(0)';
        }
    }, 500);

    setTimeout(() => {
        if(actions) {
            actions.style.transition = 'all 1s cubic-bezier(0.165, 0.84, 0.44, 1)';
            actions.style.opacity = '1';
            actions.style.transform = 'translateY(0)';
        }
    }, 700);

    setTimeout(() => {
        if(scrollInd) {
            scrollInd.style.transition = 'opacity 1.5s ease';
            scrollInd.style.opacity = '0.6';
        }
    }, 1200);


    /*
     * 5. Mobile Menu Toggle
     * Simple visual toggle for mobile version
     */
    const mobileBtn = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if(mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            const isVisible = navLinks.style.display === 'flex';
            
            if(isVisible) {
                navLinks.style.display = 'none';
                mobileBtn.innerHTML = '<i class="fas fa-bars"></i>';
            } else {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.background = 'rgba(10, 10, 12, 0.95)';
                navLinks.style.padding = '2rem';
                navLinks.style.borderBottom = '1px solid rgba(255,255,255,0.08)';
                mobileBtn.innerHTML = '<i class="fas fa-times"></i>';
            }
        });
    }
});