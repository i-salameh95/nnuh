window.Popper = require('popper.js').default;
require('bootstrap');

import { far } from '@fortawesome/free-regular-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { config, library, dom } from '@fortawesome/fontawesome-svg-core'
config.searchPseudoElements=true;
library.add(far, fas, fab);
dom.i2svg();
window.library = library;
window.dom = dom;
window.far = far;
window.fas = fas;
window.fab = fab;

require('owl.carousel');

require("../scss/app.scss");
require("./offcanvas");


$(function () {
    $('.accordion [aria-expanded="false"]:first-child').trigger('click');
    $('[data-toggle="tooltip"]').tooltip();
    $(window).scroll(function (event) {
        var scroll = $(window).scrollTop();
        if (scroll > 50) {
            $('.header').addClass('is-sticky');
        } else if (scroll == 0) {
            $('.header').removeClass('is-sticky');
        }
    });
});

