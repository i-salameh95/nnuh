$(function () {
  'use strict'

  $('[data-toggle="offcanvas"]').on('click', function () {
      // console.log('offcanvas');
    $('.offcanvas-collapse').toggleClass('open');
    // $('.navbar-main').toggleClass('bg-transparent');
    $(this).toggleClass('open');
    // $(this).find('.fa').toggleClass('fa-bars').toggleClass('fa-close');
  });
})
