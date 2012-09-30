$(function() {
    $('#inventory .checkbox').click(function() {
        // get the item id
        var $self = $(this);
        var itemid = $self.val();
        var $drpdwn = $self.parents('tr').find('.person-list');
        // get the person id
        var personid = $drpdwn.val();

        if (!parseInt(personid)) {
            this.checked = false;
            alert('Pick a person');
            return;
        }

        $drpdwn.attr('disabled', this.checked);

        if (!this.checked) {
            $drpdwn.val(0);
        }

        // post check in/out change
        $.ajax({
            url: '/inventory-update',
            type: 'POST',
            data : {
                'personid' : personid,
                'itemid' : itemid,
                'status' : (this.checked ? 2 : 1)
            },
            success: function(req, status, xhr) {
                //var data = $.parseJSON(req);
            },
            error: function(req, status) {
                $drpdwn.attr('disabled', false);
                //if (req.status == 500) { }
            }
        });
    });
});