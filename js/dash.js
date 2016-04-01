$(document).on('click',
    function()
    {
        
        $.ajax({
            type: 'GET',
            url: 'http://appclippy.herokuapp.com/dashboard',
            data: '{}', // or JSON.stringify ({name: 'jonas'}),
            success: function(data) { $('body').text('red'); 
            console.log(data);},
            contentType: "application/json",
            dataType: 'json'
        });
    }
);
