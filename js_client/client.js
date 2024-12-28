
const baseEndpoint = 'http://127.0.0.1:8000/api'
const handleSubmit = event => {
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    const formData = new FormData(loginForm)
    const formObj = Object.fromEntries(formData)

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObj)
    }

    fetch(loginEndpoint, options)
        .then(response => {
            console.log('first response: ', response)
            return response.json()
        })
        .then(result => {
            console.log('result: ', result)
            return result
        })
        .catch(err => console.log(err))
}

const loginForm = document.getElementById('login-form')

if (loginForm) {
    loginForm.addEventListener('submit', handleSubmit)
}