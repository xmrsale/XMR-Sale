// Payment logic, talks to satsale.py
function payment(payment_data) {
    $('document').ready(function(){
        var payment_uuid;
        var invoiceData = {amount: payment_data.amount, method: payment_data.method};

        // If a webhook URL is provided (woocommerce)
        if (payment_data.w_url) {
            invoiceData['w_url'] = payment_data.w_url
        }

        $.get("/api/createpayment", invoiceData).then(function(data) {
            invoice = data.invoice;
            payment_uuid = invoice.uuid;

            $('#address').text(invoice.address).html();
            $('#amount').text(invoice.btc_value).html();
            $('#amount_sats').text(Math.round(invoice.btc_value * 10**8)).html();
            $('#timer').text(Math.round(invoice.time_left)).html();

            // If we want to run both lnd and onchain payments (qrbit / flicker mode)
            if (payment_data.lnd_enabled) {
                var invoiceDataOnChain = invoiceData;
                invoiceDataOnChain.method = "bitcoind";
                $.get("/api/createpayment", invoiceDataOnChain).then(function(data_Onchain) {
                    invoice_Onchain = data_Onchain.invoice;
                    payment_uuid_Onchain = invoice_Onchain.uuid;
                    const qr_refreshInterval = setInterval(function(){load_flicker_qr(payment_uuid, payment_uuid_Onchain);}, 1000);

                });
            }
            else {
            // Otherwise run normally
                load_qr(payment_uuid);
            }
            document.getElementById('timerContainer').style.visibility = "visible";

            return payment_uuid;

        }).then(function(payment_uuid) {
            // Pass payment uuid and the interval process to check_payment
            var checkinterval = setInterval(function() {check_payment(payment_uuid, checkinterval, payment_data);}, 1000);
        })
    });
}

function check_payment(payment_uuid, checkinterval, payment_data) {
    $.get("/api/checkpayment", {uuid: payment_uuid}).then(function(checkpayment_data) {
        payment_status = checkpayment_data.status;
        console.log(payment_status);
        if (payment_status.expired == 1) {
            $('#status').text("Payment expired.").html();
            document.getElementById('timerContainer').style.visibility = "hidden";
            clearInterval(checkinterval);
            return 1;
        }

        if (payment_status.payment_complete == 1) {
            $('#status').text("Payment confirmed.").html();
            document.getElementById('timerContainer').style.visibility = "hidden";
            complete_payment(payment_uuid, payment_data);
            // clearInterval(checkinterval);
            return 1;
        }
        else {
            if (payment_status.unconfirmed_paid > 0) {
                $('#status').text("Discovered payment. Waiting for more confirmations...").html();
                return 0;
            }
            else {
                $('#status').text("Waiting for payment...").html();
                return 0;
            }
        }
    });
}

function complete_payment(payment_uuid, payment_data) {
    var order_id = location.search.split('id=')[1];
    $.get("/api/completepayment", {uuid: payment_uuid, id: order_id}).then(function(payment_completion) {
        console.log(payment_completion);
        $('#status').text(payment_completion.message).html();
    });
    setTimeout(() => {  window.location.replace(payment_data.redirect);  }, 5000);
}

function load_qr(payment_uuid) {
    // Display QR code
    if (payment_uuid != null) {
        // Change image id to qr id
        document.getElementById('qrImage').className = "qr";
        // Insert image and link
        document.getElementById('qrClick').href = "/static/qr_codes/" + payment_uuid + ".png";
        document.getElementById('qrImage').src = "/static/qr_codes/" + payment_uuid + ".png";
    }
}


var current_qr_uuid;
function load_flicker_qr(payment_uuid, payment_uuid_Onchain) {
    if (payment_uuid != current_qr_uuid) {
        current_qr_uuid = payment_uuid;
        load_qr(payment_uuid);
    } else {
        current_qr_uuid = payment_uuid_Onchain;
        load_qr(payment_uuid_Onchain);
    }
}


function replaceUrlParam(url, paramName, paramValue)
{
    console.log(url);
    var href = new URL(url);
    href.searchParams.set(paramName, paramValue);
    window.location = href;
    return
}

// Payment timer, can't go below zero, update every second
intervalTimer = setInterval(function () {
    var currentTime = document.getElementById('timer').innerHTML;
    if (currentTime <= 0) {
        currentTime = 1;
    }
    document.getElementById('timer').innerHTML = Math.round(currentTime - 1);
}, 1000)

// Copy text functions
function copyText(text) {
  navigator.clipboard.writeText(text);
}
function copyTextFromElement(elementID) {
  let element = document.getElementById(elementID); //select the element
  let elementText = element.textContent; //get the text content from the element
  copyText(elementText); //use the copyText function below
  alert("Copied address:" + elementText)
}
