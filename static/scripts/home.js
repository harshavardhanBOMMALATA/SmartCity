const hamburger = document.getElementById("hamburger");
const navMenu = document.getElementById("navMenu");

hamburger.addEventListener("click", function () {
    navMenu.classList.toggle("show");
    hamburger.classList.toggle("active");
});
document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/posts/")
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const cardsContainer = document.getElementById("cardsContainer");
            cardsContainer.innerHTML = "";

            data.content.forEach(post => {
                const card = document.createElement("div");
                card.className = "card";

                card.innerHTML = `
                    <div class="image-box" onclick="gotopost(${post.id})">
                        ${post.image ? `<img src="${post.image}" alt="Post Image">` : ``}
                    </div>
                    <div class="post-content" onclick="gotopost(${post.id})">
                        <div class="post-title">${post.id} ${post.title}</div>
                        <div class="post-desc">${post.shortdescription}</div>
                        <div class="post-meta">
                            <div>📍 ${post.location}</div>
                            <div>👤 ${post.author_email}</div>
                        </div>
                    </div>
                `;
                card.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
                card.style.borderRadius = "12px";
                card.style.cursor = "pointer";
                card.style.transition = "transform 0.3s ease, box-shadow 0.3s ease";
                
                card.addEventListener("mouseenter", () => {
                    card.style.transform = "translateY(-5px)";
                    card.style.boxShadow = "0 8px 20px rgba(0,0,0,0.25)";
                });

                card.addEventListener("mouseleave", () => {
                    card.style.transform = "translateY(0)";
                    card.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
                });

                cardsContainer.appendChild(card);
            });
        })
        .catch(error => {
            console.error("Error fetching posts:", error);
        });
});


function gotopost(id){
    window.location.href = `/post/${id}/`;
}
