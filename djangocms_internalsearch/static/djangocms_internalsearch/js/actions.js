(function($) {
    if (!$) {
        return;
    }

    $(function() {
        $('.js-internal-search-close-sideframe').on('click', function () {
            try {
                window.top.CMS.API.Sideframe.close();
            } catch (e) {}
        });
    });

})((typeof django !== 'undefined' && django.jQuery) || (typeof CMS !== 'undefined' && CMS.$) || false);
