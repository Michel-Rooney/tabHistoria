const btnMode = document.querySelector('#change-theme')
const main = document.querySelector('main')

btnMode.addEventListener('click', ()=> {
    if (main.classList.contains('dark-mode')) {

        main.classList.remove('dark-mode')
        main.classList.add('ligth-mode')
        btnMode.classList.remove('bi-brightness-high')
        btnMode.classList.add('bi-moon-stars')
    } else {
        
        main.classList.remove('ligth-mode')
        main.classList.add('dark-mode')
        btnMode.classList.remove('bi-moon-stars')  
        btnMode.classList.add('bi-brightness-high')
    }
})