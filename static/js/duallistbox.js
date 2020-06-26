$(window).on('load', function() {
    // Multiple selection Listbox
    $('.listbox-no-selection').bootstrapDualListbox({
        preserveSelectionOnMove: 'moved',
        moveOnSelect: false
    });
});