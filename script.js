document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const nav = document.querySelector('.nav');

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            nav.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }

    // Close menu when a link is clicked
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                nav.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    });

    // Floating language switcher
    const navLangSwitch = document.querySelector('.lang-switch');
    if (navLangSwitch) {
        const normalizePath = (path) => {
            if (!path) return '/';
            let normalized = path.replace(/index\.html$/i, '');
            if (normalized.length > 1 && normalized.endsWith('/')) {
                normalized = normalized.slice(0, -1);
            }
            return normalized || '/';
        };

        const langWidget = document.createElement('div');
        langWidget.className = 'lang-switcher-float';

        const widgetOptions = document.createElement('div');
        widgetOptions.className = 'lang-switcher-options';

        const currentPath = normalizePath(window.location.pathname);

        navLangSwitch.querySelectorAll('a').forEach(anchor => {
            const clone = anchor.cloneNode(true);
            clone.classList.add('lang-switcher-option');

            try {
                const targetUrl = new URL(clone.getAttribute('href'), window.location.href);
                const targetPath = normalizePath(targetUrl.pathname);
                if (targetPath === currentPath) {
                    clone.classList.add('active');
                }
            } catch (err) {
                // ignore invalid URLs
            }

            widgetOptions.appendChild(clone);
        });

        langWidget.appendChild(widgetOptions);
        document.body.appendChild(langWidget);
    }

    // Active navbar state on scroll (Only for index.html or pages with sections)
    const sections = document.querySelectorAll('section');
    if (sections.length > 0) {
        window.addEventListener('scroll', () => {
            let current = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                
                if (pageYOffset >= (sectionTop - 150)) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href').includes(current)) {
                    link.classList.add('active');
                }
            });
        });
    }
});
