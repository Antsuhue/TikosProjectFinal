const form = document.querySelector('form');
let button = document.querySelector('button.submit');
const inputsProduct = document.querySelectorAll('input.product2');
let altura = 380
let qntd = 1

const iconPlus = document.querySelectorAll('i.fa-plus');
iconPlus.forEach(function(icon, indice){
    icon.addEventListener('click', function(){

        form.removeChild(button)

        const label = document.createElement('label');
        label.className = 'name'
        label.innerHTML = 'Nome do Produto:'
        form.appendChild(label)

        const div = document.createElement('div');
        div.className = 'select2'
        form.appendChild(div)

        const inputProduct = document.createElement('input');
        inputProduct.className = 'product2'
        inputProduct.name = "nome_produto" + qntd
        inputProduct.placeholder = 'Digite o nome do produto, ex: Arroz.'
        inputProduct.required = "required"
        div.appendChild(inputProduct)

        const select = document.createElement('select');
        select.className = 'medidas'
        select.name = "unidade" + qntd
        div.appendChild(select)

        const option = document.createElement('option');
        option.innerHTML = 'KG'
        select.appendChild(option)

        const option1 = document.createElement('option');
        option1.innerHTML = 'LTs'
        select.appendChild(option1)

        const option2 = document.createElement('option');
        option2.innerHTML = 'Unidade'
        select.appendChild(option2)

        const option3 = document.createElement('option');
        option3.innerHTML = 'Pct-1kg'
        select.appendChild(option3)

        const option4 = document.createElement('option');
        option4.innerHTML = 'Pct-5kg'
        select.appendChild(option4)

        const labelPrice = document.createElement('label');
        labelPrice.className = 'price'
        labelPrice.innerHTML = 'Preço do Produto:'
        form.appendChild(labelPrice)

        const inputPrice = document.createElement('input');
        inputPrice.className = 'input-price2'
        inputPrice.required = "required"
        inputPrice.min = "0"
        inputPrice.name = "preco" + qntd
        inputPrice.placeholder = 'Digite o preço do produto, ex: 18.'
        form.appendChild(inputPrice)

        const labelProduct = document.createElement('label');
        labelProduct.className = 'qtd'
        labelProduct.innerHTML = 'Quantidade:'
        form.appendChild(labelProduct)

        const inputQtd = document.createElement('input');
        inputQtd.className = 'input-qtd2'
        inputQtd.required = "required"
        inputQtd.min = "0"
        inputQtd.placeholder = 'Digite a quantidade de produtos, ex: 25.'
        inputQtd.name = "quantidade" + qntd
        
        form.appendChild(inputQtd)

        const labelMin = document.createElement('label');
        labelMin.className = 'min'
        labelMin.innerHTML = 'Estoque Mínimo:'
        form.appendChild(labelMin)

        const inputMin = document.createElement('input');
        inputMin.className = 'input-min2'
        inputMin.required = "required"
        inputMin.min = "0"
        inputMin.placeholder = 'Digite o estoque mínimo do produto, ex: 50.'
        inputMin.name = "min" + qntd
        
        form.appendChild(inputMin)

        const labelDeleteNew = document.createElement('label');
        labelDeleteNew.className = 'delete'
        labelDeleteNew.innerHTML = 'Excluir Produto'
        labelDeleteNew.className = 'delete new'
        form.appendChild(labelDeleteNew)

        const iconTimes = document.createElement('i');
        iconTimes.className = 'fa fa-times'
        labelDeleteNew.appendChild(iconTimes)

        let new_button = document.createElement('button');
        new_button.className = 'submit'
        new_button.innerHTML = 'CADASTRAR PRODUTO'
        form.appendChild(new_button)

        qntd++

        button = new_button
        altura += 380
        form.style.height = altura + 'px'

        const inputQtdIngredient = document.querySelector('input.quantidade-ingrediente');
        inputQtdIngredient.value = qntd

        const divs = document.querySelectorAll('div.select2');
        const labelsName = document.querySelectorAll('label.name');
        const labelsPrice = document.querySelectorAll('label.price');
        const labelsQtd = document.querySelectorAll('label.qtd');
        const labelsMin = document.querySelectorAll('label.min');
        const labelsDelete = document.querySelectorAll('label.delete');
        const inputsPrice = document.querySelectorAll('input.input-price2');
        const inputsQtd = document.querySelectorAll('input.input-qtd2');
        const inputsMin = document.querySelectorAll('input.input-min2');
        const iconsTimes = document.querySelectorAll('i.fa-times');
        iconsTimes.forEach(function(icon, indice){
        icon.addEventListener('click', function(){
        form.removeChild(divs[indice])
        form.removeChild(labelsName[indice])
        form.removeChild(labelsQtd[indice])
        form.removeChild(labelsPrice[indice])
        form.removeChild(labelsMin[indice])
        form.removeChild(labelsDelete[indice])
        form.removeChild(inputsPrice[indice])
        form.removeChild(inputsMin[indice])
        form.removeChild(inputsQtd[indice])
        altura -= 380
        form.style.height = altura + 'px'
        });
        });


    });

});