$(function () {
  $('input[type=file]').each(function (i, el) {
    var $el = $(this);

    $el.fileupload({
      dataType: 'json',
      done: function (e, data) {
        var data   = data.result,
            img    = $('<img />'),
            $el    = $('input[type=file]').eq(i),
            inputs = ['x','y','x2','y2'],
            file   = $('<input />'),
            size   = data.size;

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
            $(['x','y','x2','y2']).each(function (i, el) {
              var $el = inputs[i];
              $el.val(c[el]);
            });
          },
          boxWidth: 500,
          trueSize: [size.width, size.height]
        });
      }
    });
  });
});

