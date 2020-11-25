const iconPlus = document.querySelector('i.fa-plus');
const input = document.querySelectorAll('input.input-ingredient');
const inputQtd = document.querySelectorAll('input.input-qtd');
let button = document.querySelector('button.submit');
const form = document.querySelector('form.teste');
const div = document.querySelectorAll('div.select');
let qntd = 0
let qntd2 = document.querySelector('input.tamanho');

let altura = 300 + (qntd2.value * 90)
form.style.height = altura + 'px'

iconPlus.addEventListener('click', function(){
    // DIV - INPUT INGREDIENT - INPUT QTD - SELECT - OPTION - I
    const new_div = document.createElement('div');
    new_div.className = 'select2'
    form.appendChild(new_div);

    // INPUT INGREDIENT
    const new_input = document.createElement('input');
    new_input.className = 'input-ingredient2'
    new_input.name = "name_ingrediente" + qntd
    new_input.placeholder = 'Digite um ingrediente, ex: Arroz.'
    new_input.onkeypress = function Letras(e, t) {
        try {
            if (window.event) {
                var charCode = window.event.keyCode;
            } else if (e) {
                var charCode = e.which;
            } else {
                return true;
            }
            if ((charCode == 00 || charCode == 32) || (charCode >= 48 && charCode <= 57) || (charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122))
                return true;
            else
                return false;
        } catch (err) {
            alert(err.Description);
        }
    }
    new_input.required = "required"
    new_div.appendChild(new_input);

    // INPUT QTD
    const new_inputQtd = document.createElement('input');
    new_inputQtd.className = 'input-qtd2'
    new_inputQtd.placeholder = 'Quantidade'
    new_inputQtd.required = "required"
    new_inputQtd.min = "0"
    new_inputQtd.name = "qtd_ingrediente" + qntd
    new_inputQtd.type = 'number'
    new_div.appendChild(new_inputQtd);

    // SELECT
    const new_select = document.createElement('select');
    new_select.className = 'medidas2'
    new_select.name = "unidade_ingrediente" + qntd
    new_div.appendChild(new_select);

    const new_option = document.createElement('option');
    new_option.innerHTML = 'Kilograma'
    new_select.appendChild(new_option);

    const new_option2 = document.createElement('option');
    new_option2.innerHTML = 'Litros'
    new_select.appendChild(new_option2);

    const new_option3 = document.createElement('option');
    new_option3.innerHTML = 'Unidade'
    new_select.appendChild(new_option3);

    const new_option4 = document.createElement('option');
    new_option4.innerHTML = 'Pacote'
    new_select.appendChild(new_option4);
    form.removeChild(button);

    qntd++

    // I

    const newIcon = document.createElement('i');
    newIcon.className = 'fa fa-times';
    newIcon.style.color = 'black'
    newIcon.style.position = 'static'
    newIcon.style.marginTop = '15px'
    newIcon.marginLeft = '10px'
    const newSpan = document.createElement('span');
    const newA = document.createElement('a');
    new_div.appendChild(newSpan);
    newSpan.appendChild(newA);
    newA.appendChild(newIcon);

    // BUTTON
    const new_button = document.createElement('button');
    new_button.className = 'submit'
    new_button.innerHTML = 'ATUALIZAR PRATO'
    form.appendChild(new_button);
    button = new_button

    // FORM
    altura+=60
    form.style.height = altura + 'px'

    const inputQtdIngredient = document.querySelector('input.tamanhoAdd');
    inputQtdIngredient.value = qntd

    // DELETE
    const iconTimes = document.querySelectorAll('i.fa-times');
    const div2 = document.querySelectorAll('div.select2');
    iconTimes.forEach(function(icon, indice){
        icon.addEventListener('click', function(){
            form.removeChild(div2[indice-qntd2.value])
            qntd2 + 1
            altura-=60
            form.style.height = altura + 'px'
        })
    });

});

function Letras(e, t) {
    try {
        if (window.event) {
            var charCode = window.event.keyCode;
        } else if (e) {
            var charCode = e.which;
        } else {
            return true;
        }
        if ((charCode == 00 || charCode == 32) || (charCode >= 48 && charCode <= 57) || (charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122))
            return true;
        else
            return false;
    } catch (err) {
        alert(err.Description);
    }
}