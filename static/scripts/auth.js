const loginForm = document.getElementById('form');

if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const emailinput = document.getElementsByName('email')[0].value;
        const passwordinput = document.getElementsByName('password')[0].value;

        fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: emailinput.trim(),
                password: passwordinput.trim()
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementsByClassName('message')[0].innerText =
                    'Login successful!';
            } else {
                document.getElementsByClassName('message')[0].innerText =
                    'Login failed';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementsByClassName('message')[0].innerText =
                'An error occurred during login.';
        });
    });
}
