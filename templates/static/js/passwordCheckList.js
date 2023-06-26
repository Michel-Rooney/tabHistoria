class RegisterPasswordValidation{
  constructor(){
    this.password = document.querySelector('input#password')
    const ul = document.querySelector('ul#password-check-list')
    this.listItems = ul.querySelectorAll('li')
    this.form = document.querySelector('form.valid-form')
    this.events()
    this.password.addEventListener('keydown', () => {
      this.validPassword(this.password.value)
      console.log('deu bom')
    })
  }
  events() {
    this.form.addEventListener('submit', e => {
      e.preventDefault
      if ( validPassword == true ) this.form.submit()
    })
  }

  validPassword(pass) {
    const lengthOfPassword = pass.length >=6 ? true : false
    if ( lengthOfPassword ) {
      this.listItems[3].style.color = 'green'
      console.log(this.listItems)
      return true
    }
    else  this.listItems[3].style.color = 'red'
  }
}

const sla = new RegisterPasswordValidation()