$(function () {
  $('input[type=file]').each(function (i, el) {
    var $el         = $(this),
        cropperTemp = null;

    $el.fileupload({
      dataType: 'json',
      done: function (e, data) {
        var data     = data.result,
            img      = $('<img />'),
            $el      = $('input[type=file]').eq(i),
            inputs   = ['x','y','x2','y2'],
            $file    = $('<input />'),
            size     = data.size,
            $cropper = $('#' + $el.attr('name') + '-cropper');

        if (cropperTemp) { 
          $.post('/admin/mirrorimage/clean/', {
            filename: cropperTemp
          });
        }

        cropperTemp  = data.filename;

        $file.attr({
          name:  'image-' + i,
          value: data.filename,
          type:  'hidden'
        });

        img.attr('src', data.url);

        $cropper.html('');
        $cropper.append(img).append($file);

        inputs = $(inputs).map(function () {
          var $inp = $('<input />').attr({
            type: 'hidden',
            name: 'image-' + i + this
          });

          $cropper.append($inp);
          return $inp;
        });

        img.Jcrop({
          onChange: function (c) {
            $(['x','y','x2','y2']).each(function (i, el) {
              var $el = inputs[i];
              $el.val(c[el]);
            });
          },
          aspectRatio: 260 / 150,
          boxWidth: 500,
          trueSize: [size.width, size.height],
          minSize: [260, 150],
        });
      }
    });
  });
});

