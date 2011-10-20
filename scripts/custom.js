jQuery(document).ready(function() {
    $('#large').find('tr:nth-child(odd)').hide().end().find('tr:nth-child(even)').click(function() {
        $(this).next().slideToggle();
    });
    $('#searchResults').find('.input').hide().end().find('.data').click(function() {
        $(this).next().slideToggle();
    });
});