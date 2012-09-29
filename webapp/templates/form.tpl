
<form method="POST" action="" class="form-horizontal">
    {{ form.hidden_tag() }}
    {% for field in form if field.type != 'CSRFTokenField' %}
    <div class="control-group">
        <label class="control-label" for="{{ field.id }}">{{ field.label }}</label>
        <div class="controls">{{ field }}</div>
        {% if field.errors %}
        <ul>
            {% for error in field.errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
        {% endif %}
    </div>
    {% endfor %}
    <div class="control-group">
        <div class="controls">
            <button type="submit" class="btn">Sign in</button>
        </div>
    </div>
</form>
