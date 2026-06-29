// Navbar Scroll Effect
window.addEventListener("scroll", () => {
    const nav = document.getElementById("navbar");

    if (window.scrollY > 50) {
        nav.classList.add("scrolled");
    } else {
        nav.classList.remove("scrolled");
    }
});

// Reveal Animation
function reveal() {
    const reveals = document.querySelectorAll(".reveal");

    reveals.forEach(item => {
        const windowHeight = window.innerHeight;
        const elementTop = item.getBoundingClientRect().top;
        const visible = 150;

        if (elementTop < windowHeight - visible) {
            item.classList.add("active");
        }
    });
}

window.addEventListener("scroll", reveal);
reveal();

// Counter Animation
const counters = document.querySelectorAll(".counter");
const speed = 200;

function startCounters() {
    counters.forEach(counter => {

        const updateCount = () => {
            const target = +counter.dataset.target;
            const count = +counter.innerText;

            const increment = target / speed;

            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target;
            }
        };

        updateCount();
    });
}

let started = false;

window.addEventListener("scroll", () => {
    if (window.scrollY > 300 && !started) {
        startCounters();
        started = true;
    }
});