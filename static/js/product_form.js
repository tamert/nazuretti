$(function () {
  $('input[type=file]').each(function (i, el) {
    var $el = $(this);

    $el.fileupload({
      dataType: 'json',
      done: function (e, data) {
        var data   = data.result,
            img    = $('<img />'),
            $el    = $('input[type=file]').eq(i),
            inputs = ['x','y','w','h'],
            file   = $('<input />');

        file.attr({
          name:  'image-' + i,
          value: data.filename,
          type:  'hidden'
        });

        img.attr('src', data.url);
        $el.parent().append($('<div>').append(img));
        $el.parent().append(file);

        inputs = $(inputs).map(function () {
          var $inp = $('<input />').attr({
            type: 'hidden',
            name: 'image-' + i + this
          });

          $el.parent().append($inp);
          return $inp;
        });

        img.Jcrop({
          onChange: function (c) {
            $(['x','y','w','h']).each(function (i, el) {
              var $el = inputs[i];
              $el.val(c[el]);
            });
          }
        });
      }
    });
  });
});

