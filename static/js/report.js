function generate() {
  var fromdate = document.getElementById('from-date').value;
  var todate = document.getElementById('to-date').value;
  console.log(fromdate);
  var doc = new jsPDF('p', 'pt', 'letter');
  var htmlstring = '';
  var tempVarToCheckPageHeight = 0;
  var pageHeight = 0;
  pageHeight = doc.internal.pageSize.height;
  specialElementHandlers = {
    // element with id of "bypass" - jQuery style selector  
    '#bypassme': function (element, renderer) {
      // true = "handled elsewhere, bypass text extraction"  
      return true
    }
  };
  margins = {
    top: 15,
    bottom: 6,
    left: 10,
    right: 10,
    width: 100
  };
  var y = 20;
  doc.setLineWidth(2);
  if (document.getElementById('report')) {
    var res = doc.autoTableHtmlToJson(document.getElementById('report'));
    doc.autoTable(res.columns, res.data);
  }
  if (document.getElementById('myTable1')) {
    var res1 = doc.autoTableHtmlToJson(document.getElementById('myTable1'));
    doc.autoTable(res1.columns, res1.data);
  }
  // doc.autoTable(res1.columns, res1.data);
  if (document.getElementById('myTable2')) {
    var res2 = doc.autoTableHtmlToJson(document.getElementById('myTable2'));
    doc.autoTable(res2.columns, res2.data);
  }
  // doc.autoTable(res2.columns, res2.data);
  if (document.getElementById('myTable3')) {
    var res3 = doc.autoTableHtmlToJson(document.getElementById('myTable3'));
    doc.autoTable(res3.columns, res3.data);
  }
  // doc.autoTable(res3.columns, res3.data);
  if (document.getElementById('totalTable')) {
    var res4 = doc.autoTableHtmlToJson(document.getElementById('totalTable'));
    doc.autoTable(res4.columns, res4.data, {
      theme: 'grid',

    })
  }

  doc.save(fromdate + "__" + todate + '_report.pdf');
  // doc.output('dataurlnewwindow');
}


function SearchbyNameReport() {
  let field = document.getElementById('search_field').value;
  let value = document.getElementById('search_value').value;
  let rank = document.getElementById('select-rank').value;

  if (["Staff","Members","Army","other"].includes(rank)) {

  if (field != '' && value != '') {
    $.ajax({
      method: "GET",
      url: "/api/SearchbyNameReport/",
      data: { "field": field, "value": value, "rank": rank },
      success: function (data) {
        // console.log("success on search" + data);
        update_table(data)
      },
      error: function () {
        console.log('error');
      }

    })
  }
}
else{
  console.log(field,value)
  if (field != '' && value != '') {
    $.ajax({
      method: "GET",
      url: "/api/SearchbyNameReport/",
      data: { "field": field, "value": value },
      success: function (data) {
        // console.log("success on search" + data);
        update_table(data)
      },
      error: function () {
        console.log('error');
      }

    })
  }
}
};

function SearchByRankReport(data){
  let rank = data.value;
  if (["Staff","Members","Army","other"].includes(rank)) {
  $.ajax({
    method: "GET",
    url: "/api/sales/SearchByRankReport/",
    data: {"rank": rank},
    success: function (data) {
      // console.log("success on search" + data);
      update_table(data)
    },
    error: function () {
      console.log('error');
    }

  })
}
else{
  alert("Please select a rank");
}
};

function update_table(data) {
  console.log(data);
  let row;
  let all_rows = '';

  Object.keys(data).forEach(key => {
    elem = data[key];
    console.log(elem['status']);
    if (elem['status'] == 'Paid') {
      row = '<tr>' +
        // '<td>'+elem['id']+'</td>' +
        '<td>' + elem['sale_id']['bill_no'] + '</td>' +
        '<td>' + elem['rv_no'] + '</td>' +
        '<td>' + elem['sale_id']['PoS_no'] + '</td>' +
        '<td>' + elem['sale_id']['customer_id']['customer_rank'] + '</td>' +
        '<td>' + elem['sale_id']['customer_id']['customer_name'] + '</td>' +
        '<td>' + elem['sale_id']['address'] + '</td>' +
        '<td>' + elem['sale_id']['created_date'] + '</td>' +
        '<td>' + elem['sale_id']['account_of'] + '</td>' +
        '<td>' + elem['sale_id']['month'] + '</td>' +
        '<td>' + elem['amount'] + '</td>' +
        '<td>' + elem['date'] + '</td>' +
        '<td>' +
        '<p class="modal" style="background-color: #0c7ed6; text-align: center; color: rgb(246, 244, 244);">' + elem['status'] + '</p>' +
        '</td>' +
        '</tr>'
    }
    else if (elem['status'] == 'Complementery') {
      row = '<tr>' +
        // '<td>'+elem['id']+'</td>' +
        '<td>' + elem['sale_id']['bill_no'] + '</td>' +
        '<td>' + elem['rv_no'] + '</td>' +
        '<td>' + elem['sale_id']['PoS_no'] + '</td>' +
        '<td>' + elem['sale_id']['customer_id']['customer_rank'] + '</td>' +
        '<td>' + elem['sale_id']['customer_id']['customer_name'] + '</td>' +
        '<td>' + elem['sale_id']['address'] + '</td>' +
        '<td>' + elem['sale_id']['created_date'] + '</td>' +
        '<td>' + elem['sale_id']['account_of'] + '</td>' +
        '<td>' + elem['sale_id']['month'] + '</td>' +
        '<td>' + elem['amount'] + '</td>' +
        '<td>' + elem['date'] + '</td>' +
        '<td>' +
        '<p class="modal" style="background-color: #1e659c; text-align: center; color: rgb(246, 244, 244);">' + elem['status'] + '</p>' +
        '</td>' +
        '</tr>'
    }
    else if (elem['status'] == 'Cancelled') {
      row = '<tr>' +
        // '<td>'+elem['id']+'</td>' +
        '<td>' + elem['sale_id']['bill_no'] + '</td>' +
        '<td>' + elem['rv_no'] + '</td>' +
        '<td>' + elem['sale_id']['PoS_no'] + '</td>' +
        '<td>' + elem['sale_id']['customer_id']['customer_rank'] + '</td>' +
        '<td>' + elem['sale_id']['customer_id']['customer_name'] + '</td>' +
        '<td>' + elem['sale_id']['address'] + '</td>' +
        '<td>' + elem['sale_id']['created_date'] + '</td>' +
        '<td>' + elem['sale_id']['account_of'] + '</td>' +
        '<td>' + elem['sale_id']['month'] + '</td>' +
        '<td>' + elem['amount'] + '</td>' +
        '<td>' + elem['date'] + '</td>' +
        '<td>' +
        '<p class="modal" style="background-color: #6a6a6a; text-align: center; color: rgb(246, 244, 244);">' + elem['status'] + '</p>' +
        '</td>' +
        '</tr>'
    }
    all_rows += row;
  }
  );
  $('#report tbody').html(all_rows);

}