$(function() {
    toastr.options = {
        // docs: http://codeseven.github.com/toastr/
	    debug: false,
	    positionClass: 'toast-top-left',
        fadeIn: 500,
        fadeOut: 1000,
        onclick: null
	};
    
    // top banner <select> element
    $('#group-list').change(function() {
        this.form.submit();
    });

    // auto-check-out when a person is selected
    $('#inventory .person-list').change(function() {
        $row = $(this).parents('tr');
        sendInventoryChangeState($row, {'checked': true});
        $row.data('checked-out', 'yes');
    });
    
    // inventory row clicked
    $('#inventory .item-data').click(function() {
        var checkedOut = ($(this).parents('tr').data('checked-out') == 'yes');
        if (checkedOut) {
            // show check-in
            sendInventoryChangeState($(this).parents('tr'), {'checked': false});
        } else { 
            // show dropdown
            // make fake mouse event to invoke display of the drop down
            var event = document.createEvent('MouseEvents');
            event.initMouseEvent('mousedown', true, true, window);
            // send event to <select>
            $select = $(this).find('.person select');
            $select.get(0).dispatchEvent(event);
        }
    });
    
    function sendInventoryChangeState($row, params) {
        var $drpdwn = $row.find('.person-list');
        var personid = $drpdwn.val();
        // if no person selected
        if (!parseInt(personid)) {
            return;
        }

        var $inventoryMeta = $('#inventory-meta');
        var itemName = $row.find('.device-name').data('name');
        var personName = $drpdwn.find('option:selected').text();
        var itemid = $row.data('item-id');
        var checked = params.checked;
        

        $drpdwn.attr('disabled', checked);

        // if about to be checked in
        if (!checked) {
            var confirmMsg = $.sprintf('Check in %s\nAre you sure?', itemName);
            if ($inventoryMeta.data('confirmation-checkin') == 'yes' &&
                confirm(confirmMsg) === false) {
                    $row.data('checked-out', 'yes');
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
                
                updateInventoryRow($row, checked);
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
                
                updateInventoryRow($row, !checked);
            }
        });
    }
    
    function updateInventoryRow($row, checkedOut) {
        $row.data('checked-out', checkedOut ? 'yes' : 'no');
        $row.find('.item-data').toggleClass('btn-inverse');
        $row.find('.person').toggleClass('hidden');
    }
});