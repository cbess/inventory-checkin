$(function() {
    toastr.options = {
        // docs: http://codeseven.github.com/toastr/
	    debug: false,
	    positionClass: 'toast-top-left',
        fadeIn: 500,
        fadeOut: 1000,
        onclick: null
	};
    
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
        var $inventoryMeta = $('#inventory-meta');
        var checked = this.checked;
        var $row = $self.parents('tr');
        var $drpdwn = $row.find('.person-list');
        var itemName = $row.find('.device-name').data('name');
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

        // if about to be checked in
        if (!checked) {
            var confirmMsg = $.sprintf('Check in %s\nAre you sure?', itemName);
            if ($inventoryMeta.data('confirmation-checkin') == 'yes' &&
                confirm(confirmMsg) === false) {
                    this.checked = true;
                    return;
                }
                
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
                'status' : (checked ? 2 /* check out */ : 1 /* check in */)
            },
            success: function(req, status, xhr) {
                //var data = $.parseJSON(req);

                // show the notification
                toastr.options.fadeOut = 1000;
                toastr.options.timeOut = 3000;
                // change visual/func type based on action
                toastr[checked ? 'info' : 'success']($.sprintf(
                    '%s<br />Checked <b><u>%s</u> %s</b>', 
                    personName, 
                    checked ? 'OUT' : 'IN', 
                    itemName
                ));
            },
            error: function(req, status) {
                $drpdwn.attr('disabled', false);
                
                // show the error, it persists
                toastr.options.fadeOut = 0;
                toastr.options.timeOut = 0;
                toastr.error($.sprintf(
                    '%s <b>unable</b> to check %s %s',
                    personName,
                    checked ? 'out' : 'in', 
                    itemName
                ), 'error');
                //if (req.status == 500) { }
            }
        });
    });
});