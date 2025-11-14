document.addEventListener("DOMContentLoaded", () => {
    const sections = [
        "home",
        "recently-played",
        "top-tracks",
        "top-artists",
        "genre-chart"
    ];

    const navbar = document.getElementById("navbar");
    navbar.innerHTML = `
    <ul class="nav-list">
        <li><a href="#" data-target="home">Home</a></li>
        <li><a href="#" data-target="top-tracks">Top Tracks</a></li>
        <li><a href="#" data-target="top-artists">Top Artists</a></li>
        <li><a href="#" data-target="recently-played">Recently Played</a></li>
        <li><a href="#" data-target="genre-chart">Genres</a></li>
    </ul>
    `;


    function showSection(id) {
        sections.forEach(section => {
            const el = document.getElementById(section);
            if (el) {
                el.style.display = section === id ? "block" : "none";
            }
        });
        if (id === "genre-chart" && typeof renderGenreChart === "function") {
            renderGenreChart();
        }
    }


    navbar.addEventListener("click", (e) => {
        if (e.target.tagName === "A") {
            e.preventDefault();
            const target = e.target.getAttribute("data-target");
            showSection(target);
        }
    });

    // Show default section
    showSection("home");
});
