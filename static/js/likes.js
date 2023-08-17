const like = document.querySelector('.like')
const deslike = document.querySelector('.deslike')

like.addEventListener('click', ()=> {
    if (like.classList.contains('bi-hand-thumbs-up')) {
        like.classList.remove('bi-hand-thumbs-up')
        like.classList.add('bi-hand-thumbs-up-fill')
    } else {
        like.classList.remove('bi-hand-thumbs-up-fill')
        like.classList.add('bi-hand-thumbs-up')
    }  
})

deslike.addEventListener('click', ()=> {
    if (deslike.classList.contains('bi-hand-thumbs-down')) {
        deslike.classList.remove('bi-hand-thumbs-down')
        deslike.classList.add('bi-hand-thumbs-down-fill')
    } else {
        deslike.classList.remove('bi-hand-thumbs-down-fill')
        deslike.classList.add('bi-hand-thumbs-down')
    }  
})