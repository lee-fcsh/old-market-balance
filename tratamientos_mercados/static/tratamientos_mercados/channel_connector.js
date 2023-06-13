const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const tratamientos_mercadosSocketPath = ws_scheme + '://' + window.location.host + "/tratamientos_mercados/" + group_pk + '/' + player_pk;
const tratamientos_mercadosSocket = new WebSocket(tratamientos_mercadosSocketPath);
const changepriceButton = $('button#changepricebtn');
const first_Button = $('button#first_btn');
const price = $('span#price');
const table_vendedores = $('#table_vendedores');
const table_compradores = $('#table_compradores');



function actualizar_valores_vendidos() {
    $(".fila_vendida").remove();

    for (let index = 0; index < valores_vendidos.length; index++) {
        table_compradores.append(
            $('<tr>').addClass('fila_vendida table-success')
            .append(
                $('<td>')
                .append(
                    valores_vendidos[index]
                )
            )
        )
        table_vendedores.append(
            $('<tr>').addClass('fila_vendida table-success')
            .append(
                $('<td>')
                .append(
                    valores_vendidos[index]
                )
            )
        )

    }
   
}


actualizar_valores_vendidos()

function actualizar_tabla_vendedores() {
    $(".fila_vendedora").remove();
    for (let index = 0; index < obj_vendedores.length; index++) {
        if (obj_vendedores[index].value == null) {
            continue;
        }
        table_vendedores.append(
            $('<tr>').addClass('fila_vendedora').attr('id',obj_vendedores[index].name)
            .append(
                $('<td>')
                .append(
                    obj_vendedores[index].value
                )
            )
            
        )
    }
        
    if (role == 'comprador' && obj_vendedores.length > 0) {
        if (obj_vendedores[obj_vendedores.length -1].value == null) {
            
        }else{
            if (obj_vendedores[obj_vendedores.length -1].value > carta) {
                table_vendedores.append(
                    $('<tr>').addClass('fila_vendedora')
                    .append(
                        $('<td>')
                        .append(
                            $('<button>').attr('type','button').addClass('btn btn-danger disabled').text('comprar').attr('style','width: 100%;')
                        )
                    )
                    
                )
            }else{
                table_vendedores.append(
                    $('<tr>').addClass('fila_vendedora')
                    .append(
                        $('<td>')
                        .append(
                            $('<button>').attr('type','button').addClass('btn btn-success').text('comprar').attr('onClick',"buy_item('"+obj_vendedores[obj_vendedores.length -1].name+"')").attr('style','width: 100%;')
                        )
                    )
                    
                )
            }
        }
    }
        
    
}

function actualizar_tabla_compradores() {
    $(".fila_compradora").remove();

    for (let index = 0; index < obj_compradores.length; index++) {
        if (obj_compradores[index].value == null) {
            continue;
        }

        table_compradores.append(
            $('<tr>').addClass('fila_compradora').attr('id',obj_compradores[index].name)
            .append(
                $('<td>')
                .append(
                    obj_compradores[index].value
                )
            )
        )

    }

    if (role == 'vendedor' && obj_compradores.length > 0) {
        if (obj_compradores[obj_compradores.length -1].value == null) {
            
        }else{

            table_compradores.append(
                $('<tr>').addClass('fila_compradora').attr('id',obj_compradores[obj_compradores.length -1].name)
                .append(
                    $('<td>')
                    .append(
                        $('<button>').attr('type','button').addClass('btn btn-success').text('Vender').attr('onClick',"buy_item('"+obj_compradores[obj_compradores.length -1].name+"')").attr('style','width: 100%;')
                    )
                )
            )
        }

    }    
}

function cambiar_valor_array(array,id,valor) {
    var c = array.push({name:id, value:valor});
}

function removeItemFromArr (array) {
    array.length = 0;
}

ordenar_arrays();
actualizar_tabla_vendedores();
actualizar_tabla_compradores();

// AQUI SE RECIBE LA INFORMACION PAR TODOS LOS PARTICIPANTES
tratamientos_mercadosSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data.proceso) {
        if (data.rol == 'comprador') {
            var spam_limite = $('span#oferta_actual');
        } else {
            var spam_limite = $('span#precio_actual');
        }
        spam_limite.html(data.price);
        actualizar_parametros(data.price, data.rol);
        if (data.rol == 'comprador') {
            var spam_limite = $('span#' + data.id + '_ultima_oferta');
        } else {
            var spam_limite = $('span#' + data.id + '_ultimo_precio');
        }
        spam_limite.html(data.price);

        if (data.id == identificador) {
            document.getElementById("error_message").style.display = 'none';
        }

        if (data.rol == 'comprador') {
            cambiar_valor_array(obj_compradores,data.id,data.price);
            ordenar_arrays();
            actualizar_tabla_compradores();
        }
        else{
            cambiar_valor_array(obj_vendedores,data.id,data.price);
            ordenar_arrays();
            actualizar_tabla_vendedores();

        }
    } else {
        if (identificador == data.id || identificador == data.id2) {
            nextButton.click();
        }
        else{
            removeItemFromArr(obj_compradores);
            removeItemFromArr(obj_vendedores);
            valores_vendidos.push(data.valor_venta);
            actualizar_valores_vendidos();
            actualizar_tabla_compradores();
            actualizar_tabla_vendedores();
        }
        actualizar_parametros(data.actualo, 'comprador');
        actualizar_parametros(data.actualp, 'vendedor');
        var spam_limite = $('span#oferta_actual');
        spam_limite.html("");
        var spam_limite = $('span#precio_actual');
        spam_limite.html("");
        document.getElementById('precio').value = '';
        document.getElementById('error_message').style.display = 'none';

    }
    
    
};

// En caso de problemas
tratamientos_mercadosSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

// FUNCION PARA CAMBIAR EL PRECIO
const changeprice = () => {

    var new_value = document.getElementById("precio").value;

    if (validar_rango( new_value)) {
        document.getElementById("precio").value = ''
        tratamientos_mercadosSocket.send(JSON.stringify({
            'bid_up': true,
            'player_pk': player_pk, // do we need that? it is in kwargs?
            'new_value': new_value,
        }));
    } else {
        const error_message =  document.getElementById("error_message")
        if (role == 'vendedor' ) {
            error_message.textContent =
              new_value >= carta
                ? "No puedes vender a un precio superior al de mercado!"
                : "No puedes vender con perdidas!";
          } else {
            error_message.textContent =
              new_value <= carta
                ? "No puedes ofretar un precio mayor al de mercado!"
                : "No puedes ofertar un precio mayor a tu presupuesto!";
          }
          error_message.style.display = "block";
    }
};

changepriceButton.on('click', changeprice);

$(document).keypress(
    function (event) {
        if (event.which == '13') {
            event.preventDefault();
        }
});


first_Button.click(function () {
    document.getElementById("error_message").style.display = 'none';
    document.getElementById("precio").value = null;
});

function buy_item(id_btn) {
    tratamientos_mercadosSocket.send(JSON.stringify({
        'bid_up': false,
        'player_pk': player_pk, // do we need that? it is in kwargs?
        'id_btn': id_btn,
    }));
}

$(function () {
    $('.otree-timer__time-left').on('update.countdown', function (event) {
        if (event.offset.totalSeconds === 10) {
            $('.otree-timer__time-left').value = 120;
        }
    });
});