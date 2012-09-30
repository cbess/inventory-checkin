$(function() {
    $('#group-list').change(function() {
        this.form.submit();
    });

    // auto-check the checkbox when a person is selected
    $('#inventory .person-list').change(function() {
        var $checkbox = $(this).parents('tr').find('.checkbox');
        var checkbox = $checkbox.get(0);
        // disables drpdown when a name is selected, so assuming 'true' is ok
        checkbox.checked = true;

        // simulate checkbox click
        $checkbox.click();
        checkbox.checked = true; // make sure its stays checked
    });

    // send inventory change
    $('#inventory .checkbox').click(function() {
        var $self = $(this);
        var checked = this.checked;
        var $row = $self.parents('tr');
        var $drpdwn = $row.find('.person-list');
        var itemName = $row.find('.device-name').text();
        var personName = $drpdwn.find('option:selected').text();
        var personid = $drpdwn.val();
        var itemid = $self.val();

        // if no person selected
        if (!parseInt(personid)) {
            this.checked = false;
            alert('Pick a person');
            return;
        }

        $drpdwn.attr('disabled', checked);

        if (!checked) {
            // select empty option
            $drpdwn.val(0);
        }

        // post check in/out change
        $.ajax({
            url: '/inventory-update',
            type: 'POST',
            data : {
                'personid' : personid,
                'itemid' : itemid,
                'status' : (checked ? 2 : 1)
            },
            success: function(req, status, xhr) {
                //var data = $.parseJSON(req);
                var $alert =  $('.alert').alert();
                var format = null;
                if (checked) {
                    format = '%s checked out %s';
                } else {
                    format = '%s checked in %s';
                }

                $alert.html($.sprintf('<strong>info</strong> '+format, personName, itemName)).fadeIn();

                // hide it
                setTimeout(function() {
                    $alert.fadeOut();
                }, 3000);
            },
            error: function(req, status) {
                $drpdwn.attr('disabled', false);
                //if (req.status == 500) { }
            }
        });
    });
});