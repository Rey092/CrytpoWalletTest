// helper functions for Wallet Page-------------------------------------------------------------------------------------
// =====================================================================================================================
function timer(value) {
    let date = new Date(value)
    let seconds = Math.floor((new Date() - date) / 1000)
    let minutes = seconds / 60
    let hours = minutes / 60
    let days = hours / 24

    if (seconds < 60) {
        return Math.floor(seconds) + " secs"
    }
    if (minutes < 60) {
        return `${Math.floor(minutes) } mins`
    }
    if (hours < 24) {
        return Math.floor(hours) + " hrs " + Math.floor(minutes / 60) + " mins"
    }
    return Math.floor(days) + " days " + Math.floor(hours / 24) + " hrs"
}

function get_hours_and_minutes_time() {
    let date = new Date()
    let res = [date.getHours(), date.getMinutes()].map(function (x) {
      return x < 10 ? "0" + x : x
    }).join(":")
    return res
}

function toastr_options() {
    toastr.options = {
      "closeButton": true,
      "debug": false,
      "newestOnTop": false,
      "progressBar": false,
      "positionClass": "toast-bottom-right",
      "preventDuplicates": false,
      "onclick": null,
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": 0,
      "extendedTimeOut": 0,
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut",
      "tapToDismiss": false
    }
}
// =====================================================================================================================
