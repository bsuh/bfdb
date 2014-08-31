window.jsel = JSONSelect.match

$(function () {
  var data;

  $('select').chosen();
  $.get('info.json', function (r) {
    data = _.map(r, function (obj, name) {
      return _.extend({}, obj, {'name': name});
    });

    data = _.filter(data, function (unit) {
      return (unit.name != 'Metal Mimic');
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
    var tier = (max - min) / 5;

    var grouped = _.groupBy(data, function (unit) {
      var result = groupQuery(unit);
      if (typeof result === 'number' && max - min > 10) {
        return Math.floor(Math.floor((result - min) / tier) * tier + min);
      } else {
        return result;
      }
    });

    var _data = _.map(grouped, function (list, groupVar) {
      return {
        key: groupVar,
        values: _.filter(_.map(list, function (unit) {
          return _.extend({
            x: xQuery(unit),
            y: yQuery(unit),
            size: sizeQuery(unit),
          }, unit)
        }), function (point) {
          return isFinite(point.x) && isFinite(point.y);
        })
      };
    });

    var lastPoint;
    nv.addGraph(function() {
      var chart = nv.models.scatterChart()
        .showDistX(true)
        .showDistY(true)
        .color(d3.scale.category10().range());

      chart.tooltipContent(function(key, x, y, e, graph) {
        lastPoint = e.point;
        return '<h3>' + e.point.name + '</h3><p>' +
          $('#groupSelect option:selected').text() + ': ' + groupQuery(e.point) +
          '<br/>' +
          $('#sizeSelect option:selected').text() + ': ' + e.point.size + '</p>';
      });

      d3.select('#chart svg')
        .datum(_data)
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    }, function () {
      d3.selectAll('.nv-point-paths').on('click', function () {
        $('#detailedinfo').html(JSON.stringify(
          _.omit(lastPoint, ['x', 'y', 'size', 'series']), null, 2));
      });
    });
  }

  $('select').change(draw);
});
