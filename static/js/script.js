
// ==========================================
// ENCANTAR CERIMONIAL
// JAVASCRIPT PRINCIPAL
// ==========================================



// ==========================================
// BOTÃO VOLTAR AO TOPO
// ==========================================


const botaoTopo = document.getElementById("topo");


if (botaoTopo) {


    window.addEventListener(
        "scroll",
        function () {


            if (window.scrollY > 300) {


                botaoTopo.style.display = "block";


            } else {


                botaoTopo.style.display = "none";


            }


        }

    );


}



// ==========================================
// CONFIRMAÇÃO DE EXCLUSÃO
// ==========================================


const formulariosExclusao = document.querySelectorAll(
    "form[onsubmit]"
);


formulariosExclusao.forEach(
    function(formulario) {


        formulario.addEventListener(
            "submit",
            function(evento) {


                const confirmar = confirm(
                    "Tem certeza que deseja realizar esta ação?"
                );


                if (!confirmar) {

                    evento.preventDefault();

                }


            }

        );


    }

);




// ==========================================
// ANIMAÇÃO SUAVE AO CARREGAR
// ==========================================


document.addEventListener(
    "DOMContentLoaded",
    function() {


        const elementos = document.querySelectorAll(
            ".card, .botao, section"
        );


        elementos.forEach(
            function(elemento, indice) {


                elemento.style.animationDelay =
                    `${indice * 0.05}s`;


            }

        );


    }

);




// ==========================================
// PREVISUALIZAÇÃO DE IMAGEM
// PARA UPLOAD DE EVENTOS
// ==========================================


const inputImagem = document.querySelector(
    'input[type="file"]'
);


if (inputImagem) {


    inputImagem.addEventListener(
        "change",
        function() {


            const arquivo = this.files[0];


            if (arquivo) {


                const leitor = new FileReader();



                leitor.onload = function(e) {


                    let imagemPreview =
                        document.getElementById(
                            "preview-imagem"
                        );



                    if (imagemPreview) {


                        imagemPreview.src =
                            e.target.result;


                    }


                };



                leitor.readAsDataURL(arquivo);


            }


        }

    );


}



// ==========================================
// MENSAGENS FLASH
// DESAPARECER AUTOMATICAMENTE
// ==========================================


setTimeout(
    function() {


        const alertas =
            document.querySelectorAll(
                ".alert"
            );



        alertas.forEach(
            function(alerta) {


                alerta.style.opacity = "0";


                setTimeout(
                    function() {

                        alerta.remove();

                    },
                    500
                );


            }
        );


    },
    4000
);
