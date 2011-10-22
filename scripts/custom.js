jQuery(document).ready(function() {
    $('#searchResults').find('.input').hide().end().find('.data').click(function() {
        $(this).next().slideToggle();
    });
});