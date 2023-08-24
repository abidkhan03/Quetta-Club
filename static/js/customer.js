// function SearchCustomer() {
//   let field = document.getElementById('search_field').value;
//   let value = document.getElementById('search_value').value;

//   if (field != '' && value != '') {
//     $.ajax({
//       method: "GET",
//       url: "/api/SearchCustomer/",
//       data: { "field": field, "value": value },
//       success: function (data) {
//         // console.log("success on search" + data);
//         update_table(data)
//       },
//       error: function () {
//         console.log('error');
//       }

//     })
//   }
// };

var $rows = $('#tbody tr');
$('#search_value').keyup(function() {
    // var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
    
    // $rows.show().filter(function() {
    //     var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
    //     return !~text.indexOf(val);
    // }).hide();
    var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
    let select= document.getElementById('search_field').value;
    console.log(val);

    if (select == 'Name') {
      $rows.show().filter(function() {
        var text = $(this).find('td').eq(1).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
      }).hide();
    }
    else if (select == 'ID') {
      $rows.show().filter(function() {
        var text = $(this).find('td').eq(3).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
      }).hide();
    }
    else if (select == 'Address') {
      $rows.show().filter(function() {
        var text = $(this).find('td').eq(2).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
      }).hide();
    }
    else if (select == 'Rank') {
      $rows.show().filter(function() {
        var text = $(this).find('td').eq(0).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
      }).hide();
    }
});

function update_table(data) {
  console.log(data);
  let row;
  let all_rows = '';
  Object.keys(data).forEach(key => {
    console.log(data[key]);
    elem = data[key];
    console.log(elem);
    
    if (elem['customers_table']) {
    row = '<tr>' +
      '<td>' + elem['customer_rank'] + '</td>' +
      '<td>' + elem['customer_name'] + '</td>' +
      '<td>' + elem['customer_address'] + '</td>' +
      '<td>' + elem['customer_id'] + '</td>' +
      '<td>' + elem['total_amount'] + '</td>' +
      '<td>' +
      '<div class="list-btn">' +
      '<a href="/customer_bill/?id='+elem['id']+'" style="background-color:#1e659c; text-align: center;">Add a Bill</a>' +
      '<a href="/customer_details/?id='+elem['id']+'" style="text-align: center;">All Bills</a>' +
      '<a href="/customer_update/?id='+elem['id']+'" style="background-color: #1e659c;">Edit</a>' +
      '</div>' +
      '</td>' +
      '</tr>'
    }
    else {
      row = '<tr>' +
      '<td>' + elem['customer_rank'] + '</td>' +
      '<td>' + elem['customer_name'] + '</td>' +
      '<td>' + elem['customer_address'] + '</td>' +
      '<td>' + elem['customer_id'] + '</td>' +
      '<td>' + elem['0'] + '</td>' +
      '<td>' +
      '<div class="list-btn">' +
      '<a href="/customer_bill/?id='+elem['id']+'" style="background-color:#1e659c; text-align: center;">Add a Bill</a>' +
      '<a href="/customer_details/?id='+elem['id']+'" style="text-align: center;">All Bills</a>' +
      '<a href="/customer_update/?id='+elem['id']+'" style="background-color: #1e659c;">Edit</a>' +
      '</div>' +
      '</td>' +
      '</tr>'
    }
    all_rows += row;
  });
  $('#Customers_Data tbody').html(all_rows);
};

function SearchbyName() {
  let field = document.getElementById('search_field').value;
  let value = document.getElementById('search_value').value;

  if (field != '' && value != '') {
    $.ajax({
      method: "GET",
      url: "/api/SearchbyName/",
      data: { "field": field, "value": value },
      success: function (data) {
        // console.log("success on search" + data);
        update_bill_table(data)
      },
      error: function () {
        console.log('error');
      }

    })
  }
};

function update_bill_table(data) {
  console.log(data);
  let row;
  let all_rows = '';

  Object.keys(data).forEach(key => {
    elem = data[key];
    console.log(elem);
    console.log(elem['amount'] > 0);
    if (elem['amount'] > 0) {
      row = '<tr>' +
        // '<td>'+elem['id']+'</td>' +
        '<td>' + elem['bill_no'] + '</td>' +
        '<td>' + elem['month'] + '</td>' +
        '<td>' + elem['customer_id']['customer_rank'] + '</td>' +
        '<td>' + elem['PoS_no'] + '</td>' +
        '<td>' + elem['customer_id']['customer_name'] + '</td>' +
        // '<td>'+elem['customer_id']+'</td>' +
        '<td>' + elem['address'] + '</td>' +
        '<td>' + elem['account_of'] + '</td>' +
        '<td>' + elem['date'] + '</td>' +
        '<td>' + elem['amount'] + '</td>' +
        '<td>' + elem['discount'] + '</td>' +
        '<td>' + elem['net_amount'] + '</td>' +
        '<td>' + elem['remarks'] + '</td>' +
        '<td>' +
        '<div class="list">' +
        '<a href="/Sales/update_sales/?id=' +elem['id']+'" style="background-color: #1e659c; ">Edit</a>' +
        '<button class="modal" id="paid_modal" onclick="paidMOdalOpen('+elem['id']+','+elem['net_amount']+')" style="background-color: #1e659c; ">Paid</button>' +
        '<button id="comp_modal" class="modal" onclick="compModalOpen('+elem['id']+','+elem['net_amount']+')">Complemantery</button>' +
        '<button id="cancel_modal" class="modal" onclick="cancelModalOpen('+elem['id']+','+elem['net_amount']+')" style="background-color: #6a6a6a;;">Cancelled</button>' +
        '</div>' +
        '</td>' +
        '</tr>'
      all_rows += row;
    }
  });
  $('#Sales_data tbody').html(all_rows);

}



let paidModal = document.querySelector(".paidModal-open")
let compModal = document.querySelector(".compModal-open")
let cancelModal = document.querySelector(".cancelModal-open")

// paid model load on click
function paidMOdalOpen(id, value) {
  paidModal.style.display = "block";
  document.getElementById("paid-form-id").value = id;
  document.getElementById("pay_bill_modal_balance").value = value;
}

// paid Modal submit
function paidModalSubmit() {

  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  let data;
  if ($("#paid_amount").val() > $("#pay_bill_modal_balance").val()) {
    alert("Paid amount is greater than Net Amount! Please enter less or equal Amount");
    return false;
  }
  else {
    data = {
      id: $("#paid-form-id").val(),
      rv_no: $("#rv_no").val(),
      paid_date: $("#today-date").val(),
      amount: $("#paid_amount").val(),
      remaining_amount: $("#pay_bill_modal_balance").val() - $("#paid_amount").val()
    };
  }
  console.log(data);
  $.ajax({
    method: 'POST',
    url: "/api/customer/pay_bill/",
    data: data,
    csrfmiddlewaretoken: window.CSRF_TOKEN,
    // data: {
    //   "id": $("#paid-form-id").val(),
    //   "rv_no": $("#rv_no").val(),
    //   "paid_date": $("#today-date").val(),
    //   "amount": $("#paid_amount").val(),
    //   "remaining_amount": $("#pay_bill_modal_balance").val() - $("#paid_amount").val(),
    //   csrfmiddlewaretoken: window.CSRF_TOKEN,
    // },
    dataType: "json",
  })
  paidModal.style.display = "none";
  window.location.reload();
}


function closeModal(model) {
  console.log(model)
  document.querySelector(model).style.display = "none";
}

// open complementory modal window
function compModalOpen(id, value) {
  compModal.style.display = "block";
  document.getElementById("comp-form-id").value = id;
  document.getElementById("comp_bill_modal_balance").value = value;
}

// complementory modal submit button
function compModalSubmit() {

  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  let data;
  if ($("#comp_amount").val() > $("#comp_bill_modal_balance").val()) {
    alert("Complementary amount is greater than Net Amount! Please enter less or equal Amount");
    return false;
  }
  else {
    data = {
      id: $("#comp-form-id").val(),
      comp_date: $("#comp-today-date").val(),
      comp_remarks: $("#comp_remarks").val(),
      comp_amount: $("#comp_amount").val(),
      remaining_amount: $("#comp_bill_modal_balance").val() - $("#comp_amount").val()
    };
  }
  $.ajax({
    method: "POST",
    url: "/api/customer/comp_bill/",
    data: data,
    csrfmiddlewaretoken: window.CSRF_TOKEN,
    // data: {
    //   "id": $("#comp-form-id").val(),
    //   'comp_date': $("#comp-today-date").val(),
    //   'comp_remarks': $("#comp_remarks").val(),
    //   'comp_amount': $("#comp_amount").val(),
    //   // 'balance': $("#comp_bill_modal_balance").val(),
    //   "remaining_amount": $("#comp_bill_modal_balance").val() - $("#comp_amount").val(),
    //   csrfmiddlewaretoken: window.CSRF_TOKEN,
    // },
    dataType: "json",
  })
  compModal.style.display = "none";
  window.location.reload();
}

// open cancel modal window
function cancelModalOpen(id, value, amount) {
  cancelModal.style.display = "block";
  document.getElementById("cancel-form-id").value = id;
  document.getElementById("cancel_bill_modal_balance").value = value;
  document.getElementById("bill_amount").value = amount;
}

// cancel modal submit button
function cancelModalSubmit() {

  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $.ajax({
    method: "POST",
    url: "/api/customer/cancel_bill/",
    data: {
      'id': $("#cancel-form-id").val(),
      'cancel_date': $("#cancel-today-date").val(),
      'reason': $("#reason").val(),
      "remaining_amount": $("#cancel_bill_modal_balance").val() * 0 ,
      'amount': $("#bill_amount").val() * 0,
      csrfmiddlewaretoken: window.CSRF_TOKEN,
    },
    dataType: "json",
  })
  cancelModal.style.display = "none";
  window.location.reload();
};

let today = new Date();
document.getElementById("today-date").value = today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) + '-' + ('0' + today.getDate()).slice(-2);

let compToday = new Date();
document.getElementById("comp-today-date").value = compToday.getFullYear() + '-' + ('0' + (compToday.getMonth() + 1)).slice(-2) + '-' + ('0' + compToday.getDate()).slice(-2);

let cancelToday = new Date();
document.getElementById("cancel-today-date").value = cancelToday.getFullYear() + '-' + ('0' + (cancelToday.getMonth() + 1)).slice(-2) + '-' + ('0' + cancelToday.getDate()).slice(-2);

// function for export to excel or csv file 
function download_table_as_csv(Sales_data, separator = ',') {
  // Select rows from table_id
  var rows = document.querySelectorAll('table#' + Sales_data + ' tr');
  // Construct csv
  var csv = [];
  for (var i = 0; i < rows.length; i++) {
    var row = [], cols = rows[i].querySelectorAll('td, th');
    for (var j = 0; j < cols.length; j++) {
      // Clean innertext to remove multiple spaces and jumpline (break csv)
      var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
      // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
      data = data.replace(/"/g, '""');
      // Push escaped string
      row.push('"' + data + '"');
    }
    csv.push(row.join(separator));
  }
  var csv_string = csv.join('\n');
  // Download it
  var filename = Sales_data + '_' + new Date().toLocaleDateString() + '.csv';
  var link = document.createElement('a');
  link.style.display = 'none';
  link.setAttribute('target', '_blank');
  link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
// auto fill the paid remaining amount on paid modal
document.getElementById("paid_amount").onchange = function () {
  var balance = document.getElementById('pay_bill_modal_balance').value;
  var amount = document.getElementById('paid_amount').value;
  var total = balance - amount;
  document.getElementById('remaing_amount').value = total;
};


function paid_all_bills() {
  check=window.confirm("Are you sure you want to paid all bills?");
  if(check==true){
    let rv=window.prompt("Enter your RV number");
    let datetime=window.prompt("enter Date");
    datetime=new Date(datetime)
    month=datetime.getMonth()+1
    datetime=datetime.getDate()+'-'+month+'-'+datetime.getFullYear()
    console.log(datetime)

     var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  // loop table using jquery
  $("tbody > tr").each(function(row, tr) {
    let amount=$(tr).find('td:eq(10)').text();
    let id = $(tr).find('td:eq(11)').text();
    console.log(amount,id);
    $.ajax({
      method: 'POST',
      url: "/api/customer/pay_all_bills/",
      data: {
        "id": id,
        "rv_no": rv,
        "paid_date": datetime,
        "amount": amount,
        "remaining_amount": 0,
        csrfmiddlewaretoken: window.CSRF_TOKEN,
      },
      dataType: "json",
    })
    // console.log(id)
    paidModal.style.display = "none";
    window.location.reload();


  });
  

  
  // window.location.reload();



  }
  else{
    return false;
  }
 
};
