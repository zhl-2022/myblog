/*------------------------------------- Page Loader �������أ�Http://www.bootstrapmb.com -------------------------------------*/
$(document).ready(function () {
    setTimeout(function () {
        $('.page-loader').fadeOut('slow');
    }, 500);
});

/*------------------------------------- AOS Scroll Animation -------------------------------------*/
AOS.init({
    duration: 1600,
})
$(window).on("scroll", function () {
    AOS.init();
});

/*------------------------------------- Sticky Header -------------------------------------*/
$(document).ready(function () {
    $(window).scroll(function () {
        var scrollPosition = $(window).scrollTop();
        if (scrollPosition >= 20) {
            $('#top-header, #top-navbar').addClass('fixed');
        } else {
            $('#top-header, #top-navbar').removeClass('fixed');
        }
    });
});

/*------------------------------------- Cursor Move images section one -------------------------------------*/
$(document).ready(function () {
    var worked_box = $('#worked_box');
    var JessicaBiogi_main = $('#JessicaBiogi_main');
    var arrow = $('#arrow');
    var layer = $('#main');

    layer.mousemove(function (e) {
        var ivalueX = (e.pageX * -1 / 60);
        var ivalueY = (e.pageY * -1 / 60);
        var cvalueX = (e.pageX * -1 / 80);
        var cvalueY = (e.pageY * -1 / 90);
        worked_box.css('transform', 'translate3d(' + ivalueX + 'px,' + ivalueY + 'px, 0)');
        JessicaBiogi_main.css('transform', 'translate3d(' + cvalueX + 'px,' + cvalueY + 'px, 0)');
        arrow.css('transform', 'translate3d(' + cvalueX + 'px,' + cvalueY + 'px, 0)');
    });
});

/*------------------------------------- Accordion Home -------------------------------------*/
$(document).ready(function () {
    $('.nested-accordion').find('.comment').not(':first').slideUp();
    $('.nested-accordion:first').find('h3').addClass('selected');
    $('.nested-accordion').find('h3').click(function () {
        $(this).next('.comment').slideToggle(100);
        $(this).toggleClass('selected');
        $('.nested-accordion').not($(this).parent()).find('.comment').slideUp();
        $('.nested-accordion').not($(this).parent()).find('h3').removeClass('selected');
    });
});

/*------------------------------------- Scroll counter -------------------------------------*/
var counted = 0;
$(window).scroll(function () {
    var oTop = $('.counter').offset()?.top - window.innerHeight;
    if (counted == 0 && $(window).scrollTop() > oTop) {
        $('.count').each(function () {
            var $this = $(this),
                countTo = $this.attr('data-count');
            $({
                countNum: $this.text()
            }).animate({
                    countNum: countTo
                },
                {
                    duration: 800,
                    easing: 'swing',
                    step: function () {
                        $this.text(Math.floor(this.countNum));
                    },
                    complete: function () {
                        $this.text(this.countNum);
                    }

                });
        });
        counted = 1;
    }
});

/*------------------------------------- Tabs Buttons -------------------------------------*/
var tabButtons = document.querySelectorAll('.tab-button');
var tabPanes = document.querySelectorAll('.tab-pane');

tabButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var tabId = button.getAttribute('data-tab');

        tabButtons.forEach(function (btn) {
            btn.classList.remove('active');
        });
        button.classList.add('active');

        tabPanes.forEach(function (pane) {
            pane.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');
    });
});

/*------------------------------------- Gallary code -------------------------------------*/
window.addEventListener("load", () => {
    for (let i of document.querySelectorAll(".gallery img")) {
        i.onclick = () => i.classList.toggle("full");
    }
});

/*------------------------------------- Pop Videos -------------------------------------*/
$(document).ready(function () {
    $('#vimeo').magnificPopup({
        items: {
            src: 'https://vimeo.com/259411563'
        },
        type: 'iframe'
    });

    $('.youtube').magnificPopup({
        items: {
            src: 'https://www.youtube.com/watch?v=IMxDeACOWCE'
        },
        type: 'iframe'
    });

    $('.link').magnificPopup({
        type: 'soundcloud',
        items: {
            src: 'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/163522130&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true'
        },
        type: 'iframe',
    });
});

/*------------------------------------- Html Video Pop Up -------------------------------------*/
$(document).ready(function () {
    $(".html-popup").on('click', function () {
        $(".custom-model-main").addClass('model-open');
    });

    $(".close-btn, .bg-overlay").click(function () {
        $(".custom-model-main").removeClass('model-open');
    });
});

/*------------------------------------- Gallery Fancy Box -------------------------------------*/
$('[data-fancybox="gallery"]').fancybox({
    buttons: [
        "slideShow",
        "thumbs",
        "zoom",
        "fullScreen",
        "share",
        "close"
    ],
    loop: false,
    protect: true
});

/*------------------------------------- Containet Pop Up -------------------------------------*/
$(document).ready(function () {
    $('.trigger').click(function () {
        $('.modal-wrapper').toggleClass('open');
        $('.page-wrapper').toggleClass('blur');
        return false;
    });
});

/*------------------------------------- Testimonial Slider -------------------------------------*/
$(document).ready(function () {
    $('.testimonial_slider').slick({
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 1,
        autoplay: true,
        arrows: true,
        dots: false,
        speed: 1000,
        prevArrow: '<button type="button" class="slick-prev"><img src="/static/assets/images/slider-right-arrow.svg" alt="slider-right-arrow"></button>', // 这里注意使用/static,不能使用../
        nextArrow: '<button type="button" class="slick-next"><img src="/static/assets/images/slider-left-arrow.svg" alt="slider-left-arrow"></button>',
        responsive: [
            {
                breakpoint: 991,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    autoplay: true,
                    arrows: false,
                }
            }
        ]
    });
});

/*------------------------------------- Cursor -------------------------------------*/
let cursor = document.querySelector('.cursor');
let cursorScale = document.querySelectorAll('a,button,.nested-accordion,.trigger,.html-popup,.youtube,#vimeo,.link,.new-img-box-main,.cursor-pointer,.cursor-arrow,.play-button,.cf_image');
let mouseX = 0;
let mouseY = 0;

gsap.to({}, 0.016, {
    repeat: -1,
    onRepeat: function () {
        gsap.set(cursor, {
            css: {
                left: mouseX,
                top: mouseY,
            }
        })
    }
});

window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
})
cursorScale.forEach(link => {
    link.addEventListener('mousemove', () => {
        cursor.classList.add('grow');
        if (link.classList.contains('small')) {
            cursor.classList.remove('grow');
            cursor.classList.add('grow-small');
        }
    });

    link.addEventListener('mouseleave', () => {
        cursor.classList.remove('grow');
        cursor.classList.remove('grow-small');
    });
});

/*------------------------------------- Load More View Less btn -------------------------------------*/
$(document).ready(function () {
    $("#toggle").click(function () {
        var elem = $("#toggle").text();
        if (elem == "Load More") {
            $("#toggle").text("Load Less");
            $(".text").slideDown();
        } else {
            $("#toggle").text("Load More");
            $(".text").slideUp();
        }
    });
});

/*------------------------------------- Share Pop Up -------------------------------------*/
const viewBtn = document.querySelector(".view-modal");
const overlay2 = document.querySelector(".overlay2");
if (viewBtn) {
    viewBtn.onclick = () => {
        const popup = document.querySelector(".popup");
        const close = popup.querySelector(".close");

        popup.classList.toggle("show");
        overlay2.classList.toggle("show");

        close.onclick = () => {
            viewBtn.click();
        }

    }
}

/*------------------------------------- Scroll Bottom To Top -------------------------------------*/
var progressPath = document.querySelector('.progress-wrap path');
var pathLength = progressPath.getTotalLength();
progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
progressPath.style.strokeDashoffset = pathLength;
progressPath.getBoundingClientRect();
progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
var updateProgress = function () {
    var scroll = $(window).scrollTop();
    var height = $(document).height() - $(window).height();
    var progress = pathLength - (scroll * pathLength / height);
    progressPath.style.strokeDashoffset = progress;
}
updateProgress();
$(window).scroll(updateProgress);
var offset = 150;
var duration = 550;
jQuery(window).on('scroll', function () {
    if (jQuery(this).scrollTop() > offset) {
        jQuery('.progress-wrap').addClass('active-progress');
    } else {
        jQuery('.progress-wrap').removeClass('active-progress');
    }
});
jQuery('.progress-wrap').on('click', function (event) {
    event.preventDefault();
    jQuery('html, body').animate({
        scrollTop: 0
    }, duration);
    return false;
})

/*------------------------------------- Side Menu Accordion -------------------------------------*/
$(document).ready(function () {
    $(".accordion").on("click", ".heading", function () {
        if ($(this).hasClass("active")) {
            $(this).removeClass("active").next().slideUp(300);
        } else {
            $(".accordion .heading").removeClass("active");
            $(".accordion .contents").slideUp(300);
            $(this).addClass("active").next().slideDown(300);
        }
    });

    $(".accordion").on("click", ".sub-menu-side-menu", function () {
        if ($(this).hasClass("active")) {
            $(this).removeClass("active").next().slideUp(300);
        } else {
            $(".accordion .sub-menu-side-menu").removeClass("active");
            $(".accordion .sub-menu-side-menu").next(".contents").slideUp(300);
            $(this).addClass("active").next(".contents").slideDown(300);
        }
    });
});

/*------------------------------------- Full Screen Portfolio v6 -------------------------------------*/
(function ($) {
    "use strict";
    $(document).ready(function () {
        $('.case-study-name:nth-child(1)').on('mouseenter', function () {
            $('.case-study-name.active').removeClass('active');
            $('.case-study-images li.show').removeClass("show");
            $('.case-study-images li:nth-child(1)').addClass("show");
            $('.case-study-name:nth-child(1)').addClass('active');
        })
        $('.case-study-name:nth-child(2)').on('mouseenter', function () {
            $('.case-study-name.active').removeClass('active');
            $('.case-study-images li.show').removeClass("show");
            $('.case-study-images li:nth-child(2)').addClass("show");
            $('.case-study-name:nth-child(2)').addClass('active');
        })
        $('.case-study-name:nth-child(3)').on('mouseenter', function () {
            $('.case-study-name.active').removeClass('active');
            $('.case-study-images li.show').removeClass("show");
            $('.case-study-images li:nth-child(3)').addClass("show");
            $('.case-study-name:nth-child(3)').addClass('active');
        })
        $('.case-study-name:nth-child(4)').on('mouseenter', function () {
            $('.case-study-name.active').removeClass('active');
            $('.case-study-images li.show').removeClass("show");
            $('.case-study-images li:nth-child(4)').addClass("show");
            $('.case-study-name:nth-child(4)').addClass('active');
        })
        $('.case-study-name:nth-child(5)').on('mouseenter', function () {
            $('.case-study-name.active').removeClass('active');
            $('.case-study-images li.show').removeClass("show");
            $('.case-study-images li:nth-child(5)').addClass("show");
            $('.case-study-name:nth-child(5)').addClass('active');
        })
        $('.case-study-name:nth-child(1)').trigger('mouseenter')

    });
})(jQuery);

/*------------------------------------- Hover gallery portfolio v7 -------------------------------------*/
jQuery(document).ready(function ($) {

    var $overlay = $('<div id="overlay"></div>')
    var $image = $('<img>');

    $overlay.append($image);

    $('.thumb img').hover(function () {
        var $src = $(this).attr('src');
        $('#main-img img').attr('src', $src);
    });

    $('#main-img img').click(function () {
        $overlay.show();

        var imageLoad = $(this).attr('src');
        $image.attr('src', imageLoad);

    });

    $overlay.click(function () {
        $overlay.hide();
    });

});

/*------------------------------------- Infinite Marquee -------------------------------------*/
document.querySelectorAll('.logos').forEach(function (logosContainer) {
    const copy = logosContainer.querySelector('.logos-slide').cloneNode(true);
    logosContainer.appendChild(copy);
});

/*------------------------------------- Single Page Yoube Vimeo sound cloud Video -------------------------------------*/
function playVideo() {
    var cover = document.querySelector('.video-container img.cover');
    var playButton = document.querySelector('.video-container img.play-button');
    var iframe = document.getElementById('youtube-video');
    cover.style.display = 'none';
    playButton.style.display = 'none';
    iframe.src = "https://www.youtube.com/embed/f7sIhhjIBzc?autoplay=1";
    iframe.style.display = 'block';
}

function playVimeoVideo() {
    var cover = document.querySelector('.video-container img.cover');
    var playButton = document.querySelector('.video-container img.play-button');
    var iframe = document.getElementById('vimeo-video');
    cover.style.display = 'none';
    playButton.style.display = 'none';
    iframe.src = "https://player.vimeo.com/video/76979871?autoplay=1";
    iframe.style.display = 'block';
}

function playSoundCloudMusic() {
    var container = event.currentTarget;
    var cover = container.querySelector('img.cover');
    var playButton = container.querySelector('img.play-button');
    var iframe = container.querySelector('iframe');
    cover.style.display = 'none';
    playButton.style.display = 'none';
    iframe.src = "https://w.soundcloud.com/player/?url=https%3A//soundcloud.com/alanwalker/faded-slushii-remix-1?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true";
    iframe.style.display = 'block';
}

/*------------------------------------- Services-gallery-main-slider -------------------------------------*/
$(document).ready(function () {
    $('.services-gallery-main').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        arrows: true,
        dots: false,
        speed: 1600,
        prevArrow: '<button type="button" class="services-gallery-main-prev"><img src="/static/assets/images/slider-right-arrow.svg" alt="slider-right-arrow"></button>',
        nextArrow: '<button type="button" class="services-gallery-main-next"><img src="/static/assets/images/slider-left-arrow.svg" alt="slider-left-arrow"></button>',
    });
});