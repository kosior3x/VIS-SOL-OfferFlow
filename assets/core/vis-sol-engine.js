// Create animated background elements
function createBackground() {
    const background = document.getElementById('ai-background');
    if (!background) return;

    // Create neurons (dots)
    for (let i = 0; i < 50; i++) {
        const neuron = document.createElement('div');
        neuron.className = 'neuron';
        neuron.style.left = `${Math.random() * 100}%`;
        neuron.style.top = `${Math.random() * 100}%`;
        neuron.style.animationDelay = `${Math.random() * 3}s`;
        neuron.style.animationDuration = `${2 + Math.random() * 3}s`;
        background.appendChild(neuron);
    }
}

// Case Form Management
function initCaseForm() {
    const caseOverlay = document.getElementById('overlay-case');
    if (!caseOverlay) return;
    const caseForm = document.getElementById('caseForm');
    const cancelBtn = document.getElementById('caseFormCancel');

    // Open case form from various triggers
    const triggers = [
        ...document.querySelectorAll('.case-trigger'),
        document.getElementById('heroCaseTrigger'),
        document.getElementById('sectionCaseTrigger'),
        document.getElementById('footerCaseTrigger'),
        document.getElementById('globalCaseTrigger')
    ];

    triggers.forEach(trigger => {
        if (trigger) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();

                if (this.hasAttribute('data-category')) {
                    document.getElementById('caseCategory').value = this.getAttribute('data-category');
                } else {
                    document.getElementById('caseCategory').value = '';
                }

                caseOverlay.classList.add('active');
                document.body.style.overflow = 'hidden';

                setTimeout(() => {
                    document.getElementById('caseName').focus();
                }, 300);
            });
        }
    });

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            caseOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
}

// Overlay Management
function initOverlays() {
    document.body.addEventListener('click', function(e) {
        if (e.target.matches('[data-overlay]')) {
            const overlayId = 'overlay-' + e.target.getAttribute('data-overlay');
            const overlay = document.getElementById(overlayId);
            if (overlay) {
                overlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }

        if (e.target.matches('.close-overlay')) {
            const overlay = e.target.closest('.overlay');
            if(overlay) {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    });

    document.querySelectorAll('.overlay').forEach(overlay => {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.overlay.active').forEach(overlay => {
                overlay.classList.remove('active');
                document.body.style.overflow = '';
            });
        }
    });
}

// Shadow Window Loading System
async function loadContent(url, target) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const content = await response.text();
        const targetElement = document.getElementById(target);
        if (targetElement) {
            targetElement.innerHTML = content;

            // Re-initialize scripts if they are part of the loaded content
            const scripts = targetElement.getElementsByTagName('script');
            for (let i = 0; i < scripts.length; i++) {
                const script = document.createElement('script');
                script.text = scripts[i].innerText;
                scripts[i].parentNode.replaceChild(script, scripts[i]);
            }
             // After loading content, re-initialize overlays and forms
            initOverlays();
            initCaseForm();
        }
    } catch (error) {
        console.error("Failed to load content:", error);
    }
}


function initShadowWindows() {
    const mainContent = document.getElementById('main-content');

    // Load default content
    loadContent('case_study.html', 'main-content');

    document.querySelectorAll('[data-load]').forEach(element => {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('data-load');
            loadContent(url, 'main-content');
        });
    });
}


// Mobile menu toggle
function initMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });

        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }
}

// Add scroll effect to navbar
function initScrollEffects() {
    window.addEventListener('scroll', function() {
        const nav = document.querySelector('nav');
        if (nav) {
            if (window.scrollY > 50) {
                nav.style.padding = '0.8rem 5vw';
                nav.style.background = 'rgba(10, 14, 23, 0.98)';
            } else {
                nav.style.padding = '1.2rem 5vw';
                nav.style.background = 'rgba(10, 14, 23, 0.95)';
            }
        }
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    createBackground();
    initMobileMenu();
    initScrollEffects();
    initShadowWindows();
});
