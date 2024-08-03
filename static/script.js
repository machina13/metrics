
$(document).ready(function() {
    $('#generation').change(function() {
        var generation = $(this).val();
        $.post('/get_servers', {generation: generation}, function(data) {
            $('#server').empty().append('<option value="" disabled selected>Seleccione un server</option>');
            data.forEach(function(server) {
                $('#server').append('<option value="'+server[0]+'">'+server[0]+'</option>');
            });
        });
    });

    $('#server').change(function() {
        var server = $(this).val();
        $.post('/get_cores', {server: server}, function(data) {
            $('#cores').empty().append('<option value="" disabled selected>Seleccione cores</option>');
            data.forEach(function(core) {
                $('#cores').append('<option value="'+core[0]+'">'+core[0]+'</option>');
            });
        });
    });

    $('#cores').change(function() {
        var cores = $(this).val();
        $.post('/get_smt', {cores: cores}, function(data) {
            $('#smt').empty().append('<option value="" disabled selected>Seleccione SMT</option>');
            data.forEach(function(smt) {
                $('#smt').append('<option value="'+smt[0]+'">'+smt[0]+'</option>');
            });
        });
    });

    $('#smt').change(function() {
        var smt = $(this).val();
        $.post('/get_rperf', {smt: smt}, function(data) {
            $('#rperf').empty().append('<option value="" disabled selected>Seleccione rPerf</option>');
            data.forEach(function(rperf) {
                $('#rperf').append('<option value="'+rperf[0]+'">'+rperf[0]+'</option>');
            });
        });
    });

    $('#add-button').click(function() {
        var generation = $('#generation').val();
        var server = $('#server').val();
        var cores = $('#cores').val();
        var smt = $('#smt').val();
        var rperf = $('#rperf').val();

        $.post('/add_configuration', {
            generation: generation,
            server: server,
            cores: cores,
            smt: smt,
            rperf: rperf
        }, function(data) {
            if (data.status === 'success') {
                updateTable();
            }
        });
    });

    function updateTable() {
        $.get('/get_configurations', function(data) {
            var tbody = $('#configurations-table tbody');
            tbody.empty();
            data.forEach(function(row) {
                var tr = $('<tr>');
                tr.append('<td>'+row[0]+'</td>');
                tr.append('<td>'+row[1]+'</td>');
                tr.append('<td>'+row[2]+'</td>');
                tr.append('<td>'+row[3]+'</td>');
                tr.append('<td>'+row[4]+'</td>');
                tbody.append(tr);
            });
        });
    }

    // Inicializar la tabla
    updateTable();
});

