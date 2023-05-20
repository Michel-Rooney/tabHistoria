const btnResponse = document.querySelector('.response')
const textArea = document.querySelector('.form')
const cancel = document.querySelector('.cancel')


btnResponse.addEventListener('click', ()=> {
    console.log('clicou carai')
    if ( textArea.classList.contains('d-none') ) {
        console.log('tem o d none')
        textArea.classList.remove('d-none')
    }
})
cancel.addEventListener('click', ()=>{
    textArea.classList.add('d-none')
})