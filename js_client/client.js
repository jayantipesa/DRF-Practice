
const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')
const contentContainer = document.getElementById('content-container')
const baseEndpoint = 'http://127.0.0.1:8000/api'

const populateContent = data => {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"
    }
}

const handleAuthData = (authData, callback = null) => {
    localStorage.setItem('access', authData.access)
    localStorage.setItem('refresh', authData.refresh)
    callback && callback()
}

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
        .then(response => response.json())
        .then(data => handleAuthData(data, fetchProductList))
        .catch(err => console.log(err))
}

const getFetchOption = (method = null, body = null) => {
    return {
        method: method ?? 'GET',
        headers: {
            'Content-type': 'application/json',
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body
    }
}
const performRefresh = () => {
    const endpoint = `${baseEndpoint}/token/refresh`
    const options = {
        method: 'POST',
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify({
            'refresh': localStorage.getItem('refresh')
        })
    }
    fetch(endpoint, options)
        .then(response => response.json())
        .then(data => fetchProductList())
        .catch(err => alert('Please login again!'))
}

const isTokenNotValid = (response) => {
    if (response.code && response.code === 'token_not_valid') {
        alert('Please login again!')
        return false
    }
    return true
}

const fetchProductList = () => {
    const endpoint = `${baseEndpoint}/products/`
    const options = getFetchOption()
    fetch(endpoint, options)
        .then(response => response.json())
        .then(data => {
            const isValid = isTokenNotValid(data)
            if (isValid) {
                populateContent(data)
            }
        })
}

const handleSearch = (event) => {
    event.preventDefault()
    const formData = new FormData(searchForm)
    const data = Object.fromEntries(formData)
    const params = new URLSearchParams(data)

    const options = {
        method: 'GET',
        headers: {
            'Content-type': 'application/json',
        }
    }

    const endpoint = `${baseEndpoint}/search/?${params}`
    fetch(endpoint, options)
        .then(response => response.json())
        .then(populateContent)
}

if (loginForm) {
    loginForm.addEventListener('submit', handleSubmit)
}
if (searchForm) {
    searchForm.addEventListener('submit', handleSearch)
}