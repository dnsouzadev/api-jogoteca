$('form input[type="file"]').change(event => {
    let arquivos = event.target.files;
    if (arquivos.length == 0) {
        console.log('Nenhum arquivo selecionado');
    } else {
        console.log('Arquivo selecionado:', arquivos[0].name);
        if (arquivos[0].type == 'image/jpeg') {
            $('img').remove();
            let imagem = $('<img class="img-responseive">')
                .attr('src', URL.createObjectURL(arquivos[0]))
            $('figure').prepend(imagem);
        } else {
            console.alert('Selecione um arquivo do tipo JPEG');
        }
    }
})
