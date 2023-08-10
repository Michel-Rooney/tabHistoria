function messageAlert() {
	var mensagem = document.getElementById('message-alert-id');
	mensagem.style.display = 'flex'; // exibe mensagem
	setTimeout(function() {
		mensagem.style.display = 'none'; // inicia animação de slide out
	}, 5000);
}