$(function () {
  $('select').chosen();

  $('#groupSelect').change(function () {
    var selector = $(this).val();
  });

  $.get('info.json', function (r) {
    data = r;

    var with_name = _.map(data, function (obj, name) {
      return _.extend({}, obj, {'name': name});
    });

    var by_rarity = _.groupBy(with_name, 'rarity');

    var atk_vs_effhp = _.map(by_rarity, function (list, rarity) {
      return {
        key: rarity + '*',
        values: _.map(list, function (unit) {
          return {
            x: unit['lord hp'] + unit['lord def'] / 3,
            y: unit['lord atk'],
            size: (unit.sbb && (unit.sbb['max bc generated'] || unit.sbb.levels[9]['max bc generated'])) ||
              (unit.bb && (unit.bb['max bc generated'] || unit.bb.levels[9]['max bc generated'])) ||
              unit['max bc generated'],
            name: unit['name']
          };
        })
      };
    });

    var dmg_vs_effhp = _.map(by_rarity, function (list, rarity) {
      return {
        key: rarity + '*',
        values: _.map(list, function (unit) {
          function getDmg(unit) {
            var dmg = 'lord damage range';
            if (unit.sbb && unit.sbb.levels[9][dmg]) {
              return Number(unit['sbb'].levels[9][dmg].split('~')[1]);
            }

            if (unit.bb && unit.bb.levels[9][dmg]) {
              return Number(unit['bb'].levels[9][dmg].split('~')[1]);
            }

            return Number(unit[dmg].split('~')[1]);
          }

          return _.extend({}, {
            x: unit['lord hp'] + unit['lord def'] / 3,
            y: getDmg(unit),
            size: (unit.sbb && (unit.sbb['max bc generated'] || unit.sbb.levels[9]['max bc generated'])) ||
              (unit.bb && (unit.bb['max bc generated'] || unit.bb.levels[9]['max bc generated'])) ||
              unit['max bc generated'],
          }, unit);
        })
      };
    });

    nv.addGraph(function() {
      var chart = nv.models.scatterChart()
        .showDistX(true)
        .showDistY(true)
        .color(d3.scale.category10().range());

      chart.tooltipContent(function(key, x, y, e, graph) {
        return '<h3>' + e.point.name + '</h3>';
      });

      chart.xAxis.tickFormat(d3.format('100f'));
      chart.yAxis.tickFormat(d3.format('100f'));

      d3.select('#chart svg')
        .datum(dmg_vs_effhp)
        .transition().duration(500)
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
  });
});
