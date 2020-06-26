// Allow CSS transitions when page is loaded
$(window).on('load', function() {
    $('#sidebar-width').val($('.sidebar-content').width());    
    $('.margin-left-sidebar').css('margin-left','548%');

    // Record Listing    
    $("#record-listing").select2({
        placeholder: "",
        minimumResultsForSearch: Infinity,        
    });

    //ListBox
    // Basic example
    //$('.listbox').bootstrapDualListbox();
  
});

$(document).ready(function() {
    $('#website_language').on('change', function() {
        this.form.submit();
    });
});

//Custom Sidebar float width set
function calculateSidebarWidth(){
    var wid = $('.sidebar-content:visible').width();       
    if(wid == undefined){    
        var width_sidebar = $('.sidebar-content').width();        
        $('.margin-left-sidebar').css('margin-left','548%');
    }else{
        $('.margin-left-sidebar').css('margin-left','-2px');
    }
}

// Record Listing    
$("#record-listing").select2({
    placeholder: "",
    minimumResultsForSearch: Infinity,        
});

$('.selectpicker').select2({
    minimumResultsForSearch: Infinity,
    width : 100
});

//Change Master Status
// function change_status(element){
//     var listing_value = $(element).val();        
//     $.ajax({
//         url: '{{ajax_begining_path}}ajax/change_listing_count/',
//         data: {
//         'listing_value': listing_value
//         },
//         dataType: 'json',
//         success: function (data) {
//         if (data.is_status) {
//             window.location = window.location.pathname;
//         }
//         }
//     });
// }
