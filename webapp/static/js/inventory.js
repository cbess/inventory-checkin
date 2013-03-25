// InventoryMate
// Created by: Christopher Bess (https://github.com/cbess/inventory-checkin)
// Copyright 2013

$(function() {
    toastr.options = {
        // docs: http://codeseven.github.com/toastr/
	    debug: false,
	    positionClass: 'toast-top-left',
        fadeIn: 500,
        fadeOut: 1000,
        onclick: null
	};
    
    var $checkoutModal = $('#co-modal');
    var $personSelect = $('#person-list');
    var $inventoryMeta = $('#inventory-meta');
    
    // top banner group <select> element
    $('#group-list').change(function() {
        this.form.submit();
    });
    
    // inventory row clicked
    $('#inventory .item-data').click(function() {
        // check permissions
        if ($inventoryMeta.data('can-edit') == 'no')
            return;
            
        var $row = $(this).parents('tr');
        var checkedOut = ($row.data('checked-out') == 'yes');
        if (checkedOut) {
            // start check-in workflow
            sendInventoryChangeState($row, {'checked': false});
        } else { 
            // show the check-out modal
            $('#co-modal-label').html($row.data('device-name'));
            $checkoutModal.data('item-id', $row.data('item-id'));
            
            $checkoutModal.modal('show');
        }
    });
    
    // checkout button in modal clicked
    $('#co-btn-checkout').click(function() {
        $row = $('#item-'+$checkoutModal.data('item-id'));
        
        // set the needed person data
        var personId = $personSelect.val();
        if (!parseInt(personId)) {
            alert('Please select a person.');
            return;
        }
            
        $row.data('person-id', personId);
        var personName = $personSelect.find('option:selected').text();
        $row.data('person-name', personName);
        
        sendInventoryChangeState($row, {'checked': true});
        setRowCheckedOut($row, true);
        
        $checkoutModal.modal('hide');
    });
    
    // reset the modal fields
    $checkoutModal.on('hidden', function() {
        // reset the fields
        $('#person-list').val(0);
        $('#duration-info #duration').val('');
        $('#duration-info #duration-type').val(0);
        $('#ooo').get(0).checked = false;
    });
    
    /*
     Sends the inventory change state request from the specified row.
     @param params {'checked': true|false}
    */
    function sendInventoryChangeState($row, params) {
        var personid = $row.data('person-id');
        // if no person selected
        if (!parseInt(personid)) {
            setRowCheckedOut($row, false);
            return;
        }

        var itemName = $row.data('device-name');
        var personName = $row.data('person-name');
        var itemid = $row.data('item-id');
        var checked = params.checked;

        // if about to be checked in
        if (!checked) {
            var confirmMsg = $.sprintf('Check in %s\nAre you sure?', itemName);
            if ($inventoryMeta.data('confirmation-checkin') == 'yes') {
                if (confirm(confirmMsg) === false) {
                    setRowCheckedOut($row, true);
                    return;
                } else {
                    var checkinText = $inventoryMeta.data('checkin-complete-msg');
                    if (checkinText) {
                        alert($.sprintf(checkinText, itemName));
                    }
                }
            }
        }

        // post check in/out change
        $.ajax({
            url: '/inventory/update',
            type: 'POST',
            dataType: 'json',
            data : {
                'personid' : personid,
                'itemid' : itemid,
                'status' : (checked ? 2 /* check out */ : 1 /* check in */),
                'duration' : $('#duration-info #duration').val(),
                'duration_type' : $('#duration-info #duration-type').val(),
                'ooo' : ($('#ooo').get(0).checked ? 1 : 0)
            },
            success: function(data, status, xhr) {
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
                
                updateInventoryRow($row, checked, $.parseJSON(xhr.responseText));
            },
            error: function(req, status) {
                // show the error, it persists
                toastr.options.fadeOut = 0;
                toastr.options.timeOut = 0;
                toastr.error($.sprintf(
                    '%s <b>unable</b> to check %s %s',
                    personName,
                    checked ? 'out' : 'in', 
                    itemName
                ), 'error');

                // make sure the attempted state change is reverted
                setRowCheckedOut($row, !checked);
            }
        });
    }
    
    function updateInventoryRow($row, checkedOut, responseJson) {
        setRowCheckedOut($row, checkedOut);
        $row.find('.item-data').toggleClass('btn-inverse');
        $row.find('.person').toggleClass('hidden');
        
        // update the checkout info
        if (checkedOut) {
            $row.find('.check-out-info').removeClass('hidden');
            $row.find('.check-out-info .name').html(responseJson.person.name);
            $row.find('.check-out-info .duration').html($.sprintf(
                // if format changed here, then change the inventory template
                '%s - %s',
                responseJson.duration.dateAdded,
                responseJson.duration.description
            ));
        } else {
            $row.find('.check-out-info').addClass('hidden');
        }
    }
    
    function setRowCheckedOut($row, checkedOut) {
        $row.data('checked-out', checkedOut ? 'yes' : 'no');
    }
});