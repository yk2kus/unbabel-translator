$(document).ready(function() {
    setInterval("check_status()", 10000); // call every 10 seconds
    setInterval("generate_uid()", 30000); // this is called only for unset UID
});

function generate_uid() {
    console.log("generate uid.................");
    $("td#row-uid:empty").each(function() {
        console.log("found unset................")
        var input_text = this.parentNode.getElementsByClassName('input-text')[0].textContent
        var hash = hashCode(input_text);
        $.getJSON('/queueTerm', {
                input: input_text,
                unique_hash: hash,
            },
            function(data) {
                console.log("uid................", data);
                //   data is a java script object like python dict with 1 key and 1 value   {48640724: "70aa995ab4"}
                var hash = Object.keys(data)[0];
                var uid = Object.values(data)[0];
                //  $("#destination-text").val(data);
                //  Find all td with hash and set value of uid
                var $uid = $("td[uid='" + hash + "']")
                $uid.html(uid) // set uid column
                $uid.parent().attr("uid", uid); // set uid in row
                //do nothing
            });

    });
}

function check_status() {
    console.log("calling every 10 seconds");
    // Access all non-trasnlated
    var non_translated_terms = [];

    $("td#translated-text:empty").each(function() {
        var parent_uid = this.parentNode.getAttribute("uid");
        if (non_translated_terms.indexOf(parent_uid) === -1) {
            non_translated_terms.push(parent_uid);
        }
    });


    //reload result into element with id "sysStatus"
    //  Call only if there is an item left for translation
    if (non_translated_terms != "" || non_translated_terms.length != 0) {
        var non_translated_terms = non_translated_terms.join(',');
        console.log("this...........", non_translated_terms);

        $.getJSON('/checkStatus', {
                terms_to_translate: non_translated_terms,
            },
            function(data) {
                console.log("uid............;;;;....", JSON.stringify(data));
                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        console.log(key + " -> " + data[key]);
                        // All rows with current key
                        // $rows = $("tr[uid="+key+"]")
                        // set translation
                        $("tr[uid=" + key + "]>td[id='row-status']").html(data[key][0]);
                        $("tr[uid=" + key + "]>td[id='translated-text']").html(data[key][1]);

                    }
                }
            });
    }
}