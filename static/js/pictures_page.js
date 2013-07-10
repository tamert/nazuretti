$(function($) {
  //$(".preload").preloadify({ imagedelay:400 });
  $('a[data-rel]').each(function() {
    $(this).attr('rel', $(this).data('rel'));
  });
  $(".gallery-list a[rel^='prettyPhoto']").prettyPhoto({social_tools:false});		
});
