document.addEventListener("DOMContentLoaded", () => {
    console.log("working");

    /* ===== POST ID ===== */
    const postEl = document.getElementById("postID");
    if (!postEl) return;
    const postId = JSON.parse(postEl.textContent);

    /* ===== FETCH POST ===== */
    fetch(`/post/api/${postId}/`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("title").innerText = data.post.title;
            document.getElementById("author").innerText = "- " + data.post.author_email;
            initDescription(data.post.description);
        })
        .catch(console.error);

    /* ===== CAROUSEL ===== */
    let index = 0;
    const track = document.getElementById("carouselTrack");
    const carousel = document.querySelector(".carousel");

    if (track && carousel) {
        window.moveSlide = step => {
            index = Math.max(0, Math.min(index + step, track.children.length - 1));
            track.style.transform = `translateX(-${index * carousel.offsetWidth}px)`;
        };

        window.addEventListener("resize", () => {
            track.style.transform = `translateX(-${index * carousel.offsetWidth}px)`;
        });
    }

    /* ===== READ MORE ===== */
    const descriptionEl = document.getElementById("description");
    const readBtn = document.getElementById("readMoreBtn");

    let fullText = "";
    let expanded = false;

    window.initDescription = text => {
        fullText = text;
        if (text.length <= 140) {
            descriptionEl.innerText = text;
            readBtn.style.display = "none";
            return;
        }
        descriptionEl.innerText = text.substring(0, 140) + "...";
        readBtn.innerText = "Read more";
        expanded = false;
    };

    window.toggleRead = () => {
        expanded = !expanded;
        descriptionEl.innerText = expanded
            ? fullText
            : fullText.substring(0, 140) + "...";
        readBtn.innerText = expanded ? "Read less" : "Read more";
    };

    /* response */
    fetch(`/post/poll/response/${postId}/`)
    .then(response => response.json())
    .then(data => {
        if(data.response===true){
            document.getElementById("agreeBtn").style.display = "none";
            document.getElementById("disagreeBtn").style.display = "none";
            document.getElementById("pollresult").style.display="Thank you for responding";
        }

    })
    .catch(error => console.log(error));

    /* ===== POLL ===== */
    function updateCounts() {
        fetch(`/post/poll/result/${postId}/`)
            .then(r => r.json())
            .then(data => {
                document.getElementById("agreeCount").innerText = data.pcount;
                document.getElementById("disagreeCount").innerText = data.ncount;
            })
            .catch(console.error);
    }

    updateCounts(); // load counts on page load
    verdicts();
});

function trigger(i) {
    fetch(`${window.location.origin}/post/poll/loginornot/`)
    .then(response=>response.json())
    .then(data=>{
        if(data.verdict===false){
            window.location.href='/';
        }
    })

    const postEl = document.getElementById("postID");
    if (!postEl) return;

    const postId = JSON.parse(postEl.textContent);

    if (i === '0') {
        // AGREE
        voteUrl = `/post/poll/agree/${postId}/`;

    } else if (i === '1') {
        // DISAGREE
        voteUrl = `/post/poll/disagree/${postId}/`;
    } else {
        return;
    }

    fetch(voteUrl)
    .then(response=>response.json())
    .then(data=>{
        console.log(data);
        const officialEl = document.getElementById("officialverdict");
        const pollEl = document.getElementById("pollverdict");
        document.getElementById("agreeCount").innerText=data.pcount;
        document.getElementById("disagreeCount").innerText=data.ncount;
        if(data.ncount>data.pcount){
            document.getElementById("pollverdict").style.backgroundColor="red";
        }else if(data.ncount<data.pcount){
            document.getElementById("pollverdict").style.backgroundColor="green";
        }else{
            document.getElementById("pollverdict").style.backgroundColor="blue";
        }
    })
    .catch(error=>{
        console.error(error);
    });
}

function verdicts() {
    const postEl = document.getElementById("postID");
    if (!postEl) return;
    const postId = JSON.parse(postEl.textContent);

    fetch(`/post/verdict/${postId}/`)
        .then(response => response.json())
        .then(data => {
            const officialEl = document.getElementById("officialverdict");
            const pollEl = document.getElementById("pollverdict");

            // Official verdict
            if (data.officialverdict === true) {
                officialEl.style.color = "white";
                 officialEl.style.backgroundColor = "green";               
            } else if (data.officialverdict === false) {
                officialEl.style.color = "white";
                officialEl.style.backgroundColor = "red";   
            } else {
                officialEl.style.color = "white";
                officialEl.style.backgroundColor = "blue";   
            }

            // Poll verdict
            if (data.pollverdict === true) {
                pollEl.style.color = "white";
                pollEl.style.backgroundColor = "green";
            } else if (data.pollverdict === false) {
                pollEl.style.color = "white";
                pollEl.style.backgroundColor = "red";
            } else {
                pollEl.style.color = "white";
                pollEl.style.backgroundColor = "blue";
            }
        })
        .catch(error => console.error(error));
}
