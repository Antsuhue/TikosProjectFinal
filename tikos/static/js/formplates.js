const iconPlus = document.querySelector('i.fa-plus');
const input = document.querySelectorAll('input.input-ingredient');
const inputQtd = document.querySelectorAll('input.input-qtd');
let button = document.querySelector('button.submit');
const form = document.querySelector('form.teste');
const div = document.querySelectorAll('div.select');
let altura = 350
let qtd = 1

iconPlus.addEventListener('click',function(){
    // DIV - INPUT INGREDIENT - INPUT QTD - SELECT - OPTION - I
    const new_div = document.createElement('div');
    new_div.className = 'select2'
    form.appendChild(new_div);

    // INPUT INGREDIENT
    const new_input = document.createElement('input');
    new_input.className = 'input-ingredient2'
    new_input.type = "text"
    new_input.name = "product_name" + qtd
    new_input.placeholder = 'Digite um ingrediente, ex: Arroz.'
    new_div.appendChild(new_input);

    // INPUT QTD
    const new_inputQtd = document.createElement('input');
    new_inputQtd.className = 'input-qtd2'
    new_inputQtd.required = "required"
    new_inputQtd.min = "0"
    new_inputQtd.type = "number"
    new_inputQtd.name = "product_qntd" + qtd
    new_inputQtd.placeholder = 'Quantidade'
    new_inputQtd.type = 'number'
    new_div.appendChild(new_inputQtd);

    // SELECT
    const new_select = document.createElement('select');
    new_select.className = 'medidas2'
    new_select.name = "unidade" + qtd
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

    qtd+=1

    // I

    const newIcon = document.createElement('i')
    newIcon.className = 'fa fa-times'
    new_div.appendChild(newIcon)

    // BUTTON
    const new_button = document.createElement('button');
    new_button.className = 'submit'
    new_button.innerHTML = 'CADASTRAR PRATO'
    form.appendChild(new_button);
    button = new_button

    // FORM
    altura+=50
    form.style.height = altura + 'px'

    const inputQtdIngredient = document.querySelector('input.quantidade-ingrediente');
    inputQtdIngredient.value = qtd

    // DELETE
    const iconTimes = document.querySelectorAll('i.fa-times');
    const div2 = document.querySelectorAll('div.select2');
    iconTimes.forEach(function(icon, indice) {
    icon.addEventListener('click', function(){
        form.removeChild(div2[indice])
        altura-=50
        qtd -= 1
        inputQtdIngredient.value = qtd
        form.style.height = altura + 'px'
        });
    });
});

// function Letras(e, t) {
//     try {
//         if (window.event) {
//             var charCode = window.event.keyCode;
//         } else if (e) {
//             var charCode = e.which;
//         } else {
//             return true;
//         }
//         if ((charCode >= 33 && charCode <= 38) || (charCode >= 39 && charCode <= 47) || (charCode >= 58 && charCode <= 64) || (charCode >= 91 && charCode <= 93) || (charCode >= 95 && charCode <=) || (charCode >= 123 && charCode <= 125) || (charCode >= 155 && charCode <= 159) || (charCode >= 164 && charCode <= 180) || (charCode >= 184 && charCode <= 197) || (charCode >= 200 && charCode <= 209) || (charCode >= 217 && charCode <= 223) || (charCode == 225) || (charCode >= 230 && charCode <= 232) || (charCode >= 236 && charCode <= 254))
//             return false;
//         else
//             return true;
//     } catch (err) {
//         alert(err.Description);
//     }
// }