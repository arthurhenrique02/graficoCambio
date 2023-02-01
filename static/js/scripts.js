// store data into memory
stored_data = [];
categories_datetime = [];

var options = {

    // title text
    title: {
        text: "Exchange rate per day",
        align: "center",
        margin: 15,
        offsetY: 5,
    },

    // create chart
    chart: {
        height: "100%",
        width: "100%",
        type: "area",
        background: "#FFFFFF",
        foreColor: "#000000",
        toolbar: {
            autoSelected: "pan",
            // get rid of toolbar
            show: false
          }
    },

    // graph color
    colors: ["#6100FF"],

    // curves and lines
    stroke: {
        curve: "smooth",
        width: 2,
    },

    // add and style marks
    markers: {
        size: 2,
        colors: "#6200ffE0",
        strokeColor: "#6200ff",
        strokeWidth: 2,
    },

    // style grid
    grid:{
        borderColor: "#000000",
        clipMarkers: false,
        // get rid of grid lines
        yaxis: {
            lines: {
                show: false,
            },
        },
        xaxis: {
            lines: {
                show: false,
            },
        },
    },

    // add data
    series: [{
    name: 'Exchange value',
    data: stored_data
  }],

  dataLabels: {
    enabled: false
  },

  xaxis: {
    type: 'datetime',
    categories: stored_data
  },

  tooltip: {
    theme: "",
    x: {
      format: 'dd/MM/yy'
    },
  },
  };

  var exchangeChart = new ApexCharts(document.querySelector("#chart"), options);
  exchangeChart.render();


// define 7 days by default
atual_days = 7;
// change days
async function changeDays(value){
  // change atual days variables
  async function newDays(){
    // if is valid value, put into atual_days
    if (value == 7 || value == 30){
      atual_days = value;
      return;
    };
    // if not valid, days are equals 7
    atual_days = 7;
    return;
  }

  // exec change currencie function, to change graph
  newDays().then(
    changeCurrencie(document.getElementById("currencies").value)
  )
};

// function to connect api and change graph
async function changeCurrencie(currencie){
    // API URL
    const API_URL = "http://127.0.0.1:5000/exchanges/";

    // fetch response
    const response = await fetch(API_URL + currencie + "/" + atual_days);
    // make json response
    const dataResponse = await response.json();

    // clear stored data lists
    stored_data = []
    categories_datetime = []

    // save date and exchanges
    for(let item in dataResponse.exchanges){
        stored_data.push(dataResponse.exchanges[item].rates)
        categories_datetime.push(dataResponse.exchanges[item].date)
    };


    // change today`s text
    document.getElementById("convertText").innerHTML=(`EUR to ${currencie}`)
    document.getElementById("exchangeValue").innerHTML=(`$${stored_data[0]}`)

    // Update graph
    exchangeChart.updateOptions({
      series: [{
        data: stored_data
      }],
      xaxis: {
        categories: categories_datetime,
      }
    })
};

// load USD currencies when pages load
window.addEventListener("load", changeCurrencie("USD"))