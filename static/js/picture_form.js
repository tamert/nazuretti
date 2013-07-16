$(function () {
  $('input[data-crop=true]').each(function (i, el) {
    var $el         = $(el),
        cropperTemp = null,
        modelName   = $el.data('model-name');

    $el.fileupload({
      dataType: 'json',
      formData: (modelName ? {model_name:modelName} : {}),
      done: function (e, data) {
        var data     = data.result,
            img      = $('<img />'),
            $el      = $('input[data-crop=true]').eq(i),
            inputs   = ['x','y','x2','y2'],
            $file    = $('<input />'),
            size     = data.size,
            name     = $el.attr('name'),
            
            minWidth = $el.data('crop-min-width'),
            minHeight = $el.data('crop-min-height'),
            maxWidth  = $el.data('max-width'),
            ratio     = $el.data('crop-ratio'),

      
            mirrorUrl = $el.data('mirror-url');

        if (cropperTemp) { 
          options = { filename: cropperTemp };
          
          if (modelName) {
            options.model_name = modelName;
          }

          $.post(mirrorUrl + 'clean/', options);
        }

        cropperTemp  = data.filename;

        $file.attr({
          name:  name + '-filename',
          value: data.filename,
          type:  'hidden'
        });

        img.attr('src', data.url);

        var $cropper = $('#' + name + '-cropper');
        if ($cropper.length == 0) {
          $cropper = $('<div id="' + name + '-cropper">')
          $cropper.appendTo($el.parent());
        }

        $cropper.html('');
        $cropper.append(img).append($file);

        inputs = $(inputs).map(function () {
          var $inp = $('<input />').attr({
            type: 'hidden',
            name: name+'-' + this
          });

          $cropper.append($inp);
          return $inp;
        });

        options = {
          onChange: function (c) {
            $(['x','y','x2','y2']).each(function (i, el) {
              var $el = inputs[i];
              $el.val(c[el]);
            });
          },
          trueSize: [size.width, size.height],
        };

        if (ratio) {
          options.aspectRatio = parseFloat(ratio);
        }

        if (maxWidth) {
          options.boxWidth    = maxWidth;
        }

        if (minWidth || minHeight) {
          options.minSize     = [minWidth, minHeight];
        }

        img.Jcrop(options);
      }
    });
  });
});

