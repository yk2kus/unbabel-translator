$(function() {
    // This will generate a unique ID
    https: //stackoverflow.com/a/15710692/9968872
        hashCode = function(s) {
            return s.split("").reduce(function(a, b) {
                a = ((a << 5) - a) + b.charCodeAt(0);
                return a & a
            }, 0);
        }


    $('button.btn-submit').bind('click', function(e) {
        // Prevent form reload
        e.preventDefault();
        var response = grecaptcha.getResponse();
        if (response.length == 0) {
            Swal({
                type: 'error',
                title: 'Oops...',
                text: "The reCAPTCHA wasn't entered correctly. Go back and try it again.!",
            })
            console.log("InValidated....................!!")
        } else {

            console.log("form submitted ......")
            grecaptcha.reset(); // recaptcha version: 2
            var input_text = $('textarea[name="source-text"]').val().trim();
            hash = hashCode(input_text);
            var uid = '';
            var status = 'new';
            var output_text = '';
            if (input_text) {
                var $new_row = $('table tbody');
                var row = "<tr'><td class='input-text' id=" + hash + ">" + input_text + "</td><td style='display:none' id='row-uid' uid=" + hash + ">" + uid + "</td><td id='row-status' status=" + hash + ">" + status + "</td><td id='translated-text' output=" + hash + ">" + output_text + "</td></tr>"
                $new_row.prepend(row);

            }

            //Validate JSON String
//            try{
//            JSON.parse(JSON.stringify({"value": input_text}))
//            }catch (e){
//                Swal({
//                type: 'error',
//                title: 'Oops...',
//                text: "Invalid JSON Request!!",
//            })
//            }



            //Catch result form /translate_term and update web page with Ajax
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
                });
            return false;

            console.log("Validated....................!!")

        }

    });
});