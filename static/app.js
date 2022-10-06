// ###### Post a cupcake ######

const $cupcakeList = $('#cupcake-list');

async function addCupcake(event) {
    event.preventDefault();

    const data = {
        flavor: $('#flavor').val(),
        size: $('#size').val(),
        rating: $('#rating').val()
    }
    if ($('#image').val() != '') {
        data.image = $('#image').val();
    }
    await axios.post('http://127.0.0.1:5000/api/cupcakes', data);
    listCupcakes();
}

$('#submit').click(addCupcake);

// ###### List Cupcakes ######

async function listCupcakes(event) {
    $cupcakeList.empty();
    const cupcakes = await axios.get('http://127.0.0.1:5000/api/cupcakes');
    for (let cupcake of cupcakes.data.cupcakes) {
        //console.log(cupcake);
        $cupcakeList.append(`<li>${cupcake.flavor} ${cupcake.size} ${cupcake.rating}</li>`);
    }
}

$('#list_button').click(listCupcakes);