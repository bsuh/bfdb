window.jsel = JSONSelect.match

$(function () {
  var data;

  $('select').chosen();
  $.get('info.json', function (r) {
    data = _.map(r, function (obj, name) {
      return _.extend({}, obj, {'name': name});
    });

    data = _.filter(data, function (unit) {
      return (unit.name != 'Metal Mimic') &&
        (unit.name != 'Creator Maxwell');
    });

    draw();
  });

  var fnCache = {};
  function draw() {
    function query(selector) {
      return function (unit) {
        var src = '(unit) -> ' + $(selector).val();
        var fn = fnCache[src] || eval(CoffeeScript.compile(src, { bare: true }));
        fnCache[src] = fn;
        return fn(unit);
      };
    };

    if (!data) {
      return;
    }

    var groupQuery = query('#groupSelect');
    var xQuery = query('#xSelect');
    var yQuery = query('#ySelect');
    var sizeQuery = query('#sizeSelect');

    var min = groupQuery(_.min(data, groupQuery));
    var max = groupQuery(_.max(data, groupQuery)) + 1;

    var grouped = _.groupBy(data, function (unit) {
      return groupQuery(unit);
    });

    var colors = {
      'fire': 'rgb(214, 39, 40)',
      'light': 'rgb(247, 182, 210)',
      'thunder': 'rgb(255, 127, 14)',
      'dark': 'rgb(127, 127, 127)',
      'water': 'rgb(31, 119, 180)',
      'earth': 'rgb(44, 160, 44)',
    };

    function defaultColor(i) {
      var colors = d3.scale.category10().range();
      return colors[i % colors.length];
    }

    var i = 0;
    var _data = _.map(grouped, function (list, groupVar) {
      i += 1;
      return {
        name: groupVar,
        data: _.filter(_.map(list, function (unit) {
          return {
            x: xQuery(unit),
            y: yQuery(unit),
            z: sizeQuery(unit),
            extra: unit
          };
        }), function (point) {
          return isFinite(point.x) && isFinite(point.y);
        }),
        color: colors[groupVar] || defaultColor(i-1)
      };
    });

    $('#chart').highcharts({
      chart: {
        type: 'bubble',
        zoomType: 'xy',
      },

      title: {
        text: null
      },

      legend: {
        layout: 'horizontal',
        align: 'right',
        verticalAlign: 'top',
        x: 0,
        y: -10,
        floating: true,
        backgroundColor: '#FFFFFF',
      },

      tooltip: {
        headerFormat: '<span style="font-size: 16px">{point.point.extra.name}</span><br/>',
        pointFormat: $('#ySelect option:selected').text() + ': {point.y}<br/>' +
          $('#xSelect option:selected').text() + ': {point.x}<br/>' +
          $('#sizeSelect option:selected').text() + ': {point.z}'
      },

      plotOptions: {
        bubble: {
          maxSize: 32/Math.PI,
          minSize: 8/Math.PI,
          dataLabels: {
            enabled: false,
            formatter: function () {
              return this.point.extra.name;
            }
          }
        },

        series: {
          point: {
            events: {
              click: function () {
                $('#detailedinfo').html(JSON.stringify(this.extra, null, 2));
              }
            }
          }
        }
      },

      xAxis: {
        gridLineWidth: 1
      },

      series: _data
    });
  }

  $('select').change(draw);
});
