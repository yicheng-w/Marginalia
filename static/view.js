console.log("loaded view.js");

$('.actual-switch').on('click', function() {
    // ajax call to share site
    var id_val = this.getAttribute('id');
    var new_stat = this.checked;
    console.log(id_val);
    $.post("/change_perm/", {'id': id_val, 'to': new_stat} , function(data) {
        if (data['status'] == 'success') {
            // do something
            Materialize.toast(data['msg'], 3000);

            console.log("#sharing-link-"+data['id']);
            if (data['to'] == 'true') {
                var loc = document.getElementById("sharing-link-"+data['id']);
                loc.style.visibility='visible';
            }
            else {
                var loc = document.getElementById("sharing-link-"+data['id']);
                loc.style.visibility='hidden';
            }
        }
        else {
            Materialize.toast("<strong>Permission Change Failed</strong> " + data['msg'], 3000);
            setTimeout(location.reload(true), 3000);
        }
    }, 'json');
});

$('.slink').click(function() {
    var text = $(this).text();
    var $this = $(this);
    var $input = $('<input type=text>');
    $input.prop('value', text);
    $input.insertAfter($(this));
    $input.focus();
    $input.select();
    $this.hide();
    $input.focusout(function(){
        $this.show();
        $input.remove();
    });
});

var deleteSite = function(id) {
    $.post('/delete/', {'id' : id}, function(data) {
        Materialize.toast(data['msg'], 1000);
        if (data['status'] == 'success') {
            document.getElementById('entry-'+id).style.display = 'none';
        }
    }, 'json');
}

$('.removal').click(function() {
    var id_str = this.getAttribute('id');
    var id = parseInt(id_str.substr(id_str.lastIndexOf('-') + 1), 10);

    console.log(document.getElementById('not-again').checked);

    if (document.getElementById('not-again').checked) { // make sure they are sure
        deleteSite(id);
    }
    else {
        $('#are-you-sure').openModal();

        $('#nvm').click(function() {
            $('#are-you-sure').closeModal()
            return;
        });

        $('#sure').click(function() {
            $('#are-you-sure').closeModal();
            deleteSite(id);
        });
    }
});
