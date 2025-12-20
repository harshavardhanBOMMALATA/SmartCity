document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("cardsContainer");
    const noHistory = document.getElementById("nohistory");

    fetch('/post/all-myposts/')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network error");
            }
            return response.json();
        })
        .then(data => {

            console.log(data); // DEBUG

            if (!data.all_my_posts || data.all_my_posts.length === 0) {
                noHistory.style.display = "block";
                return;
            }

            data.all_my_posts.forEach(p => {
                const card = document.createElement("div");
                card.className = "post-card";

                card.innerHTML = `
                    <div class="image-box">
                        <img src="${p.photo || 'https://picsum.photos/400/300?1'}">
                    </div>
                    <div class="post-content">
                        <div class="post-title">${p.title}</div>
                        <div class="post-desc">${p.short_description}</div>
                        <div class="post-meta">
                            <span>#${p.id}</span>
                            <span class="post-location">${p.location}</span>
                        </div>
                    </div>
                `;

                card.onclick = () => {
                    window.location.href = `/post/${p.id}/`;
                };

                container.appendChild(card);
            });

        })
        .catch(error => {
            console.error(error);
            noHistory.style.display = "block";
        });

});
