// Défilement fluide vers les sections
function scrollToSection(sectionId) {
    document.querySelector(`#${sectionId}`).scrollIntoView({
        behavior: 'smooth'
    });
}

// Simulation d'affichage de vidéos par catégorie
function showVideos(category) {
    alert(`Affichage des vidéos de la catégorie : ${category}`);
    // Pour un projet avancé, vous pourriez filtrer les vidéos ici
}

// Animation au chargement avec délai progressif
window.addEventListener('load', () => {
    const cards = document.querySelectorAll('.category-card, .video-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index); // Délai progressif pour chaque carte
    });
});
