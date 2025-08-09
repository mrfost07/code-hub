/* global Chart:false */

$(function () {
  'use strict';

  function initializeDashboard() {
    // Initialize Sales Chart
    var salesChart = $('#salesChart');
    if (salesChart.length > 0) {
      var salesChartCanvas = salesChart.get(0).getContext('2d');
      if (salesChartCanvas) {
        var salesChartData = {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
          datasets: [{
            label: 'Digital Goods',
            backgroundColor: 'rgba(60,141,188,0.9)',
            borderColor: 'rgba(60,141,188,0.8)',
            pointRadius: false,
            pointColor: '#3b8bba',
            pointStrokeColor: 'rgba(60,141,188,1)',
            pointHighlightFill: '#fff',
            pointHighlightStroke: 'rgba(60,141,188,1)',
            data: [28, 48, 40, 19, 86, 27, 90]
          }]
        };

        var salesChartOptions = {
          maintainAspectRatio: false,
          responsive: true,
          legend: { display: false },
          scales: {
            xAxes: [{ gridLines: { display: false } }],
            yAxes: [{ gridLines: { display: false } }]
          }
        };

        new Chart(salesChartCanvas, {
          type: 'line',
          data: salesChartData,
          options: salesChartOptions
        });
      }
    }

    // Initialize Pie Chart
    var pieChart = $('#pieChart');
    if (pieChart.length > 0) {
      var pieChartCanvas = pieChart.get(0).getContext('2d');
      if (pieChartCanvas) {
        var pieData = {
          labels: ['Chrome', 'IE', 'FireFox', 'Safari', 'Opera', 'Navigator'],
          datasets: [{
            data: [700, 500, 400, 600, 300, 100],
            backgroundColor: ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de']
          }]
        };

        new Chart(pieChartCanvas, {
          type: 'doughnut',
          data: pieData,
          options: { legend: { display: false } }
        });
      }
    }

    // Initialize World Map
    var worldMap = $('#world-map-markers');
    if (worldMap.length > 0) {
      try {
        worldMap.mapael({
          map: {
            name: 'usa_states',
            zoom: {
              enabled: true,
              maxLevel: 10
            }
          }
        });
      } catch (e) {
        console.warn('Failed to initialize world map:', e);
      }
    }
  }

  // Initialize all components
  try {
    initializeDashboard();
  } catch (e) {
    console.warn('Error initializing dashboard:', e);
  }
});
  'use strict';

  // Handle missing elements gracefully
  function safeGet(selector) {
    return $(selector).length > 0 ? $(selector) : null;
  }

  // Safely get canvas context
  function getContext(selector) {
    var element = safeGet(selector);
    return element ? element.get(0).getContext('2d') : null;
  }

  // Safely get canvas context
  function getContext(selector) {
    var element = $(selector);
    return element.length > 0 ? element.get(0).getContext('2d') : null;
  }

  // Safely initialize chart
  function initializeChart(selector, chartType, data, options) {
    var context = getContext(selector);
    if (!context) return null;
    
    try {
      return new Chart(context, {
        type: chartType,
        data: data,
        options: options
      });
    } catch (e) {
      console.warn('Failed to initialize chart:', selector, e);
      return null;
    }
  }

  /* ChartJS
   * -------
   * Here we will create a few charts using ChartJS
   */

  // Initialize all charts conditionally
  function initializeCharts() {
    // Sales Chart
    if ($('#salesChart').length > 0) {
      var salesChartData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [
          {
            label: 'Digital Goods',
            backgroundColor: 'rgba(60,141,188,0.9)',
            borderColor: 'rgba(60,141,188,0.8)',
            pointRadius: false,
            pointColor: '#3b8bba',
            pointStrokeColor: 'rgba(60,141,188,1)',
            pointHighlightFill: '#fff',
            pointHighlightStroke: 'rgba(60,141,188,1)',
            data: [28, 48, 40, 19, 86, 27, 90]
          }
        ]
      };

      var salesChartOptions = {
        maintainAspectRatio: false,
        responsive: true,
        legend: { display: false },
        scales: {
          xAxes: [{ gridLines: { display: false } }],
          yAxes: [{ gridLines: { display: false } }]
        }
      };

      initializeChart('#salesChart', 'line', salesChartData, salesChartOptions);
    }

    // Pie Chart
    if ($('#pieChart').length > 0) {
      var pieData = {
        labels: ['Chrome', 'IE', 'FireFox', 'Safari', 'Opera', 'Navigator'],
        datasets: [{
          data: [700, 500, 400, 600, 300, 100],
          backgroundColor: ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de']
        }]
      };

      initializeChart('#pieChart', 'doughnut', pieData, {
        legend: { display: false }
      });
    }

    // World Map
    var worldMap = $('#world-map-markers');
    if (worldMap.length > 0) {
      try {
        worldMap.mapael({
          map: {
            name: 'usa_states',
            zoom: { enabled: true, maxLevel: 10 }
          }
        });
      } catch (e) {
        console.warn('Failed to initialize world map:', e);
      }
    }
  }

  // Initialize everything
  initializeCharts();

  // Get context with jQuery - using jQuery's .get() method.
  var salesChart = $('#salesChart');
  if (salesChart.length > 0) {
    var salesChartCanvas = salesChart.get(0).getContext('2d');
  } else {
    return; // Exit if chart element doesn't exist
  }

  var salesChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'Digital Goods',
        backgroundColor: 'rgba(60,141,188,0.9)',
        borderColor: 'rgba(60,141,188,0.8)',
        pointRadius: false,
        pointColor: '#3b8bba',
        pointStrokeColor: 'rgba(60,141,188,1)',
        pointHighlightFill: '#fff',
        pointHighlightStroke: 'rgba(60,141,188,1)',
        data: [28, 48, 40, 19, 86, 27, 90]
      },
      {
        label: 'Electronics',
        backgroundColor: 'rgba(210, 214, 222, 1)',
        borderColor: 'rgba(210, 214, 222, 1)',
        pointRadius: false,
        pointColor: 'rgba(210, 214, 222, 1)',
        pointStrokeColor: '#c1c7d1',
        pointHighlightFill: '#fff',
        pointHighlightStroke: 'rgba(220,220,220,1)',
        data: [65, 59, 80, 81, 56, 55, 40]
      }
    ]
  }

  var salesChartOptions = {
    maintainAspectRatio: false,
    responsive: true,
    legend: {
      display: false
    },
    scales: {
      xAxes: [{
        gridLines: {
          display: false
        }
      }],
      yAxes: [{
        gridLines: {
          display: false
        }
      }]
    }
  }

  // This will get the first returned node in the jQuery collection.
  // eslint-disable-next-line no-unused-vars
  var salesChart = new Chart(salesChartCanvas, {
    type: 'line',
    data: salesChartData,
    options: salesChartOptions
  }
  )

  //---------------------------
  // - END MONTHLY SALES CHART -
  //---------------------------

  //-------------
  // - PIE CHART -
  //-------------
  // Get context with jQuery - using jQuery's .get() method.
  var pieChartCanvas = $('#pieChart').get(0).getContext('2d')
  var pieData = {
    labels: [
      'Chrome',
      'IE',
      'FireFox',
      'Safari',
      'Opera',
      'Navigator'
    ],
    datasets: [
      {
        data: [700, 500, 400, 600, 300, 100],
        backgroundColor: ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de']
      }
    ]
  }
  var pieOptions = {
    legend: {
      display: false
    }
  }
  // Create pie or douhnut chart
  // You can switch between pie and douhnut using the method below.
  var pieChartElement = $('#pieChart');
  if (pieChartElement.length > 0) {
    var pieChartCanvas = pieChartElement.get(0).getContext('2d');
    // eslint-disable-next-line no-unused-vars
    var pieChart = new Chart(pieChartCanvas, {
      type: 'doughnut',
      data: pieData,
      options: pieOptions
    });
  }

  //-----------------
  // - END PIE CHART -
  //-----------------

  /* jVector Maps
   * ------------
   * Create a world map with markers
   */
  var worldMap = $('#world-map-markers');
  if (worldMap.length > 0) {
    worldMap.mapael({
    map: {
      name: 'usa_states',
      zoom: {
        enabled: true,
        maxLevel: 10
      }
    }
  })

  // $('#world-map-markers').vectorMap({
  //   map              : 'world_en',
  //   normalizeFunction: 'polynomial',
  //   hoverOpacity     : 0.7,
  //   hoverColor       : false,
  //   backgroundColor  : 'transparent',
  //   regionStyle      : {
  //     initial      : {
  //       fill            : 'rgba(210, 214, 222, 1)',
  //       'fill-opacity'  : 1,
  //       stroke          : 'none',
  //       'stroke-width'  : 0,
  //       'stroke-opacity': 1
  //     },
  //     hover        : {
  //       'fill-opacity': 0.7,
  //       cursor        : 'pointer'
  //     },
  //     selected     : {
  //       fill: 'yellow'
  //     },
  //     selectedHover: {}
  //   },
  //   markerStyle      : {
  //     initial: {
  //       fill  : '#00a65a',
  //       stroke: '#111'
  //     }
  //   },
  //   markers          : [
  //     {
  //       latLng: [41.90, 12.45],
  //       name  : 'Vatican City'
  //     },
  //     {
  //       latLng: [43.73, 7.41],
  //       name  : 'Monaco'
  //     },
  //     {
  //       latLng: [-0.52, 166.93],
  //       name  : 'Nauru'
  //     },
  //     {
  //       latLng: [-8.51, 179.21],
  //       name  : 'Tuvalu'
  //     },
  //     {
  //       latLng: [43.93, 12.46],
  //       name  : 'San Marino'
  //     },
  //     {
  //       latLng: [47.14, 9.52],
  //       name  : 'Liechtenstein'
  //     },
  //     {
  //       latLng: [7.11, 171.06],
  //       name  : 'Marshall Islands'
  //     },
  //     {
  //       latLng: [17.3, -62.73],
  //       name  : 'Saint Kitts and Nevis'
  //     },
  //     {
  //       latLng: [3.2, 73.22],
  //       name  : 'Maldives'
  //     },
  //     {
  //       latLng: [35.88, 14.5],
  //       name  : 'Malta'
  //     },
  //     {
  //       latLng: [12.05, -61.75],
  //       name  : 'Grenada'
  //     },
  //     {
  //       latLng: [13.16, -61.23],
  //       name  : 'Saint Vincent and the Grenadines'
  //     },
  //     {
  //       latLng: [13.16, -59.55],
  //       name  : 'Barbados'
  //     },
  //     {
  //       latLng: [17.11, -61.85],
  //       name  : 'Antigua and Barbuda'
  //     },
  //     {
  //       latLng: [-4.61, 55.45],
  //       name  : 'Seychelles'
  //     },
  //     {
  //       latLng: [7.35, 134.46],
  //       name  : 'Palau'
  //     },
  //     {
  //       latLng: [42.5, 1.51],
  //       name  : 'Andorra'
  //     },
  //     {
  //       latLng: [14.01, -60.98],
  //       name  : 'Saint Lucia'
  //     },
  //     {
  //       latLng: [6.91, 158.18],
  //       name  : 'Federated States of Micronesia'
  //     },
  //     {
  //       latLng: [1.3, 103.8],
  //       name  : 'Singapore'
  //     },
  //     {
  //       latLng: [1.46, 173.03],
  //       name  : 'Kiribati'
  //     },
  //     {
  //       latLng: [-21.13, -175.2],
  //       name  : 'Tonga'
  //     },
  //     {
  //       latLng: [15.3, -61.38],
  //       name  : 'Dominica'
  //     },
  //     {
  //       latLng: [-20.2, 57.5],
  //       name  : 'Mauritius'
  //     },
  //     {
  //       latLng: [26.02, 50.55],
  //       name  : 'Bahrain'
  //     },
  //     {
  //       latLng: [0.33, 6.73],
  //       name  : 'São Tomé and Príncipe'
  //     }
  //   ]
  // })
})

// lgtm [js/unused-local-variable]