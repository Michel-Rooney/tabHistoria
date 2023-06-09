class RegisterPasswordValidation{
  constructor(){
    this.password = document.querySelector('input#password')
    const ul = document.querySelector('ul#password-check-list')
    this.listItems = ul.querySelectorAll('li')
    this.form = document.querySelector('form.valid-form')
    this.activeCheckPassword()
    this.events()
    this.password.addEventListener('keyup', () => {
      this.validPassword(this.password.value)
    })
  }

  events() {
    this.form.addEventListener('submit', e => {
      e.preventDefault
      if ( validPassword == true ) this.form.submit()
    })
  }

  activeCheckPassword() {
    this.password.addEventListener('click', () => {
      const checkPass = this.form.querySelector('div.check-pass')
      checkPass.classList.remove('d-none')
      checkPass.classList.add('d-block')
    })
  }

  validPassword(pass) {
    const lengthOfPassword = pass.length >= 6 ? true : false
    this.easterEgg(pass)
    if (this.hasLowerCase(pass)) {
      this.listItems[0].classList.remove('text-danger')
      this.listItems[0].classList.add('text-success')
    } else {
      this.listItems[0].classList.add('text-danger')
      this.listItems[0].classList.remove('text-success')
    }
    if ( lengthOfPassword === false ) {
      this.listItems[3].classList.add('text-danger')
      this.listItems[3].classList.remove('text-success')
      console.log('false')
      return false
    } else {
      this.listItems[3].classList.remove('text-danger')
      this.listItems[3].classList.add('text-success')
    }

    if (this.hasUpperCase(pass)) {
      this.listItems[1].classList.remove('text-danger')
      this.listItems[1].classList.add('text-success')
    } else {
      this.listItems[1].classList.add('text-danger')
      this.listItems[1].classList.remove('text-success')
    }
    
    if (this.hasNumber(pass) === false) {
      this.listItems[2].classList.add('text-danger')
      this.listItems[2].classList.remove('text-success')
      console.log('false')
      return false
    } else {
      this.listItems[2].classList.remove('text-danger')
      this.listItems[2].classList.add('text-success')
    }
    
    // if (lengthOfPassword && this.hasNumber(pass) && this.hasUpperCase(pass) && this.hasLowerCase(pass)) {
    //   const checkPass = this.form.querySelector('div.check-pass')
    //   checkPass.classList.add('d-none')
    //   checkPass.classList.remove('d-block')
    // }
    return true
  }

  hasNumber(str) {
    const re = /[0-9]/
    return re.test(str)
  }

  hasUpperCase(str) {
    const re = /[a-z]/
    return re.test(str)
  }

  hasLowerCase(str) {
    const re = /[A-Z]/
    return re.test(str)
  }

  easterEgg(str) {
    if ( str.toLowerCase() == 'lgbt' ) {
      for (let i of this.listItems) {
        i.classList.remove('text-danger')
        i.classList.remove('text-success')
        i.style = 'background-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);' +
        '-webkit-background-clip: text;' +
        '-webkit-text-fill-color: transparent;'
      }
    } else {
      for (let i of this.listItems) {
        i.classList.add('text-danger')
        i.classList.add('text-success')
        i.style = ''
      }
    }
  }
}

const sla = new RegisterPasswordValidation()