/*const btnResponse = document.querySelector('.response')
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
})*/

const btnResponse = document.getElementsByClassName('response')
const btnCancel = document.getElementsByClassName('cancel')
const textArea = document.getElementsByClassName('form')


for (let i = 0; i < btnResponse.length; i++) {
    let element = btnResponse[i]
    element.addEventListener('click', () => {
        console.log(`clicou`)
        if (textArea[i].classList.contains('d-none')){
            btnResponse[i].classList.add('d-none')
            textArea[i].classList.remove('d-none')
        }
    })
    btnCancel[i].addEventListener('click', () => {
        textArea[i].classList.add('d-none')
        btnResponse[i].classList.remove('d-none')
    })
}